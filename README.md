# Payment Gateway Companies Analysis

This project aims to analyze and segment payment gateway companies based on various criteria, including company size and industry sub-sectors. It utilizes web-scraped data online.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Analysis Overview](#analysis-overview)
- [Project Structure](#project-structure)
- [License](#license)

## Features

- Web scraping capabilities for company data.
- Data cleaning and deduplication.
- Segmentation of companies by employee size and industry sub-sectors.
- Statistical analysis to identify patterns and trends.
- Output of cleaned and segmented data to a CSV file.

## Installation

To set up the project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd "Payment Gateway companies"
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    (If you are using Anaconda, you can use `conda activate base` if you intend to use your base environment, or create a new one: `conda create -n payment_gateway python=3.x` and then `conda activate payment_gateway`)

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the data scraping script (if needed):**
    The `src/main.py` script is designed to scrape data. Before running, ensure `CHROME_DRIVER` in `src/main.py` is updated to your ChromeDriver path if you are not using `undetected_chromedriver` for its auto-download feature.
    
    ```bash
    python src/main.py
    ```
    This will generate `payment_gateways.csv` in the `data/` directory.

2.  **Run the data analysis:**
    The core analysis, cleaning, and segmentation are performed in the Jupyter Notebook.
    
    First, ensure the `payment_gateways.csv` is in the `data/` folder.
    
    Then, open the Jupyter Notebook:
    
    ```bash
    jupyter notebook notebooks/analysis.ipynb
    ```
    Execute the cells in the notebook to see the data cleaning steps, segmentation, statistical analysis, and visualizations.
    
    The cleaned and segmented data will be saved as `data/segmented_payment_gateway_companies.csv`.


## Analysis Overview

| **Dimension** | **Biggest** **Slice** | **Relevance** |
| --- | --- | --- |
| Region | Americas (13 / 24) | Content is skewed to US topics now but translating/adapting for EU rules will widen the addressable audience. |
| Size | Micro (1-19 employees) - 75 % | Start-ups mostly → they buy quickly if you show clear ROI and practical guides |
| Sub-sector | General Gateway (15) | Core processing still dominates, but **Crypto (6)** is a fast-growing niche. |
| Industry | Financial Services (15) | Confirms this is fintech space, not generic SaaS → compliance & trust messaging is key. |

## Project Structure

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── data/
│   └── apollo_payment_gateways.csv
│   └── segmented_payment_gateway_companies.csv
├── src/
│   └── main.py
└──  notebooks/
   └── analysis.ipynb

```

## License

This project is licensed under the [MIT License](LICENSE). 