import pandas as pd
import os
from my_functions import scatter_area, count_plotter, top_k_what_plotter, ratio_plotter,read_data,stacked_top_k_bar
from utils import check_file_exists, ensure_dir

def run_scatter_area(config_df, file_map, output_dir='outputs/scatter_area'):
    ensure_dir(output_dir)
    for plot_title, group in config_df.groupby('plot_title'):
        files = []
        for _, row in group.iterrows():
            query = row['query_name']
            var = row['vars']
            file = file_map[query][var]
            check_file_exists(file)
            files.append(file)
        scatter_area(file_list=files, ylabel=row.get('ylabel', 'Counts'))

def run_count_plotter(config_df, file_map, output_dir='outputs/count_plotter'):
    ensure_dir(output_dir)
    for plot_title, group in config_df.groupby('plot_title'):
        files = []
        for _, row in group.iterrows():
            query = row['query_name']
            print(query)
            var = row['vars']
            title = row['plot_title']
            name = row['name_in_legend']
            
            file = file_map[query][var]
            check_file_exists(file)
            files.append(file)
        count_plotter(files, title = title, name = name, ylabel=row.get('ylabel', 'Counts'))

def run_top_k(config_df, file_map, output_dir='outputs/top_k'):
    ensure_dir(output_dir)
    for _, row in config_df.iterrows():
        query = row['query_name']
        var = row['vars']
        what = row['what']
        k = int(row['k'])
        stack_by = row.get('stack_by') if 'stack_by' in row else None

        file = file_map[query][var]
        check_file_exists(file)

        filename = os.path.basename(file)
        dirpath = os.path.dirname(file)

        top_k_what_plotter(file=filename, what=what, k=k, dir=dirpath, stack_by=stack_by)


def run_ratio_plotter(config_df, file_map, output_dir='outputs/ratio'):
    ensure_dir(output_dir)

    for plot_title, group in config_df.groupby('plot_title'):
        print(f"📊 Plotting ratio chart: {plot_title}")
        ratio_plotter(group, file_map, plot_title=plot_title)
        
        
def run_stacked_top_k(config_df, file_map, output_dir='outputs/stacked_top_k'):
    ensure_dir(output_dir)

    for _, row in config_df.iterrows():
        query1 = row['query1']
        var1 = row['var1']
        query2 = row['query2']
        var2 = row['var2']
        x_col = row['x_col']
        k = int(row['k'])
        name1 = row.get('name1', f"{query1}_{var1}")
        name2 = row.get('name2', f"{query2}_{var2}")
        stack_or_group = row['stack_or_group']

        file1 = file_map[query1][var1]
        file2 = file_map[query2][var2]
        check_file_exists(file1)
        check_file_exists(file2)

        df1, _ = read_data(os.path.basename(file1), os.path.dirname(file1))
        df2, _ = read_data(os.path.basename(file2), os.path.dirname(file2))

        stacked_top_k_bar(df1, df2, x_col=x_col, k=k, name1=name1, name2=name2,stack_or_group = stack_or_group)



