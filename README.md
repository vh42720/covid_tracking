# Covid-19 tracking with Voice Assistance.

### Introduction

This program is a short voice assistance that keeps track of current  
coronavirus cases and deaths worldwide. It can also return cases/deaths  
for specific country and update the data when asked.

### Data

The data is from [Worldometer](https://www.worldometers.info/coronavirus/)
and scraped through [parsehub](https://www.parsehub.com/)

### Commands

As long as the sentences include these words, the results will be returned
accordingly.
The list of keywords is as followed:
1. total cases/deaths: return total cases/death worldwide.
2. country cases/deaths: return specific cases/death for that country.
3. update: update the data - please wait while it is updating.
4. stop: stop the program.

### Installation

Install the requirements from requirement.txt. Pyaudio need to be downloaded
and install manually and not through Pip. Link is below.
Create the config folder with a config.py file. Inside this config.py,
includes these:
API_KEY = {your api key as string}
PROJECT_TOKEN = {your project token as string}

Run the script inside IDE/command prompt.

### Reference

[Tech with Tim](https://www.youtube.com/watch?v=gJY8D468Jv0)

[Pyaudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

