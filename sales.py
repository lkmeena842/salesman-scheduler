import csv
import os
from geopy.geocoders import Nominatim
from haversine import haversine, Unit
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import itertools


# Reading address dataset file path
file_path = r"C:\Users\lksar\OneDrive\Desktop\Salesman Project\smp_address_dataset.csv"

SCOPES = ['https://www.googleapis.com/auth/calendar']
 

# Function to read customers data from CSV
def read_customers_data(file_path):
    customers = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            customers.append({
                'name': row['name'],
                'address': row['address'],
                'zipcode': row['zip']
            })
    return customers


# Function to convert address into coordinates
def geocode_address(address):
    geolocator = Nominatim(user_agent="salesman_scheduler")
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return (location.latitude, location.longitude)
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error: {e}")
    return None


# Function to calculate Distance between two addresses
def calculate_distance(coord1, coord2):
    return haversine(coord1, coord2, unit=Unit.KILOMETERS)


# Function to find the optimal route using TSP (brute-force approach for simplicity)
def tsp_brute_force(customers_with_coords):
    if not customers_with_coords:
        return []

    start = customers_with_coords[0]
    others = customers_with_coords[1:]

    shortest_route = None
    min_distance = float('inf')

    for perm in itertools.permutations(others):
        route = [start] + list(perm)
        distance = sum(calculate_distance(route[i]['coords'], route[i+1]['coords']) for i in range(len(route) - 1))
        
        if distance < min_distance:
            min_distance = distance
            shortest_route = route

    return shortest_route


# Function to create Google Calendar events
def create_google_calendar_event(service, customer, start_time, end_time):
    event = {
        'summary': f'Meeting with {customer["name"]}',
        'location': f'{customer["address"]}, {customer["zipcode"]}',
        'description': 'Sales meeting',
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Kolkata',
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')


def main(file_path):
    customers = read_customers_data(file_path)

    for customer in customers:
        address = f"{customer['address']}, {customer['zipcode']}"
        coords = geocode_address(address)
        
        if coords:
            customer['coords'] = coords
        else:
            print(f"Can't find geocode address for {customer['name']}")
            customer['coords'] = None

    customers_with_coords = [customer for customer in customers if customer['coords']]
    optimized_customers = tsp_brute_force(customers_with_coords)

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    start_time = datetime.datetime(2024, 7, 13, 10, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
    duration = 1  # Take each meeting  1hours

    for customer in optimized_customers:
        end_time = start_time + datetime.timedelta(hours=duration)
        create_google_calendar_event(service, customer, start_time.isoformat(), end_time.isoformat())
        start_time = end_time

if __name__ == '__main__':
    main(file_path)
