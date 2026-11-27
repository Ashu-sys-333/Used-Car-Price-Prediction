# 🚗 Used Car Price Prediction – AutoValue

## About the Project

AutoValue is a Machine Learning project that predicts the estimated asking price of a used car based on its features.

The application takes car details such as brand, model, age, kilometres driven, transmission, owner type and fuel type as input and predicts its estimated price.

A user-friendly web application has been developed using Streamlit.

## Project Objective

The main objective of this project is to understand how Machine Learning can be used to solve a real-world price prediction problem and develop an application that is easy to use.

## Dataset Information

The dataset initially contained approximately 15,000 used car records. After data cleaning and preprocessing, 13,906 records were used for model development.

### Input Features

- Car Brand
- Car Model
- Car Age
- Kilometres Driven
- Transmission
- Owner Type
- Fuel Type

### Target Variable

- AskPrice (Listed Asking Price)

## Project Workflow

1. Importing the required Python libraries.
2. Loading and understanding the dataset.
3. Handling missing values and duplicate records.
4. Cleaning and preprocessing the data.
5. Performing Exploratory Data Analysis (EDA).
6. Converting categorical data into numerical values using One-Hot Encoding.
7. Splitting the dataset into 80% training and 20% testing data.
8. Training and comparing Machine Learning models.
9. Evaluating model performance.
10. Performing hyperparameter tuning.
11. Testing outlier removal and monotonic constraints.
12. Comparing age and mileage prediction consistency.
13. Selecting and saving the final model.
14. Developing and testing the Streamlit web application.

## Machine Learning Models

The following regression algorithms were used:

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor

Random Forest Regressor provided the best initial performance. Further experiments were conducted to improve prediction consistency.

## Model Performance

| Model | MAE (₹) | RMSE (₹) | R² Score |
|---|---:|---:|---:|
| Linear Regression | 4,66,144 | 9,02,300 | 0.5609 |
| Decision Tree Regressor | 2,32,954 | 10,11,590 | 0.4480 |
| Random Forest Regressor | 1,78,842 | 5,32,334 | 0.8471 |
| Random Forest with mileage constraint (Final Model) | 1,87,087 | 5,46,480 | 0.8389 |

## Model Improvement Experiments

### Outlier Detection and Handling

The IQR (Interquartile Range) method was used to identify unusually high mileage values.

- Q1: 44,000 km
- Q3: 87,000 km
- IQR: 43,000 km
- Upper limit: 1,51,500 km
- Lower limit: -20,500 km

Cars at least 3 years old with mileage below 1,000 km were also considered suspicious. A total of 672 records were excluded in an experimental dataset, leaving 13,234 records. The filtered model was trained using the remaining training records and evaluated on the original test set. Its R² decreased to 0.8241 and mileage inconsistency remained. Therefore, the additional filtering was not used for the final model.

### Hyperparameter Tuning

GridSearchCV with 3-fold cross-validation was used to test different values of `max_depth` and `min_samples_leaf`. The best combination was `max_depth=None` and `min_samples_leaf=1` among the tested settings.

### Monotonic Constraints

The original model sometimes predicted a higher price when age or mileage increased while other inputs remained unchanged. Monotonic constraints were tested to improve this behaviour.

| Experiment | R² Score |
|---|---:|
| Original Random Forest | 0.8471 |
| Random Forest after additional outlier removal | 0.8241 |
| Random Forest with age and mileage constraints | 0.7786 |
| HistGradientBoosting with age and mileage constraints | 0.7332 |
| Random Forest with mileage constraint only | 0.8389 |

The final model uses a constraint of -1 for `kmDriven` and 0 for all other encoded features. It is still trained on all seven input features. Increasing mileage cannot increase the estimated price when other inputs remain unchanged. Prices may remain the same over some mileage ranges.

### Prediction Consistency Testing

Both Random Forest models were compared using Force Gurkha, Skoda Kushaq, Hyundai Xcent, Mitsubishi Pajero Sport and BMW X3.

Mileage was varied from 10,000 to 1,50,000 km at six selected values. Age was varied from 1 to 15 years at seven selected values, with mileage fixed at 45,000 km.

| Test | Original Model | Mileage-Constrained Model |
|---|---:|---:|
| Mileage price increases (25 changes) | 6 | 0 |
| Age price increases (30 changes) | 2 | 2 |
| Total price increases (55 changes) | 8 | 2 |
| Overall consistency in selected tests | 85.45% | 96.36% |

These tests measure prediction consistency, not accuracy. Some hypothetical combinations may be unrealistic for particular car models. The same test dataset was used during model comparisons, so independent evaluation would be useful. IQR thresholds were calculated before the experimental training subset was selected.

## Final Model Selection

The mileage-constrained Random Forest (`rf_model_km`) was selected for the final application. It uses 100 decision trees and achieves an R² score of 0.8389, explaining approximately 83.89% of the variation in asking prices on the test dataset.

Although the original model has a slightly higher R², the final model provides more consistent mileage predictions. The R² reduction is approximately 0.82 percentage points and MAE increases by approximately ₹8,245. Age consistency is not guaranteed.

The original model was saved separately as a local backup. The final model was saved as `used_car_price_model.pkl` and its mileage predictions were verified in the Streamlit application using a Maruti Suzuki Swift.

## Technologies Used

- Python
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Streamlit
- Joblib

## Application Features

- Simple and user-friendly interface.
- Dynamic car model selection based on the selected brand.
- Car age and kilometres driven inputs.
- Transmission, ownership and fuel type selection.
- Estimated price in Indian currency format.
- Summary of selected vehicle details.
- Model performance information.
- Frequently asked questions.

## Project Files

| File | Description |
|---|---|
| app.py | Streamlit web application |
| used_car_price_model.pkl | Trained mileage-constrained Random Forest model |
| used_car_columns.pkl | Feature columns used during training |
| used_car_categories.pkl | Car categories and brand-model information |
| requirements.txt | Required Python libraries |
| README.md | Project documentation |
| .gitignore | Specifies files to exclude from Git |

The Jupyter Notebook contains the data preprocessing, analysis, model training, evaluation and experimental work.

## How to Run the Project

### Step 1: Download the Project

Download or clone the GitHub repository and open the project folder.

### Step 2: Install the Required Libraries

```bash
python -m pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your web browser at `http://localhost:8501`. Use Python and library versions compatible with the saved model.

## Project Limitations

- Predictions depend on the quality and availability of the training data.
- Some predictions may not follow the expected depreciation pattern with increasing age.
- Mileage predictions are non-increasing, but this does not guarantee accurate prices or a strict decrease at every mileage value.
- Factors such as vehicle condition, accident history, service history and location are not included.
- The model uses historical data, so predictions may differ from current market prices.

## Future Improvements

- Use a larger and more recent dataset.
- Include additional vehicle features.
- Improve age prediction consistency without significantly reducing predictive performance.
- Further improve model performance.

## Note

The predicted price is an estimate generated by a Machine Learning model and is not a guaranteed market price.

## Conclusion

This project demonstrates the practical application of Machine Learning in used car price prediction. It covers the complete process from data collection and preprocessing to model training, evaluation and web application development.

Developed as a B.Tech Machine Learning academic project.