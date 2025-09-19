# Pivot Table Generator
Task DA-1-20 for NSU "Project Introduction" course

## Task Description
Create pivot tables from datasets with categorical and numeric data using `pandas.pivot_table()` with mean aggregation.

## Features
- **Pivot Table Creation**: Generates pivot tables with mean aggregation using `pandas.pivot_table()`.
- **Flexible Input**: Accepts string, list, or set for index, columns, and aggregation columns.
- **Auto-Selection**: Automatically selects categorical columns for grouping and numeric columns for aggregation if not specified.
- **File Support**: Reads and writes CSV and Excel (.xlsx) files (limited by dependencies: pandas, openpyxl).
- **Error Handling**: Validates inputs, file existence, column types, and formats.

## Functions

### `read_table(source_path)`
Reads a dataset from a CSV or Excel file.

**Parameters:**
- `source_path` (str): Path to the input file (.csv, .xlsx).

**Returns:**
- `pd.DataFrame`: Loaded DataFrame.

**Raises:**
- `FileNotFoundError`: If file does not exist.
- `TypeError`: If file extension is unsupported.

### `make_pivot_table(table, aggregation_col=None, index_col=None, columns=None, fill_val=None, output_path=None)`
Creates a pivot table with mean aggregation.

**Parameters:**
- `table` (pd.DataFrame): Input DataFrame.
- `aggregation_col` (str, list, or set, optional): Numeric column(s) for aggregation. Defaults to last numeric column.
- `index_col` (str, list, or set, optional): Row grouping column(s). Defaults to last categorical column.
- `columns` (str, list, or set, optional): Column grouping column(s). Defaults to second-to-last categorical column if available.
- `fill_val` (any, optional): Value to replace NaN. Defaults to None.
- `output_path` (str, optional): Path to save pivot table (.csv or .xlsx). Defaults to None.

**Returns:**
- `pd.DataFrame`: Pivot table with mean aggregation.

**Raises:**
- `TypeError`: If table is not a DataFrame, columns have invalid types, or fill_val is not numeric.
- `ValueError`: If table is empty, no numeric/categorical columns, columns not found, or index/columns coincide.

### `main()`
Demonstrates pivot table creation with interactive user input.

**Features:**
- Loads dataset from a user-specified file.
- Prompts for index, columns, aggregation columns, fill value, and output path.
- Displays the input dataset and pivot table.

## Running the Demo
```bash
python pivot_table.py
```

**Example Input/Output:**
```bash
Enter the path to the table
./tests/titanic.csv
Enter index column(s) (comma-separated, press Enter for auto):
Pclass
Enter column(s) for grouping (comma-separated, press Enter for auto):
Sex, Embarked
Enter aggregation column(s) (comma-separated, press Enter for auto):
Fare
Enter fill value for NaN (press Enter for None):
 
Enter output file path (.csv or .xlsx, press Enter for no save):


Pivot table(mean aggregation):
                 Fare                                                       
Sex           female                             male                      
Embarked           C          Q          S          C          Q          S
Pclass                                                                     
1         115.640309  90.000000  99.026910  93.536707  90.000000  52.949947
2          25.268457  12.350000  21.912687  25.421250  12.350000  19.232474
3          14.694926  10.307833  18.670077   9.352237  11.924251  13.307149
```

## Dependencies
- `pandas`: For DataFrame operations and pivot table creation.
- `openpyxl`: For Excel (.xlsx) file support.

## Installation
```bash
pip install pandas openpyxl
```

## Implementation Details
- Uses `pandas.pivot_table()` for mean aggregation of numeric columns.
- Supports flexible input formats (str, list, set) for column specification.
- Automatically selects categorical and numeric columns when not provided.
- Employs vectorized operations for validation (e.g., `dtypes.apply`).
- Tested on datasets with categorical and numeric data (e.g., Titanic, employee data).

## Materials
- [Pandas Pivot Table Documentation](https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html)
- [Pandas DataFrame Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
- [Openpyxl Documentation](https://openpyxl.readthedocs.io/en/stable/)