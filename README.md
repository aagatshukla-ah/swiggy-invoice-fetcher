# Swiggy Invoice Fetcher (Interactive Version)

This script fetches Swiggy invoice emails via IMAP, filters by EarnIn office address and date, downloads invoice PDFs, and merges them into a single file — all via **interactive terminal prompts**.

---
Quick-start for *non-tech users*

1. **Download & unzip** the latest release.  
- The folder contains:
- Swiggy Invoice Fetcher # macOS/Linux binary or .exe on Windows
- settings.ini # <- edit me  

2. **Edit `settings.ini`** in any text editor  
- `EMAIL` – your Gmail address  
- `APP_PASSWORD` - a 16-char Gmail App Password  
- `START_DATE`, `END_DATE` - in `DD-MM-YY` format  
- (optional) adjust output-folder paths

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
git clone git@github.com:aagatshukla-ah/swiggy-invoice-fetcher.git
cd swiggy-invoice-fetcher 
python3 -m venv test
source test/bin/activate
pip install -r requirements.txt
python3 fetch_invoices.py
```

You’ll be prompted to enter:
- Your Gmail address
- Your App Password (hidden input)
- Start and end date (in `DD-MM-YY` format)
- Output folder paths and merged PDF name

---
## 💡 Example Run

```text
(test) aagatshukla@AShukla-mbp swiggy-invoice-fetcher % python3 fetch_invoices.py
Enter your Gmail address: aagat.shukla@earnin.com
Enter your Gmail App Password (input hidden): 
Enter your office address to filter by [default: Earnin India Office]: 
Enter start date (DD-MM-YY): 24-06-25
Enter end date (DD-MM-YY): 17-07-25
Enter directory to store downloaded invoices [default: ./swiggy_invoices]: 
Enter directory to store filtered invoices [default: ./filtered_invoices]: 
Enter full path for merged PDF [default: ./swiggy_invoices_merged.pdf]: 
Connecting to IMAP server...
Logging in...
Searching for Swiggy emails from 24-Jun-2025 to 18-Jul-2025...
Found 26 Swiggy emails.
Downloaded: 0171768062400035_9208c959-3c26-414d-b8ed-01fb4550567d.pdf
✔ Kept: 0171768062400035_9208c959-3c26-414d-b8ed-01fb4550567d.pdf (matched address and date: 24-Jun-2025)
Downloaded: 0171768062500022_028f9a8d-8ea7-4817-bbbd-8ea1f024596d.pdf
✔ Kept: 0171768062500022_028f9a8d-8ea7-4817-bbbd-8ea1f024596d.pdf (matched address and date: 25-Jun-2025)
Downloaded: 0171768062600027_b72d31d9-2e27-429c-8d61-8785ee9df8de.pdf
✔ Kept: 0171768062600027_b72d31d9-2e27-429c-8d61-8785ee9df8de.pdf (matched address and date: 26-Jun-2025)
Downloaded: 0272237062600039_15714841-06f0-4beb-8a14-482ac0bfd097.pdf
✘ Removed: 0272237062600039_15714841-06f0-4beb-8a14-482ac0bfd097.pdf (no address match)
Downloaded: 0171768062700019_9740397b-a0fe-4154-910c-aeba30d3b3d1.pdf
✔ Kept: 0171768062700019_9740397b-a0fe-4154-910c-aeba30d3b3d1.pdf (matched address and date: 27-Jun-2025)
Downloaded: 250628PF00007214_4d95646a-9e5d-4588-ba7f-301613d0096b.pdf
✘ Removed: 250628PF00007214_4d95646a-9e5d-4588-ba7f-301613d0096b.pdf (no address match)
Downloaded: 0201224062900255_713063af-d8ac-4a9f-8ce3-ed7565582407.pdf
✘ Removed: 0201224062900255_713063af-d8ac-4a9f-8ce3-ed7565582407.pdf (no address match)
Downloaded: 0524353062900098_8b7178ee-aef8-407f-a47b-c32684f6fad9.pdf
✘ Removed: 0524353062900098_8b7178ee-aef8-407f-a47b-c32684f6fad9.pdf (no address match)
Downloaded: 0256913063000006_944e902a-db3c-4465-b9dc-6da176d0471f.pdf
✔ Kept: 0256913063000006_944e902a-db3c-4465-b9dc-6da176d0471f.pdf (matched address and date: 30-Jun-2025)
Downloaded: 0171768063000028_4bf1e3a6-00c8-4643-8e5d-c07d276d5ce1.pdf
✔ Kept: 0171768063000028_4bf1e3a6-00c8-4643-8e5d-c07d276d5ce1.pdf (matched address and date: 30-Jun-2025)
Downloaded: 0352309070100003_be1122c2-10b6-434b-abe5-c29d72c2978e.pdf
✔ Kept: 0352309070100003_be1122c2-10b6-434b-abe5-c29d72c2978e.pdf (matched address and date: 01-Jul-2025)
Downloaded: 0299893070200001_c5e21a70-e1bf-4977-94c4-d4e42831e659.pdf
✘ Removed: 0299893070200001_c5e21a70-e1bf-4977-94c4-d4e42831e659.pdf (no address match)
Downloaded: 0171768070200039_e8580ed6-01d1-4ffa-98da-7fecf47e7aa7.pdf
✔ Kept: 0171768070200039_e8580ed6-01d1-4ffa-98da-7fecf47e7aa7.pdf (matched address and date: 02-Jul-2025)
Downloaded: 0256913070300009_35abb3b8-4d70-4c74-ae43-0ab79624423c.pdf
✔ Kept: 0256913070300009_35abb3b8-4d70-4c74-ae43-0ab79624423c.pdf (matched address and date: 03-Jul-2025)
Downloaded: 0171768070400044_3e03129a-929c-415d-98a3-194c4bfbcdcd.pdf
✔ Kept: 0171768070400044_3e03129a-929c-415d-98a3-194c4bfbcdcd.pdf (matched address and date: 04-Jul-2025)
Downloaded: 0000304070500301_15c1f01b-9bbe-474d-909b-efa79710e1ca.pdf
✘ Removed: 0000304070500301_15c1f01b-9bbe-474d-909b-efa79710e1ca.pdf (no address match)
Downloaded: 0299893070500047_cd75d6ae-e983-4fad-a2eb-69515efe1d63.pdf
✘ Removed: 0299893070500047_cd75d6ae-e983-4fad-a2eb-69515efe1d63.pdf (no address match)
Downloaded: 0171768070700028_b163d22f-629c-4442-9d9e-47458450b195.pdf
✔ Kept: 0171768070700028_b163d22f-629c-4442-9d9e-47458450b195.pdf (matched address and date: 07-Jul-2025)
Downloaded: 0000307070800129_bab8eb0a-3592-4a63-a21a-1f78514405d5.pdf
✔ Kept: 0000307070800129_bab8eb0a-3592-4a63-a21a-1f78514405d5.pdf (matched address and date: 08-Jul-2025)
Downloaded: 0171768070900038_c1a667d7-44bc-4597-a3c0-05fcf6d7b08a.pdf
✔ Kept: 0171768070900038_c1a667d7-44bc-4597-a3c0-05fcf6d7b08a.pdf (matched address and date: 09-Jul-2025)
Downloaded: 0171768071000032_bfe3b928-6eb6-48fc-894b-5d6083e89161.pdf
✔ Kept: 0171768071000032_bfe3b928-6eb6-48fc-894b-5d6083e89161.pdf (matched address and date: 10-Jul-2025)
Downloaded: 0171768071100069_b903ce27-7376-4325-b095-9b7ceab049d5.pdf
✔ Kept: 0171768071100069_b903ce27-7376-4325-b095-9b7ceab049d5.pdf (matched address and date: 11-Jul-2025)
Downloaded: 0171768071600042_71757a19-552e-4889-bf24-df927ceecf80.pdf
✔ Kept: 0171768071600042_71757a19-552e-4889-bf24-df927ceecf80.pdf (matched address and date: 16-Jul-2025)
Downloaded: 0577801071600091_5cb67295-0477-4531-9bf9-81ab304709f4.pdf
✘ Removed: 0577801071600091_5cb67295-0477-4531-9bf9-81ab304709f4.pdf (no address match)
Downloaded: 0577801071700007_dae7e1af-bd2f-41e0-808a-38468f065da9.pdf
✔ Kept: 0577801071700007_dae7e1af-bd2f-41e0-808a-38468f065da9.pdf (matched address and date: 17-Jul-2025)

