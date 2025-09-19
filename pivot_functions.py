import pandas as pd
import os

# Global extension dictionary (limited by dependencies: pandas for csv, openpyxl for xlsx)
_EXTENSION_DICT = {".xlsx": "excel", ".csv": "csv"}

def read_table(source_path):
    """
    Reads a table from a file (CSV or Excel).
    
    Args:
        source_path (str): Path to the input file (.csv, .xlsx).
    
    Returns:
        pd.DataFrame: Loaded DataFrame.
    
    Raises:
        FileNotFoundError: If file does not exist.
        TypeError: If file extension is unsupported.
    """
    if os.path.isfile(source_path):
        _, ext = os.path.splitext(source_path)
        if ext in _EXTENSION_DICT:
            read_func = getattr(pd, "read_" + _EXTENSION_DICT[ext])
            return read_func(source_path)
        raise TypeError("Unsupported file type")
    raise FileNotFoundError("File not found")

def make_pivot_table(table=pd.DataFrame(), aggregation_col=None, index_col=None, columns=None, fill_val=None, output_path=None):
    """
    Creates a pivot table with mean aggregation, auto-selecting columns if not specified.
    
    Args:
        table (pd.DataFrame): Input DataFrame with data to aggregate.
        aggregation_col (str, list or set, optional): Numeric column(s). Defaults to last numeric column.
        index_col (str, list or set, optional): Row grouping column(s). Defaults to last categorical column.
        columns (str, list or set, optional): Column grouping column(s). Defaults to second-to-last categorical column if available.
        fill_val (any, optional): Value to replace NaN. Defaults to None.
        output_path (str, optional): Path to save pivot table (.csv or .xlsx). Defaults to None.
    
    Returns:
        pd.DataFrame: Pivot table with mean aggregation.
    
    Raises:
        TypeError: If table is not a pandas DataFrame, columns have invalid types, or fill_val is not numeric.
        ValueError: If table is empty, no numeric/categorical columns, columns not found, or index/columns coincide.
    
    Example:
        >>> df = pd.read_csv('titanic.csv')
        >>> pivot = make_pivot_table(df, index_col='Pclass', columns='Sex', aggregation_col='Age')
    """
    if not isinstance(table, pd.DataFrame):
        raise TypeError("Use only pandas.DataFrame type")
    if table.empty:
        raise ValueError("Empty table")

    # Normalize parameters to lists
    index_col = list(index_col) if isinstance(index_col, (set, tuple)) else [index_col] if isinstance(index_col, str) else index_col if index_col else None
    columns = list(columns) if isinstance(columns, (set, tuple)) else [columns] if isinstance(columns, str) else columns if columns else None
    aggregation_col = list(aggregation_col) if isinstance(aggregation_col, (set, tuple)) else [aggregation_col] if isinstance(aggregation_col, str) else aggregation_col if aggregation_col else None

    # Auto-select index and columns if not provided
    if index_col is None:
        categorial_cols = table.select_dtypes(include=['object', 'category']).columns.tolist()
        if not categorial_cols:
            raise ValueError("No categorical columns for grouping")
        index_col = [categorial_cols[-1]]
        if columns is None and len(categorial_cols) > 1:
            columns = [categorial_cols[-2]]

    # Validate index_col
    if index_col is not None and not set(index_col).issubset(table.columns):
        raise ValueError(f"Index column(s) {index_col} not found")

    # Validate columns
    if columns is not None and not set(columns).issubset(table.columns):
        raise ValueError(f"Column(s) {columns} not found")

    # Check if columns and index_col overlap
    if columns is not None and index_col is not None and set(index_col) & set(columns):
        raise ValueError("columns and index_col cannot be the same")

    # Auto-select numeric column for aggregation if not provided
    if aggregation_col is None:
        num_cols = table.select_dtypes(include=['float']).columns.tolist()
        if not num_cols:
            num_cols = table.select_dtypes(include=['number']).columns.tolist()
        if not num_cols:
            raise ValueError("No numeric columns for aggregation")
        aggregation_col = [num_cols[-1]]

    # Validate aggregation_col
    if aggregation_col is not None and not set(aggregation_col).issubset(table.columns):
        raise ValueError(f"Aggregation column(s) {aggregation_col} not found")
    if aggregation_col is not None and not table[aggregation_col].dtypes.apply(pd.api.types.is_numeric_dtype).all():
        raise ValueError(f"Aggregation column(s) {aggregation_col} must be numeric")

    # Validate fill_val
    if fill_val is not None and not isinstance(fill_val, (int, float)):
        raise TypeError("fill_val must be numeric or None")

    # Create pivot table with mean aggregation
    pivot = pd.pivot_table(
        table,
        values=aggregation_col,
        index=index_col,
        columns=columns,
        aggfunc='mean',
        fill_value=fill_val
    )

    # Save pivot table if output_path is provided
    if output_path:
        _, ext = os.path.splitext(output_path)
        if ext == '.csv':
            pivot.to_csv(output_path)
        elif ext == '.xlsx':
            pivot.to_excel(output_path)
        else:
            raise TypeError("Output must be .csv or .xlsx")

    return pivot

def main():
    print("Enter the path to the table")
    src_path = input().strip()

    try:
        table = read_table(src_path)
        print("\n", table)

        print("\nEnter index column(s) (comma-separated, press Enter for auto):")
        index_input = input().strip()
        index_col = pd.Series(index_input.split(','), dtype=str).str.strip().loc[lambda x: x != ''].tolist() if index_input.strip() else None

        print("Enter column(s) for grouping (comma-separated, press Enter for auto):")
        columns_input = input().strip()
        columns = pd.Series(columns_input.split(','), dtype=str).str.strip().loc[lambda x: x != ''].tolist() if columns_input.strip() else None

        print("Enter aggregation column(s) (comma-separated, press Enter for auto):")
        agg_input = input().strip()
        aggregation_col = pd.Series(agg_input.split(','), dtype=str).str.strip().loc[lambda x: x != ''].tolist() if agg_input.strip() else None

        print("Enter fill value for NaN (press Enter for None):")
        fill_input = input().strip()
        try:
            fill_val = float(fill_input) if fill_input else None
        except ValueError:
            raise TypeError("fill_val must be numeric or None")

        print("Enter output file path (.csv or .xlsx, press Enter for no save):")
        output_path = input().strip() or None

        pivot = make_pivot_table(table, aggregation_col, index_col, columns, fill_val, output_path)
        print("\nPivot table(mean aggregation):\n", pivot)

    except (ValueError, TypeError, FileNotFoundError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()