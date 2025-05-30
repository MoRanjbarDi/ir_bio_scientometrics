import pandas as pd

VARIATION_MAP = {
    "global_ar_re": "",
    "iran_ar_re": " AND AFFILCOUNTRY(Iran)",
    "global_ar_0": " AND DOCTYPE(ar)",
    "global_re_0": " AND DOCTYPE(re)",
    "iran_ar_0": " AND AFFILCOUNTRY(Iran) AND DOCTYPE(ar)",
    "iran_re_0": " AND AFFILCOUNTRY(Iran) AND DOCTYPE(re)",
}

def load_config(excel_file):
    config = pd.ExcelFile(excel_file)
    sheets = {}
    for sheet in config.sheet_names:
        sheets[sheet] = config.parse(sheet)
    return sheets

def collect_needed_queries(sheets, query_dict):
    rows = []
    pairs = set()

    if 'scatter_area' in sheets:
        df = sheets['scatter_area']
        for _, row in df.iterrows():
            pairs.add((row['query_name'], row['vars']))

    if 'count_plotter' in sheets:
        df = sheets['count_plotter']
        for _, row in df.iterrows():
            pairs.add((row['query_name'], row['vars']))

    if 'top_k_what_plotter' in sheets:
        df = sheets['top_k_what_plotter']
        for _, row in df.iterrows():
            pairs.add((row['query_name'], row['vars']))
    if 'stacked_top_k_plotter' in sheets:
        df = sheets['stacked_top_k_plotter']
        for _, row in df.iterrows():
            pairs.add((row['query1'], row['var1']))
            pairs.add((row['query2'], row['var2']))

    if 'ratio_plotter' in sheets:
        df = sheets['ratio_plotter']
        for _, row in df.iterrows():
            pairs.add((row['numerator_query'], row['numerator_vars']))
            pairs.add((row['denominator_query'], row['denominator_vars']))

    for query, var in pairs:
        query_string = query_dict[query] + VARIATION_MAP.get(var, "")
        output_file = f"{query}_{var}.csv"
        rows.append({
            'query_name': query,
            'vars': var,
            'query_string': query_string,
            'output_file': output_file
        })


    return pd.DataFrame(rows)