✅ Merged 17 invoices into ./swiggy_invoices_merged.pdf

📄 Processing file: ./swiggy_invoices_merged.pdf
  ➜ Page 1 totals found: ['259.35']
  ➜ Page 2 totals found: ['491.40']
  ➜ Page 3 totals found: ['249.90']
  ➜ Page 4 totals found: ['36.75']
  ➜ Page 5 totals found: ['366.82']
  ➜ Page 6 totals found: ['389.55']
  ➜ Page 7 totals found: ['184.80']
  ➜ Page 8 totals found: ['260.40']
  ➜ Page 9 totals found: ['184.80']
  ➜ Page 10 totals found: ['184.80']
  ➜ Page 11 totals found: ['346.50']
  ➜ Page 12 totals found: ['249.90']
  ➜ Page 13 totals found: ['249.90']
  ➜ Page 14 totals found: ['346.87']
  ➜ Page 15 totals found: ['249.90']
  ➜ Page 16 totals found: ['249.90']
  ➜ Page 17 totals found: ['184.80']

💰 Estimated total amount across all invoices: ₹4486.34

```

➡️ The script will download matching Swiggy invoice PDFs, filter by your address and dates, merge them, and show the total invoice amount.
## 📦 Output

- PDFs downloaded to the folder you specify
- Valid invoices filtered by office address and date
- Merged PDF file with total amount printed at the end

---

## 🔐 Security Tip

Never share or commit your app password. It is safer than using your real password, but still sensitive.


Only maintainers need this.
# clean previous build
rm -rf build/ dist/ *.spec

# build new binary (mac/Linux shown; add .exe on Windows)
pyinstaller --onefile \
            --name "Swiggy Invoice Fetcher" \
            fetch_invoices.py
# copy artefacts into release folder
mkdir -p release
cp dist/"Swiggy Invoice Fetcher" release/
cp settings.ini release/
