import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import numpy as np # pyright: ignore[reportMissingImports]
import joblib # pyright: ignore[reportMissingImports]
import plotly.express as px # type: ignore
from PIL import Image # pyright: ignore[reportMissingImports]
from src.api_fetcher import fetch_weather_data

# Load model
model = joblib.load("models/rf_model.pkl")

# Page config
st.set_page_config(page_title="Smart Climate & AQI Predictor", layout="wide")

# Load and display banner
try:
    banner = Image.open("assets/banner.png")
    st.image(banner, use_container_width=True)
except Exception:
    st.warning("Banner image not found. Please check assets/banner.png")

# Welcome message
st.markdown("""
<div style='text-align: center; font-size: 24px; font-weight: bold; margin-top: -20px;'>
Welcome to Smart Climate & AQI Predictor
</div>
""", unsafe_allow_html=True)

# Sidebar
try:
    st.sidebar.image("assets/logo.png", use_container_width=True)
except Exception:
    st.sidebar.warning("Logo not found. Please check assets/logo.png")

st.sidebar.title("🌍 Smart Climate & AQI Predictor")
city = st.sidebar.text_input("Enter City Name", "Delhi")
st.sidebar.markdown("Built for real-time climate awareness and air quality forecasting.")

# Main layout
st.title("📊 Climate Dashboard")
st.markdown("### Real-time Weather & AQI Insights")

# Fetch data
if city:
    try:
        data = fetch_weather_data(city)

        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🌡️ Temperature", f"{data['temperature']} °C")
        col2.metric("💧 Humidity", f"{data['humidity']} %")
        col3.metric("🧪 Live AQI", data['aqi'])

        # Prediction
        features = np.array([[data["temperature"], data["humidity"]]])
        predicted_aqi = model.predict(features)[0]
        col4.metric("🔮 Predicted AQI", round(predicted_aqi, 2))

        # Alert
        if predicted_aqi > 150:
            st.error("⚠️ Unhealthy Air Quality! Consider wearing a mask or staying indoors.")
        elif predicted_aqi > 100:
            st.warning("⚠️ Moderate Pollution. Sensitive groups should take precautions.")
        else:
            st.success("✅ Air Quality is Good!")

        # Historical chart
        st.markdown("### 📈 Historical AQI Trends")
        df = pd.read_csv("data/historical_data.csv")
        fig = px.line(df, x="date", y="AQI", markers=True, title=f"AQI Trend in {city}")
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error fetching data: {e}")
