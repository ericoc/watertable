# 💧 Water Table 🚰

The [Philadelphia Water Department](https://water.phila.gov/) website allows
for water usage to be exported in "comma-separated values" (CSV) format.

### Export Philadelphia Water Department Water Usage

Water usage can be downloaded by "Gallons" used "Daily" from the
"[Detailed Usage](https://secure8.i-doxs.net/CityOfPhiladelphiaWRB/Secure/Usage.aspx)"
section of the Philadelphia Water Department (PWD) website.

![Export Philadelphia Water Department Detailed Usage Screenshot](export.png)

The default export file is named "`ChartData.csv`", containing data
such as the following:
```
Access Code, Time Interval, Consumption, Units
00145xxxx, 11/27/2024, 18.7013, Gallons
00145xxxx, 11/28/2024, 35.9065, Gallons
etc..
```
Only the second and third columns of this CSV file matter, since the first
column  seems to be associated to the PWD account, while the fourth column
row value should always be " ` Gallons`".

---
### Convert Water Usage CSV to JSON

The [`convert.py`](convert.py) script within this repository will convert the
downloaded "`ChartData.csv`" file into JSON and create a `water.json` file,
such as the following:
```
[
    {
        "date": "2024-11-27",
        "gallons": 18.7013
    },
    {
        "date": "2024-11-28",
        "gallons": 35.9065
    },
    {
        etc...
    },
]
```
---
### Using JSON

Once the water usage data (again, in gallons) has been converted into JSON,
and the `water.json` file has been populated, DataTables and HighCharts should work.

#### DataTables
The main [`index.html`](index.html) page uses DataTables to display the water
usage from the `water.json` file.

#### HighCharts
[`highcharts/index.html`](highcharts/index.html) uses HighCharts to chart water
usage from the `water.json` file.

---

### Refreshing Data
Finally, downloading a fresh `ChartData.csv` file from the Philadelphia Water
Department website, and running `convert.py` will merge the data between the
existing `water.json` file and the new `ChartData.csv` file.

The merged data will be rewritten back to the `water.json` file.
This allows for simple, and continual, updates over time, without risk of
losing any historical data.

It appears that the Philadelphia Water Department website may only preserve approximately two (2)
years of historical water usage.

---

### Examples
- [DataTables](https://water.ericoc.com/)
- [HighCharts](https://water.ericoc.com/highcharts/)
