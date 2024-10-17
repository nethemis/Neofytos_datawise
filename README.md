# Senior Data Scientist Project - Neofytos

## Overview

This project analyzes order data for 2022 and 2023. The goal is to:

1. Analyze order journeys and calculate conversion rates.
2. Develop a recommendation system for items displayed on the website's landing page.

## Project Structure

- **/data/**: Raw datasets.
- **/src/**: Python scripts for ETL, analysis, and recommendations.
- **/tests/**: Unit tests.
- **/database/**: The directory where the local database is stored

## How to set-up (first time)

1. Create a virtual environment and install dependencies `make install`
2. Copy the input csv file to the data directory.

## How to run

1. Activate the virtual environment `make activate`
2. Run ETL and create the DB: `make setup_db`
3. Run part A1: `make run-A1`
4. Run part A2: `make run-A2`
5. Run part B: `make run-B1`
6. Run tests: `make test`

## How to run (without using the Makefile)

1. (only first time) setup venv: `python -m venv venv/`
2. Activate the venv: `source venv/bin/activate`
3. (only first time) install dependencies: `pip install -r requirements.txt`
4. Run ETL and create the DB: `python src/setup_db.py`
5. Run part A1: `python src/A1.Volumetrics.py`
6. Run part A2: `python src/A2.Conversion_rate.py `
7. Run part B: `python src/B.recommendation_system.py `
8. Run tests: `pytest tests/`
