# Gemini Project: geoparquet

## Project Overview

This is a Python project named "geoparquet". Based on the name, it might be intended to work with geospatial data and the Parquet file format. The main entry point is `main.py`, which currently imports the `duckdb` library to execute a simple SQL query.

## Building and Running

This project uses `uv` as a package manager.

**Dependencies:**

The project currently has no explicitly declared dependencies in `pyproject.toml`. However, `main.py` imports `duckdb`. To run the project, you will likely need to install this dependency.

**Running the project:**

1.  **Install dependencies:**
    ```bash
    uv pip install duckdb
    ```

2.  **Run the main script:**
    ```bash
    python main.py
    ```

**TODO:** The `duckdb` dependency should be added to the `pyproject.toml` file.

## Development Conventions

*   The project uses `uv` for package management.
*   The main application logic is in `main.py`.
