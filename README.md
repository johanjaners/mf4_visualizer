# 🔍 mf4_visualizer

A simple Python tool for visualizing signals in `.mf4` log files.  
Focused on EV battery test data through signal filtering and exportable plots.

---

## ✨ Features

📂 Auto-loads the latest `.mf4` file  
🔎 Signal filtering using `KEYWORD_MAP`  
📈 Plots signals with time axis 
🖼 Exports individual plots as `.png`  
📄 Combines all plots into a single `.pdf`  
🚫 `.gitignore` excludes log files and exports

---

## 🌆 Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Use

1. Place `.mf4` files in `mf4_logfiles/`  
2. Adjust `KEYWORD_MAP` in `mf4_visualizer.py` if needed  
3. Run the visualizer:
```bash
python mf4_visualizer.py
```
4. View exported plots in `mf4_exports/`  
5. PDF will open automatically after running

---

## 🗂 Version History

**v1.0.0** – Initial version with plotting and export

---

## 📘 License

MIT License – use freely, credit appreciated

