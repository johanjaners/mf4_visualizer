# mf4_visualizer.py

"""
🔍 MF4 Visualizer 

A simple Python tool for visualizing signals in .mf4 log files.
Focused on EV battery test data through signal filtering and visualization.

Features:
- Auto-loads latest `.mf4` file
- Filters signals by keyword
- Plots signals over time

Usage:
    - Place .mf4 logs in `mf4_logfiles/`
    - Adjust `KEYWORD_MAP` if needed
    - Run to generate plots and summaries

Author: J2 (GitHub: johanjaners)
Version 1.0.0
"""

import os
import subprocess
from asammdf import MDF
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# === GLOBAL SETTINGS ===
INPUT_DIR = "./mf4_logfiles"
EXPORT_DIR = "./mf4_exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

# === SIGNAL MAPPING ===
KEYWORD_MAP = {
    "cell voltage": ["CellVMax", "CellVMin"],
    "cell temperature": ["TempAvg", "TempMax", "TempMin"],
    "pack voltage": ["PackVolt"],
    "coolant temperature": ["CoolantTemp"],
    "pack current": ["PackCurr"],
    "charge current limit": ["ChargeCurrLim"],
    "soc": ["SOC", "SOCMin", "SOCMax"],
    "power limit": ["ChargePowerLim", "DischargePowerLim"],
    "fault flags": ["FaultFlag"]
}

# === Load latest MF4 file ===
def load_latest_mf4(directory=INPUT_DIR):
    mf4_files = sorted(
        [f for f in os.listdir(directory) if f.lower().endswith(".mf4")],
        key=lambda f: os.path.getmtime(os.path.join(directory, f)),
        reverse=True
    )
    for file in mf4_files:
        try:
            path = os.path.join(directory, file)
            mdf = MDF(path, memory='minimum')
            print(f"✅ Loaded file: {file}")
            return mdf, file
        except Exception as e:
            print(f"⚠️ Failed to load {file}: {e}")
    raise FileNotFoundError("❌ No .mf4 files could be loaded.")

# === Extract and Export Signals ===
def extract_signals(mdf):
    signal_data = {}
    pdf_path = os.path.join(EXPORT_DIR, "all_plots.pdf")
    with PdfPages(pdf_path) as pdf:
        for key, names in KEYWORD_MAP.items():
            signal_data[key] = []
            for name in names:
                try:
                    sig = mdf.get(name)
                    entry = {
                        "name": name,
                        "unit": sig.unit,
                        "samples": sig.samples.tolist(),
                        "timestamps": sig.timestamps.tolist(),
                        "min": float(np.min(sig.samples)),
                        "max": float(np.max(sig.samples))
                    }
                    signal_data[key].append(entry)
                except Exception as e:
                    print(f"⚠️ Could not extract {key}: {e}")
            if signal_data[key]:
                export_group_plot(signal_data[key], key, pdf)
    return pdf_path

# === Export Plot ===
def export_group_plot(signals, key, pdf):
    plt.figure(figsize=(10, 4))
    for sig in signals:
        plt.plot(sig["timestamps"], sig["samples"], label=sig["name"])
    plt.xlabel("Time (s)")
    plt.ylabel(signals[0]["unit"] if signals[0]["unit"] else "Value")
    plt.title(key.replace("_", " ").title())
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    png_path = os.path.join(EXPORT_DIR, f"{key.replace(' ', '_')}.png")
    plt.savefig(png_path)
    pdf.savefig()
    plt.close()

# === MAIN ===
def main():
    mdf, filename = load_latest_mf4()
    print(f"Analyzing: {filename}")
    pdf_path = extract_signals(mdf)
    print(f"All plots exported to {EXPORT_DIR}")
    print(f"PDF with all plots saved to {pdf_path}")

    # Open PDF
    try:
        if os.name == 'nt':
            os.startfile(pdf_path)
        elif os.name == 'posix':
            subprocess.run(['xdg-open', pdf_path], check=False)
    except Exception as e:
        print(f"⚠️ Could not open PDF: {e}")

if __name__ == "__main__":
    main()
