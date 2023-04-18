import numpy as np 
import pandas as pd
from scipy.stats import norm 

# making data 
norm_range = np.linspace(-3.0, 3.0, 1_000)
normal_df: pd.DataFrame = pd.DataFrame(
    {
        "x": norm_range, 
        "cdf_target": norm.cdf(norm_range)
    }
)

# saving to txt file for c++ 
normal_df.to_csv("./normal_benchmark.csv", index=False)

# saving as a sql script to insert into table 
# internal table named t_0001 with cols "x_val" and "cdf_benchmark" 
initial_str: str = """\
INSERT INTO t_0001 ("x_val", "cdf_benchmark") 
VALUES 
"""
with open("sql_scripts/insert_to_table.sql", "w") as sql_f: 
    sql_f.write(initial_str)
    for (x_val, cdf_val) in normal_df.itertuples(index=False): 
        if x_val >= 3.0: # if last line 
            sql_f.write(f"    ({x_val}, {cdf_val});")
        else: 
            sql_f.write(f"    ({x_val}, {cdf_val}),\n")
    