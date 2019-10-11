import urllib.request
import json


def main():
    # webUrl = urllib.request.urlopen("https://data.buienradar.nl/2.0/feed/json")
    webUrl =  open('sample_json')
    weatherData = json.load(webUrl)["actual"]

    for s in weatherData["stationmeasurements"]:
        print(s)

main()