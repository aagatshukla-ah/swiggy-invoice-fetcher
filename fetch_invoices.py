import imaplib
import email
from email import message_from_bytes
import os
import re
from datetime import datetime, timedelta
from PyPDF2 import PdfReader, PdfMerger
import getpass

# === USER INPUT ===
def get_user_inputs():
    email_address = input("Enter your Gmail address: ")
    password = getpass.getpass("Enter your Gmail App Password (input hidden): ")
    office_address = input("Enter your office address to filter by [default: Earnin India Office]: ") or "Earnin India Office"
    start_date_str = input("Enter start date (DD-MM-YY): ")
    end_date_str = input("Enter end date (DD-MM-YY): ")
    start_date = datetime.strptime(start_date_str, "%d-%m-%y")
    end_date = datetime.strptime(end_date_str, "%d-%m-%y") + timedelta(days=1)
    invoice_dir = input("Enter directory to store downloaded invoices [default: ./swiggy_invoices]: ") or "./swiggy_invoices"
    filtered_dir = input("Enter directory to store filtered invoices [default: ./filtered_invoices]: ") or "./filtered_invoices"
    merged_pdf = input("Enter full path for merged PDF [default: ./swiggy_invoices_merged.pdf]: ") or "./swiggy_invoices_merged.pdf"
    return {
        "email_address": email_address,
        "password": password,
        "office_address": office_address,
        "start_date": start_date,
        "end_date": end_date,
        "invoice_dir": invoice_dir,
        "filtered_dir": filtered_dir,
        "merged_pdf": merged_pdf
    }

# === UTILITIES ===
def setup_directories(invoice_dir, filtered_dir):
    os.makedirs(invoice_dir, exist_ok=True)
    os.makedirs(filtered_dir, exist_ok=True)
    for directory in [invoice_dir, filtered_dir]:
        for file in os.listdir(directory):
            os.remove(os.path.join(directory, file))

def extract_invoice_date(text):
    match = re.search(r'Date of Invoice:\s*(\d{2}-\d{2}-\d{4})', text)
    return datetime.strptime(match.group(1), "%d-%m-%Y") if match else None

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
            total_amount += sum(float(amt.replace(",", "")) for amt in matches)
        print(f"\n💰 Estimated total amount: ₹{total_amount:.2f}")
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")

# === MAIN LOGIC ===
def process_emails(config):
    imap_server = 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(config["email_address"], config["password"])
    mail.select("INBOX")

    start_str = config["start_date"].strftime("%d-%b-%Y")
    end_str = config["end_date"].strftime("%d-%b-%Y")
    print(f"Searching for Swiggy emails from {start_str} to {end_str}...")

    status, data = mail.search(None, f'(FROM "Swiggy" SINCE "{start_str}" BEFORE "{end_str}")')
    email_ids = data[0].split()
    print(f"Found {len(email_ids)} Swiggy emails.")

    for num in email_ids:
        _, msg_data = mail.fetch(num, '(RFC822)')
        msg = message_from_bytes(msg_data[0][1])

        for part in msg.walk():
            if part.get_content_type() == 'application/pdf' and part.get_filename():
                original_filename = os.path.basename(part.get_filename())
                unique_filename = f"{num.decode()}_{original_filename}"
                file_path = os.path.join(config["invoice_dir"], unique_filename)

                try:
                    with open(file_path, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    print(f"Downloaded: {unique_filename}")
                except Exception as e:
                    print(f"❌ Failed to save {unique_filename}: {e}")
                    continue

                try:
                    reader = PdfReader(file_path)
                    full_text = "".join(page.extract_text() or "" for page in reader.pages)
                    invoice_date = extract_invoice_date(full_text)
                    filtered_path = os.path.join(config["filtered_dir"], unique_filename)

                    if invoice_date and config["start_date"] <= invoice_date < config["end_date"] and config["office_address"].lower() in full_text.lower():
                        if not os.path.exists(filtered_path):
                            os.rename(file_path, filtered_path)
                            print(f"✔ Kept: {unique_filename} (date: {invoice_date.strftime('%d-%b-%Y')})")
                        else:
                            print(f"⚠️ Skipping move (already exists): {unique_filename}")
                            os.remove(file_path)
                    else:
                        os.remove(file_path)
                        reason = "address mismatch" if invoice_date and config["office_address"].lower() not in full_text.lower() else "date missing or out of range"
                        print(f"✘ Removed: {unique_filename} ({reason})")
                except Exception as e:
                    print(f"Failed to process {unique_filename}: {e}")
                    os.remove(file_path)
    mail.logout()

# === MERGE PDFs ===
def merge_filtered_pdfs(filtered_dir, merged_pdf):
    pdfs = [os.path.join(filtered_dir, f) for f in os.listdir(filtered_dir) if f.endswith(".pdf")]
    if not pdfs:
        print("\n⚠️ No matching invoices found to merge.")
        return

    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(merged_pdf)
    merger.close()

    print(f"\n✅ Merged {len(pdfs)} invoices into {merged_pdf}")
    extract_total_from_pdf(merged_pdf)

# === ENTRY POINT ===
if __name__ == "__main__":
    try:
        config = get_user_inputs()
        setup_directories(config["invoice_dir"], config["filtered_dir"])
        process_emails(config)
        merge_filtered_pdfs(config["filtered_dir"], config["merged_pdf"])
    except imaplib.IMAP4.error as e:
        print(f"IMAP Error: {e}")
    except Exception as e:
        print(f"General Error: {e}")
