import openai
import re
import datetime
import add_to_gcal as gcal

# Function to read the API key from a separate file
def read_api_key():
    try:
        with open('api_key.txt', 'r') as file:
            api_key = file.read().strip()
        return api_key
    except FileNotFoundError:
        print("API key file 'api_key.txt' not found.")
        return None

# Read the API key
api_key = read_api_key()

if api_key:
    # Function to format event text using OpenAI's GPT-3
    def format_event_text(input_text):
        openai.api_key = api_key


        # Prompt instructing GPT-3 to format the text with the formatted date
        prompt = f"Format the following event text in the format(time in 24 hour format) 'date (format: DD MMM) | start time (HH:MM) - end time (HH:MM) | Event Title | Event Description': '{input_text}'"

        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=50  # Adjust this value as needed
            )
            formatted_text = response.choices[0].text.strip()
            return formatted_text
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    # User input
    user_input = input("Enter event details or 'x' to use default: ")
    if user_input.lower() == 'x':
        user_input = '12th November, Auckland Rose Society Spring show/ Selwyn Library Hall. 10 St Stephens Ave Parnell. Plant Sales & Raffles. Entry Free. 11-3pm'


    formatted_text = format_event_text(user_input)

    if formatted_text:
        print(f"Formatted event text: '{formatted_text}'")
        # Create .ics file
        gcal.create_ics_file(formatted_text)
    else:
        print("Failed to format the input text.")
else:
    print("API key not found. Please make sure to create a 'api_key.txt' file with your OpenAI API key.")
