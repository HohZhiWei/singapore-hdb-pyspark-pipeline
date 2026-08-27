# Singapore HDB Resale PySpark Pipeline

A beginner level data engineering project built to develop and demonstrate practical PySpark skills with Singapore HDB resale transaction data.

## Project Overview

This project processes Singapore HDB resale transaction data using PySpark.

The pipeline will transform raw transaction data into cleaned, enriched, and aggregated datasets for downstream usage.

The project follows a medallion-style architecture:

- Bronze: Raw transaction data
- Silver: Cleaned and enriched transaction data
- Gold: Aggregated analytical datasets

## Technology

- Python
- PySpark
- Apache Spark
- Databricks
- Delta Lake
- Git / GitHub

## Data Source

Singapore HDB resale flat price data published on data.gov.sg.

Dataset:
Resale flat prices based on registration date from January 2017 and onwards.

## Architecture

```text
HDB Resale CSV
      |
      v
    Bronze
      |
      | PySpark transformations
      v
    Silver
      |
      | PySpark aggregations
      v
     Gold