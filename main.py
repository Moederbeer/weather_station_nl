import urllib.request
import csv
import json
from datetime import datetime
from tkinter import *
from tkinter import ttk


class WeatherStation():
    def __init__(self, time, jsonid, stationid, stationname, lat, lon, region,
                 timestamp, weatherdescription, winddirection, airpressure,
                 temperature,
                 groundtemperature, feeltemperature, visibility, windgusts,
                 windspeed,
                 windspeedbft, humidity, precipitation, sunpower,
                 rainfalllast24hour, rainfalllasthour, winddirectiondegrees):
        self.time = time
        self.id = jsonid
        self.stationId = stationid
        self.stationName = stationname
        self.lat = lat
        self.lon = lon
        self.region = region
        self.timestamp = timestamp
        self.weatherDescription = weatherdescription
        self.airPressure = airpressure
        self.windDirection = winddirection
        self.temperature = temperature
        self.groundTemperature = groundtemperature
        self.feelTemperature = feeltemperature
        self.visibility = visibility
        self.windGusts = windgusts
        self.windSpeed = windspeed
        self.windSpeedBft = windspeedbft
        self.humidity = humidity
        self.precipitation = precipitation
        self.sunPower = sunpower
        self.rainFallLast24Hour = rainfalllast24hour
        self.rainFallLastHour = rainfalllasthour
        self.windDirectionDegrees = winddirectiondegrees

    def writecsvrow(self):
        with open('weatherdata.csv', mode='a', newline='') as weatherfile:
            fieldnames = ['time', 'id', 'temperature', 'airPressure',
                          'precipitation',
                          'sunPower', 'windSpeed']
            weather_writer = csv.DictWriter(weatherfile, fieldnames=fieldnames,
                                            delimiter=';',
                                            quotechar='"',
                                            extrasaction='ignore',
                                            quoting=csv.QUOTE_MINIMAL)
            weather_writer.writerow(self.__dict__)
        return


class Window(Frame):
    counter = 0
    selectedstation = 1
    hottest = []
    coldest = []

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        # changing the title of the master window
        self.master.title("Weerstation")
        # setting a grid

        left_frame = Frame(root, bg='cyan', width=450, height=500, pady=3)
        left_frame.grid(sticky=NS)
        left_frame.columnconfigure(0, minsize=200)

        # allowing the widget to take the full space of the root window
        # self.pack(fill=BOTH, expand=1)

        # create list of stations
        self.tkvar = StringVar(self.master)
        # set choices of popupmenu
        choices = getvallist("stationName", 1)
        # set default menuitem
        self.tkvar.set(choices[0])
        # make a popupmenu
        popupmenu = OptionMenu(left_frame, self.tkvar, *choices,
                               command=self.selected_station)
        # place it in the grid
        popupmenu.grid(sticky=EW)

        # selected station data
        # weather description, visibility, temperature, air pressure,
        # sun power, rain, wind-direction/power/gusts
        Label(left_frame, text=stations[
            self.selectedstation].weatherDescription, anchor=W).grid(
            sticky=EW)
        Label(left_frame, text=stations[
            self.selectedstation].visibility, anchor=W).grid(
            sticky=EW)
        Label(left_frame, text=stations[
            self.selectedstation].temperature, anchor=W).grid(
            sticky=EW)
        Label(left_frame, text=stations[
            self.selectedstation].airPressure, anchor=W).grid(
            sticky=EW)
        Label(left_frame, text=stations[
            self.selectedstation].sunPower, anchor=W).grid(
            sticky=EW)
        Label(left_frame, text=stations[
            self.selectedstation].rainFallLastHour, anchor=W).grid(
            sticky=EW)
        Label(left_frame, text=stations[
            self.selectedstation].windDirection, anchor=W).grid(
            sticky=EW)
        Label(left_frame, text=stations[
            self.selectedstation].windSpeed, anchor=W).grid(
            sticky=EW)
        Label(left_frame, text=stations[
            self.selectedstation].windGusts, anchor=W).grid(
            sticky=EW)



        # show assignment data of other stations
        coldest = getcoldest()
        hottest = gethottest()
        windiest = getmostwindiest()
        leastwindiest = getleastwindiest()
        sunniest = getsunniest()

        Label(left_frame, text=f"Koudste: {coldest[0]}°C", anchor=W).grid(
            sticky=EW)
        Label(left_frame, text=coldest[2], anchor=W).grid(sticky=EW)
        Label(left_frame, text="").grid(sticky=EW)

        Label(left_frame, text=f"Heetste: {hottest[0]}°C", anchor=W).grid(
            sticky=EW)
        Label(left_frame, text=hottest[2], anchor=W).grid(sticky=EW)
        Label(left_frame, text="").grid(sticky=EW)

        Label(left_frame, text=f"Max wind: {windiest[0]} Km/h", anchor=W).grid(
            sticky=EW)
        Label(left_frame, text=windiest[2], anchor=W).grid(sticky=EW)
        Label(left_frame, text="").grid(sticky=EW)

        Label(left_frame, text=f"Min wind: {leastwindiest[0]} Km/h",
              anchor=W).grid(sticky=EW)
        Label(left_frame, text=leastwindiest[2], anchor=W).grid(sticky=EW)
        Label(left_frame, text="").grid(sticky=EW)

        Label(left_frame, text=f"Zonnigst: {sunniest[0]} W/m²",
              anchor=W).grid(sticky=EW)
        Label(left_frame, text=sunniest[2], anchor=W).grid(sticky=EW)

        # creating a button instance
        quitbutton = Button(left_frame, text="Exit", command=self.client_exit)
        # placing the button on my window
        quitbutton.grid(sticky=SW)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)
        # create the file object)
        file = Menu(menu, tearoff=False)
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Save", command=self.client_exit)
        file.add_command(label="Open", command=self.client_exit)
        file.add_command(label="Exit", command=self.client_exit)
        # added "file" to our menu
        menu.add_cascade(label="File", menu=file)
        # create the file object)
        edit = Menu(menu, tearoff=False)
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label="About", command=self.about_window)
        # added "file" to our menu
        menu.add_cascade(label="Help", menu=edit)


        # self.pack(fill=BOTH, expand=1)

    def client_exit(self):
        exit()

    def about_window(self):
        sub = Toplevel()
        sub.title("About")
        sub.geometry("320x240")

    def selected_station(self, value):
        print(value)
        # get the id of the chosen station and set this as selectedstation
        for i in range(0, len(stations)):
            for k, v in stations[i].__dict__.items():
                if k == "stationName" and v == value:
                    self.selectedstation = stations[i].id


