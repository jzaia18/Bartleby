from typing import Tuple
import requests
import urllib.parse
import sys


def dbg(*args, **kwargs):
    if __name__ == '__main__':
        print(*args, **kwargs, file=sys.stderr)


def getLatLon(address: str) -> Tuple[float, float]:
    url = 'https://nominatim.openstreetmap.org/search/' + \
            urllib.parse.quote(address) +'?format=json'
    
    response = requests.get(url).json()
    
    if len(response) == 0:
        dbg(f"{response = }")
        return (43.157285, -77.615214)
    
    return (response[0]["lat"], response[0]["lon"])


def getWeatherPoint(lat: float, lon: float) -> Tuple[str, int, int]:
    url = f"https://api.weather.gov/points/{lat},{lon}"
    
    response = requests.get(url).json()
    
    if 'properties' not in response:
        dbg(f"{response}")
        return ("BUF", 76, 64)
    
    prop = response['properties']
    
    return (prop['gridId'], prop['gridX'], prop['gridY'])


def getForecast(gridId: str, gridX: int, gridY: int):
    url = f"https://api.weather.gov/gridpoints/{gridId}/{gridX},{gridY}/forecast"
    
    response = requests.get(url).json()
    
    if 'properties' not in response:
        dbg(f"{response}")
        return None
    
    dbg(f"{response['properties']['periods'][0]}")
    return response["properties"]["periods"][0]


def getDetails(forecastObj: dict) -> str:
    return forecastObj["detailedForecast"]

def getTemp(forecastObj: dict) -> int:
    return forecastObj['temperature']

def getPrecipChance(forecastObj: dict) -> int:
    return forecastObj['probabilityOfPrecipitation']['value'] or 0

def getWindSpeed(forecastObj: dict) -> float:
    if " to " in forecastObj['windSpeed']:
        start, end = forecastObj['windSpeed'].split(" to ")
    else:
        end = forecastObj['windSpeed']
        start = end[:-4]
    start = float(start)
    end = float(end[:-4])
    return (start + end) / 2

# full process
def forecastFromLocation(location: str):
    dbg(f"{(latLon := getLatLon(location)) = }")
    dbg(f"{(pt := getWeatherPoint(*latLon)) = }")
    dbg(f"{(forecast := getForecast(*pt)) = }")
    dbg(f"{(wind := getWindSpeed(forecast)) = }")
    return forecast
    

if __name__ == '__main__':
    while True:
        inputLoc = input()
        print(forecastFromLocation(inputLoc))