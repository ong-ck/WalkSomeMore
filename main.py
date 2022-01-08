#Library for the telegram bot
import telebot

#Libraries for processing of data from LTA
import json 
from urllib.parse import urlparse  
import httplib2 as http #External library 
from datetime import datetime

#other relevant libraries
from keep_alive import keep_alive
from config import environ #config stores all the environment variables
import time
from songs import songs
import pacing as pc

#Library for MongoDB database
from pymongo import MongoClient

#API variables
Telegram_API = environ['telegram']
LTA_API = environ['LTA']
MongoDB_API = environ['database']

#MongoDB database reference
cluster = MongoClient(MongoDB_API)
db = cluster["test"]
collection = db["test"]

#Keeps the bot alive
keep_alive()

#Variables
user = ""
bus_list = {}
height = 0

loc = True #True -> Runs calibation, False -> Runs walking speed calculation 

#For calibration of user pace
location_now = 'off'
user_location = {'start': {'lat':'', 'long':''}, 'end': {'lat':'', 'long':''}}
user_time = {'start': 0, 'end': 0}
curr_location = {'lat': '', 'long': ''}

#For bus arrival timings and distance from bus stop
busstop = '' #Variable to store the bus stop id if it is valid
busstop_location = {'lat':'', 'long':''}


bot = telebot.TeleBot(Telegram_API)
@bot.message_handler(commands=['start'])
def start(message):
  global bus_list
  bus_list = {}
  starting_message = 'Hello, this is the bus metronome bot. To request for a caliberation of your pace, please select /calibration.\n\nTo find out if you are able to make it in time for your bus, please input the bus stop ID.'
  global user
  user = message.chat.id
  bot.send_message(message.chat.id, starting_message)

#Differentiated response based on user input
def response_type(message):
  if message.text == '/calibration':
    global loc
    loc = False
    return calibration(message)
  elif len(message.text) == 5:
    try:
      int(message.text)
      return True
    except:
      error_message = 'This is not a valid bus stop'
      bot.send_message(message.chat.id, error_message)
      return start(message)
  else:
    error_message = 'This is not a valid input'
    bot.send_message(message.chat.id, error_message)
    return start(message)

