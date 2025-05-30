
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
def scatter_area(file_list, ignore_current_year=1, queryprint=0, ylabel="Counts", template=None, renderer="notebook"):
    """
    Plots overlapping scatter area charts from CSV list.

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
    fig = go.Figure()

    for filepath in file_list:
        filename = os.path.basename(filepath)
        dirpath = os.path.dirname(filepath)
        data, query = read_data(filename, dirpath)
        year_data = data[['YEAR', 'YEAR_COUNTS']].dropna().iloc[ignore_current_year:, :]
        title = filename[:-4]
        if queryprint == 0:
            query = ""
        fig.add_trace(go.Scatter(
            x=year_data["YEAR"],
            y=year_data["YEAR_COUNTS"],
            fill='tozeroy',
            mode="lines",
            name=title,
            hovertemplate=f"<b>{title}</b><br>Year: %{{x}}<br>Count: %{{y}}<extra>{query}</extra>",
            opacity = 0.1
        ))

    fig.update_layout(
        title="Counts Over Time",
        xaxis_title="Year",
        yaxis_title=ylabel,
        xaxis=dict(tickmode="linear", dtick=4),
        yaxis=dict(nticks=10),
        template=template,
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




def top_k_what_plotter(file: str, what: str = "AFFILIATION", k: int = 10,
                       dir: str = "./files", renderer: str = "notebook", template=None, stack_by=None):
    """
    Plots top-k bar chart (optionally stacked) of a specified column using plotly.graph_objects.

    Parameters:
        file (str): File name
        what (str): Column to sort
        k (int): Number of top rows to show
        dir (str): Directory path
        renderer (str): Plotly renderer
        template (str): Plotly theme
        stack_by (str): Column name to stack bars by
    """
    template = template or get_plot_theme()
    df, query = read_data(file, dir)

    # Parse count column
    count_col = f"{what}_COUNTS"
    df[count_col] = pd.to_numeric(df[count_col], errors="coerce")

    # If stacking is enabled
    if stack_by and stack_by in df.columns:
        df = df[[what, stack_by, count_col]].dropna()

        # Aggregate counts
        grouped = df.groupby([what, stack_by])[count_col].sum().reset_index()

        # Get top-K by total count
        top_k_keys = (
            grouped.groupby(what)[count_col]
            .sum()
            .sort_values(ascending=False)
            .head(k)
            .index.tolist()
        )

        grouped = grouped[grouped[what].isin(top_k_keys)]

        fig = go.Figure()
        for stack_val in grouped[stack_by].unique():
            sub_df = grouped[grouped[stack_by] == stack_val]
            fig.add_trace(go.Bar(
                x=sub_df[count_col],
                y=sub_df[what],
                orientation='h',
                name=str(stack_val)
            ))
    else:
        # Regular top-k flat bars
        top_k = df[[what, count_col]].dropna().sort_values(by=count_col, ascending=False).head(k)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top_k[count_col],
            y=top_k[what],
            orientation='h',
            name=f"Top {k} {what}"
        ))

    fig.update_layout(
        title=f"Top {k} by {what} Count",
        xaxis_title="Count",
        yaxis_title=what,
        barmode='stack' if stack_by else 'group',
        template=template
    )

    fig.show(renderer=renderer)



def ratio_plotter(ratio_df, file_map, plot_title="Ratio Plot", template=None, renderer="notebook"):
    """
    Plots a single ratio chart with multiple lines (one trace per row).
    
    Parameters:
        ratio_df (pd.DataFrame): DataFrame for a single plot_title group.
        file_map (dict): mapping query_name + var → filepath
        plot_title (str): Title of the plot
        template (str): Plotly theme template
        renderer (str): Plotly renderer
    """
    if ratio_df.empty:
        print(f"⚠️ Skipping ratio plot: '{plot_title}' is empty.")
        return

    template = template or get_plot_theme()
    fig = go.Figure()

    for _, row in ratio_df.iterrows():
        name = row["name_in_legend"]
        numerator_query = row["numerator_query"]
        numerator_var = row["numerator_vars"]
        denominator_query = row["denominator_query"]
        denominator_var = row["denominator_vars"]

        num_file = file_map[numerator_query][numerator_var]
        denom_file = file_map[denominator_query][denominator_var]

        numerator_df, _ = read_data(os.path.basename(num_file), os.path.dirname(num_file))
        denominator_df, _ = read_data(os.path.basename(denom_file), os.path.dirname(denom_file))

        # Merge and compute ratio
        ratio = pd.merge(numerator_df, denominator_df, on='YEAR', suffixes=('_num', '_denom'))
        ratio["Counts Ratio"] = ratio["YEAR_COUNTS_num"] / ratio["YEAR_COUNTS_denom"]

        fig.add_trace(go.Scatter(
            x=ratio["YEAR"],
            y=ratio["Counts Ratio"],
            mode='lines+markers',
            name=name
        ))

    fig.update_layout(
        title=plot_title,
        xaxis_title="Year",
        yaxis_title="Counts Ratio",
        template=template,
        legend=dict(
            title="Legend",
            orientation="v",
            x=0.5,
            xanchor="left",
            y=1,
            yanchor="top",
            borderwidth=1
        )
    )

    fig.show(renderer=renderer)



def count_plotter(file_list, ignore_current_year=1, queryprint=0, ylabel="Counts", template=None, renderer="notebook"):
    """
    Plot lines from a specific list of CSV files.
    """
    template = template or get_plot_theme()
    fig = go.Figure()

    for filepath in file_list:
        filename = os.path.basename(filepath)
        dirpath = os.path.dirname(filepath)
        data, query = read_data(filename, dirpath)
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
        template=template,
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
    
    
def stacked_top_k_bar(df1, df2, x_col="AFFILIATION", k=10, name1="Dataset 1", name2="Dataset 2", template=None, renderer="notebook",stack_or_group="stack"):
    template = template or get_plot_theme()

    col_counts = f"{x_col}_COUNTS"
    df1 = df1[[x_col, col_counts]].copy()
    df2 = df2[[x_col, col_counts]].copy()

    df1["__source__"] = name1
    df2["__source__"] = name2

    combined = pd.concat([df1, df2])
    grouped = combined.groupby([x_col, "__source__"])[col_counts].sum().reset_index()

    top_k_names = (
        grouped.groupby(x_col)[col_counts].sum()
        .sort_values(ascending=False)
        .head(k)
        .index.tolist()
    )

    grouped = grouped[grouped[x_col].isin(top_k_names)]
    pivot_df = grouped.pivot(index=x_col, columns="__source__", values=col_counts).fillna(0)

    pivot_df["__total__"] = pivot_df.sum(axis=1)
    pivot_df = pivot_df.sort_values("__total__", ascending=False).drop(columns="__total__")

    fig = go.Figure()
    for source_name in pivot_df.columns:
        fig.add_trace(go.Bar(x=pivot_df.index, y=pivot_df[source_name], name=source_name,))

    fig.update_layout(
        barmode=stack_or_group,
        title=f"Top {k} by {x_col} ({stack_or_group}ed)",
        xaxis_title=x_col,
        yaxis_title="Total Count",
        template=template
    )

    fig.show(renderer=renderer)
