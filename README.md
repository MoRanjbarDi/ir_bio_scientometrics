
# 🔍 Scopus Filter Counts Exporter

This Python script uses [Playwright](https://playwright.dev/) to automatically extract **filter/facet counts** from [Scopus](https://www.scopus.com) for a series of predefined search queries. It is designed for scientometric analysis and supports different combinations of document types and country affiliations — including a focus on **Iranian publications**.

---

## 📂 Project Structure

```
.
├── scopus_export.py         # Main script
├── requirements.txt         # Python dependencies (optional)
└── scopus_filter_counts2/   # Folder where CSV downloads are saved
```

---

## 🚀 Features

- Supports multiple **biomedical and immunotherapy-related queries**
- Automatically extracts **facet counts** from Scopus (e.g., by subject area, country, document type)
- Downloads data as `.csv` files for easy downstream analysis
- Designed to handle different scopes:
  - **All results**
  - **Only articles (`ar`)**
  - **Only reviews (`re`)**
  - **Only Iranian-affiliated papers**
  - Combinations of the above

---

## 🔍 What It Extracts

For each keyword query, it runs **six variants**:

| Label             | Description                           |
|------------------|---------------------------------------|
| `global_ar_re`   | All document types, all countries     |
| `iran_ar_re`     | All document types, Iran only         |
| `global_ar`      | Articles only, all countries          |
| `global_re`      | Reviews only, all countries           |
| `iran_ar`        | Articles only, Iran only              |
| `iran_re`        | Reviews only, Iran only               |

Example output filenames:
```
til_iran_ar.csv
nk_cell_global_re.csv
immuno_global_ar_re.csv
```

---
## 🔑 Access Requirements

To access Scopus search results, authentication is necessary. You must either:

- Log in through your personal Scopus account,
- Be connected to a network with institutional access (e.g., university IP address),
- Or use a proxy or VPN that routes through an institution with a Scopus subscription.

The script will:

1. Launch the Scopus homepage in a browser window.
2. Allow you to manually authenticate if required.
3. Automatically continue with query execution and CSV export once access is granted.

---


## 🧠 Predefined Topics

Queries include:

- **immuno**: general immunotherapy terms
- **car_t_cell**
- **til**: Tumor-infiltrating lymphocytes
- **nk_cell**
- **macrophage**
- **checkpoint_inhibitors**
- **monoclonal_antibodies**
- **adcs**: Antibody-Drug Conjugates
- **oncolytic_virus**
- **cancer_vaccine**
- **life_sciences**: biomedical subject areas in general
- **all_articles**: global query to fetch everything

---

## ✅ Requirements

Install Python packages:

```bash
pip install playwright
playwright install
```

Linux users may also need:

```bash
playwright install-deps
```

---

## 🖥️ How to Run

```bash
python scopus_export.py
```

---

### ➕ Optional: Run in Headless Mode

To run without opening a visible browser window, change this line in the script:

```python
browser = p.chromium.launch(headless=False)
```

to:

```python
browser = p.chromium.launch(headless=True)
```

---

## 📁 Output

CSV files will be saved to the `scopus_filter_counts2/` directory with filenames formatted as:

```
<query_label>_<variation_label>.csv
```

Example:
```
checkpoint_inhibitors_iran_re.csv
```

---

## 🧑‍🔬 Author

created by me! Mohammad Ranjbar.
---

## 📜 License

This project is licensed under the MIT License.
