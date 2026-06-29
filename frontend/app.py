import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AgriIntel Dashboard",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 AgriIntel — Agricultural Intelligence Platform")
st.markdown("AI-powered crop yield prediction, fertilizer recommendation, and weather intelligence.")
st.divider()

page = st.sidebar.selectbox(
    "Navigate",
    ["Weather Intelligence", "Yield Prediction", "Fertilizer Recommendation", "Disease Detection", "Prediction History"]
)

# ─── WEATHER PAGE ───────────────────────────────────────
if page == "Weather Intelligence":
    st.header("Weather Intelligence")
    st.write("Get real-time weather data for any location.")

    city = st.text_input("Enter city name", placeholder="e.g. Delhi, Mumbai, Shimla")

    if st.button("Get Weather", type="primary"):
        if not city.strip():
            st.warning("Please enter a city name.")
        else:
            with st.spinner("Fetching weather data..."):
                try:
                    response = requests.get(f"{API_BASE}/weather", params={"city": city})
                    data = response.json()

                    if "error" in data:
                        st.error(f"Error: {data['error']}")
                    else:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Temperature", f"{data['temperature_c']} C")
                            st.metric("Feels Like", f"{data['feels_like_c']} C")
                        with col2:
                            st.metric("Humidity", f"{data['humidity_percent']}%")
                            st.metric("Wind Speed", f"{data['wind_speed_ms']} m/s")
                        with col3:
                            st.metric("Condition", data['condition'])
                            st.metric("Pressure", f"{data['pressure_hpa']} hPa")

                        st.success(f"Weather in {data['city']}, {data['country']}: {data['description'].title()}")
                except Exception as e:
                    st.error(f"Could not connect to API server. Is it running? ({e})")

# ─── YIELD PREDICTION PAGE ──────────────────────────────
elif page == "Yield Prediction":
    st.header("Crop Yield Prediction")
    st.write("Predict expected crop yield based on environmental and agricultural factors.")

    col1, col2 = st.columns(2)
    with col1:
        area = st.selectbox("Country / Region", [
            "India", "United States of America", "China", "Brazil",
            "Australia", "Germany", "France", "United Kingdom",
            "Canada", "Japan", "Pakistan", "Bangladesh"
        ])
        item = st.selectbox("Crop Type", [
            "Wheat", "Rice, paddy", "Maize", "Potatoes",
            "Soybeans", "Sorghum", "Cassava", "Sweet potatoes", "Yams"
        ])
        year = st.number_input("Year", min_value=1990, max_value=2030, value=2024)

    with col2:
        rainfall = st.number_input("Average Rainfall (mm/year)", min_value=0.0, max_value=5000.0, value=1083.0)
        pesticides = st.number_input("Pesticides Used (tonnes)", min_value=0.0, max_value=500000.0, value=15000.0)
        temp = st.number_input("Average Temperature (C)", min_value=-10.0, max_value=50.0, value=25.0)

    if st.button("Predict Yield", type="primary"):
        with st.spinner("Running prediction..."):
            try:
                payload = {
                    "area": area, "item": item, "year": year,
                    "rainfall": rainfall, "pesticides": pesticides, "temp": temp
                }
                response = requests.post(f"{API_BASE}/predict-yield", json=payload)
                data = response.json()

                if "error" in data:
                    st.error(f"Error: {data['error']}")
                else:
                    st.success("Prediction complete!")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Yield (kg/ha)", f"{data['predicted_yield_kg_per_ha']:,.0f}")
                    with col2:
                        st.metric("Yield (hg/ha)", f"{data['predicted_yield_hg_per_ha']:,.0f}")
                    with col3:
                        st.metric("Prediction ID", f"#{data['prediction_id']}")
                    st.info(f"Prediction saved to database with ID #{data['prediction_id']}")
            except Exception as e:
                st.error(f"Could not connect to API server. Is it running? ({e})")

