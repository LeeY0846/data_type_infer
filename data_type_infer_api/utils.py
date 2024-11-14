import pandas as pd
import numpy as np

NUMBER = "number"
BOOL = "bool"
DATE = "datetime"
COMPLEX = "complex"
CATEGORY = "category"
OBJECT = "object"

CHUNK_SIZE = 200


def is_np_complex(s):
    try:
        return pd.api.types.is_complex(np.complex128(s))
    except (ValueError):
        return False
    
def convert_complex(s):
    try:
        return np.complex128(s)
    except (ValueError):
        return np.nan
    
def convert_bool(s):
    return True if s else False

def convert_string(s):
    return str(s)
    
is_complex = np.vectorize(is_np_complex)
is_numeric = np.vectorize(pd.api.types.is_number)
is_bool = np.vectorize(pd.api.types.is_bool)

convert_complex_vec = np.vectorize(convert_complex)
convert_bool_vec = np.vectorize(convert_bool)
convert_string_vec = np.vectorize(convert_string)

def infer_types(df, check_rows = 200, type_percent_threshold = 0.5, max_category_percent = 0.5, max_category_count = 15):
    types_dict = {}
    rows = min(check_rows, df.shape[0])
    dc = df.loc[:rows-1]
    for col in dc.columns:
        number_converted = pd.to_numeric(dc[col], errors='coerce')
        number_count = rows - number_converted.isna().sum()
        if number_count > rows * type_percent_threshold:
            types_dict[col] = NUMBER
            continue
        
        if pd.api.types.is_bool_dtype(dc[col]):
            types_dict[col] = BOOL
            continue
        
        try:
            dc[col] = pd.to_datetime(dc[col], errors="raise")
            types_dict[col] = DATE
            continue
        except (ValueError, TypeError):
            pass
        
        complex_count = is_complex(dc[col]).sum()
        if complex_count > rows * type_percent_threshold:
            types_dict[col] = COMPLEX
            continue
        
        unique_count = len(dc[col].unique())
        if unique_count <= min(max_category_count, max_category_percent * rows):
            types_dict[col] = CATEGORY
            continue
        
        types_dict[col] = OBJECT
    return types_dict


def convert_data_with_types(df, type_dict):
    for col in type_dict:
        type = type_dict[col]
        if type == NUMBER:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        elif type == BOOL:
            df[col] = convert_bool_vec(df[col])
        elif type == DATE:
            df[col] = pd.to_datetime(df[col])
        elif type == COMPLEX:
            df[col] = convert_complex_vec(df[col])
        elif type == CATEGORY:
            df[col] = pd.Categorical(df[col])
        elif type == OBJECT:
            pass
        else:
            raise TypeError("Invalid type: " + str(type))
    return df
  
def get_inferred_types(filepath):
  if filepath.endswith(".csv"):
    df = pd.read_csv(filepath, nrows=CHUNK_SIZE)
    types = infer_types(df)
    return types
  elif filepath.endswith(".xlsx"):
    pass
  else:
    raise TypeError("Invalid file type " + filepath)
  
def get_chunked_data(filepath, start, columns):
  if filepath.endswith(".csv"):
    df = pd.read_csv(filepath, skiprows=start + 1, nrows=CHUNK_SIZE, names=columns, index_col=False)
    return { "data": df, "ended": df.shape[0] < CHUNK_SIZE }
  elif filepath.endswith(".xlsx"):
    pass
  else:
    raise TypeError("Invalid file type " + filepath)
  
def get_chunked_typed_data(filepath, start, types):
  data = get_chunked_data(filepath, start, [col for col in types])
  data['data'] = convert_data_with_types(data['data'], types).to_json(orient="index")
  return data