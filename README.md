# Swiggy Invoice Fetcher

This script fetches Swiggy invoice emails via IMAP, filters by EarnIn address and date, downloads invoice PDFs, and merges them into a single file.

## 🛠 Requirements

- Python 3.7+
- Enable IMAP in Gmail
- Use App Passwords if using Gmail with 2FA

## 🔧 Setup

```bash
pip install -r requirements.txt
```

### ✉️ IMAP in Gmail

To allow this script to access your Gmail inbox, complete the following steps:

---

#### ✅ Step 1: Enable 2-Step Verification

Enable 2FA so you can create an App Password.

```bash
https://myaccount.google.com/security
```
→ Scroll to **"Signing in to Google"**  
→ Enable **2-Step Verification**

---

#### ✅ Step 2: Generate an App Password

Create a one-time password to use securely in the script.

```bash
https://myaccount.google.com/apppasswords
```
→ Select **App: Mail**, **Device: Other** → name it `Swiggy Script`  
→ Click **Generate** and **copy the 16-character password**

Use this password in your `config.yaml` as the `PASSWORD` field (never use your main Gmail password).

---

## 📁 Configuration

Edit the `config.yaml` file:

```yaml
EMAIL: 'your-email@gmail.com'
PASSWORD: 'your-app-password'
START_DATE: '24-06-25'
END_DATE: '16-07-25'
```

## 🚀 Run

```bash
python fetch_invoices.py
```

PDFs will be saved in `./swiggy_invoices`, filtered PDFs in `./filtered_invoices`, and the merged PDF at the location you specify.
