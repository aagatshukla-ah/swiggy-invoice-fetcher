# Swiggy Invoice Fetcher (Interactive Version)

This script fetches Swiggy invoice emails via IMAP, filters by EarnIn office address and date, downloads invoice PDFs, and merges them into a single file — all via **interactive terminal prompts**.

---

## 🛠 Requirements

- Python 3.7+
- IMAP enabled in Gmail
- App Password (not your Gmail password)

---

## 🔧 Setup

Install required libraries:

```bash
pip install -r requirements.txt
```

### ✉️ IMAP in Gmail

To allow this script to access your Gmail inbox, complete the following steps:

---

#### ✅ Step 1: Enable 2-Step Verification

```bash
https://myaccount.google.com/security
```

→ Scroll to **"Signing in to Google"**  
→ Enable **2-Step Verification**

---

#### ✅ Step 2: Generate an App Password

```bash
https://myaccount.google.com/apppasswords
```

→ Select **App: Mail**, **Device: Other** → name it `Swiggy Script`  
→ Click **Generate** and **copy the 16-character password**  
→ You'll use this at runtime when prompted.

---

## 🚀 Run

Run the interactive script:

```bash
python fetch_invoices_interactive.py
```

You’ll be prompted to enter:
- Your Gmail address
- Your App Password (hidden input)
- Start and end date (in `DD-MM-YY` format)
- Output folder paths and merged PDF name

---

## 📦 Output

- PDFs downloaded to the folder you specify
- Valid invoices filtered by office address and date
- Merged PDF file with total amount printed at the end

---

## 🔐 Security Tip

Never share or commit your app password. It is safer than using your real password, but still sensitive.

