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

# File names.
FILENAMES = {"csv": "ChartData.csv", "json": "water.json"}
logger.debug("Files:\t%s" % FILENAMES)

# Create dictionary from (new) CSV data.
new = {}
with open(file=FILENAMES["csv"], mode="r", encoding="utf-8") as csv_fh:
    for csv_row in DictReader(csv_fh):
        assert csv_row[" Units"] == " Gallons", "Invalid unit."
        date_parts = csv_row[" Time Interval"].strip().split('/')
        date_iso = f"{date_parts[2]}-{date_parts[0]}-{date_parts[1]}"
        water_date = date.fromisoformat(date_iso)
        new[water_date] = float(csv_row[" Consumption"].strip())
    logger.info("New CSV:\t%i (%s)" % (len(new), FILENAMES["csv"]))

# Create dictionary from (existing) JSON data.
existing = {}
with open(file=FILENAMES["json"], mode="r", encoding="utf-8") as existing_fh:
    existing_usage = json.load(existing_fh)
    for existing_row in existing_usage:
        existing_date = date.fromisoformat(existing_row["date"])
        existing[existing_date] = existing_row["gallons"]
    logger.info("Existing:\t%i (%s)" % (len(existing), FILENAMES["json"]))

# Merge dictionaries of new and existing data.
merged = new | existing

# Create, and sort, a list of the merged data dictionaries.
usage = []
for day, gallons in merged.items():
    usage.append({"date": day.isoformat(), "gallons": gallons})
usage = sorted(usage, key=lambda i: i["date"])

# Display minimum and maximum dates from the merged list.
dt_fmt = "%A, %B %d, %Y"
min_date = date.fromisoformat(usage[0]["date"])
logger.info('Minimum:\t%s (%s)' % (min_date.strftime(dt_fmt), min_date))
max_date = date.fromisoformat(usage[-1]["date"])
logger.info('Maximum:\t%s (%s)' % (max_date.strftime(dt_fmt), max_date))

# Write the list of merged data to existing JSON file.
with open(file=FILENAMES["json"], mode="w", encoding="utf-8") as merged_fh:
    json.dump(usage, merged_fh, indent=4)
    merged_fh.write("\n")
    logger.info("Done:\t%i (%s)" % (len(usage), FILENAMES["json"]))
