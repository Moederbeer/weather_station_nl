import urllib.request
import json


class weatherStation:
    def __init__(self, id, stationId, stationName, lat, lon, region, timestamp,
                 weatherDescription, windDirection, temperature,
                 groundTemperature, feelTemperature, windGusts, windSpeed,
                 windSpeedBft, humidity, precipitation, sunPower,
                 rainFallLast24Hour, rainFallLastHour, windDirectionDegrees):
        self.id = id
        self.stationId = stationId
        self.stationName = stationName
        self.lat = lat
        self.lon = lon
        self.region = region
        self.timestamp = timestamp
        self.weatherDescription = weatherDescription
        self.windDirection = windDirection
        self.temperature = temperature
        self.groundTemperature = groundTemperature
        self.feelTemperature = feelTemperature
        self.windGusts = windGusts
        self.windSpeed = windSpeed
        self.windSpeedBft = windSpeedBft
        self.humidity = humidity
        self.precipitation = precipitation
        self.sunPower = sunPower
        self.rainFallLast24Hour = rainFallLast24Hour
        self.rainFallLastHour = rainFallLastHour
        self.windDirectionDegrees = windDirectionDegrees

    def getvaluefromkey(self, key):
        return self.__getattribute__(key)


def getweatherdata():
    # jsonraw = urllib.request.urlopen("https://data.buienradar.nl/2.0/feed/json")
    jsonraw = open('sample_json')
    weatherdata = json.load(jsonraw)["actual"]

    for station in weatherdata["stationmeasurements"]:
        stations.append(weatherStation(station.get("$id", "na"),
                                       station.get("stationid", "na"),
                                       station.get("stationname", "na"),
                                       station.get("lat", "na"),
                                       station.get("lon", "na"),
                                       station.get("regio", "na"),
                                       station.get("weatherdescription", "na"),
                                       station.get("timestamp", "na"),
                                       station.get("winddirection", "na"),
                                       station.get("temperature", "na"),
                                       station.get("groundtemperature", "na"),
                                       station.get("feeltemperature", "na"),
                                       station.get("windgusts", "na"),
                                       station.get("windspeed", "na"),
                                       station.get("windspeedBft", "na"),
                                       station.get("humidity", "na"),
                                       station.get("precipitation", "na"),
                                       station.get("sunpower", "na"),
                                       station.get("rainFallLast24Hour", "na"),
                                       station.get("rainFallLastHour", "na"),
                                       station.get("winddirectiondegrees",
                                                   "na")))


def getvallist(keystr):  # gets all valid values from keystr with
    # associated index
    itemlist = []
    for i in range(0, len(stations)):
        for key, val in stations[i].__dict__.items():
            if key.__contains__(keystr) and val != 'na':
                itemlist.append([float(val), i])
            else:
                continue
    return itemlist


def gethottest():
    return max(getvallist('temperature'))


def getcoldest():
    return min(getvallist('temperature'))


def getsunniest():
    pass


def getmostwindiest():
    return max(getvallist('windSpeed'))


def getleastwindiest():
    return min(getvallist('windSpeed'))


def main():

    getweatherdata()

    #print(getvallist('temperature'))

    hottest = gethottest()
    coldest = getcoldest()
    windiest = getmostwindiest()
    leastwindiest = getleastwindiest()
    print(f"The temperature is currently highest at weather station: "
          f"{stations[hottest[1]].stationName}, it's {hottest[0]} degrees "
          f"there.")
    print(f"The temperature is currently lowest at weather station: "
          f"{stations[coldest[1]].stationName}, it's {coldest[0]} degrees "
          f"there.")
    print(f"The wind is currently highest at weather station: "
          f"{stations[windiest[1]].stationName}, the wind speed is"
          f" {windiest[0]} km/h "
          f"there.")
    print(f"The wind is currently lowest at weather station: "
          f"{stations[leastwindiest[1]].stationName}, the wind speed is"
          f" {leastwindiest[0]} km/h "
          f"there.")


if __name__ == "__main__":
    stations = []
    main()
