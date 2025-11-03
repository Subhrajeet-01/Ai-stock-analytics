# this file defines the base model for other models to inherit from
import pydantic
from pydantic import BaseModel as PydanticBaseModel

# Use the proper config key for the installed pydantic major version
_pydantic_major = int(pydantic.__version__.split(".")[0])


class BaseModel(PydanticBaseModel):
    # pydantic v2 expect 'from_attributes' in model_config 
    model_config = {
        "from_attributes": True
    }   


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



# this file is for initializing the FastAPI application and including routers