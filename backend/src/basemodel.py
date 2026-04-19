# this file defines the base model for other models to inherit from
import pydantic
from pydantic import BaseModel as PydanticBaseModel
from datetime import datetime, date


# Use the proper config key for the installed pydantic major version
_pydantic_major = int(pydantic.__version__.split(".")[0])


class BaseModel(PydanticBaseModel):
    # pydantic v2 expect 'from_attributes' in model_config 
    model_config = {
        "from_attributes": True
    }   

# --------------------------- Example Models for DataBase --------------------------- #
class stockDataModel(BaseModel):
    symbol: str
    date: str
    open: float
    close: float
    high: float
    low: float
    adj_close: float
    volume: int


class NewsArticleModel(BaseModel):
    title: str
    content: str
    published_at: str
    source: str
    url: str

# --------------------------- Example Models for DataFrame Validation --------------------------- #

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
class StockDataFrameModel(BaseModel):
    Date: datetime
    Close: float
    High: float
    Low: float
    Open: float
    Volume: int
    diff_open_close: float
    diff_high_low: float
    day_of_week: int
    VMA_5: float
    VMA_10: float
    VMA_20: float
    RSI_14: float
    rolling_mean_3: float
    rolling_std_3: float
    rolling_mean_7: float
    rolling_std_7: float
    rolling_mean_21: float
    rolling_std_21: float
    target: float
    Daily_Return: float
    Target_Return: float
    SnP: float
    NASDAQ: float
