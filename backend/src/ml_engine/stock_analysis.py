
from backend.src.ml_engine.feature_extraction import final_df
from backend.src.ml_engine.data_preparation import index_data
from backend.src.ml_engine.prediction import predict_tomorrow
import joblib
from tensorflow.keras.models import load_model
import warnings
warnings.filterwarnings("ignore")

START_DATE = "2025-07-01"
ticker = ["^NSEI", "^GSPC", "^IXIC"]


# ----------------------------------- Data Preparation ----------------------------------- #
Nifty_50, SnP_500_df, NASDAQ_df = index_data(START_DATE, ticker)
df = final_df(Nifty_50, SnP_500_df, NASDAQ_df)
print(df.head())
print(df.tail())
#---------------------------------------Data Scaling---------------------------------------#
# Select Features (X) and the new Target (y)
# Features (X) are the scaled columns PLUS the current day's return
X_cols = [col for col in df.columns if 'Feature' in col or col in ['Close', 'Daily_Return']]
X_raw = df[X_cols]
y_raw = df['Target_Return'].values.reshape(-1, 1)

# Load the saved scalers
file_path = "backend/src/ml_engine/models/"
feature_scaler = joblib.load(file_path + "feature_scaler.pkl")  # ensures same scaling as training
target_scaler = joblib.load(file_path + "target_scaler.pkl")    # ensures same scaling as training

# Scale the features and target
scaled_X_values = feature_scaler.transform(X_raw)
scaled_y_values = target_scaler.transform(y_raw)


#---------------------------------------Prediction Preparation---------------------------------------#
# Prepare the input for prediction (last available day)
# 4. Final Threshold
THRESHOLD = 0.0003
TIME_STEPS = 60  # Number of time steps the model was trained on
last_60_days_raw = X_raw.tail(TIME_STEPS)
N_FEATURES = scaled_X_values.shape[1]  # Number of features used in the model


# --- Load model ---
model = load_model(file_path + "stock_lstm_model.h5")

# ----------------------------------- EXECUTE PREDICTION ------------------------------ #
predicted_return, action, confidence = predict_tomorrow(
    last_60_days_raw,
    feature_scaler,
    target_scaler,
    model,
    THRESHOLD,
    N_FEATURES,
    TIME_STEPS
)

print("\n--- Tomorrow's Prediction Report ---")
print(f"Based on the last {TIME_STEPS} days of data:")
print(f"Predicted Next Day Return: {predicted_return * 100:.4f}%")
print(f"Trading Action (Threshold={THRESHOLD*100:.2f}%): {action}")
print(f"Predicted Direction/Magnitude: {confidence}")
print("\nRecommendation: A trading action is executed only if the predicted return exceeds the threshold.")


if __name__ == "__main__":
    print("Stock analysis module executed")
    N_FEATURES = scaled_X_values.shape[1]  # Number of features used in the model
    print("module executed")