# ─── FERTILIZER RECOMMENDATION PAGE ────────────────────
elif page == "Fertilizer Recommendation":
    st.header("Fertilizer Recommendation")
    st.write("Get AI-powered fertilizer recommendations based on soil and crop conditions.")

    col1, col2 = st.columns(2)
    with col1:
        soil_type = st.selectbox("Soil Type", ["Sandy", "Loamy", "Black", "Red", "Clayey"])
        crop_type = st.selectbox("Crop Type", [
            "Maize", "Sugarcane", "Cotton", "Tobacco",
            "Paddy", "Barley", "Wheat", "Millets", "Oil seeds", "Pulses", "Ground Nuts"
        ])
        temperature = st.slider("Temperature (C)", min_value=25, max_value=45, value=34)
        humidity = st.slider("Humidity (%)", min_value=50, max_value=75, value=65)

    with col2:
        moisture = st.slider("Soil Moisture (%)", min_value=25, max_value=65, value=45)
        nitrogen = st.number_input("Nitrogen (N)", min_value=0, max_value=50, value=10)
        potassium = st.number_input("Potassium (K)", min_value=0, max_value=25, value=5)
        phosphorous = st.number_input("Phosphorous (P)", min_value=0, max_value=50, value=20)

    if st.button("Get Recommendation", type="primary"):
        with st.spinner("Analysing soil conditions..."):
            try:
                payload = {
                    "temperature": temperature, "humidity": humidity,
                    "moisture": moisture, "soil_type": soil_type,
                    "crop_type": crop_type, "nitrogen": nitrogen,
                    "potassium": potassium, "phosphorous": phosphorous
                }
                response = requests.post(f"{API_BASE}/predict-fertilizer", json=payload)
                data = response.json()

                if "error" in data:
                    st.error(f"Error: {data['error']}")
                else:
                    st.success("Recommendation ready!")
                    st.metric("Recommended Fertilizer", data['recommended_fertilizer'])
                    st.info(f"Prediction saved to database with ID #{data['prediction_id']}")
            except Exception as e:
                st.error(f"Could not connect to API server. Is it running? ({e})")

# ─── HISTORY PAGE ───────────────────────────────────────
elif page == "Disease Detection":
    st.header("Crop Disease Detection")
    st.write("Upload a leaf image to identify diseases using AI. Supported crops: Apple, Corn, Grape, Peach, Pepper, Potato, Soybean, Tomato, Rice, Wheat.")

    uploaded_file = st.file_uploader(
        "Upload a leaf image",
        type=["jpg", "jpeg", "png"],
        help="Take a clear photo of the affected leaf against a plain background for best results"
    )

    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(uploaded_file, caption="Uploaded leaf image", use_container_width=True)

        with col2:
            if st.button("Detect Disease", type="primary"):
                with st.spinner("Analysing leaf..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        response = requests.post(f"{API_BASE}/predict-disease", files=files)
                        data = response.json()

                        if "error" in data:
                            st.error(f"Error: {data['error']}")
                        else:
                            if data["is_healthy"]:
                                st.success("This leaf appears HEALTHY")
                            else:
                                st.error(f"Disease detected!")

                            st.metric("Crop", data["crop"])
                            st.metric("Diagnosis", data["disease"])
                            st.metric("Confidence", f"{data['confidence_percent']}%")

                            if not data["is_healthy"]:
                                st.warning(
                                    f"Recommended action: Consult your local agricultural extension "
                                    f"officer about treatment options for {data['disease']} in {data['crop']}."
                                )
                    except Exception as e:
                        st.error(f"Could not connect to API server. Is it running? ({e})")
elif page == "Prediction History":
    st.header("Prediction History")
    st.write("View all past predictions stored in the database.")

    tab1, tab2 = st.tabs(["Yield Predictions", "Fertilizer Predictions"])

    with tab1:
        limit = st.number_input("Number of records", min_value=1, max_value=100, value=10, key="yield_limit")
        if st.button("Load Yield History"):
            try:
                response = requests.get(f"{API_BASE}/predictions/yield", params={"limit": limit})
                data = response.json()
                predictions = data.get("predictions", [])
                if not predictions:
                    st.info("No yield predictions found yet.")
                else:
                    st.success(f"Showing {len(predictions)} predictions")
                    st.dataframe(predictions, use_container_width=True)
            except Exception as e:
                st.error(f"Could not connect to API server. ({e})")

    with tab2:
        limit2 = st.number_input("Number of records", min_value=1, max_value=100, value=10, key="fert_limit")
        if st.button("Load Fertilizer History"):
            try:
                response = requests.get(f"{API_BASE}/predictions/fertilizer", params={"limit": limit2})
                data = response.json()
                predictions = data.get("predictions", [])
                if not predictions:
                    st.info("No fertilizer predictions found yet.")
                else:
                    st.success(f"Showing {len(predictions)} predictions")
                    st.dataframe(predictions, use_container_width=True)
            except Exception as e:
                st.error(f"Could not connect to API server. ({e})")