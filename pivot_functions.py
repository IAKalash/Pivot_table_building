import pandas as pd
import os

def read_table(source_path):
    """
    Reads a table from a file (CSV or Excel).
    
    Args:
        source_path (str): Path to the input file (.csv, .xls, .xlsx).
    
    Returns:
        pd.DataFrame: Loaded DataFrame.
    
    Raises:
        FileNotFoundError: If file does not exist.
        TypeError: If file extension is unsupported.
    """
    # Dictionary mapping file extensions to Pandas read functions
    extension_dictionary = {".xls": "excel", ".xlsx": "excel", ".csv": "csv"}

    # Check if file exists
    if os.path.isfile(source_path):
        _, extension = os.path.splitext(source_path)

        # Check if extension is supported and load the table
        if extension in extension_dictionary:
            read_func = getattr(pd, "read_" + extension_dictionary[extension])
            table = read_func(source_path)
            return table
        else:
            raise TypeError("Unsupported file type")
    else:
        raise FileNotFoundError("File not found")

def make_pivot_table(table=pd.DataFrame(), aggregation_col=None, index_col=None, columns=None, fill_val=None):
    """
    Creates a pivot table with mean aggregation, auto-selecting columns if not specified.
    
    Args:
        table (pd.DataFrame): Input DataFrame with data to aggregate.
        aggregation_col (str, optional): Numeric column for aggregation. Defaults to first numeric column.
        index_col (str, optional): Column for row grouping. Defaults to last categorical column.
        columns (str, optional): Column for column grouping. Defaults to second-to-last categorical column if available.
        fill_val (any, optional): Value to replace NaN in pivot table. Defaults to None.
    
    Returns:
        pd.DataFrame: Pivot table with mean aggregation.
    
    Raises:
        TypeError: If table is not a pandas DataFrame.
        ValueError: If table is empty, no numeric/categorical columns, or specified columns not found.
    
    Example:
        >>> df = pd.read_csv('./tests/titanic.csv')
        >>> pivot = make_pivot_table(df, index_col='Pclass', columns='Sex', aggregation_col='Age')
    """
    # Validate input: ensure table is a DataFrame and not empty
    if not isinstance(table, pd.DataFrame):
        raise TypeError("Use only pandas.DataFrame type")
    if table.empty:
        raise ValueError("Empty table")

    # Auto-select index and columns if not provided
    if index_col is None:
        # Find categorical columns (strings or categories) for grouping
        categorial_cols = table.select_dtypes(include=['object', 'category']).columns.to_list()
        if not categorial_cols:
            raise ValueError("No index columns")
        else:
            index_col = categorial_cols[-1]  # Select last categorical column
            if columns is None:
                if len(categorial_cols) > 1:
                    columns = categorial_cols[-2]  # Select second-to-last if available

    # Validate index_col if provided
    elif not set(index_col).issubset(set(table.columns)):
        raise ValueError(f"Column(s) {index_col} not found")

    # Auto-select numeric column for aggregation if not provided
    if aggregation_col is None:
        # First try float columns, then any numeric (int/float)
        num_cols = table.select_dtypes(include='float').columns.to_list()
        if not num_cols:
            num_cols = table.select_dtypes(include='number').columns.to_list()
            if not num_cols:
                raise ValueError("No numeric columns for aggregation")
        aggregation_col = num_cols[-1]  # Select last numeric column

    # Validate aggregation_col if provided
    elif not set(aggregation_col).issubset(set(table.columns)):
        raise ValueError(f"Column(s) {aggregation_col} not found")

    # Create pivot table with mean aggregation
    pivot = pd.pivot_table(
        table,
        values=aggregation_col,
        index=index_col,
        columns=columns,
        aggfunc='mean',
        fill_value=fill_val
    )

    return pivot

def main():
    # Prompt user for file path
    print("Enter the path to the table")
    src_path = input()

    try:
        # Load table from file
        table = read_table(src_path)
        # Display input DataFrame
        print("\n", table)

        # Create and display pivot table
        print(make_pivot_table(table))

    except (ValueError, TypeError, FileNotFoundError) as e:
        # Handle errors during file loading or pivot creation
        print(f"Error: {e}")

main()