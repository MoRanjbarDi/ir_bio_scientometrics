
import os
import pandas as pd
import plotly.graph_objects as go

# Global theme variable
PLOTLY_THEME = "ggplot2"


def set_plot_theme(theme_name: str):
    """Set the global plot theme."""
    global PLOTLY_THEME
    PLOTLY_THEME = theme_name


def get_plot_theme() -> str:
    """Get the current plot theme."""
    return PLOTLY_THEME


def read_data(filename: str, dir: str = "./files"):
    """
    Reads a CSV file exported from Scopus count results.

    Parameters:
        filename (str): CSV file name
        dir (str): Directory path

    Returns:
        Tuple[pd.DataFrame, str]: Processed DataFrame and query string
    """
    filepath = os.path.join(dir, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        for _ in range(3):
            query = next(f)
        query = query[6:-2]

    df = pd.read_csv(filepath, skiprows=7)
    cols = df.columns.tolist()
    new_cols = []
    for i, col in enumerate(cols):
        if col.startswith("Unnamed"):
            new_cols.append(new_cols[i - 1] + "_COUNTS" if i > 0 else "UNKNOWN")
        else:
            new_cols.append(col)
    df.columns = new_cols

    return df, query


def scatter_area(dir: str = "./scatter_area", ylabel: str = "Number of Papers", ignore_current_year: int = 1,
                 past_what_years: int = 30, random_color: int = 0, renderer: str = "notebook", template=None):
    """
    Plots overlapping scatter area charts from CSVs in a folder.

    Parameters:
        dir (str): Folder path containing CSVs
        ylabel (str): Y-axis label
        ignore_current_year (int): Skip the most recent years
        past_what_years (int): Max number of years
        random_color (int): Reserved for future use
        renderer (str): Plotly renderer
        template (str): Plotly theme template
    """
    template = template or get_plot_theme()
    csv_files = [f for f in os.listdir(dir) if f.endswith('.csv')]
    all_data = []

    for file in csv_files:
        df, _ = read_data(file, dir)
        if 'YEAR' in df.columns and 'YEAR_COUNTS' in df.columns:
            df = df[['YEAR', 'YEAR_COUNTS']].dropna()
            df['YEAR'] = df['YEAR'].astype(int)
            df['YEAR_COUNTS'] = df['YEAR_COUNTS'].astype(int)

            latest_year = df['YEAR'].max()
            df = df[df['YEAR'] < latest_year - ignore_current_year + 1]
            df = df[df['YEAR'] >= latest_year - past_what_years + 1]

            df['Source'] = file[:-4]
            all_data.append(df)
        else:
            print(f"Skipping {file} — required columns not found.")

    combined_df = pd.concat(all_data)
    fig = go.Figure()

    for source in combined_df['Source'].unique():
        df_sub = combined_df[combined_df['Source'] == source]
        fig.add_trace(go.Scatter(
            x=df_sub['YEAR'],
            y=df_sub['YEAR_COUNTS'],
            mode='lines',
            fill='tozeroy',
            name=source,
            opacity=0.1
        ))

    fig.update_layout(
        title='Overlapping Area Plot of Scopus Year Counts by Query',
        xaxis_title='Year',
        yaxis_title=ylabel,
        template=template,
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", yanchor="top")
    )

    fig.show(renderer=renderer)


def top_k_what_plotter(file: str, what: str = "AFFILIATION", k: int = 10,
                        dir: str = "./files", renderer: str = "notebook", template=None):
    """
    Plots top-k bar chart of a specified column using plotly.graph_objects.

    Parameters:
        file (str): File name
        what (str): Column to sort
        k (int): Number of top rows to show
        dir (str): Directory path
        renderer (str): Plotly renderer
        template (str): Plotly theme
    """


    template = template or get_plot_theme()
    df, query = read_data(file, dir)
    df[what+'_COUNTS'] = pd.to_numeric(df[what+'_COUNTS'], errors="coerce")
    top_k = df.sort_values(by=what+'_COUNTS', ascending=False).head(k)

    print(query)
    


    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top_k[what+'_COUNTS'],
        y=top_k[what],
        orientation='h',
        name=f"Top {k} {what}"
    ))

    fig.update_layout(
        title=f"Top {k} by {what} Count",
        xaxis_title="Count",
        yaxis_title=what,
        template=template
    )
    print()
    fig.show(renderer=renderer)


