# Used Car Price Prediction

End-to-end data science project (CDS 4003, Data Science for Business Application): predicting used car listing prices with machine learning and deploying the model as a Streamlit web app.

**Live app:** https://used-car-price-prediction-fnrdd4wrzodffcpsfcgbe6.streamlit.app/

## Business problem
Used-car dealers must price each vehicle they buy or list. Pricing too high leaves cars unsold, and pricing too low loses profit. This project builds a model that estimates a fair listing price from basic car details (year, mileage, make, model, condition and so on) so dealers can price inventory faster and check whether an asking price is reasonable. 

**Objectives**
- Build a regression model that predicts listing price with an average error below $4,000.
- Compare at least two machine learning models against a baseline.
- Deploy an app that gives a price estimate, a likely range, and a check on an asking price.

## Team
| Member | GitHub | Role |
|---|---|---|
| Ahmed Masoud AlKhoori | [@alkhoori01](https://github.com/alkhoori01) | Business problem, dataset search, data cleaning, EDA and feature engineering, README |
| Mansoor Abdulhakeem AlTamimi | [@Mansooralt](https://github.com/Mansooralt) | Modelling, tuning and evaluation, Streamlit app, documentation and deployment |

## Dataset
- **Name:** Craigslist Cars and Trucks Data
- **Source:** Kaggle, `austinreese/craigslist-carstrucks-data` (https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data)
- **Licence:** MIT
- **Size:** 295,451 listings and 41 columns (214,253 rows after cleaning)
- **How to obtain:** run `python src/download_data.py`. The full file is about 1.1 GB, so it is not stored in this repo. A 5,000-row sample is in `data/sample/vehicles_sample.csv`.

Dataset search evidence and the data dictionary are in `docs/`.

## Repository structure
```
├── app/                      Streamlit app (app.py, requirements.txt)
├── data/
│   ├── raw/                  full dataset (git-ignored, created by the download script)
│   ├── processed/            cleaned and feature data (git-ignored, created by notebooks)
│   └── sample/               small sample of the raw data
├── docs/                     data dictionary, dataset search evidence, AI usage
├── models/                   saved model and app configuration
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_features.ipynb
│   └── 04_modeling.ipynb
├── src/
│   ├── download_data.py      downloads the dataset from Kaggle
│   └── build_app_options.py  builds app configuration from the saved model
├── requirements.txt
└── README.md
```

## How to run
```bash
git clone https://github.com/alkhoori01/used-car-price-prediction.git
cd used-car-price-prediction
pip install -r requirements.txt

python src/download_data.py          # download the data (needs Kaggle access)
# Run the notebooks in order (the processed data is created by 02 and 03):
#   notebooks/02_data_cleaning.ipynb
#   notebooks/03_eda_features.ipynb
#   notebooks/04_modeling.ipynb
python src/build_app_options.py      # build app configuration
streamlit run app/app.py             # start the app locally
```
The trained model (`models/price_model.joblib`) is included, so the app can run without retraining.

## Method summary
1. **Business problem:** pricing support for used-car dealers (regression).
2. **Data collection:** compared several candidate datasets, then chose Craigslist Cars and Trucks (see `docs/dataset_search_evidence.md`).
3. **Cleaning:** converted text prices, standardised text, removed 47,299 near-duplicate listings, removed impossible values (price 500–100,000, year 1990–2026, odometer 1–500,000) and labelled missing categories "unknown". Rows went from 295,451 to 214,253 and missing cells fell from 525,698 to 144,911.
4. **EDA and features:** price is right-skewed, so log price is the target. Features include car age and log odometer. Price depends mainly on year, mileage, seller type, condition, and fuel and drive type.
5. **Models:** mean baseline, Ridge, Random Forest and HistGradientBoosting, compared with 3-fold cross-validation.
6. **Tuning:** RandomizedSearchCV with 3-fold cross-validation on HistGradientBoosting and Random Forest.
7. **Deployment:** Streamlit Community Cloud app that estimates a price, gives a likely range and checks an asking price.

## Results (20% held-out test set)
| Model | MAE ($) | RMSE ($) | R² | Median % error |
|---|---|---|---|---|
| Ridge | 4,919 | 8,754 | 0.66 | 22.0 |
| HistGradientBoosting (default) | 3,895 | 6,709 | 0.80 | 18.6 |
| **HistGradientBoosting (tuned)** | **3,469** | **6,027** | **0.84** | **16.5** |
| Random Forest (default, 80k rows) | 3,545 | 6,292 | 0.82 | 17.1 |
| Random Forest (tuned, 80k rows) | 3,443 | 6,179 | 0.83 | 16.6 |

The final model is the tuned HistGradientBoosting: it has the best RMSE and R², was trained on all the data, and its file is only 0.6 MB.

## Limitations
- Craigslist prices are asking prices, not final sale prices.
- Random Forest was trained on a subsample because of memory limits.
- Predictions are less reliable for rare, classic or very expensive cars.
- Data covers one period and needs retraining as the market changes.

## AI usage declaration
AI tools were used for debugging support. Full details are in `docs/ai_usage.md`.

## Acknowledgements
Dataset by Austin Reese on Kaggle.
