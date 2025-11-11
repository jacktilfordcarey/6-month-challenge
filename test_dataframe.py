import pandas as pd
import numpy as np

# Test the DataFrame creation that's causing the error
test_data = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

# Test the specific DataFrame creation from the error
dtype_df = pd.DataFrame({
    'Column': test_data.dtypes.index,
    'Data Type': test_data.dtypes.values.astype(str),
    'Non-Null Count': [len(test_data) - test_data[col].isnull().sum() for col in test_data.columns]
})

print("DataFrame creation successful!")
print(dtype_df)