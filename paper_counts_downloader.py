import os
from pathlib import Path
from playwright.sync_api import sync_playwright
import pandas as pd

query_list = pd.read_csv("to_download.csv")

QUERIES = dict(zip(query_list['query_name'], query_list['query_string']))





VARIATIONS = [
    ("global_ar_re", ""),
    ("iran_ar_re", " AND AFFILCOUNTRY(Iran)"),
    ("global_ar_0", " AND DOCTYPE(ar)"),
    ("global_re_0", " AND DOCTYPE(re)"),
    ("iran_ar_0", " AND AFFILCOUNTRY(Iran) AND DOCTYPE(ar)"),
    ("iran_re_0", " AND AFFILCOUNTRY(Iran) AND DOCTYPE(re)"),
    
]

DOWNLOAD_DIR = "files"


def run_scopus_export(query, download_folder, label):
    os.makedirs(download_folder, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("Opening Scopus. Please log in manually if needed.")
        page.goto("https://www.scopus.com")

        #input("After logging in and seeing the Scopus homepage, press ENTER to continue...")

        for var_label, var_suffix in VARIATIONS:
            save_path = Path(download_folder) / f"{label}_{var_label}.csv"
            if save_path.exists():
                print(f"⏩ Skipping already downloaded: {save_path}")
                continue

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
