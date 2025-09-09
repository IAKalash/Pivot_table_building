import pandas as pd
import pivot_functions

src_path = ""
src_table_name = "titanic.csv"
src_type = "csv"

table = read(src_path, src_table_name, src_type)

print(table)