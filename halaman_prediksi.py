import streamlit as st
import joblib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
import math

# Load models
arima_model = joblib.load('training_model/arima_model.pkl')
hw_model = joblib.load('training_model/holtwinters_model.pkl')

# Function to make ARIMA predictions
def make_arima_prediction(model, start_date, end_date):
    # Generate date range
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    num_steps = len(date_range)

    # Predict using ARIMA model
    arima_forecast = model.forecast(steps=num_steps)

    return arima_forecast, date_range

# Function to make Holt-Winters predictions
def make_hw_prediction(model, start_date, end_date):
    # Generate date range (use the same as ARIMA)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    num_steps = len(date_range)

    # Predict using Holt-Winters model
    hw_forecast = model.forecast(steps=num_steps)

    return hw_forecast, date_range

# Function to calculate required stock
def calculate_required_stock(forecast, buffer_stock=0, rounding_method='round'):
    required_stock = forecast + buffer_stock
    
    if rounding_method == 'round':
        required_stock = np.round(required_stock)
    elif rounding_method == 'ceil':
        required_stock = np.ceil(required_stock)
    elif rounding_method == 'floor':
        required_stock = np.floor(required_stock)
    
    return required_stock

# Function to display the prediction page
def show_halaman_prediksi():
    st.title('Stock Forecasting App')

    # Interface for user input
    model_selection = st.selectbox('Select model:', ['ARIMA', 'Holt-Winters'])
    buffer_stock = st.number_input('Buffer Stock:', min_value=0, value=10)
    rounding_method = st.selectbox('Rounding Method:', ['round', 'ceil', 'floor'])

    if model_selection == 'ARIMA':
        start_date = st.date_input('Start date for ARIMA prediction:')
        end_date = st.date_input('End date for ARIMA prediction:')

        if start_date and end_date:
            # Button to trigger ARIMA prediction
            if st.button('Predict ARIMA'):
                arima_forecast, date_range = make_arima_prediction(arima_model, start_date, end_date)

                # Calculate required stock
                required_stock = calculate_required_stock(arima_forecast, buffer_stock, rounding_method)

                # Display ARIMA predictions
                st.write("ARIMA Forecast:")
                st.write(pd.DataFrame({'Date': date_range, 'Forecast': arima_forecast, 'Required Stock': required_stock}))

                # Explanation
                st.write(f"""
                **ARIMA Forecast Explanation:**
                ARIMA forecast predicts stock levels from {start_date} to {end_date} based on historical data. The plot below shows the forecasted stock levels in red.
                """)

                # Plot ARIMA forecast
                plt.figure(figsize=(10, 6))
                plt.plot(date_range, arima_forecast, label='ARIMA Forecast', color='red')
                plt.plot(date_range, required_stock, label='Required Stock', color='blue')
                plt.title('ARIMA Stock Forecast and Required Stock')
                plt.xlabel('Date')
                plt.ylabel('Values')
                plt.legend()
                st.pyplot(plt)

                # Add download button for ARIMA forecast
                csv = pd.DataFrame({'Date': date_range, 'Forecast': arima_forecast, 'Required Stock': required_stock}).to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="arima_forecast.csv">Download ARIMA Forecast as CSV</a>'
                st.markdown(href, unsafe_allow_html=True)

    elif model_selection == 'Holt-Winters':
        start_date = st.date_input('Start date for Holt-Winters prediction:')
        end_date = st.date_input('End date for Holt-Winters prediction:')

        if start_date and end_date:
            # Button to trigger Holt-Winters prediction
            if st.button('Predict Holt-Winters'):
                hw_forecast, date_range = make_hw_prediction(hw_model, start_date, end_date)

                # Calculate required stock
                required_stock = calculate_required_stock(hw_forecast, buffer_stock, rounding_method)

                # Display Holt-Winters predictions
                st.write("Holt-Winters Forecast:")
                st.write(pd.DataFrame({'Date': date_range, 'Forecast': hw_forecast, 'Required Stock': required_stock}))

                # Explanation
                st.write(f"""
                **Holt-Winters Forecast Explanation:**
                Holt-Winters forecast predicts stock levels from {start_date} to {end_date} based on historical data. The plot below shows the forecasted stock levels in green.
                """)

                # Plot Holt-Winters forecast
                plt.figure(figsize=(10, 6))
                plt.plot(date_range, hw_forecast, label='Holt-Winters Forecast', color='green')
                plt.plot(date_range, required_stock, label='Required Stock', color='blue')
                plt.title('Holt-Winters Stock Forecast and Required Stock')
                plt.xlabel('Date')
                plt.ylabel('Values')
                plt.legend()
                st.pyplot(plt)

                # Add download button for Holt-Winters forecast
                csv = pd.DataFrame({'Date': date_range, 'Forecast': hw_forecast, 'Required Stock': required_stock}).to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="hw_forecast.csv">Download Holt-Winters Forecast as CSV</a>'
                st.markdown(href, unsafe_allow_html=True)

if __name__ == '__main__':
    show_halaman_prediksi()
