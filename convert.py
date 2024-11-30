#!/usr/bin/env python3.13
import json
import logging
from csv import DictReader
from datetime import date


logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S %Z %z",
    format="%(asctime)s [%(levelname)s] (%(process)d): %(message)s",
    handlers=(logging.StreamHandler(),),
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def parse_date(item: str) -> date:
    date_parts = item.strip().split('/')
    date_iso = f"{date_parts[2]}-{date_parts[0]}-{date_parts[1]}"
    return date.fromisoformat(date_iso)

water_usage = []
try:
    with open(file="ChartData.csv", mode="r") as csv_fh:
        reader = DictReader(csv_fh)
        for row in reader:
            assert row[" Units"] == " Gallons", "Invalid Units!"
            water_usage.append(
                {
                    "date": parse_date(row[" Time Interval"]).isoformat(),
                    "gallons": float(row[" Consumption"].strip())
                }
            )

except AssertionError as assert_err:
    logging.exception(msg=f"Invalid row: {row}", exc_info=assert_err)

with open(file="water.json", mode="w") as json_fh:
    json.dump(water_usage, json_fh)
    logger.info("OK!")
