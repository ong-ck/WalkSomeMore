import json
import math
import requests
from config import environ

#API Variable
Maps_API = environ['maps']

def get_distance(lat_ori, long_ori, lat_dest, long_dest):

  url = f"https://maps.googleapis.com/maps/api/distancematrix/json?destinations={lat_ori}%2C{long_ori}&origins={lat_dest}%2C{long_dest}&mode=walking&key={Maps_API}"

  payload = {}
  headers = {}

  response = requests.request("GET", url, headers=headers, data=payload)

  res = json.loads(response.text)

  distance = res['rows'][0]['elements'][0]['distance']['value']

  return distance

def num_of_steps(height, distance):
  stride_length = height * 0.43
  steps = math.ceil(distance / stride_length)
  return steps

def get_pace(steps, user_time):
  time_taken = math.ceil((user_time['end'] - user_time['start']) / 60)
  pace = steps / time_taken
  return pace