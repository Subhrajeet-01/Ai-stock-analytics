import numpy as np
import pandas as pd

def predict_tomorrow(last_60_days_raw, feature_scaler, target_scaler, model, threshold, N_FEATURES, TIME_STEPS):
    """
    Prepares the last sequence of data, scales it, predicts the next day's return,
    and determines the trading action based on the threshold.
    """
    # 1. Reshape the last sequence into the required 3D format (1 sample, 60 time steps, 18 features)
    # The input to the scaler must be 2D (time_steps * features), not 3D
    last_sequence_2d = last_60_days_raw.values.reshape(-1, N_FEATURES)

    # 2. Scale the input features using the trained feature_scaler
    scaled_input_2d = feature_scaler.transform(last_sequence_2d)

    # 3. Reshape scaled data back to 3D for the LSTM model (1, 60, N_FEATURES)
    scaled_input_3d = scaled_input_2d.reshape(1, TIME_STEPS, N_FEATURES)

    # 4. Generate the scaled prediction
    scaled_prediction = model.predict(scaled_input_3d, verbose=0)

    # 5. Inverse transform the prediction to get the actual percentage return
    predicted_return_2d = target_scaler.inverse_transform(scaled_prediction)
    predicted_return = predicted_return_2d[0][0] # Extract the single float value

    # 6. Determine the trading action based on the threshold
    if predicted_return > threshold:
        action = "STRONG BUY"
        confidence = f"{predicted_return * 100:.4f}% UP"
    elif predicted_return < -threshold:
        action = "STRONG SELL"
        confidence = f"{-predicted_return * 100:.4f}% DOWN"
    else:
        action = "HOLD / WEAK SIGNAL"
        confidence = f"{predicted_return * 100:.4f}% (Magnitude too small)"

    return predicted_return, action, confidence
