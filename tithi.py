import csv
import pytz
from datetime import datetime, timedelta
from skyfield.api import load
from icalendar import Calendar, Event

# Load pure Python planetary data
ts = load.timescale()
planets = load('de421.bsp')
earth, sun, moon = planets['earth'], planets['sun'], planets['moon']

def get_sun_moon_angle(t):
    """Calculates the exact angular distance between Sun and Moon."""
    e = earth.at(t)
    s = e.observe(sun).apparent()
    m = e.observe(moon).apparent()
    
    # Use built-in ecliptic method instead of framelib
    _, slon, _ = s.ecliptic_latlon()
    _, mlon, _ = m.ecliptic_latlon()
    
    angle = (mlon.degrees - slon.degrees) % 360.0
    return angle, slon.degrees

def get_lahiri_ayanamsa(year):
    """Mathematical approximation of Lahiri Ayanamsa for the given year."""
    return 24.2747 + (year - 2000) * (50.290966 / 3600.0)

def main():
    target_year = datetime.now().year
    
    cal = Calendar()
    cal.add('prodid', '-//Community Tithi Pravesha Calendar//')
    cal.add('version', '2.0')
    
    with open('Kula_Tithi_Pravesha.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            name = row['Name']
            b_day = int(row['Birth_Day'])
            b_month = int(row['Birth_Month'])
            b_year = int(row['Birth_Year'])
            b_hour, b_minute = map(int, row['Birth_Time'].split(':'))
            timezone = row['Timezone']
            
            # 1. Convert local birth time to UTC
            local_tz = pytz.timezone(timezone)
            dt_local = local_tz.localize(datetime(b_year, b_month, b_day, b_hour, b_minute))
            dt_utc = dt_local.astimezone(pytz.utc)
            
            # 2. Find Natal Angles
            t_birth = ts.from_datetime(dt_utc)
            natal_angle, natal_sun_trop = get_sun_moon_angle(t_birth)
            natal_sun_sidereal = (natal_sun_trop - get_lahiri_ayanamsa(b_year)) % 360.0
            
            # 3. Scan the target year for the return
            start_dt = datetime(target_year, 1, 1, tzinfo=pytz.utc)
            best_date = None
            smallest_diff = 360.0
            
            # Step through the year to find the convergence
            for day in range(365):
                current_dt = start_dt + timedelta(days=day, hours=12) # Check daily at noon
                t_current = ts.from_datetime(current_dt)
                
                curr_angle, curr_sun_trop = get_sun_moon_angle(t_current)
                curr_sun_sidereal = (curr_sun_trop - get_lahiri_ayanamsa(target_year)) % 360.0
                
                # Check if Sun is in the same Vedic sign (within 15 degrees of birth position)
                sun_diff = abs(curr_sun_sidereal - natal_sun_sidereal)
                if sun_diff > 15.0 and sun_diff < 345.0:
                    continue
                    
                # Find how close the Moon is to the natal angle
                angle_diff = abs(curr_angle - natal_angle)
                if angle_diff > 180.0:
                    angle_diff = 360.0 - angle_diff
                    
                if angle_diff < smallest_diff:
                    smallest_diff = angle_diff
                    best_date = current_dt
            
            # 4. Add to Calendar
            if best_date:
                event = Event()
                event.add('summary', f"{name}'s Tithi Pravesha")
                event.add('dtstart', best_date.date())
                event.add('description', f"Automated Skyfield Calculation for {name}.")
                cal.add_component(event)
                
    with open('Tithi_Birthdays.ics', 'wb') as my_file:
        my_file.write(cal.to_ical())
        
    print(f"Success. Tithi_Birthdays.ics has been generated for the year {target_year}.")

if __name__ == "__main__":
    main()