import imaplib
import email
from email import message_from_bytes
import os
import re
from datetime import datetime, timedelta
from PyPDF2 import PdfReader, PdfMerger
import getpass
from config_loader import load_settings
cfg = load_settings()

EMAIL  = cfg["EMAIL"]
PASSWORD = cfg["PASSWORD"]
EARNIN_OFFICE_ADDRESS = cfg["OFFICE_ADDRESS"]
START_DATE_INPUT = cfg["START_DATE"]
END_DATE_INPUT   = cfg["END_DATE"]
INVOICE_DIR  = cfg["INVOICE_DIR"]
FILTERED_DIR = cfg["FILTERED_DIR"]
MERGED_PDF   = cfg["MERGED_PDF"]

# === INTERACTIVE PROMPTS ===

IMAP_SERVER = 'imap.gmail.com'

# Convert dates
start_dt = datetime.strptime(START_DATE_INPUT, "%d-%m-%y")
end_dt = datetime.strptime(END_DATE_INPUT, "%d-%m-%y") + timedelta(days=1)
START_DATE_STR = start_dt.strftime("%d-%b-%Y")
END_DATE_STR = end_dt.strftime("%d-%b-%Y")

os.makedirs(INVOICE_DIR, exist_ok=True)
os.makedirs(FILTERED_DIR, exist_ok=True)

# === HELPERS ===
def extract_invoice_date(text):
    match = re.search(r'Date of Invoice:\s*(\d{2}-\d{2}-\d{4})', text)
    if match:
        return datetime.strptime(match.group(1), "%d-%m-%Y")
    return None

def extract_total_from_pdf(pdf_path):
    total_amount = 0.0
    currency_pattern = re.compile(r'Invoice Total\s+([\d,]+\.\d{2})')
    try:
        reader = PdfReader(pdf_path)
        print(f"\n📄 Processing file: {pdf_path}")
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            matches = currency_pattern.findall(text)
            if matches:
                print(f"  ➜ Page {i+1} totals found: {matches}")
            for amt_str in matches:
                amt_str_clean = amt_str.replace(",", "")
                total_amount += float(amt_str_clean)
        print(f"\n💰 Estimated total amount across all invoices: ₹{total_amount:.2f}")
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")

# === MAIN LOGIC ===
try:
    print("Connecting to IMAP server...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    print("Logging in...")
    mail.login(EMAIL, PASSWORD)
    mail.select("INBOX")

    print(f"Searching for Swiggy emails from {START_DATE_STR} to {END_DATE_STR}...")
    search_criteria = f'(FROM "google.com" SINCE "{START_DATE_STR}" BEFORE "{END_DATE_STR}")'
    status, data = mail.search(None, search_criteria)
    email_ids = data[0].split()

    print(f"Found {len(email_ids)} Swiggy emails.")

    for num in email_ids:
        status, msg_data = mail.fetch(num, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = message_from_bytes(raw_email)

        for part in msg.walk():
            if part.get_content_type() == 'application/pdf' and part.get_filename():
                filename = os.path.basename(part.get_filename())
                filepath = os.path.join(INVOICE_DIR, filename)
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                print(f"Downloaded: {filename}")

                try:
                    reader = PdfReader(filepath)
                    full_text = "".join(page.extract_text() or "" for page in reader.pages)
                    invoice_date = extract_invoice_date(full_text)

                    if (
                        invoice_date and start_dt <= invoice_date < end_dt
                        and EARNIN_OFFICE_ADDRESS.lower() in full_text.lower()
                    ):
                        filtered_path = os.path.join(FILTERED_DIR, filename)
                        os.rename(filepath, filtered_path)
                        print(f"✔ Kept: {filename} (matched address and date: {invoice_date.strftime('%d-%b-%Y')})")
                    else:
                        os.remove(filepath)
                        reason = "no address match" if invoice_date and EARNIN_OFFICE_ADDRESS.lower() not in full_text.lower() else "date out of range or not found"
                        print(f"✘ Removed: {filename} ({reason})")
                except Exception as e:
                    print(f"Failed to process {filename}: {e}")
                    os.remove(filepath)

    merger = PdfMerger()
    filtered_files = [f for f in os.listdir(FILTERED_DIR) if f.endswith(".pdf")]
    for file in filtered_files:
        merger.append(os.path.join(FILTERED_DIR, file))

    if filtered_files:
        merger.write(MERGED_PDF)
        merger.close()
        print(f"\n✅ Merged {len(filtered_files)} invoices into {MERGED_PDF}")
        extract_total_from_pdf(MERGED_PDF)
    else:
        print("\n⚠️ No matching invoices found to merge.")

    mail.logout()

except imaplib.IMAP4.error as e:
    print(f"IMAP Error: {e}")
except Exception as e:
    print(f"General Error: {e}")
