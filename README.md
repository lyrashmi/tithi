# Tithi Pravesha Calendar Generator

This Python script calculates the exact times of **Tithi Pravesha** for multiple individuals based on their birth details. It processes the data from a CSV file for a specified year and exports all calculated events into a single `.ics` calendar file, which can be easily imported into Google Calendar, Apple Calendar, Outlook, etc.

## ✨ Features

- Calculate Tithi Pravesha for multiple people simultaneously.
- Accurate calculations using the `skyfield` library.
- Handles different timezones accurately using IANA timezone data.
- Generates a standard `.ics` file for seamless calendar integration.

## 📋 Prerequisites

Make sure you have Python 3.7+ installed on your system.

### Install Dependencies

Install the required Python packages using pip:

```bash
pip install skyfield icalendar pytz
```

## 📂 CSV Input Format

Create a CSV file (e.g., `birth_details.csv`) with the following exact column headers. 

| Column | Description | Format / Example |
| :--- | :--- | :--- |
| `Name` | Full name of the individual | `John Doe` |
| `Birth_Day` | Day of birth (1-31) | `15` |
| `Birth_Month` | Month of birth (1-12) | `8` |
| `Birth_Year` | Year of birth | `1990` |
| `Birth_Time` | Time of birth in 24-hour format | `14:14` |
| `Timezone` | IANA timezone of the birth place | `America/New_York` |

## 🚀 Usage

1. Ensure your CSV file is ready and formatted correctly as shown above.
2. Run the script from your terminal. 

```bash
python tithi_pravesha.py --csv birth_details.csv --year 2026
```

*(Note: If the script does not use command-line arguments, simply update the `CSV_FILE` and `TARGET_YEAR` variables at the top of the Python script and run `python tithi_pravesha.py`)*.

## 📅 Output

The script will generate an `.ics` file (e.g., `tithi_pravesha_2026.ics`) in the same directory. 

## 🛠️ Troubleshooting

- **Invalid Timezone Error:** Ensure the `Timezone` column uses the exact IANA format (e.g., `Asia/Kolkata`, `America/Los_Angeles`). You can find a full list of valid timezones [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
- **Time Format Error:** Ensure `Birth_Time` is strictly in `HH:MM` 24-hour format (e.g., `09:05`, `14:14`). Do not use AM/PM.
