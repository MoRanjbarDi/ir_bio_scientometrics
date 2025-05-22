# regarding the limitations with playwright, this code is less likely 
# to run correctly on of google.colab free tier, even if set to headless mode!


import os
from pathlib import Path
from playwright.sync_api import sync_playwright

QUERIES = {
    "immuno": 'TITLE-ABS-KEY (immunotherap*) OR TITLE-ABS-KEY ("immuno engineering") OR TITLE-ABS-KEY ("immunoengineering")',
    "all_articles   ": 'PUBYEAR > 1',
    "life_sciences": 'PUBYEAR > 1 AND ( LIMIT-TO ( SUBJAREA , "MEDI" ) OR LIMIT-TO ( SUBJAREA , "BIOC" ) OR LIMIT-TO ( SUBJAREA , "IMMU" ) OR LIMIT-TO ( SUBJAREA , "PHAR" ) OR LIMIT-TO ( SUBJAREA , "AGRI" ) OR LIMIT-TO ( SUBJAREA , "NEUR"))',
    "cancer_vaccine": 'TITLE-ABS-KEY("Cancer Vaccin*")',
    "car_t_cell": 'TITLE-ABS-KEY("chimeric antigen receptor")',
    "til": 'TITLE-ABS-KEY("Tumor-infiltrating lymphocytes") OR TITLE-ABS-KEY("Lymphocytes, Tumor-Infiltrating")',
    "nk_cell": '(TITLE-ABS-KEY("NK therap*") OR TITLE-ABS-KEY("Natural Killer Cel*") OR TITLE-ABS-KEY("Killer Cells, Natural"))',
    "macrophage": 'TITLE-ABS-KEY(macrophag*)',
    "checkpoint_inhibitors": 'TITLE-ABS-KEY("checkpoint inhibit*")',
    "oncolytic_virus": '(TITLE-ABS-KEY("oncolytic virus*") OR TITLE-ABS-KEY("Oncolytic Virotherap*") OR TITLE-ABS-KEY("Oncolytic Adenovirus*") OR TITLE-ABS-KEY(virotherapy))',
    "monoclonal_antibodies": '(TITLE-ABS-KEY("Monoclonal Antibod*") OR TITLE-ABS-KEY("Antibodies, Monoclonal"))',
    "adcs": '(TITLE-ABS-KEY("Antibody-drug conjugat*") OR TITLE-ABS-KEY("Antibody drug conjugat*"))'
}

VARIATIONS = [
    ("global_ar_re", ""),
    ("iran_ar_re", " AND AFFILCOUNTRY(Iran)"),
    ("global_ar", " AND DOCTYPE(ar)"),
    ("global_re", " AND DOCTYPE(re)"),
    ("iran_ar", " AND AFFILCOUNTRY(Iran) AND DOCTYPE(ar)"),
    ("iran_re", " AND AFFILCOUNTRY(Iran) AND DOCTYPE(re)"),
    
]

DOWNLOAD_DIR = "scopus_filter_counts2"


def run_scopus_export(query, download_folder, label):
    os.makedirs(download_folder, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("Opening Scopus. Please log in manually if needed.")
        page.goto("https://www.scopus.com")

        #input("After logging in and seeing the Scopus homepage, press ENTER to continue...")

        for var_label, var_suffix in VARIATIONS:
            search_query = query + var_suffix
            search_url = (
                "https://www.scopus.com/results/results.uri?src=s&editSaveSearch=&origin=searchbasic&"
                "rr=&zone=resultslist&txGid=&s=" + search_query.replace(" ", "+")
            )

            print(f"Opening search results for {label} - {var_label}...")
            page.goto(search_url)

            try:
                page.wait_for_selector("span:has-text('Export filter counts')", timeout=30000)
                print("Clicking 'Export filter counts'...")
                page.click("span:has-text('Export filter counts')", force=True)

                with page.expect_download() as download_info:
                    print("Waiting for the download...")
                    download = download_info.value

                save_path = Path(download_folder) / f"{label}_{var_label}.csv"
                download.save_as(save_path)
                print(f"✅ Downloaded to: {save_path}")

            except Exception as e:
                print(f"Error with {label} - {var_label}: {e}")

        browser.close()


if __name__ == "__main__":
    for label, query in QUERIES.items():
        run_scopus_export(query, DOWNLOAD_DIR, label)
