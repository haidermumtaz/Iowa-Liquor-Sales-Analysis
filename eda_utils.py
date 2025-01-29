import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def bar_plot_top_n(data, group_by_col, value_col=None, title=None, xlabel=None, ylabel=None, agg_func='sum', top_n=10):
    """
    Create a bar plot of the top N entries based on specified grouping and metrics.
    If value_col is None, plots counts of group_by_col.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        The input DataFrame (can be multi-indexed)
    group_by_col : str
        Column to group by (e.g., 'City', 'Category Name')
    value_col : str, optional
        Column to aggregate (e.g., 'Sale (Dollars)', 'Store Number')
        If None, counts occurrences of group_by_col
    title : str, optional
        Plot title. If None, generates based on parameters
    xlabel : str, optional
        X-axis label. If None, generates based on parameters
    ylabel : str, optional
        Y-axis label. If None, uses group_by_col
    agg_func : str, optional
        Aggregation function ('sum', 'count', 'mean', 'nunique', etc.)
        Default is 'sum'
    top_n : int, optional
        Number of top entries to display
        Default is 10
    """
    # Reset index if it's a multi-index DataFrame
    if isinstance(data.index, pd.MultiIndex):
        df = data.reset_index()
    else:
        df = data.copy()
    
    # Group and aggregate data
    if value_col is None:
        # Count occurrences if no value column specified
        grouped_data = (df[group_by_col].value_counts()
                       .head(top_n))
        # Set default labels for count plot
        if xlabel is None:
            xlabel = 'Count'
        if title is None:
            title = f'Top {top_n} {group_by_col} by Count'
    else:
        # Aggregate by specified column and function
        grouped_data = (df.groupby(group_by_col)[value_col]
                       .agg(agg_func)
                       .sort_values(ascending=False)
                       .head(top_n))
        # Set default labels for value plot
        if xlabel is None:
            xlabel = f'{value_col} ({agg_func})'
        if title is None:
            title = f'Top {top_n} {group_by_col} by {value_col} ({agg_func})'
    
    # Adjust figure size based on number of entries
    fig_height = max(6, top_n * 0.4)  # Dynamic height based on top_n
    plt.figure(figsize=(12, fig_height))
    
    # Create plot
    sns.barplot(x=grouped_data.values, 
                y=grouped_data.index)
    
    # Format x-axis labels to use regular numbers instead of scientific notation
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    # Customize plot
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel if ylabel else group_by_col)
    plt.tight_layout()
    plt.show()


def map_to_coarse_category(category, coarse_category_mapping):
    """
    Maps detailed liquor categories to coarse-grained categories.
    
    Parameters:
    -----------
    category : str
        The detailed category name to map
    coarse_category_mapping : dict
        Dictionary mapping coarse categories to lists of detailed categories
        
    Returns:
    --------
    str
        The coarse category name or 'UNKNOWN' if no match found
    """
    if pd.isna(category):
        return 'UNKNOWN'
    for coarse_category, detailed_categories in coarse_category_mapping.items():
        if category in detailed_categories:
            return coarse_category
    return 'UNKNOWN'


def extract_city_from_store(store_name):
    """
    Extracts city name from store name that follows pattern 'STORE NAME / CITY'
    
    Parameters:
    -----------
    store_name : str
        The store name potentially containing city information
        
    Returns:
    --------
    str or None
        Extracted city name if found, None otherwise
    """
    if pd.isna(store_name):
        return None
    parts = store_name.split('/')
    if len(parts) > 1:
        return parts[-1].strip()
    return None


