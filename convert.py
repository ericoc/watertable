#!/usr/bin/env python3.13
import json
import logging
from csv import DictReader
from datetime import date


# Logging.
logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S %Z %z",
    format="%(asctime)s [%(levelname)s] (%(process)d): %(message)s",
    handlers=(logging.StreamHandler(),),
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Read and parse new CSV file data into a dictionary.
new_days = {}
with open(file="ChartData.csv", mode="r", encoding="utf-8") as csv_fh:
    for csv_row in DictReader(csv_fh):
        date_parts = csv_row[" Time Interval"].strip().split('/')
        date_iso = f"{date_parts[2]}-{date_parts[0]}-{date_parts[1]}"
        water_date = date.fromisoformat(date_iso)
        new_days[water_date] = float(csv_row[" Consumption"].strip())
logger.info(f"CSV:\t{len(new_days)}")

# Read and parse existing JSON file data into a dictionary.
existing_days = {}
with open(file="water.json", mode="r", encoding="utf-8") as existing_fh:
    existing_usage = json.load(existing_fh)
    for existing_row in existing_usage:
        existing_date = date.fromisoformat(existing_row["date"])
        existing_days[existing_date] = existing_row["gallons"]
logger.info(f"Existing:\t{len(existing_days)}")

# Merge dictionaries of new CSV data with existing JSON data.
merged_days = new_days | existing_days
logger.info(f"Merged:\t{len(merged_days)}")

# Create a list of the merged data dictionaries.
merged_usage = []
for day, gallons in merged_days.items():
    merged_usage.append({
        "date": day.isoformat(),
        "gallons": gallons
    })

# Sort the list, by date, of all merged data.
merged_usage = sorted(merged_usage, key=lambda i: i["date"])
logger.info(f"Max:\t{merged_usage[-1]['date']}")
logger.info(f"Min:\t{merged_usage[0]['date']}")
with open(file="water.json", mode="w", encoding="utf-8") as merged_fh:
    json.dump(merged_usage, merged_fh, indent=4)
    merged_fh.write("\n")
