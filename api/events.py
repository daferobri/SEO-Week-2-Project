#TicketMaster's API Logic Implemented here
import ticketpy
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import os
from send_email import send_email

load_dotenv()
api_key = os.getenv("API_KEY") #get api key from the env file
ticketclient = ticketpy.ApiClient(api_key) #fetch the api key to use the api

timezones = { #HashMap to quickly retrieve the timeZone of the user based off state code
    'AL': 'America/Chicago',
    'AK': 'America/Anchorage',
    'AZ': 'America/Phoenix',
    'AR': 'America/Chicago',
    'CA': 'America/Los_Angeles',
    'CO': 'America/Denver',
    'CT': 'America/New_York',
    'DE': 'America/New_York',
    'FL': 'America/New_York',
    'GA': 'America/New_York',
    'HI': 'Pacific/Honolulu',
    'ID': 'America/Boise',
    'IL': 'America/Chicago',
    'IN': 'America/Indiana/Indianapolis',
    'IA': 'America/Chicago',
    'KS': 'America/Chicago',
    'KY': 'America/New_York',
    'LA': 'America/Chicago',
    'ME': 'America/New_York',
    'MD': 'America/New_York',
    'MA': 'America/New_York',
    'MI': 'America/New_York',
    'MN': 'America/Chicago',
    'MS': 'America/Chicago',
    'MO': 'America/Chicago',
    'MT': 'America/Denver',
    'NE': 'America/Chicago',
    'NV': 'America/Los_Angeles',
    'NH': 'America/New_York',
    'NJ': 'America/New_York',
    'NM': 'America/Denver',
    'NY': 'America/New_York',
    'NC': 'America/New_York',
    'ND': 'America/Chicago',
    'OH': 'America/New_York',
    'OK': 'America/Chicago',
    'OR': 'America/Los_Angeles',
    'PA': 'America/New_York',
    'RI': 'America/New_York',
    'SC': 'America/New_York',
    'SD': 'America/Chicago',
    'TN': 'America/Chicago',
    'TX': 'America/Chicago',
    'UT': 'America/Denver',
    'VT': 'America/New_York',
    'VA': 'America/New_York',
    'WA': 'America/Los_Angeles',
    'WV': 'America/New_York',
    'WI': 'America/Chicago',
    'WY': 'America/Denver',
    'DC': 'America/New_York'
  }

def fetch_events(state_code, start_date, end_date):
  tz_string = timezones[state_code] #will return America/Phoenix for example
  #converts local time to UTC local time
  start_utc, end_utc = convert_local_date_to_UTC(start_date,end_date, tz_string)
  #find all the events
  pages = ticketclient.events.find(
    #took out the classification parameter b/c we want all events not a certain type
    state_code = state_code,
    start_date_time = start_utc,
    end_date_time = end_utc
  )
  #print the events found
  results = ""
  for page in pages:
    for event in page:
      #used the dir() method to see what methods 'event' has, i also looked at the docs for ticketpy
      results += f"Tickets for {event.name} are {event.status}\n Location for this event is: {event.venues[0]}\n"
  # print(repr(results))
  send_email("daferobri5941@gmail.com", results)

def convert_local_date_to_UTC(start_date,end_date, timezone_string):

  tz = ZoneInfo(timezone_string)
  #parse and localize the start date
  local_start_time = datetime.strptime(start_date, "%Y-%m-%d").replace(hour = 0, minute = 0, tzinfo = tz)
  #pase and localize the end date
  local_end_time = datetime.strptime(end_date, "%Y-%m-%d").replace(hour = 23, minute = 59, tzinfo = tz)

  utc_start = local_start_time.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")
  utc_end = local_end_time.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")

  return utc_start, utc_end

#testing code out
if __name__ == "__main__":
  state_code = "AZ"
  start_date = "2025-07-05"
  end_date = "2025-07-05"
  fetch_events(state_code, start_date, end_date)
