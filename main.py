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


def main():
    # webUrl = urllib.request.urlopen("https://data.buienradar.nl/2.0/feed/json")
    jsonRaw = open('sample_json')
    weatherData = json.load(jsonRaw)["actual"]
    stations = []

    for station in weatherData["stationmeasurements"]:
        print(station["$id"])
        stations.append(weatherStation(station["$id"], station[
            "stationid"], station["stationname"], station["lat"],
                                     station["lon"], station["regio"],
                                     station["timestamp"], station[
                                         "weatherdescription"], station[
                                         "winddirection"], station[
                                         "temperature"], station[
                                         "groundtemperature"], station[
                                         "feeltemperature"], station[
                                         "windgusts"], station[
                                         "windspeed"], station[
                                         "windspeedBft"], station[
                                         "humidity"], station[
                                         "precipitation"], station[
                                         "sunpower"], station[
                                         "rainFallLast24Hour"], station[
                                         "rainFallLastHour"], station[
                                         "winddirectiondegrees"]))



main()
