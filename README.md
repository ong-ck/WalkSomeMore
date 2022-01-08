<div id="top"></div>

<br />
<div align="center">

<h3 align="center">Walk Some More</h3>

  <p align="center">
    Missed the bus again? Here's the solution for you! Walk Some More is a telegram bot that provides feedback on whether you can catch your bus on time based on your own personalised pace! It lets you know how much faster you should be walking, and even provides a song link with a tempo that matches the speed that you will need to walk at to reach on time.
    <br />
    <a href="https://github.com/ong-ck/WalkSomeMore"><strong>Explore the docs »</strong></a>

</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li>
      <a href="#roadmap">Roadmap</a>
      <ul>
        <li><a href="#new-features">New Features</a></li>
        <li><a href="#user-experience">User Experience</a>
        <li><a href="#accuracy">Accuracy</a>
      </ul>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
<div id = "about-the-project"></div>

## About The Project

<div id = "built-with"></div>

### Built With

* [Python](https://www.python.org/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
<div id = "getting-started"></div>

## Getting Started

  Kindly follow the instructions below to get started.

<div id = "prerequisites"></div>

### Prerequisites

* pip
  ```sh
  pip install urllib3
  pip install httplib2
  pip install pymongo
  pip install pyTelegramBotAPI
  pip install os-sys
  pip install Flask
  pip install threaded
  pip install requests
  
  
  ```
<div id = "installation"></div>

### Installation

1. Get a free API Key from Telegram from BotFather
[https://core.telegram.org/bots](https://core.telegram.org/bots)


2. Get a free API Key from LTA DataMall at [https://datamall.lta.gov.sg/content/datamall/en.html](https://datamall.lta.gov.sg/content/datamall/en.html)


3. Get a paid API Key from Google Maps Plaform
[https://mapsplatform.google.com/maps-products/](https://mapsplatform.google.com/maps-products/)

4. Create a free account from MongoDB [https://www.mongodb.com/](https://www.mongodb.com/)


5. Clone the repo
   ```sh
   git clone 
   https://github.com/ong-ck/WalkSomeMore.git
   ```
   
6. Enter your API key for each of the APIs above in `config.py`

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
<div id = "usage"></div>

## Usage

  1. Type /start to start the bot.
  
  2. If you are a new user, calibrate your pace into the database
  by using /calibration. Otherwise skip to Step 7.

  3. Share your location on Telegram via Google.

  4. After 30 seconds, upon prompting from the bot, share the final location on Telegram via Google to finish calibration.

  5. Input your height in cm.
  
  6. Your pace will then be calculated and uploaded into the database.

  7. Input the bus stop ID. If the bus stop ID is not valid, the bot will prompt again for a new one. Otherwise, the bus timing will be shown.
     
  8. Upload current location on Telegram via Google.

  9. The bot will calculate the required pace to reach the bus stop, and play an appropriate song with the matching tempo for your required pace. Otherwise, it would advise you to take the next bus. 


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
<div id = "roadmap"></div>

## Roadmap

<div id = "new-features"></div>

### New Features
- [] Support the use of live sharing location from Telegram so that we can reflect the changes in pace needed when user stops walking, e.g. in situations like waiting to cross the road
- [] Implement a bus arrival timing updater to it accounts for bus delays/early arrival, so that we can adjust recommended pace for user in real time
- [] Support multiple users to use the Walk Some More Bot simultaneously
- [] Implement providing a screenshot of the walking path from user's current location to the bus stop
- [] Show user nearby bus stops based on their current location with bus stop code
- [] Integrate Current Rain Areas information from Weather.gov.sg to estimate delay in user walking pace and traffic, as well as suggesting indoor walking paths whenever possible
- [] Implement LTA DataMall API to show how full each bus is
- [] Implement a favourites section for users to store bus stop codes that they use frequently
- [] Implement a last bus function that informs user to run for the bus at all cost
- [] Implement simple games within Telegram for user to play when they arrive the bus stop early and after they board the bus
- [] Implement a feedback system which prompts user to give feedback on whether they managed to catch the bus in time, if yes, we will maintain the pace given to the user, else, we will provide them with reasons to choose from, such as red light, pace given was not fast enough, and adjust the database to provide a faster pace to this particular user in the future as they might not have followed their calibrated walking speed
- [] Automate the process of calibration such that they just have to type /start and the bot will take care of the rest

<div id = "user-experience"></div>

### User Experience
- [] Implement a metronome with background music that adjusts to plays sounds according to the pace required to reach bus stop on time, to replace the links to songs
- [] Create a larger library of songs/sounds used as the guide for the pace to let users have a choice between songs with the same bpm
- [] Find a suitable platform to host songs under creative commons license so that our users can play the songs ad-free for non-premium users for spotify and youtube
- [] Collaborate with National Steps Challenge to encourage people to walk more and use our bot to aid them, rather than taking private hire cars
- [] Create a theme like Bus Uncle and personify the messages sent to the user for better user experience
- [] Implement pedometer and calories counter to gamify the experience

<div id = "accuracy"></div>

### Accuracy
- [] Support the use of the user's accelerometer and pedometer so that we can get a more accurate and precise data of the user's actual pace for calibration and to get the user's current walking, which will provide a more personalised experience for the user
- [] Implement Geolocation API from Google Maps Platform to get a more accurate and precise location of the user

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
<div id = "acknowledgments"></div>

## Acknowledgments


* pyTelegramBotAPI library:
https://github.com/eternnoir/pyTelegramBotAPI
* Keep_alive function:
https://www.youtube.com/watch?v=tMH16T74fWE
* LTA DataMall API: https://datamall.lta.gov.sg/
* Google Maps Distance Matrix API: https://developers.google.com/maps/documentation/distance-matrix/overview


<p align="right">(<a href="#top">back to top</a>)</p>
