
# 📊 Scopus-Based Scientometric Dashboard

A modular Python system for downloading, managing, and visualizing scientometric data from Scopus. Built using Playwright and Plotly, it supports reproducible downloads and stunning visualizations to study scientific publishing trends, especially for customized queries (e.g., Iranian affiliations, article types, etc.).

---

## 📁 Project Structure

```
├── paper_counts_downloader.py       # Automated downloader using Playwright
├── my_functions.py                  # Utility and visualization functions
├── plotting_notebook.ipynb         # User-facing notebook to explore & plot
├── to_download.csv                 # CSV with queries to fetch from Scopus
├── files/                           # Directory containing downloaded CSVs
├── counts/, scatter_area/, ratio/  # Other directories for specific plots
├── ratio_plot_list.csv             # Defines numerator/denominator for ratios
```

---

## 🚀 Getting Started

### 1. **Install Required Libraries**

Make sure you have the following installed:

```bash
pip install pandas plotly playwright
playwright install
```

You also need **Google Chrome or Chromium** installed for Playwright to control the browser.

---

### 2. **Prepare the Queries**

Create a file named `to_download.csv` with two columns:

- `query_name`: A short label for the query (e.g., `artificial_intelligence`)
- `query_string`: A Scopus-compatible search string (e.g., `TITLE-ABS-KEY("artificial intelligence")`)

Example:

```csv
query_name,query_string
ai,TITLE-ABS-KEY("artificial intelligence")
ml,TITLE-ABS-KEY("machine learning")
```

---

### 3. **Download Data from Scopus**

To run the downloader, execute:

```bash
python paper_counts_downloader.py
```

- You will be prompted to **log into Scopus** manually.
- The script then automatically navigates to each query, downloads **filter counts**, and saves them as `.csv` files in the `files/` directory.
- It creates variations for:
  - Global vs Iran
  - Article vs Review
  - Combinations of above

Example output file names:
- `ai_global_ar_re.csv`
- `ai_iran_ar_0.csv`

---

## 📈 How to Use

### Open the `plotting_notebook.ipynb` in Jupyter Notebook or VS Code

Import your functions:

```python
from my_functions import *
```

Now you're ready to explore the data.

---

## 📊 Plotting Functions

### 1. `scatter_area()`

Overlapping area plot for multiple files.

```python
scatter_area(dir="./scatter_area")
```

#### Options:
- `ignore_current_year`: Skip most recent year(s)
- `past_what_years`: Limit to last N years
- `template`: Plotly theme (e.g., `"plotly_dark"`, `"ggplot2"`)

---

### 2. `count_plotter()`

Line chart showing trends in count data over time.

```python
count_plotter(files_directory="./counts", queryprint=1)
```

---

### 3. `top_k_what_plotter()`

Top-k bar chart of affiliations, authors, etc.

```python
top_k_what_plotter("ai_global_ar_re.csv", what="AFFILIATION", k=10)
```

---

### 4. `ratio_plotter()`

Plots ratio of two count datasets (numerator/denominator) over time.

- Requires `ratio_plot_list.csv` with columns:
  - `title`: Plot title
  - `soorat`: CSV for numerator
  - `makhraj`: CSV for denominator

Example `ratio_plot_list.csv`:

```csv
title,soorat,makhraj
Iran Share in AI,ai_iran_ar_re.csv,ai_global_ar_re.csv
```

Then run:

```python
ratio_plotter(files_directory="./ratio")
```

---

### 5. `set_plot_theme("plotly_dark")`

Change the Plotly theme globally for all plots.

---

## 🔄 Workflow

1. **Edit `to_download.csv`** as needed.
2. **Run `paper_counts_downloader.py`** to fetch updated counts.
3. **Use the notebook** to read, plot, and analyze the CSVs.
4. **Repeat** as more data becomes available.

---

## 📎 Notes

- Make sure Scopus access (e.g., through an institution) is valid.
- The downloader skips already downloaded files to save time.
- File naming is automatic and follows `[query]_[variation].csv`.

