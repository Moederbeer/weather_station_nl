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


def getWeatherData():
    # webUrl = urllib.request.urlopen("https://data.buienradar.nl/2.0/feed/json")
    jsonRaw = open('sample_json')
    weatherData = json.load(jsonRaw)["actual"]
    stations = []

    for station in weatherData["stationmeasurements"]:
        print(station["$id"])
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


def main():
    getWeatherData()


if __name__ == "__main__":
    main()
