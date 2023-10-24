import re
import datetime
from ics import Calendar, Event
import pytz

# Function to extract date, time, and title from text
def extract_event_details(text):
    try:
        segments = text.split('|')
        if len(segments) >= 3:
            date_str = segments[0].strip()
            time_str = segments[1].strip()
            title = segments[2].strip()
            description = segments[3].strip()
            
            # Extract date
            date_pattern = r'(\d{1,2} [A-Za-z]+)'
            date_match = re.search(date_pattern, date_str)
            if date_match:
                date_str = re.sub(r'(st|nd|rd|th)', '', date_match.group())
                date = datetime.datetime.strptime(date_str, '%d %b')
                current_year = datetime.datetime.now().year
                date = date.replace(year=current_year)  # Use the current year
                print(f"Date after conversion: {date.strftime('%d %b')}")
            else:
                print("Failed to extract date from the input text.")
                return None, None, None
            
            # Extract time
            # time_pattern = r'(\d{1,2}:\d{2}[apAP][mM]\s*-\s*\d{1,2}:\d{2}[apAP][mM])'
            # time_match = re.search(time_pattern, time_str)
            time_match = re.search(r'(\d{1,2}:\d{2})\s+-\s+(\d{1,2}:\d{2})', time_str)
            if time_match:
                time_str = time_match.group().strip()
                print("time_str: ", time_str)
                time_parts = time_str.split("-")
                print("time_parts: ", time_parts)
                try:
                    start_time = datetime.datetime.strptime(time_parts[0].strip(), "%H:%M").time()
                    end_time = datetime.datetime.strptime(time_parts[1].strip(), "%H:%M").time()
                    print(f"Start Time after conversion: {start_time.strftime('%H:%M')}")
                    print(f"End Time after conversion: {end_time.strftime('%H:%M')}")
                except ValueError:
                    print("Time not found in the correct format.")
                    return None, None, None
            else:
                print("Failed to extract time from the input text.")
                return None, None, None

            print(f"Title: {title}")
            return date, start_time, end_time, title, description
        else:
            print("Input format is not valid. here ")
            return None, None, None
    except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Function to create an .ics file
def create_ics_file(event_details):
    date, start_time, end_time, title, desc = extract_event_details(event_details)

    if date and start_time and end_time and title:
        # Create an iCalendar event
        c = Calendar()
        e = Event()
        e.name = title
        e.description = desc  # Set description to the title
        tz = pytz.timezone('Pacific/Auckland')  # New Zealand timezone with DST handling
        e.begin = tz.localize(datetime.datetime.combine(date, start_time))
        e.end = tz.localize(datetime.datetime.combine(date, end_time))
        c.events.add(e)

        # Split the string into words
        words = title.split()

        # Select the first 4 words
        title_first_4_words = " ".join(words[:4])

        # Write the iCalendar event to a file with the title as the filename
        with open(f'{title_first_4_words}.ics', 'w') as file:
            file.writelines(c)

        print("Event details written to '{title}.ics' file.")
    else:
        print("Failed to extract event details from the input text.")

