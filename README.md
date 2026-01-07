# Multimodal Housing Price Prediction

This project predicts housing prices using two distinct approaches: a standard **Tabular Model** (using XGBoost) and an advanced **Multimodal Fusion Model** (combining XGBoost with an EfficientNetB0 CNN trained on satellite imagery).

## 📂 Project Structure

* **`data_fetcher.py`**: A utility script that interacts with the Mapbox API to download satellite imagery for specific coordinates.
* **`preprocessing.ipynb`**: Handles data cleaning and feature engineering (e.g., calculating `house_age`, `scenic_score`) for the tabular approach.
* **`final_model.ipynb`**: **(Method A)** Trains and generates predictions using only tabular data via XGBoost.
* **`model_training.ipynb`**: **(Method B)** The Fusion approach. This script automates image downloading, trains a tabular model, trains a CNN on residuals, and fuses the results.

---

## ⚙️ Setup & Prerequisites

### 1. Install Dependencies
Ensure you have Python installed, then run:

```bash
pip install pandas numpy xgboost tensorflow opencv-python requests openpyxl
```

### 2. Mapbox API Token (Required for Fusion Model)
To use the satellite imagery features (Method B), you need a Mapbox API token.

1.  Sign up and get a token from [Mapbox.com](https://www.mapbox.com/).
2.  Set it as an environment variable in your terminal before running the scripts.

**Linux/Mac:**
```bash
export MAPBOX_TOKEN="your_token_here"
```

**Windows (Command Prompt):**
```cmd
set MAPBOX_TOKEN=your_token_here
```

### 3. Input Data
Ensure your root directory contains the necessary Excel files:
* `train(1).xlsx` (Training data)
* `test.xlsx` or `test2.xlsx` (Testing data)
  
  The training data is already preprocessed in the repository and can be directly used for training the models.

---

## 🚀 Usage Guide

There are two ways to generate price predictions in this project. Choose the one that fits your needs.

### Option 1: The Tabular Model (Fast)
*Use this method if you only want to use numerical features (square footage, year built, etc.) without downloading images.*

**Step 1: Preprocess the Data**
Run the **`preprocessing.ipynb`** notebook.
* **What it does:** Loads raw test data (`test2.xlsx`), performs feature engineering (log transforms, drops unused columns), and saves the cleaned data.
* **Output:** Creates a file named `processed_housing_dataset.xlsx`.

**Step 2: Generate Predictions**
Run the **`final_model.ipynb`** notebook.
* **What it does:** Reads the training data and the processed test data. It trains an XGBoost Regressor (1500 estimators, depth 6) on the numerical features.
* **Output:** Saves the final predictions to **`tabular_price_predictions.csv`**.

---

### Option 2: The Fusion Model (Advanced)
*Use this method for comparing accuracy by combining tabular data with visual environmental data (Satellite Imagery).*

**Step 1: Run the Training Script**
Execute the **`model_training.ipynb`** notebook.

**Step 2: Automated Pipeline**
This notebook handles the entire process automatically:
1.  **Image Fetching:** It calls `data_fetcher.py` to download satellite snapshots for every house in the training and test sets into the `satellite_images/` directory.
2.  **Tabular Baseline:** It trains an XGBoost model on the numerical data to get a baseline prediction.
3.  **Residual Analysis:** It calculates the "residuals" (the difference between the actual price and the XGBoost prediction).
4.  **CNN Training:** It fine-tunes an **EfficientNetB0** CNN on the satellite images to predict these residuals (effectively learning what the tabular model missed).
5.  **Fusion:** It combines the results using the formula:
    $$\text{Final Price} = \text{XGBoost Prediction} + (0.5 \times \text{CNN Correction})$$

**Output:**
* Saves the fused predictions to **`fusion_price_predictions.csv`**.

---

## 📝 Troubleshooting & Notes

* **Image Download Speed:** The `data_fetcher.py` script includes a small `sleep` delay to avoid hitting API rate limits. Downloading thousands of images may take time.
* **Re-running Downloads:** The fetcher checks if an image exists before downloading. If you need to force a re-download, delete the `satellite_images/` folder.
* **Data Matching:** The scripts use the `id` column to map spreadsheet rows to image filenames (`{id}.png`). We are only considering unique ids and duplicates are dropped during preprocess.