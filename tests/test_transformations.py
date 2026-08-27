from pyspark.sql import SparkSession

from src.transformations import transform_hdb_data


def test_transform_hdb_data():
    spark = SparkSession.getActiveSession()

    input_data = [
        ("2017-01", 232000.0, 44.0, 1979, "61 years 04 months")
    ]

    columns = [
        "month",
        "resale_price",
        "floor_area_sqm",
        "lease_commence_date",
        "remaining_lease"
    ]

    df = spark.createDataFrame(input_data, columns)

    result = transform_hdb_data(df).collect()[0]

    assert result.transaction_year == 2017
    assert result.transaction_month == 1
    assert result.price_per_sqm == 5272.73
    assert result.flat_age == 38
    assert result.remaining_lease_years == 61
    assert result.remaining_lease_months == 4

    

def test_remaining_lease_without_months():
    spark = SparkSession.getActiveSession()

    input_data = [
        ("2017-01", 275000.0, 68.0, 1981, "63 years")
    ]

    columns = [
        "month",
        "resale_price",
        "floor_area_sqm",
        "lease_commence_date",
        "remaining_lease"
    ]

    df = spark.createDataFrame(input_data, columns)

    result = transform_hdb_data(df).collect()[0]

    assert result.remaining_lease_years == 63
    assert result.remaining_lease_months == 0