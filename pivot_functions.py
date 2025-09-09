import pandas as pd

def read (source_path, source_table_name, source_table_type): 
    read_func = getattr(pd, "read_" + source_table_type)
    table = read_func(source_path + source_table_name)
    return table


