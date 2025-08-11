#!/usr/bin/env python3

import argparse
import imaplib
import logging
import os
import re
import sys
from datetime import datetime, timedelta
from email import message_from_bytes
from pathlib import Path

from PyPDF2 import PdfReader, PdfMerger
from config_loader import load_settings


parser = argparse.ArgumentParser(description="Fetch invoice PDFs, filter, merge")
parser.add_argument("--debug", action="store_true", help="enable verbose logs")
args = parser.parse_args()


logging.basicConfig(
    level=logging.DEBUG if args.debug else logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    handlers=[
        logging.FileHandler("fetch_invoices.log", "w"),
        logging.StreamHandler(sys.stdout),
    ],
)


cfg = load_settings()
EMAIL = cfg["EMAIL"]
PASSWORD = cfg["PASSWORD"]

START_IN = cfg["START_DATE"]  # DD-MM-YY
END_IN = cfg["END_DATE"]      # DD-MM-YY

INVOICE_DIR = cfg["INVOICE_DIR"]
FILTERED_DIR = cfg["FILTERED_DIR"]
MERGED_PDF = cfg["MERGED_PDF"]

SENDERS = [s.strip() for s in cfg["SENDERS"].split(",") if s.strip()]
ADDR_KEYWORDS = [k.strip().lower() for k in cfg["ADDRESS_KEYWORDS"].split(",") if k.strip()]

IMAP_SERVER = "imap.gmail.com"

start_dt = datetime.strptime(START_IN, "%d-%m-%y")
end_dt = datetime.strptime(END_IN, "%d-%m-%y") + timedelta(days=1)      # inclusive
START_STR = start_dt.strftime("%d-%b-%Y")
END_STR = end_dt.strftime("%d-%b-%Y")


Path(INVOICE_DIR).mkdir(parents=True, exist_ok=True)
Path(FILTERED_DIR).mkdir(parents=True, exist_ok=True)

MONTH_RE = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*"
date_regex = re.compile(
    rf"(?:Date of Invoice|Invoice Date|Order Time|Order Date):\s*"
    rf"(\d{{1,2}}[/-]\d{{1,2}}[/-]\d{{4}}|\d{{1,2}}\s+{MONTH_RE}\s+\d{{4}})",
    re.I,
)
total_regex = re.compile(r"(?:Invoice Total|Total)\s+₹?([\d,]+\.\d{2})", re.I)

def parse_any_date(raw: str):
    for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%d %B %Y", "%d %b %Y"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None

def extract_invoice_date(text: str):
    m = date_regex.search(text)
    if not m:
        return None, None
    raw = m.group(1).replace(",", "")
    return parse_any_date(raw), raw

def log_total(pdf_file: str):
    total = 0.0
    for page in PdfReader(pdf_file).pages:
        for amt in total_regex.findall(page.extract_text() or ""):
            total += float(amt.replace(",", ""))
    logging.info("Grand total across merged invoices: ₹%.2f", total)

try:
    logging.info("Connecting to %s", IMAP_SERVER)
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("INBOX")

    message_ids = []
    for sender in SENDERS:
        criteria = f'(FROM "{sender}" SINCE "{START_STR}" BEFORE "{END_STR}")'
        _, data = mail.search(None, criteria)
        found = data[0].split()
        logging.info("Sender %s: %d email(s)", sender, len(found))
        message_ids.extend(found)

    message_ids = list(dict.fromkeys(message_ids))  # de-dupe
    logging.info("Total unique emails: %d", len(message_ids))

    for mid in message_ids:
        _, data = mail.fetch(mid, "(RFC822)")
        msg = message_from_bytes(data[0][1])

        for part in msg.walk():
            if part.get_content_type() != "application/pdf" or not part.get_filename():
                continue

            filename = os.path.basename(part.get_filename())
            temp_path = Path(INVOICE_DIR) / filename
            temp_path.write_bytes(part.get_payload(decode=True))
            logging.info("Downloaded %s", filename)

            try:
                text = "".join(p.extract_text() or "" for p in PdfReader(temp_path).pages)
                inv_dt, raw_dt = extract_invoice_date(text)

                date_ok = bool(inv_dt and start_dt <= inv_dt < end_dt)
                matched_kw = next((k for k in ADDR_KEYWORDS if k in text.lower()), None)
                addr_ok = True if not ADDR_KEYWORDS else bool(matched_kw)
                keep_file = date_ok and addr_ok

                if keep_file:
                    temp_path.rename(Path(FILTERED_DIR) / filename)
                    logging.info("Kept %s (date %s)", filename, raw_dt or "n/a")
                else:
                    reasons = []
                    if not date_ok:
                        reasons.append("date-not-found" if inv_dt is None else f"date-out-of-range ({raw_dt})")
                    if not addr_ok:
                        snippet = text.lower().split("delivery address", 1)[-1][:50]
                        reasons.append(f"address-mismatch ('{snippet}...')")
                    logging.info("Removed %s (%s)", filename, ", ".join(reasons))
                    temp_path.unlink()

            except Exception as err:
                logging.error("Failed to process %s: %s", filename, err)
                temp_path.unlink(missing_ok=True)

    kept_files = [p for p in os.listdir(FILTERED_DIR) if p.lower().endswith(".pdf")]
    if kept_files:
        merger = PdfMerger()
        for p in kept_files:
            merger.append(os.path.join(FILTERED_DIR, p))
        merger.write(MERGED_PDF)
        merger.close()
        logging.info("Merged %d file(s) into %s", len(kept_files), MERGED_PDF)
        # log_total(MERGED_PDF)
    else:
        logging.warning("No PDFs passed the filters.")

    mail.logout()

except imaplib.IMAP4.error as e:
    logging.error("IMAP error: %s", e)
except Exception:
    logging.exception("Unexpected error")
