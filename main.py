import geopandas
import shapely
import duckdb
import os
import time
import numpy as np

def create_datasets(num_points=1_000_000):
    """
    Creates a large dataset of random points and saves it as both
    a GeoParquet file and a Shapefile.
    """
    print(f"--- Creating a dataset with {num_points} points ---")
    # Create a GeoDataFrame with random points
    longitudes = np.random.uniform(-180, 180, num_points)
    latitudes = np.random.uniform(-90, 90, num_points)
    geometry = [shapely.Point(lon, lat) for lon, lat in zip(longitudes, latitudes)]
    gdf = geopandas.GeoDataFrame(geometry=geometry, crs="EPSG:4326")
    gdf["id"] = range(num_points)


    # Save to GeoParquet and Shapefile
    if not os.path.exists("data"):
        os.makedirs("data")
    print("Saving to GeoParquet...")
    gdf.to_parquet("data/points.parquet")
    print("Saving to Shapefile...")
    gdf.to_file("data/points.shp")
    print("--- Datasets created ---")

def benchmark_queries():
    """
    Benchmarks spatial queries on GeoParquet and Shapefiles,
    with and without DuckDB.
    """
    print("\n--- Benchmarking Queries ---")
    bounding_box = shapely.box(-10, -10, 10, 10)

    # --- 1. Geopandas alone ---
    print("\n-- Geopandas without DuckDB --")

    # Shapefile
    start_time = time.time()
    gdf_shp = geopandas.read_file("data/points.shp")
    result_shp = gdf_shp[gdf_shp.intersects(bounding_box)]
    end_time = time.time()
    print(f"Shapefile with Geopandas: {end_time - start_time:.4f} seconds, found {len(result_shp)} points.")

    # GeoParquet
    start_time = time.time()
    gdf_parquet = geopandas.read_parquet("data/points.parquet")
    result_parquet = gdf_parquet[gdf_parquet.intersects(bounding_box)]
    end_time = time.time()
    print(f"GeoParquet with Geopandas: {end_time - start_time:.4f} seconds, found {len(result_parquet)} points.")

    # --- 2. With DuckDB ---
    print("\n-- With DuckDB --")
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")

    # Shapefile with DuckDB
    query_shp = """
    SELECT COUNT(*)
    FROM ST_Read('data/points.shp')
    WHERE ST_Intersects(geom, ST_MakeEnvelope(-10, -10, 10, 10));
    """
    start_time = time.time()
    result_duck_shp = con.execute(query_shp).fetchone()[0]
    end_time = time.time()
    print(f"Shapefile with DuckDB: {end_time - start_time:.4f} seconds, found {result_duck_shp} points.")

    # GeoParquet with DuckDB
    query_parquet = """
    SELECT COUNT(*)
    FROM 'data/points.parquet'
    WHERE ST_Intersects(geometry, ST_MakeEnvelope(-10, -10, 10, 10));
    """
    start_time = time.time()
    result_duck_parquet = con.execute(query_parquet).fetchone()[0]
    end_time = time.time()
    print(f"GeoParquet with DuckDB: {end_time - start_time:.4f} seconds, found {result_duck_parquet} points.")

    con.close()

def main():
    """
    Main function to run the benchmark.
    """
    create_datasets()
    benchmark_queries()


if __name__ == "__main__":
    main()
