import os
import pandas as pd
from config_handler import load_config, collect_needed_queries
from plot_runner import run_scatter_area, run_count_plotter, run_top_k, run_ratio_plotter
from my_functions import set_plot_theme
from plot_runner import run_stacked_top_k

from utils import ensure_dir

def build_file_map(needed_queries_df, files_dir='files'):
    """
    Builds:
    {
        'query_name': {
            'var': './files/query_var.csv'
        }
    }
    """
    file_map = {}
    for _, row in needed_queries_df.iterrows():
        query_name = row['query_name']
        print("query_name = " , query_name )
        var = row['vars']  # << direct from config
        print("var_name = " , var )
        output_file = row['output_file']
        if query_name not in file_map:
            file_map[query_name] = {}
        file_map[query_name][var] = f"{files_dir}/{output_file}"
    return file_map

def main():
    CONFIG_FILE = 'config.xlsx'
    FILES_DIR = 'files'
    OUTPUT_DIR = 'outputs'

    print("📥 Loading config...")
    sheets = load_config(CONFIG_FILE)
    query_df = sheets['query_list']
    query_dict = dict(zip(query_df['query_name'], query_df['query_string']))

    # Build exact queries with variations applied
    needed_queries_df = collect_needed_queries(sheets, query_dict)
    needed_queries_df.to_csv('to_download_queries.csv', index=False)

    # Build file map for plotting
    file_map = build_file_map(needed_queries_df, files_dir=FILES_DIR)

    ensure_dir(OUTPUT_DIR)

    # Run downloader
    os.system('python paper_counts_downloader.py')

    # Apply global theme if set
    if 'global_settings' in sheets:
        settings = sheets['global_settings']
        theme = settings.loc[settings['setting'] == 'template', 'value'].values[0]
        set_plot_theme(theme)

    # Run plots
    if 'scatter_area' in sheets:
        print("📊 Running scatter_area plots...")
        run_scatter_area(sheets['scatter_area'], file_map, output_dir=os.path.join(OUTPUT_DIR, 'scatter_area'))

    if 'count_plotter' in sheets:
        print("📊 Running count_plotter plots...")
        run_count_plotter(sheets['count_plotter'], file_map, output_dir=os.path.join(OUTPUT_DIR, 'count_plotter'))

    if 'top_k_what_plotter' in sheets:
        print("📊 Running top_k_what_plotter plots...")
        run_top_k(sheets['top_k_what_plotter'], file_map, output_dir=os.path.join(OUTPUT_DIR, 'top_k'))

    if 'ratio_plotter' in sheets:
        print("📊 Running ratio_plotter plots...")
        run_ratio_plotter(sheets['ratio_plotter'], file_map, output_dir=os.path.join(OUTPUT_DIR, 'ratio'))
    if 'stacked_top_k_plotter' in sheets:
        print("📊 Running stacked_top_k_plotter...")
        run_stacked_top_k(sheets['stacked_top_k_plotter'], file_map, output_dir=os.path.join(OUTPUT_DIR, 'stacked_top_k'))


if __name__ == "__main__":
    main()

