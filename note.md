# Geospatial Query Performance Comparison: GeoParquet vs. Shapefile with DuckDB

This document summarizes a benchmark comparing the efficiency of spatial queries on GeoParquet and Shapefile formats, both with and without the use of DuckDB.

## Benchmark Setup

*   **Dataset:** 1,000,000 randomly generated points.
*   **Query:** Spatial intersection with a bounding box (`shapely.box(-10, -10, 10, 10)`).
*   **Tools:** `geopandas` (for reading and querying), `duckdb` (for database querying).

## Benchmark Results

| Method                   | File Format  | Time (seconds) | Points Found |
| :----------------------- | :----------- | :------------- | :----------- |
| **Geopandas alone**      | Shapefile    | 1.0082         | 6210         |
| **Geopandas alone**      | GeoParquet   | 2.3249         | 6210         |
| **With DuckDB**          | Shapefile    | 2.0064         | 6210         |
| **With DuckDB**          | GeoParquet   | 0.1547         | 6210         |

## Analysis and Comments

1.  **DuckDB + GeoParquet: The Undisputed Winner**
    *   The combination of DuckDB querying a GeoParquet file yielded significantly faster results (0.15 seconds) compared to all other methods. This performance is attributed to DuckDB's in-memory analytical capabilities and its optimized handling of the columnar Parquet format, which allows it to efficiently filter and process only the necessary data.

2.  **Geopandas Direct Reads: Shapefile Outperforms GeoParquet**
    *   Surprisingly, when using `geopandas` directly without DuckDB, querying the Shapefile (1.01 seconds) was faster than querying the GeoParquet file (2.32 seconds). This outcome might be due to several factors:
        *   **Historical Optimization:** `geopandas` (and its underlying libraries like `fiona` and `pyogrio`) has a long history of optimization for the Shapefile format.
        *   **Query Specificity:** For a spatial intersection across the entire dataset, the overhead of reading and processing the full GeoParquet file into memory with `geopandas` might be higher than that of a Shapefile, depending on the specific implementation details and indexing. GeoParquet's benefits often shine with more complex queries involving many columns or large portions of data that can be filtered at the storage level.

3.  **DuckDB with Shapefiles: Slower than Geopandas Direct**
    *   DuckDB's performance with Shapefiles (2.01 seconds) was slower than `geopandas` reading Shapefiles directly. This suggests that while DuckDB can handle Shapefiles via its spatial extension, there's likely an overhead associated with converting the Shapefile data into DuckDB's internal processing format, making it less efficient than `geopandas`' native handling for this particular task.

## Conclusion

For high-performance geospatial analytical queries on large datasets, especially when filtering or aggregating data, **GeoParquet combined with DuckDB is the most efficient solution**. It leverages the strengths of both a modern columnar storage format and a fast, in-process analytical database.

While Shapefiles remain a widely used format, and `geopandas` provides excellent performance for them, relying solely on `geopandas` for GeoParquet files might not always yield the best performance for certain types of spatial queries, particularly when compared to a dedicated database engine like DuckDB. The choice of format and tool should align with the specific analytical needs and scale of the data.
