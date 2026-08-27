# Singapore HDB Resale PySpark Pipeline

A beginner-level data engineering project built to strengthen and demonstrate practical PySpark skills using Singapore HDB resale transaction data.

## Project Overview

This project processes Singapore HDB resale transactions from January 2017 onwards using PySpark and Databricks.

The pipeline follows a Bronze–Silver–Gold structure. Raw CSV data is first loaded into Databricks, then cleaned and enriched with PySpark before being aggregated into a Gold dataset for analysis.

The main goal of the project is to practise and showcase core PySpark concepts in a batch-processing workflow, including DataFrames, schemas, transformations, aggregations, window functions, Delta tables, and basic testing.

## Architecture

```text
data.gov.sg
HDB Resale CSV
      |
      | Manual download
      v
Databricks Volume
      |
      | PySpark
      v
Bronze Delta Table
      |
      | Cleaning
      | Derived columns
      | Data validation
      v
Silver Delta Table
      |
      | Aggregations
      | Window functions
      v
Gold Delta Table
```

## Tech Stack

* Python
* PySpark
* Apache Spark
* Databricks
* Delta Lake
* Git / GitHub
* pytest

## Data Source

The project uses Singapore HDB resale flat price data published by the Housing & Development Board through data.gov.sg.

Dataset used:

**Resale flat prices based on registration date from January 2017 onwards**

The raw CSV is stored separately and is not committed to this repository.

## Pipeline

### Bronze

The raw HDB CSV is read into Spark using an explicit `StructType` schema and written as a Delta table.

An ingestion timestamp is added while the original source fields are otherwise kept unchanged.

This layer provides a clean starting point for downstream processing while preserving the raw transaction data.

### Silver

The Bronze dataset is profiled before transformation.

The checks include:

* Row count
* Null-value checks
* Duplicate detection
* Numeric range checks

A small number of exact duplicate-looking records were found. These records are retained because the source dataset does not provide a unique transaction ID, so it is not possible to confidently determine whether they are true duplicates or separate transactions with identical attributes.

The Silver transformation creates several useful fields:

* `transaction_date`
* `transaction_year`
* `transaction_month`
* `price_per_sqm`
* `flat_age`
* `remaining_lease_years`
* `remaining_lease_months`

Remaining lease values are parsed including cases where the source provides only the number of remaining years without a month component.

The transformation logic is kept in a reusable Python module before the final dataset is written as a Silver Delta table.

### Gold

The Silver data is aggregated by town and transaction year to produce a simple analytical dataset.

The Gold table contains:

* Average resale price
* Average price per square metre
* Transaction count
* Town ranking by average resale price

A PySpark window function is used to rank towns within each transaction year.

## PySpark Skills Demonstrated

This project includes practical use of:

* Spark DataFrames
* `StructType` and `StructField`
* Explicit Spark data types
* `select`
* `withColumn`
* `filter`
* `groupBy`
* `agg`
* `orderBy`
* Date transformations
* Regular-expression extraction
* Column expressions
* Window functions
* Delta table reads and writes
* Basic data-quality validation

## Testing

The Silver transformation logic is separated into:

```text
src/transformations.py
```

Basic PySpark unit tests to create small controlled DataFrames and check that the transformation produces the expected output.

The tests cover:

* Transaction year and month extraction
* Price per square metre calculation
* Flat age calculation
* Remaining lease parsing
* Remaining lease values without a month component

This keeps the tests small and focused on the transformation logic rather than the full dataset.

## Project Structure

```text
singapore-hdb-pyspark-pipeline/
|
├── notebooks/
│   ├── 01_bronze_ingestion
│   ├── 02_silver_transformation
│   └── 03_gold_aggregation
|
├── src/
│   ├── __init__.py
│   └── transformations.py
|
├── tests/
│   ├── conftest.py
│   └── test_transformations.py
|
├── data/
│   └── raw/
│       └── .gitkeep
|
├── .gitignore
└── README.md
```

## What I Learned

This project has given me a hands-on experience building a small batch-processing pipeline with PySpark instead of using row-by-row Python processing.

It has gotten me more comfortable with Spark DataFrames, explicit schemas, lazy transformations, aggregations, window functions, Delta tables, data-quality checks, and writing reusable transformation logic that can be tested independently.
