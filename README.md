# Swiggy Invoice Fetcher

This script fetches Swiggy invoice emails via IMAP, filters by EarnIn address and date, downloads PDF invoices, and merges them into a single file.

## 🛠 Requirements

- Python 3.7+
- Enable IMAP in Gmail
- Use App Passwords if using Gmail with 2FA

## 🔧 Setup

```bash
pip install -r requirements.txt
```

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

