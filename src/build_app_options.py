import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

BASE = Path(__file__).resolve().parent.parent
num_cols = ["year", "odometer", "cylinders"]
cat_cols = ["manufacturer", "model", "condition", "fuel", "transmission", "drive",
            "type", "paint_color", "title_status", "seller_type", "state"]

# Same preparation as notebook 04
df = pd.read_parquet(BASE / "data/processed/vehicles_features.parquet",
                     columns=num_cols + cat_cols + ["log_price"])
X = df[num_cols + cat_cols].copy()
X["cylinders"] = X["cylinders"].astype(float)
X[cat_cols] = X[cat_cols].astype(str)
y = df["log_price"]
del df

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_test = X_train.copy(), X_test.copy()
del X

top_models = joblib.load(BASE / "models/top_models.joblib")
for d in (X_train, X_test):
    d["model"] = d["model"].where(d["model"].isin(top_models), "other")

model = joblib.load(BASE / "models/price_model.joblib")

# Typical error range: actual price / predicted price
pred = np.expm1(model.predict(X_test))
true = np.expm1(y_test.values)
ratio = true / pred
print("Test MAE ($):", round(float(np.abs(pred - true).mean())))   # should be about 3469

# Models available per manufacturer (for the dropdowns)
models_by_make = (X_train[X_train["model"] != "other"].groupby("manufacturer")["model"]
                  .agg(lambda s: sorted(s.unique())).to_dict())

# Permutation importance on a small sample, single process, to keep memory low
samp = X_test.sample(3000, random_state=42)
pi = permutation_importance(model, samp, y_test.loc[samp.index], n_repeats=2,
                            random_state=42, n_jobs=1,
                            scoring="neg_root_mean_squared_error")
importance = dict(sorted(zip(samp.columns, pi.importances_mean.round(4).tolist()),
                         key=lambda kv: kv[1], reverse=True))

opts = {
    "year_range": [int(X_train["year"].min()), int(X_train["year"].max())],
    "cylinders": sorted(X_train["cylinders"].dropna().unique().tolist()),
    "categorical": {c: sorted(X_train[c].unique().tolist())
                    for c in cat_cols if c not in ("model", "manufacturer")},
    "manufacturers": sorted(X_train["manufacturer"].unique().tolist()),
    "models_by_make": models_by_make,
    "ratio_low": float(np.quantile(ratio, 0.10)),
    "ratio_high": float(np.quantile(ratio, 0.90)),
    "metrics": {"MAE": 3469, "R2": 0.84, "median_pct_error": 16.5},
    "importance": importance,
}
with open(BASE / "models/app_options.json", "w") as f:
    json.dump(opts, f, indent=2)

print("ratio_low / ratio_high:", round(opts["ratio_low"], 3), round(opts["ratio_high"], 3))
print("importance:", importance)