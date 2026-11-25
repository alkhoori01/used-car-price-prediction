# Dataset Search Evidence

**Problem:** predicting used car prices for dealers (regression).
**Requirements:** at least 200,000 rows, at least 20 columns, real data, a clear target, a licence that allows academic use.
**Search terms used:** "used cars price", "car listings", "vehicle sales", "[ADD YOUR OWN TERMS]"
**Sources checked:** Kaggle, [UCI, Google Dataset Search, Bayanat if you used them]. **Date:** 25-11-2026

| Dataset | Source | Rows / columns | Licence | Decision | Reason |
|---|---|---|---|---|---|
| Craigslist Cars and Trucks | Kaggle | 295,451 / 41 | MIT | **Accepted** | Meets size requirements, real prices, rich features, many quality issues to clean, easy to explain to a business audience |
| Credit Card Fraud (ULB) | Kaggle | 284,807 / 31 | MIT | Rejected | Already clean and anonymised, so little to clean, and is imbalanced |
| Telco Customer Churn | Kaggle | 7043 / 21 | MIT | Rejected | Far below 200,000 rows |

## Why Craigslist Cars and Trucks
- Matches the business problem directly.
- 214,253 rows remain after cleaning, still above the 200,000 requirement.
- Mix of numeric, categorical, text and date columns.

## Limitations and bias risks
- Prices are asking prices, not final sale prices.
- Listings come from Craigslist only and may not represent the whole used-car market.
- Dealers are over-represented (about 72% of cleaned rows).
- Some listings are reposted or have unreliable fields, which cleaning only partly fixes.