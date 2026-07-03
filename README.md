# 🏆 GFG Campus Body Certificate Distribution Portal

An interactive, fast, and secure web application built with Python and Streamlit to distribute event certificates to participants. This portal allows participants to search for their name, preview their official certificate instantly in a high-definition PDF viewer, and securely download it directly to their device.

---

## ✨ Features

- **Instant Search & Selection:** Cleans and formats name data dynamically into an alphabetical, user-friendly dropdown search bar.
- **Embedded PDF Preview Pane:** Uses an elegant, secure inline frame layout to let users view their certificates before downloading, bypassing strict browser data URL blocks.
- **Robust Google Drive Integration:** Smartly converts standard sharing URLs into clean direct-stream downloads and interactive previews.
- **Fail-Safe Warning Protection:** Automatically detects if Google Drive presents an internal virus block, authentication request, or login page wall, providing a smart direct-link fallback button for affected users.
- **Error-Resistant Data Imports:** Cleans trailing whitespaces, filters empty rows, and protects against data type conversion crashes (`float` vs `str`) dynamically.

---

## 🛠️ Tech Stack & Dependencies

The project utilizes modern Python tools managed with the lightning-fast `uv` or `pip` toolchains:

- **[Streamlit](https://streamlit.io/)** (v1.58.0+) - Frontend UI layout framework.
- **[Pandas](https://pandas.pydata.org/)** (v3.0.3+) - Data structuring and CSV cleanup pipelines.
- **[Requests](https://requests.readthedocs.io/)** (v2.34.2+) - Secure file stream downloading from external networks.

---

## 📂 Project Structure

```text
gfg_certificates-main/
├── assets/
│   └── favicon.png          # App icon accent
├── certificates.csv         # Spreadsheet matching participant names to Drive links
├── main.py                  # Main operational Streamlit application script
├── pyproject.toml           # Modern package configuration metadata
├── uv.lock                  # Pinned deterministic dependencies
└── README.md                # System documentation