
"""
#   Column           Non-Null Count  Dtype         
---  ------           --------------  -----         
 0   Date             73 non-null     datetime64[ns]
 1   Close            73 non-null     float64       
 2   High             73 non-null     float64       
 3   Low              73 non-null     float64       
 4   Open             73 non-null     float64       
 5   Volume           73 non-null     int64         
 6   diff_open_close  73 non-null     float64       
 7   diff_high_low    73 non-null     float64       
 8   day_of_week      73 non-null     int32         
 9   VMA_5            73 non-null     float64       
 10  VMA_10           73 non-null     float64       
 11  VMA_20           73 non-null     float64       
 12  RSI_14           73 non-null     float64       
 13  rolling_mean_3   73 non-null     float64       
 14  rolling_std_3    73 non-null     float64       
 15  rolling_mean_7   73 non-null     float64       
 16  rolling_std_7    73 non-null     float64       
 17  rolling_mean_21  73 non-null     float64       
 18  rolling_std_21   73 non-null     float64       
 19  target           73 non-null     float64       
 20  Daily_Return     73 non-null     float64       
 21  Target_Return    73 non-null     float64       
 22  SnP              0 non-null      float64       
 23  NASDAQ           0 non-null      float64       
dtypes: datetime64[ns](1), float64(21), int32(1), int64(1)

"""
import pandas as pd
from pydantic import BaseModel, ValidationError
from backend.src.basemodel import StockDataFrameModel
from backend.src.ml_engine.feature_extraction import final_df
from backend.src.ml_engine.data_preparation import index_data


START_DATE = "2025-07-01"
ticker = ["^NSEI", "^GSPC", "^IXIC"]

Nifty_50, SnP_500_df, NASDAQ_df = index_data(START_DATE, ticker)
df = final_df(Nifty_50, SnP_500_df, NASDAQ_df)
print(df.info())

# --- 2. Validation Function ---
def validate_dataframe(df: pd.DataFrame, Model: BaseModel) -> bool:
    """
    Validates a Pandas DataFrame against a Pydantic model row by row.
    """
    print(f"Starting validation on DataFrame with {len(df)} rows...")
    
    # 1. Convert the DataFrame index (Date) back to a column for validation
    # df_reset = df.reset_index(names=['Date'])
    
    # 2. Convert DataFrame rows to a list of dictionaries for Pydantic
    records = df.to_dict('records')
    
    validation_errors = 0
    
    for i, record in enumerate(records):
        try:
            # Validate each row (dictionary) against the Pydantic model
            Model(**record)
        except ValidationError as e:
            validation_errors += 1
            if validation_errors < 5: # Limit error printing to keep output clean
                print(f"\nValidation Error on Row {i} (Date: {record.get('Date')}):")
                print(e.errors())
                print("-" * 30)
            
    if validation_errors > 0:
        print(f"\n--- Validation FAILED ---")
        print(f"Total rows with validation errors: {validation_errors}")
        return False
    else:
        print(f"\n--- Validation SUCCESSFUL ---")
        print("DataFrame structure and types match the Pydantic schema.")
        return True


# --- 3. Execute Validation ---
if __name__ == "__main__":
    is_valid = validate_dataframe(df, StockDataFrameModel)
    if is_valid:
        print("DataFrame is valid according to the StockDataFrameModel schema.")
    else:
        print("DataFrame validation failed. Please check the errors above.")