This script calculates multiple tithi pravesha's based on information from a CSV sheet for a given year and exports these as a single .ics calendar file.

To use you also need:
```
pip install skyfield icalendar pytz
```

CSV structure should look like this:
```
Name
```

```
Birth_Day
```

```
Birth_Month
```

```
Birth_Year
```

```
Birth_Time
```
(in 24h, four digit format; e.g. 14:14)

```
Timezone
```
(Timezone of birth in IANA format; e.g. America/New_York)