def getweatherdata():
    #jsonraw = urllib.request.urlopen(
        #"https://data.buienradar.nl/2.0/feed/json")
    jsonraw = open('sample_json')
    weatherdata = json.load(jsonraw)["actual"]
    time = datetime.now()

    for station in weatherdata["stationmeasurements"]:
        stations.append(WeatherStation(time,
                                       station.get("$id", "na"),
                                       station.get("stationid", "na"),
                                       station.get("stationname", "na"),
                                       station.get("lat", "na"),
                                       station.get("lon", "na"),
                                       station.get("regio", "na"),
                                       station.get("timestamp", "na"),
                                       station.get("weatherdescription", "na"),
                                       station.get("winddirection", "na"),
                                       station.get("airpressure", "na"),
                                       station.get("temperature", "na"),
                                       station.get("groundtemperature", "na"),
                                       station.get("feeltemperature", "na"),
                                       station.get("visibility", "na"),
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


def changed():
    print("changed")


# gets all valid values from keystr with associated index
def getvallist(keystr, size=3):
    itemlist = []
    # go through all stations
    for i in range(0, len(stations)):
        # get keys and values from station
        for key, val in stations[i].__dict__.items():
            # find desired key from keys
            if key.__contains__(keystr) and val != 'na':
                if size == 1:
                    if is_number(val):
                        # append value and id to list if not 'na'
                        itemlist.append(float(val))
                    else:
                        itemlist.append(val)
                elif size == 3:
                    if is_number(val):
                        # append value id and name to list if not 'na'
                        itemlist.append([float(val), i, stations[
                            i].__dict__.get("stationName")])
                    else:
                        itemlist.append([val, i, stations[i].__dict__.get(
                            "stationName")])
                else:
                    if is_number(val):
                        # append value and id to list if not 'na'
                        itemlist.append([float(val), i])
                    else:
                        itemlist.append([val, i])
            else:
                # don't do anything if value = 'na'
                continue
    return itemlist


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def writecsv():
    for i in range(0, len(stations)):
        stations[i].writecsvrow()
    return


def gethottest():
    return max(getvallist('temperature'))


def getcoldest():
    return min(getvallist('temperature'))


def getsunniest():
    return max(getvallist('sunPower'))


def getmostwindiest():
    return max(getvallist('windSpeed'))


def getleastwindiest():
    return min(getvallist('windSpeed'))


def main():
    getweatherdata()

    # print(getvallist('temperature'))

    # hottest = gethottest()
    # coldest = getcoldest()
    # windiest = getmostwindiest()
    # leastwindiest = getleastwindiest()
    # sunniest = getsunniest()
    # print(f"The temperature is currently highest at weather station: "
    #       f"{stations[hottest[1]].stationName}, it's {hottest[0]} degrees "
    #       f"there.")
    # print(
    #     f"The temperature is currently lowest at weather station: {stations[coldest[1]].stationName}, it's {coldest[0]} degrees there.")
    # print(
    #     f"The wind is currently highest at weather station: {stations[windiest[1]].stationName}, the wind speed is {windiest[0]} km/h "
    #     f"there.")
    # print(f"The wind is currently lowest at weather station: "
    #       f"{stations[leastwindiest[1]].stationName}, the wind speed is"
    #       f" {leastwindiest[0]} km/h "
    #       f"there.")
    # print(f"The sunpower is currently highest at weather station: "
    #       f"{stations[sunniest[1]].stationName}, the sunpower is "
    #       f"{sunniest[0]} watts per square meter there.")
    #
    # print(getvallist("stationName", 1))

    # writecsv()


if __name__ == "__main__":
    stations = []
    main()
    root = Tk()
    app = Window(root)
    root.geometry('1000x750')
    root.mainloop()
    print()