---

## 👤 Author

Created by a researcher working on scientometrics and data-driven insights into research publication trends.

---

## 📄 License

This project is released under the MIT License. You are free to use, modify, and distribute it.


---

## 🛠️ Function Reference & Argument Details

Below are detailed explanations of the arguments passed to each core plotting and data-handling function.

---

### 🔹 `read_data(filename, dir='./files')`

**Purpose:**  
Reads a CSV downloaded from Scopus and extracts the associated query string.

**Arguments:**
- `filename` *(str)* – Name of the CSV file (e.g. `'ai_global_ar_re.csv'`).
- `dir` *(str)* – Directory path where the file is stored. Defaults to `'./files'`.

---

### 🔹 `scatter_area(...)`

**Purpose:**  
Creates overlapping area plots of yearly paper counts from multiple CSV files in a folder.

**Arguments:**
- `dir` *(str)* – Folder with CSVs to be plotted. Example: `'./scatter_area'`.
- `ylabel` *(str)* – Y-axis label. Default is `"Number of Papers"`.
- `ignore_current_year` *(int)* – Ignores the most recent N years (often incomplete). Default: `1`.
- `past_what_years` *(int)* – Restrict to the last N years. Default: `30`.
- `random_color` *(int)* – Reserved for future use (currently unused).
- `renderer` *(str)* – How to display the plot (`"notebook"`, `"browser"`, etc.).
- `template` *(str or None)* – Plotly theme template (e.g., `"plotly_dark"`, `"ggplot2"`).

---

### 🔹 `count_plotter(...)`

**Purpose:**  
Generates line plots of yearly counts from all CSV files in a given directory.

**Arguments:**
- `files_directory` *(str)* – Directory containing CSVs. Default: `'./counts'`.
- `ignore_current_year` *(int)* – Skip the most recent N years.
- `queryprint` *(int)* – If set to `1`, shows the actual Scopus query on hover. Default: `0`.
- `ylabel` *(str)* – Y-axis label. Default: `"Counts"`.
- `template` *(str or None)* – Plotly theme.
- `renderer` *(str)* – Plot display method.

---

### 🔹 `top_k_what_plotter(file, what='AFFILIATION', k=10, dir='./files', ...)`

**Purpose:**  
Creates horizontal bar charts for the top-k entries of a specified field (e.g., top affiliations).

**Arguments:**
- `file` *(str)* – File name of the CSV (e.g. `'ai_global_ar_re.csv'`).
- `what` *(str)* – Column to plot (e.g., `"AFFILIATION"`, `"AUTHOR"`).
- `k` *(int)* – Number of top items to display. Default: `10`.
- `dir` *(str)* – Directory containing the file. Default: `'./files'`.
- `renderer` *(str)* – Plot display method.
- `template` *(str or None)* – Plotly theme.

---

### 🔹 `ratio_plotter(files_directory='./ratio', plot_list='ratio_plot_list.csv', template=None)`

**Purpose:**  
Plots ratios between two sets of yearly counts (numerator / denominator).

**Arguments:**
- `files_directory` *(str)* – Directory that contains the relevant CSV files and `plot_list` CSV.
- `plot_list` *(str)* – CSV file with columns: `title`, `soorat` (numerator), and `makhraj` (denominator).
- `template` *(str or None)* – Plotly theme.

**Example `ratio_plot_list.csv`:**

```csv
title,soorat,makhraj
Iran Share in AI,ai_iran_ar_re.csv,ai_global_ar_re.csv
```

---

### 🔹 `set_plot_theme(theme_name)`

**Purpose:**  
Set a global Plotly theme for all subsequent plots.

**Arguments:**
- `theme_name` *(str)* – Valid Plotly theme name (`"ggplot2"`, `"plotly_dark"`, `"seaborn"`, etc.).

---

### 🔹 `get_plot_theme()`

**Purpose:**  
Returns the currently active global Plotly theme.

**Returns:**
- *(str)* – Name of the active theme.
