import pandas as pd

def infer_and_convert_data_types(df, check_rows = 200):
  for col in df.columns:
    df_converted = pd.to_numeric