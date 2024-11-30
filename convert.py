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

water_days = {}
try:
    with open(file="ChartData.csv", mode="r", encoding="utf-8") as csv_fh:
        for row in DictReader(csv_fh):
            assert row[" Units"] == " Gallons", "Invalid Units!"
            date_parts = row[" Time Interval"].strip().split('/')
            date_iso = f"{date_parts[2]}-{date_parts[0]}-{date_parts[1]}"
            water_date = date.fromisoformat(date_iso)
            water_days[water_date] = float(row[" Consumption"].strip())
except AssertionError as assert_err:
    logging.exception(msg=f"Invalid row: {row}", exc_info=assert_err)
logger.info(f"CSV: {len(water_days)}")

existing_days = {}
with open(file="water.json", mode="r", encoding="utf-8") as existing_fh:
    existing_usage = json.load(existing_fh)
    for existing_row in existing_usage:
        existing_date = date.fromisoformat(existing_row["date"])
        existing_days[existing_date] = existing_row["gallons"]
logger.info(f"Existing JSON: {len(existing_days)}")

merged_days = water_days | existing_days
logger.info(f"Merged: {len(merged_days)}")

latest_usage = []
for day, gallons in merged_days.items():
    latest_usage.append(
        {
            "date": day.isoformat(),
            "gallons": gallons
        }
    )

latest_usage = sorted(latest_usage, key=lambda i: i["date"], reverse=True)
with open(file="water.json", mode="w", encoding="utf-8") as combined_fh:
    json.dump(latest_usage, combined_fh, indent=4)
    combined_fh.write("\n")
