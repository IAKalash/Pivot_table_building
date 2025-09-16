import pandas as pd
import os

def read_table (source_path):

    extension_dictionary = {".xls" : "excel", ".xlsx" : "excel", ".csv" : "csv"}
    if (os.path.isfile(source_path)):
        _, extension = os.path.splitext(source_path)

        if (extension in extension_dictionary.keys()):
            read_func = getattr(pd, "read_" + extension_dictionary[extension])
            table = read_func(source_path)
            return table
        
        else:
            raise TypeError("Unsupported file type")
    
    else:
        raise FileNotFoundError("File not found")


def make_pivot_table (table = pd.DataFrame(), aggregation_col = None, index_col = None, columns = None, fill_val = None):

    if not isinstance(table, pd.DataFrame):
        raise TypeError("Use only pandas.DataFrame type")
    if table.empty:
        raise ValueError("Empty table")
    
    if index_col == None:
        categorial_cols = table.select_dtypes(include=['object', 'category']).columns.to_list()
        if not categorial_cols:
            raise ValueError("No index columns")
        else:
            index_col = categorial_cols[-1]
            if columns == None:
                if len(categorial_cols) > 1:
                    columns = categorial_cols[-2]
    
    elif (not set(index_col).issubset(set(table.columns))):
        raise ValueError(f"Column(s) {index_col} not found")
    

    if aggregation_col == None:
        num_cols = table.select_dtypes(include='float').columns.to_list()
        if not num_cols:
            num_cols = table.select_dtypes(include='number').columns.to_list()
            if not num_cols:
                raise ValueError("No numeric columns for aggregation")
        aggregation_col = num_cols[-1]
    
    elif (not set(aggregation_col).issubset(set(table.columns))):
        raise ValueError(f"Column(s) {aggregation_col} not found")

    print(f"\n\n\nPivot table (mean {aggregation_col}):\n")

    pivot = pd.pivot_table(
        table, 
        values=aggregation_col, 
        index=index_col, 
        columns=columns,
        aggfunc='mean',
        fill_value=fill_val)
    
    return pivot


def main():

    print("Enter the path to the table")
    src_path = input()

    try:
        table = read_table(src_path)
        print("\n", table)


#############################################

        print(make_pivot_table(table))

    except (ValueError, TypeError, FileNotFoundError) as e:
        print(f"Error: {e}")


main()