import duckdb

def main():
    print("Hello from geoparquet!")
    print(duckdb.sql("SELECT 'DuckDB is ready!'").fetchall())

if __name__ == "__main__":
    main()
