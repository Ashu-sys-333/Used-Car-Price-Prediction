
import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(
    page_title="AutoValue | Used Car Price Prediction",
    page_icon="🚘",
    layout="centered"
)


# Application styling
st.markdown("""
<style>

    .block-container {
        max-width: 950px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero {
        background: linear-gradient(135deg, #0f172a, #164e63);
        padding: 35px 30px;
        border-radius: 18px;
        margin-bottom: 25px;
    }

    .brand-name {
        color: #5eead4;
        font-size: 23px;
        font-weight: bold;
        letter-spacing: 1px;
    }

    .hero h1 {
        color: #ffffff;
        font-size: 36px;
        margin-top: 15px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #cbd5e1;
        font-size: 16px;
    }

    .model-tag {
        display: inline-block;
        background-color: #134e4a;
        color: #99f6e4;
        padding: 7px 15px;
        border-radius: 20px;
        font-size: 13px;
        margin-top: 10px;
    }

    .stat-card {
        background-color: #f0fdfa;
        border: 1px solid #99f6e4;
        border-radius: 12px;
        padding: 18px 8px;
        text-align: center;
        margin-bottom: 10px;
    }

    .stat-value {
        color: #0f766e;
        font-size: 25px;
        font-weight: bold;
    }

    .stat-label {
        color: #475569;
        font-size: 13px;
        margin-top: 5px;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #0f766e, #0d9488);
        color: white;
        border: none;
        border-radius: 12px;
        min-height: 52px;
        font-size: 17px;
        font-weight: bold;
    }

    div.stButton > button:hover {
        background: #115e59;
        color: white;
        border: none;
    }

    .result-card {
        background: linear-gradient(135deg, #0f172a, #164e63);
        border: 1px solid #0d9488;
        border-radius: 18px;
        padding: 30px 20px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .result-label {
        color: #99f6e4;
        font-size: 15px;
        font-weight: bold;
        letter-spacing: 2px;
    }

    .result-price {
        color: #ffffff;
        font-size: clamp(30px, 6vw, 48px);
        font-weight: bold;
        margin: 15px 0;
    }

    .result-car {
        color: #cbd5e1;
        font-size: 20px;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        padding: 10px;
    }

</style>
""", unsafe_allow_html=True)


# Load saved model and supporting files
@st.cache_resource
def load_files():

    model = joblib.load("used_car_price_model.pkl")
    columns = joblib.load("used_car_columns.pkl")
    categories = joblib.load("used_car_categories.pkl")

    return model, columns, categories


model, columns, categories = load_files()


# Indian number formatting
def indian_format(number):

    number = str(int(round(number)))

    if len(number) <= 3:
        return number

    last_three = number[-3:]
    remaining = number[:-3]

    parts = []

    while remaining:
        parts.append(remaining[-2:])
        remaining = remaining[:-2]

    return ",".join(parts[::-1]) + "," + last_three


# Application header
st.html("""
<div class="hero">
    <div class="brand-name">🚘 AutoValue</div>
    <h1>Know your car's worth.</h1>
    <p>Estimate the resale value of your car using Machine Learning.</p>
    <div class="model-tag">Powered by Random Forest Regressor</div>
</div>
""")
# Model statistics
stat1, stat2, stat3 = st.columns(3)

with stat1:

    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">13,906</div>
        <div class="stat-label">Car Records</div>
    </div>
    """, unsafe_allow_html=True)

with stat2:

    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">100</div>
        <div class="stat-label">Decision Trees</div>
    </div>
    """, unsafe_allow_html=True)