def ratio_plotter(files_directory = "./ratio" , plot_list = "ratio_plot_list.csv",template= None):
    """takes all files specified in plot_list csv file and plots ratios"""

    template = template or get_plot_theme()
    # Load the list of datasets to be plotted
    plot_list = pd.read_csv(os.path.join(files_directory,plot_list))
    # Drop rows where either 'soorat' or 'makhraj' is missing
    plot_list = plot_list.dropna(subset=["soorat", "makhraj"])

    # Initialize a Plotly figure
    fig = go.Figure()

    # Iterate through each row in the list
    for idx, row in plot_list.iterrows():
        title = row["title"]
        soorat_file = row["soorat"]
        makhraj_file = row["makhraj"]
        color = row.get("color", None)
        line_style = row.get("line_style", "solid")  # default to solid


        # Read the numerator and denominator datasets
        soorat, _ = read_data(soorat_file, files_directory)
        makhraj, _ = read_data(makhraj_file, files_directory)

        # Merge on 'YEAR'
        ratio = pd.merge(soorat, makhraj, on='YEAR', suffixes=(soorat_file, makhraj_file))
        # print(ratio.head())

        # Compute the ratio
        ratio["Counts Ratio"] = ratio[f"YEAR_COUNTS{soorat_file}"] / ratio[f"YEAR_COUNTS{makhraj_file}"]

        # Add the trace to the figure 
        fig.add_trace(go.Scatter(
        x=ratio["YEAR"],
        y=ratio["Counts Ratio"],
        mode='lines+markers',
        name=title,
        line=dict(
            color=color if pd.notna(color) else None,
            dash=line_style if pd.notna(line_style) else "solid"
        )
    ))


    # Update the layout of the plot
    fig.update_layout(
        title="Ratios Over Time",
        xaxis_title="Year",
        yaxis_title="Counts Ratio",
        template=template,
        legend=dict(
            title="Legend",
            orientation="v",  # 'h' for horizontal
            x=0.5,
            xanchor="left",
            y=1,
            yanchor="top",
            borderwidth=1
        )
    )

    # Show the plot
    fig.show(renderer="notebook")


def count_plotter(files_directory="./counts", ignore_current_year=1, queryprint=0, ylabel="Counts", template=None,renderer: str = "notebook"):
    """ plot lines on all csv files inside a folder specifed"""
    template = template or get_plot_theme()

    fig = go.Figure()

    for filename in os.listdir(files_directory):
        if filename.endswith(".csv"):
            data, query = read_data(filename, files_directory)
            year_data = data[['YEAR', 'YEAR_COUNTS']].dropna().iloc[ignore_current_year:, :]
            title = filename[:-4]
            if queryprint == 0:
                query = ""
            fig.add_trace(go.Scatter(
                x=year_data["YEAR"],
                y=year_data["YEAR_COUNTS"],
                mode="lines+markers",
                name=title,
                hovertemplate=f"<b>{title}</b><br>Year: %{{x}}<br>Count: %{{y}}<extra>{query}</extra>"
            ))

    fig.update_layout(
        title="Counts Over Time",
        xaxis_title="Year",
        yaxis_title=ylabel,
        xaxis=dict(tickmode="linear", dtick=4),
        yaxis=dict(nticks=10),
        template = template,
        legend=dict(
            title="Legend",
            orientation="v",
            x=0.5,
            xanchor="left",
            y=1,
            yanchor="top"
        )
    )

    fig.show(renderer=renderer)


