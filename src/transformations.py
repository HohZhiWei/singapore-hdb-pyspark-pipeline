from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    to_date,
    year,
    month,
    round,
    regexp_extract,
    when,
    lit
)


def transform_hdb_data(df: DataFrame) -> DataFrame:
    return (
        df
        .withColumn(
            "transaction_date",
            to_date(col("month"), "yyyy-MM")
        )
        .withColumn(
            "transaction_year",
            year(col("transaction_date"))
        )
        .withColumn(
            "transaction_month",
            month(col("transaction_date"))
        )
        .withColumn(
            "price_per_sqm",
            round(col("resale_price") / col("floor_area_sqm"), 2)
        )
        .withColumn(
            "flat_age",
            col("transaction_year") - col("lease_commence_date")
        )
        .withColumn(
            "remaining_lease_years",
            regexp_extract(
                col("remaining_lease"),
                r"(\d+) years?",
                1
            ).cast("int")
        )
        .withColumn(
            "remaining_lease_months",
            when(
                regexp_extract(
                    col("remaining_lease"),
                    r"(\d+) months?",
                    1
                ) == "",
                lit(0)
            ).otherwise(
                regexp_extract(
                    col("remaining_lease"),
                    r"(\d+) months?",
                    1
                ).cast("int")
            )
        )
    )