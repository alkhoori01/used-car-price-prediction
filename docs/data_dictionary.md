# Data Dictionary

Source: Craigslist Cars and Trucks (Kaggle). 41 raw columns; 25 were kept for cleaning. "Used in model" refers to the final model.

## Original columns kept
| Column | Type | Description | Used in model |
|---|---|---|---|
| price | number | Listing price in USD (target; converted from text) | Target (log) |
| year | number | Model year of the car | Yes |
| manufacturer | text | Car brand | Yes |
| model | text | Car model (top 100 kept, others grouped as "other") | Yes |
| condition | category | Seller-stated condition (fair to new) | Yes |
| cylinders | number | Number of engine cylinders (extracted from text) | Yes |
| fuel | category | Fuel type | Yes |
| odometer | number | Mileage in miles | Yes |
| title_status | category | Title status (clean, rebuilt, salvage, lien and so on) | Yes |
| transmission | category | Automatic, manual or other | Yes |
| VIN | text | Vehicle identification number (used to detect reposts) | No |
| drive | category | 4wd, fwd or rwd | Yes |
| type | category | Body type (SUV, sedan, pickup and so on) | Yes |
| paint_color | category | Paint colour | Yes |
| description | text | Listing description (used for duplicate detection, length feature) | No |
| state | category | US state of the listing | Yes |
| region | text | Craigslist region | No |
| lat, long | number | Listing coordinates | No |
| posting_date | datetime | Date the listing was posted | No (used for car age) |
| seller_type | category | Dealer or owner | Yes |
| image_count | number | Number of photos | No |
| delivery_available | 0/1 | Delivery offered | No |
| odometer_broken, odometer_rolled_over | 0/1 | Odometer flags | No |

## Original columns dropped
`id`, `url`, `region_url`, `image_url`, `image_urls` (identifiers with no price information), `size` and `county` (100% empty), `monthly_payment` (98% empty), `other_attributes` (98.7% empty), and address columns, `updated_date` (high missingness or not useful).

## Engineered features (notebook 03)
| Feature | Definition | Used in model |
|---|---|---|
| car_age | posting year minus model year | No (duplicates `year`, correlation -1.00) |
| miles_per_year | odometer / (car_age + 1) | No (weak correlation with price) |
| log_odometer | log(1 + odometer) | No |
| is_luxury | 1 if brand is in a luxury list | No (near-zero correlation) |
| has_vin | 1 if a VIN is given | No (cannot be entered in the app) |
| description_length | characters in description | No (cannot be entered in the app) |
| posting_month | month of posting | No |
| log_price | log(1 + price) | Target |

## Data quality issues found and handled
| Issue | Evidence | Handling |
|---|---|---|
| Price stored as text | mixed types on load | converted to numeric |
| Impossible prices | min 0, max 1e24; 10,288 zeros | kept 500–100,000 |
| Impossible years | 1900 to 2027 | kept 1990–2026 |
| Extreme mileage | up to 10,000,000 | kept 1–500,000 |
| Near-duplicate reposts | 47,299 found | removed |
| Missing categories | condition 45.9%, cylinders 27.1%, paint_color 25.3%, drive 23.8% | filled with "unknown" (cylinders imputed in the pipeline) |
| Empty columns | size, county 100% | dropped |