with stat3:

    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">0.8389</div>
        <div class="stat-label">R² Score</div>
    </div>
    """, unsafe_allow_html=True)


# Sidebar
with st.sidebar:

    st.title("🚘 AutoValue")

    st.caption("Used Car Price Prediction")

    st.divider()

    st.subheader("About the Project")

    st.write(
        "AutoValue is a Machine Learning application "
        "that estimates used car prices based on "
        "vehicle information and usage details."
    )

    st.divider()

    st.subheader("Model Performance")

    st.write("**Algorithm:** Random Forest Regressor")

    st.metric("R² Score", "0.8389")

    st.metric("MAE", "₹1,87,087")

    st.metric("RMSE", "₹5,46,480")

    st.caption(
        "Performance measured on the project's test dataset."
    )

    st.divider()

    st.subheader("Technologies Used")

    st.markdown("""
    - Python
    - Pandas
    - NumPy
    - Scikit-learn
    - Streamlit
    - Joblib
    """)

    st.divider()

    st.caption("B.Tech Machine Learning Project")


# Vehicle details
with st.container(border=True):

    st.subheader("🚗 Vehicle Details")

    st.caption("Select the basic information about your car.")

    col1, col2 = st.columns(2)

    with col1:

        brand = st.selectbox(
            "Car Brand",
            categories["Brand"]
        )

    with col2:

        available_models = categories["brand_models"][brand]

        car_model = st.selectbox(
            "Car Model",
            available_models
        )

    col3, col4 = st.columns(2)

    with col3:

        fuel_type = st.selectbox(
            "Fuel Type",
            categories["FuelType"]
        )

    with col4:

        transmission = st.selectbox(
            "Transmission",
            categories["Transmission"]
        )


# Usage details
with st.container(border=True):

    st.subheader("📋 Usage Details")

    st.caption("Enter the age, mileage and ownership details.")

    col5, col6 = st.columns(2)

    with col5:

        age = st.number_input(
            "Car Age (Years)",
            min_value=0,
            max_value=50,
            value=5,
            step=1
        )

    with col6:

        km_driven = st.number_input(
            "Kilometres Driven",
            min_value=0,
            value=45000,
            step=1000
        )

    owner = st.selectbox(
        "Owner Type",
        categories["Owner"]
    )


# Prediction button
if st.button(
    "Calculate Estimated Price",
    use_container_width=True
):

    # Create DataFrame from user inputs
    new_car = pd.DataFrame({
        "Brand": [brand],
        "model": [car_model],
        "Age": [age],
        "kmDriven": [km_driven],
        "Transmission": [transmission],
        "Owner": [owner],
        "FuelType": [fuel_type]
    })

    # Convert categorical values into numerical columns
    new_car_encoded = pd.get_dummies(
        new_car,
        columns=[
            "Brand",
            "model",
            "Transmission",
            "Owner",
            "FuelType"
        ],
        drop_first=False,
        dtype=int
    )

    # Match the columns used during training
    new_car_encoded = new_car_encoded.reindex(
        columns=columns,
        fill_value=0
    )

    # Predict car price
    with st.spinner("Calculating estimated car value..."):

        prediction = model.predict(new_car_encoded)[0]

    # Display estimated price
    st.html(f"""
<div class="result-card">
    <div class="result-label">ESTIMATED CAR VALUE</div>
    <div class="result-price">₹{indian_format(prediction)}</div>
    <div class="result-car">Your selected vehicle</div>
</div>
""")

    # Display vehicle summary
    with st.container(border=True):

        st.subheader(f"{brand} {car_model}")

        summary1, summary2, summary3 = st.columns(3)

        with summary1:

            st.metric(
                "Car Age",
                f"{age} Years"
            )

        with summary2:

            st.metric(
                "Mileage",
                f"{indian_format(km_driven)} km"
            )

        with summary3:

            st.metric(
                "Fuel Type",
                fuel_type
            )

        st.write(f"**Transmission:** {transmission}")
        st.write(f"**Ownership:** {owner}")

    st.info(
        "This is an estimated price generated by a "
        "Machine Learning model. Actual market prices "
        "may vary depending on vehicle condition, "
        "location and demand."
    )


# Frequently asked questions
st.divider()

with st.expander("How does this application work?"):

    st.write(
        "The application collects your car details and "
        "converts them into numerical values. These values "
        "are passed to a trained Random Forest model, "
        "which estimates the price based on patterns "
        "learned from the used car dataset."
    )


with st.expander("Is the predicted price guaranteed?"):

    st.write(
        "No. The predicted price is an estimate based "
        "on historical car data. The actual selling price "
        "may depend on the car's condition, service history, "
        "location and current market demand."
    )


# Footer
st.divider()

st.markdown("""
<div class="footer">
    <b>AutoValue</b> | Used Car Price Prediction
    <br>
    Developed as a Machine Learning Academic Project
</div>
""", unsafe_allow_html=True)
