# config_loader.py
import configparser
import sys
from pathlib import Path

# When bundled with PyInstaller, sys.executable is “…/Swiggy Invoice Fetcher”
# During normal runs, __file__ is this .py file.
BASE_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
CFG_FILE = BASE_DIR / "settings.ini"          # <-- editable file beside the EXE

def load_settings() -> dict:
    """
    Load settings.ini → flat dict.
    Raises FileNotFoundError with a clear message if the file is missing.
    """
    if not CFG_FILE.exists():
        raise FileNotFoundError(
            f"{CFG_FILE} not found – copy the template or rename your file to settings.ini"
        )

    cfg = configparser.ConfigParser()
    cfg.read(CFG_FILE)

    d = cfg["DEFAULT"]
    return {
        "EMAIL":          d["EMAIL"],
        "PASSWORD":       d["APP_PASSWORD"],
        "OFFICE_ADDRESS": d.get("OFFICE_ADDRESS", "Earnin India Office"),
        "START_DATE":     d["START_DATE"],
        "END_DATE":       d["END_DATE"],
        "INVOICE_DIR":    d.get("INVOICE_DIR", "./swiggy_invoices"),
        "FILTERED_DIR":   d.get("FILTERED_DIR", "./filtered_invoices"),
        "MERGED_PDF":     d.get("MERGED_PDF", "./swiggy_invoices_merged.pdf"),
        "SENDERS":       d.get("SENDERS", "Swiggy"),
         "ADDRESS_KEYWORDS": d.get("ADDRESS_KEYWORDS", "EarnIn India Office"),
    }
