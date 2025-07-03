from database import init_database, users, get_user_by_name, save_event_for_user, get_saved_events, add_user, get_coordinates
import ticketpy
from dotenv import load_dotenv
from datetime import datetime
from send_email import send_email

import time
import os

load_dotenv()
api_key = os.getenv("API_KEY")
ticketclient = ticketpy.ApiClient(api_key)


def format_date_for_tmAPI(date_as_str):
    date = datetime.strptime(date_as_str, "%Y-%m-%d")
    start_utc = date.replace(hour=0, minute=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_utc = date.replace(hour=23, minute=59).strftime("%Y-%m-%dT%H:%M:%SZ")
    return start_utc, end_utc


def fetch_events_for_user(engine, username, date_for_event, send_email_flag=False, user_email=None):
	user = get_user_by_name(engine, username)
	email_results=""
	# if you cant find the username print out you cant find it and return
	if not user:
		print("Can't find this Username.")
		return

	start_utc, end_utc = format_date_for_tmAPI(date_for_event)

	pages = ticketclient.events.find(
		# took out the classification parameter b/c we want all events not a certain type
		latlong=user['loc'],
		radius="25",
		start_date_time=start_utc,
		end_date_time=end_utc
	)
	for page in pages:
		for event in page:
			venue = event.venues[0] if event.venues else "can't find the venue..."
			if not venue:
				continue
			email_results += f"Tickets for {event.name} are {event.status}\nLocation for this event is: {venue}\n"
			print("Tickets for " + event.name + " are", event.status)
			print("Event starts at: ", event.local_start_time)
			print("Location for this event is at: " + str(venue))
			print("Event ID: ", event.id)

			save_choice = input("Save this Event? (y/n): ").strip().lower()
			if save_choice == 'y':
				successful = save_event_for_user(engine, user['id'], event.id)
				if successful:
					print("your Event was Saved.")
				else:
					print("Event has already been saved.")
			elif save_choice == 'n':
				pass
			else:
				return

			time.sleep(0.3)

			if send_email_flag and user_email and email_results:
				send_email(user_email, email_results)
				print("Your email was sent. you better not forget...")


def fetch_events_and_send_email(engine, username, date_for_event, send_email_flag=False, user_email=None):
	user = get_user_by_name(engine, username)
	# if you cant find the username print out you cant find it and return
	if not user:
		print("Can't find this Username.")
		return

	start_utc, end_utc = format_date_for_tmAPI(date_for_event)

	pages = ticketclient.events.find(
		latlong = user['loc'],
		radius = "25",
		start_date_time = start_utc,
		end_date_time = end_utc
	)
	results = ""
	for page in pages:
		for event in page:
			venue = event.venues[0] if event.venues else "can't find the venue..."
			if not venue:
				continue
			results += f"Tickets for {event.name} are {event.status}\nLocation for this event is: {venue}\n"
		if results:
			send_email(user_email, results)
			print("Email sent, go check it out!")
		else:
			print("no events found for that date...")


def show_saved_events(engine, username):
	user = get_user_by_name(engine, username)
	if not user:
		print("can't find your username")
		return

	saved_events_id = get_saved_events(engine, user['id'])
	if not saved_events_id:
		print("you have no saved events")
		return
	
	print("Here are the saved events " + username)

	for event_id in saved_events_id:
		event = ticketclient.events.by_id(event_id)
		venue = event.venues[0] if event.venues else "can't find the venue..."
		print("Tickets for " + event.name + " are", event.status)
		print("Event starts at: ", event.local_start_time)
		print("Location for this event is at: " + str(venue))
