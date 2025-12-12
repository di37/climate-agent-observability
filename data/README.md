# Climate Agriculture Data - SQLite Database

## Overview

This directory contains climate change impact on agriculture data from 2024.

## Files

- `climate_change_impact_on_agriculture_2024.csv` - Original CSV dataset (10,000 records)
- `climate_agriculture.db` - SQLite database containing the ingested data

## Database Schema

The database contains a single table: `climate_agriculture_data`

### Table Columns

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| Year | INTEGER | Year of the record |
| Country | TEXT | Country name |
| Region | TEXT | Region within the country |
| Crop_Type | TEXT | Type of crop (Wheat, Rice, Corn, etc.) |
| Average_Temperature_C | REAL | Average temperature in Celsius |
| Total_Precipitation_mm | REAL | Total precipitation in millimeters |
| CO2_Emissions_MT | REAL | CO2 emissions in metric tons |
| Crop_Yield_MT_per_HA | REAL | Crop yield in metric tons per hectare |
| Extreme_Weather_Events | INTEGER | Number of extreme weather events |
| Irrigation_Access_% | REAL | Percentage of irrigation access |
| Pesticide_Use_KG_per_HA | REAL | Pesticide use in kg per hectare |
| Fertilizer_Use_KG_per_HA | REAL | Fertilizer use in kg per hectare |
| Soil_Health_Index | REAL | Soil health index value |
| Adaptation_Strategies | TEXT | Climate adaptation strategy used |
| Economic_Impact_Million_USD | REAL | Economic impact in million USD |

## Usage

### Python Example

```python
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('data/climate_agriculture.db')

# Query using pandas
df = pd.read_sql_query("SELECT * FROM climate_agriculture_data LIMIT 10", conn)
print(df)

# Query using raw SQL
cursor = conn.cursor()
cursor.execute("SELECT Country, AVG(Crop_Yield_MT_per_HA) FROM climate_agriculture_data GROUP BY Country")
results = cursor.fetchall()

conn.close()
```

### Command Line Example

```bash
# Open database with SQLite CLI
sqlite3 data/climate_agriculture.db

# Run queries
sqlite> SELECT COUNT(*) FROM climate_agriculture_data;
sqlite> SELECT DISTINCT Crop_Type FROM climate_agriculture_data;
sqlite> .exit
```

## Scripts

See parent directory for helper scripts:
- `ingest_data.py` - Script to ingest CSV into SQLite
- `query_database.py` - Example queries to demonstrate database usage

