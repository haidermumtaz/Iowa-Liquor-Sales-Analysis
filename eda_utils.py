import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def bar_plot_top_10(data, group_by_col, value_col, title, xlabel, ylabel=None, agg_func='sum'):
    """
    Create a bar plot of the top 10 entries based on specified grouping and metrics.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        The input DataFrame (can be multi-indexed)
    group_by_col : str
        Column to group by (e.g., 'City', 'Category Name')
    value_col : str
        Column to aggregate (e.g., 'Sale (Dollars)', 'Store Number')
    title : str
        Plot title
    xlabel : str
        X-axis label
    ylabel : str, optional
        Y-axis label (if None, uses group_by_col)
    agg_func : str, optional
        Aggregation function ('sum', 'count', 'mean', 'nunique', etc.)
        Default is 'sum'
    """
    # Reset index if it's a multi-index DataFrame
    if isinstance(data.index, pd.MultiIndex):
        df = data.reset_index()
    else:
        df = data.copy()
    
    # Group and aggregate data
    grouped_data = (df.groupby(group_by_col)[value_col]
                   .agg(agg_func)
                   .sort_values(ascending=False)
                   .head(10))
    
    # Create plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x=grouped_data.values, 
                y=grouped_data.index)
    
    # Customize plot
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel if ylabel else group_by_col)
    plt.tight_layout()
    plt.show()


