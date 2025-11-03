from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from .connect import Base, db, engine, SessionLocal
from ..basemodel import stockDataModel
from .converter import clean_number, clean_int
import csv
from pathlib import Path

base_path = Path("~") / "Desktop" / "LLM_Projects" / "Ai-stock-analytics" / "backend" / \
            "data_collection" / "stock_data" / "historical_data"


# Define the shared column structure once
def create_stock_class(symbol_name: str, base_class):
    """
    Creates a new SQLAlchemy Declarative class with a unique table name.
    """
    table_name = f"{symbol_name.split('.')[0]}"
    class_name = f"{symbol_name.split('.')[0]}Data"
    
    # Define the new class dynamically
    # type() is used to create classes dynamically: type(name, bases, dict)
    StockClass = type(class_name, (base_class,), {
        "__tablename__": table_name,
        # Standard SQLAlchemy columns
        "id": Column(Integer, primary_key=True, index=True),
        "symbol": Column(String, index=True),
        "date": Column(String),
        "open": Column(Float),
        "close": Column(Float),
        "high": Column(Float),
        "low": Column(Float),
        "adj_close": Column(Float),
        "volume": Column(Integer)
    })
    
    return StockClass



def create_tables(engine):
    """Create the table defined in Base.metadata.tables"""

    table = list(Base.metadata.tables.keys())[-1]
    print(f"\n--- Creating {table} Tables ---")
    Base.metadata.create_all(bind=engine)
    print("Tables created:", table)



#function to insert data from csv file into the database
def insert_stock_data_from_csv(file_path: str):
    """
    1. Extracts the stock symbol from the CSV file name,
    2. creates a new SQLAlchemy class for that symbol,
    3. creates the corresponding table in the database, and
    4. cleans and validates each row of data using a Pydantic model, then
    5. inserts stock data from a CSV file into the database.
    """

    symbol = file_path.name.split("_")[0].split(".")[0]
    NewStockClass = create_stock_class(symbol, Base)   # New class for each symbol
    create_tables(engine)                              # Create tables for the new class

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        with SessionLocal() as db:
            count = 0
            for row in reader:
                clean_vals = {
                    "symbol": symbol,
                    "date": row.get("Date") or "",
                    "open": clean_number(row.get("Open")) or 0.0,
                    "close": clean_number(row.get("Close")) or 0.0,
                    "high": clean_number(row.get("High")) or 0.0,
                    "low": clean_number(row.get("Low")) or 0.0,
                    "adj_close": clean_number(row.get("Adj. Close")) or 0.0,
                    "volume": clean_int(row.get("Volume")) or 0,
                }

                # validate using pydantic model
                validated = stockDataModel(**clean_vals)
                try:
                    payload = validated.model_dump()
                except AttributeError:
                    print("Error: Could not dump model data. Check pydantic version compatibility.")
                
                # create SQLAlchemy instance from validated data
                stock_data = NewStockClass(**payload)

                # Insert into the database
                db.add(stock_data)
                count += 1
            print(f"Inserted {count} rows into {NewStockClass.__tablename__}.")
            db.commit()



if __name__ == "__main__":
    # run from project root:
    # python -m backend.src.database.main
    print("main module executed as script from experiment.py")
    symbols = ["HDFCBANK.NS", "RELIANCE.NS", "TCS.NS", "ICICIBANK.NS", "INFY.NS"]  # stock symbols
    for symbol in symbols:
        filename = f"{symbol}_historical_data.csv"
        full_path = base_path / filename
        final_path = full_path.expanduser()
        print(f"\nProcessing file: {final_path}")
        insert_stock_data_from_csv(final_path)