#Suggested pace: returning time and pace needed to reach the busstop
@bot.message_handler(content_types=['location'], func= lambda run: loc)
def curr_loc(message):
  global loc
  loc = False
  curr_location['lat'] = message.location.latitude
  curr_location['long'] = message.location.longitude
  distance_to_busstop = pc.get_distance(curr_location['lat'], curr_location['long'], busstop_location['lat'], busstop_location['long'])
  
  
  #Calculating time to reach bus stop and comparing it with the pace of user
  #Telebot will respond accordingly if the pace needs to be faster
  user_timing = 0
  try:
    height = collection.find_one({"_id": user})['height']
  except:
    msg = "You have no pace data in the database, please calibrate first."
    bot.send_message(message.chat.id, msg)
    return start(message)
  step = height * 0.43
  total_steps = distance_to_busstop / step
  pace = collection.find_one({"_id": user})["pace"]
  user_timing = total_steps / pace
  reply = f'Time needed to the bus stop based on your normal walking speed: {int(user_timing)} mins\n\n'
  
  for i in bus_list:
    bus_list[i] = ((total_steps / (abs(bus_list[i]-0.5))) // 10) * 10
    instructions = 'You may walk at your normal pace\n'
    if pace < bus_list[i] <= 150:
      index = str(int(bus_list[i]))
      instructions = f'{songs[index]}\n'
    elif bus_list[i] > 150:
      instructions = 'We recommend that you take the next bus\n'
    bus_list[i] = instructions
    reply += f'To make it for {i}: {bus_list[i]}\n'
  reply += '\nTo make a new request, select /start'
  bot.reply_to(message, reply)
  

#Calibration: getting user location and differentiating the 2 times the location is shared
@bot.message_handler(content_types=['location'], func= lambda run: not loc)
def location(message):
  global location_now
  if location_now == 'off':
    location_now = 'on'
  else:
    location_now = 'off'
  if location_now == 'on':
    return begin_calibration(message)
  return end_calibration(message)

def calibration(message):
  calibration_message = 'To start caliberation, please share your current location. The timer starts when the location has been shared.'
  bot.send_message(message.chat.id, calibration_message)

def begin_calibration(message):
  collection.delete_one({"_id": user})
  user_time['start'] = time.time()
  user_location['start']['lat'] = message.location.latitude
  user_location['start']['long'] = message.location.longitude
  instructions = 'Find an open space and start walking in a straight line for 30s.'
  bot.send_message(message.chat.id, instructions)
  time.sleep(30)
  end_instructions = '30s is up. To end calibration, please share your current location again'
  bot.send_message(message.chat.id, end_instructions)

def end_calibration(message):
  global loc
  loc = True
  user_time['end'] = time.time()
  user_location['end']['lat'] = message.location.latitude
  user_location['end']['long'] = message.location.longitude
  end = "Please input your height in cm"
  bot.send_message(message.chat.id, end)


@bot.message_handler(regexp="^[0-9]{3}$")
def get_height(message):
  global height
  height = float(int(message.text) / 100)
  end_msg = 'Your pace has been uploaded, please select /start'
  bot.send_message(message.chat.id, end_msg)
  distance = pc.get_distance(user_location['start']['lat'], user_location['start']['long'], user_location['end']['lat'], user_location['end']['long'])
  steps = pc.num_of_steps(height, distance)
  pace = pc.get_pace(steps, user_time)
  post = {"_id": message.chat.id, "pace": pace, 'height': height}
  collection.insert_one(post)
  
#Getting suggested pace
@bot.message_handler(func=response_type)
def bus(message): #Takes data from LTA and formats it 
  busstop = message.text
  if __name__=="__main__":

    #Authentication parameters     
    headers = { 'AccountKey' : LTA_API, 'accept' : 'application/json'}           
    
    #API parameters     
    uri = 'http://datamall2.mytransport.sg/' #Resource URL     
    path = 'ltaodataservice/BusArrivalv2?BusStopCode='      
    BusStop = busstop    
    url = path + BusStop

    #Build query string & specify type of API call  
    target = urlparse(uri + url)      
    method = 'GET'     
    body = ''         
    
    #Get handle to http     
    h = http.Http()
     
    #Obtain results     
    response, content = h.request(target.geturl(), method, body, headers)      
    
    #Parse JSON to print (ie converting string to JSON)     
    content = json.loads(content)

    #Extract arrival date and timing of buses and storing it in a dictionary
    buses = {}
    for i in content['Services']:
        buses[f"Bus Service {i['ServiceNo']}"] = i['NextBus']['EstimatedArrival']
        
    #Accounting for no buses
    def Nil_bus(message, reply):
      bot.reply_to(message, reply)
    
    if buses == {}:
      reply = 'Oops, there are no buses available at the moment'
      return Nil_bus(message, reply)

    #Further formating data on date and arrival timings of buses
    for i in buses:
        buses[i] = buses[i].split('T')
        dnt = {'date': buses[i][0], 'time':buses[i][1][:8]}
        buses[i] = dnt

    #Getting current time and date and storing it as strings
    FMT = '%H:%M:%S'
    DMT = '%m/%d/%Y'
    date, time_now = datetime.now().strftime(DMT), datetime.now().strftime(FMT)
    #Accounting for hours that are more than 1600 since its +0800 FMT
    hour = int(time_now[:2]) + 8
    if hour >= 24:
      hour -= 24
    time_now = f'{hour}{time_now[2:9]}'
    #Accounting for hours that are < 10
    if len(time_now) != 8:
      time_now = f'0{hour}:{time_now[2:9]}'
    date = date.split('/')
    date_now = f'{date[2]}-{date[0]}-{date[1]}'
    
    #Changing data from a dictionary to a string
    reply = ''
    for i in buses:
        #t1 is the arrival timing, t2 is the current time
        t1 = int(buses[i]['time'][:2])*3600 + int(buses[i]['time'][3:5])*60 + int(buses[i]['time'][7:9])
        if buses[i]['date'] == date_now:
            t2 = int(time_now[:2])*3600 + int(time_now[3:5])*60 + int(time_now[7:9])
        else:
            t2 = int(time_now[:2])*3600 + int(time_now[3:5])*60 + int(time_now[7:9])
        diff = (t1 - t2)//60
        response = f'{i} : Arriving\n'
        if diff > 0:
          response = f'{i} : {diff}\n'
        reply += response
        bus_list[i] = diff

    #Getting location of bus stops
    #API parameters          
    path = 'ltaodataservice/BusStops' 
    url = path

    #Build query string & specify type of API call  
    target = urlparse(uri + url)      
    method = 'GET'     
    body = ''         
    
    #Get handle to http     
    h = http.Http()
     
    #Obtain results     
    response, content = h.request(target.geturl(), method, body, headers)
    
    #Parse JSON to print (ie converting string to JSON)   
    content = json.loads(content)

    #Requesting data from LTA until bus stop is inside the dataset
    skip_count = 0
    while int(content['value'][len(content['value'])-1]['BusStopCode']) < int(busstop):
        #Edit url
        skip_count += 500
        skip_url = f'?$skip={skip_count}'
        url = path + skip_url
        #Get data from LTA
        target = urlparse(uri + url) 
        response, content = h.request(target.geturl(), method, body, headers) 
        #Parse JSON to print (ie converting string to JSON)     
        content = json.loads(content)
    
    for i in content['value']:
      if i['BusStopCode'] == busstop:
        busstop_location['lat'] =  i['Latitude']
        busstop_location['long'] =  i['Longitude']
      
    reply += '\nPlease share your current location'
    
    bot.reply_to(message, reply)

    global loc  
    loc = True

bot.polling()