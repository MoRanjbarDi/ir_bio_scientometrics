import os
from pathlib import Path
from playwright.sync_api import sync_playwright
import pandas as pd

DOWNLOAD_DIR = "files"

def run_scopus_export(query_string, download_folder, output_file):
    os.makedirs(download_folder, exist_ok=True)
    save_path = Path(download_folder) / output_file
    if save_path.exists():
        print(f"✅ Already downloaded: {save_path}")
        return
    else:

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(accept_downloads=True)
            page = context.new_page()

            print("Opening Scopus. Please log in manually if needed.")
            page.goto("https://www.scopus.com")

            

            search_url = (
                "https://www.scopus.com/results/results.uri?src=s&editSaveSearch=&origin=searchbasic&"
                "rr=&zone=resultslist&txGid=&s=" + query_string.replace(" ", "+")
            )

            print(f"Opening search results for {output_file}...")
            page.goto(search_url)

            try:
                page.wait_for_selector("span:has-text('Export filter counts')", timeout=30000)
                print("Clicking 'Export filter counts'...")
                page.click("span:has-text('Export filter counts')", force=True)

                with page.expect_download() as download_info:
                    print("Waiting for the download...")
                    download = download_info.value

                download.save_as(save_path)
                print(f"✅ Downloaded to: {save_path}")

            except Exception as e:
                print(f"❌ Error with {output_file}: {e}")

            browser.close()

def main():
    query_df = pd.read_csv("to_download_queries.csv")

    for _, row in query_df.iterrows():
        run_scopus_export(
            query_string=row['query_string'],
            download_folder=DOWNLOAD_DIR,
            output_file=row['output_file']
        )

if __name__ == "__main__":
    main()

