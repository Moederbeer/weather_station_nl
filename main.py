import urllib.request
import csv
import json
from datetime import datetime
import time
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.transforms import Transform
from matplotlib.ticker import (
    AutoLocator, AutoMinorLocator)
import os.path
from os import path

import numpy as np


class WeatherStation():
    def __init__(self, time, index, jsonid, stationid, stationname, lat, lon,
                 region,
                 timestamp, weatherdescription, winddirection, airpressure,
                 temperature,
                 groundtemperature, feeltemperature, visibility, windgusts,
                 windspeed,
                 windspeedbft, humidity, precipitation, sunpower,
                 rainfalllast24hour, rainfalllasthour, winddirectiondegrees):
        self.time = time
        self.index = index
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
            fieldnames = ['time', 'index', 'temperature', 'airPressure',
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
    selectedstation = 0
    hottest = []
    coldest = []

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.callback = None

        self.canvas = None

        self.updatetime = 10 * 60 * 1000

        self.coldest = getcoldest()
        self.hottest = gethottest()
        self.windiest = getmostwindiest()
        self.leastwindiest = getleastwindiest()
        self.sunniest = getsunniest()

        self.hottestlbl0 = StringVar()
        self.coldestlbl0 = StringVar()
        self.windiestlbl0 = StringVar()
        self.leastwindiestlbl0 = StringVar()
        self.sunniestlbl0 = StringVar()

        self.hottestlbl1 = StringVar()
        self.coldestlbl1 = StringVar()
        self.windiestlbl1 = StringVar()
        self.leastwindiestlbl1 = StringVar()
        self.sunniestlbl1 = StringVar()

        self.weatherlbl = StringVar()
        self.visibilitylbl = StringVar()
        self.temperaturelbl = StringVar()
        self.pressurelbl = StringVar()
        self.sunpowerlbl = StringVar()
        self.rainlbl = StringVar()
        self.winddirectionlbl = StringVar()
        self.windspeedlbl = StringVar()
        self.windgustslbl = StringVar()

        self.init_window()

    def left_frame_data(self):
        self.coldest = getcoldest()
        self.hottest = gethottest()
        self.windiest = getmostwindiest()
        self.leastwindiest = getleastwindiest()
        self.sunniest = getsunniest()

        self.coldestlbl0.set(f"Koudste: {self.coldest[0]}°C")
        self.hottestlbl0.set(f"Heetste: {self.hottest[0]}°C")
        self.windiestlbl0.set(f"Max wind: {self.windiest[0]} Km/h")
        self.leastwindiestlbl0.set(f"Min wind: {self.leastwindiest[0]} Km/h")
        self.sunniestlbl0.set(f"Zonnigst: {self.sunniest[0]} W/m²")

        self.coldestlbl1.set(self.coldest[2])
        self.hottestlbl1.set(self.hottest[2])
        self.windiestlbl1.set(self.windiest[2])
        self.leastwindiestlbl1.set(self.leastwindiest[2])
        self.sunniestlbl1.set(self.sunniest[2])

    def right_frame_data(self):
        self.weatherlbl.set(f"{stations[self.selectedstation].weatherDescription}")
        self.visibilitylbl.set(f"{stations[self.selectedstation].visibility}")
        self.temperaturelbl.set(f"{stations[self.selectedstation].temperature}")
        self.pressurelbl.set(f"{stations[self.selectedstation].airPressure}")
        self.sunpowerlbl.set(f"{stations[self.selectedstation].sunPower}")
        self.rainlbl.set(f"{stations[self.selectedstation].rainFallLastHour}")
        self.winddirectionlbl.set(f"{stations[self.selectedstation].windDirection}")
        self.windspeedlbl.set(f"{stations[self.selectedstation].windSpeed}")
        self.windgustslbl.set(f"{stations[self.selectedstation].windGusts}")


    def init_window(self):
        # changing the title of the master window
        self.master.title("Weerstation")
        # setting a grid
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=0)
        root.grid_columnconfigure(1, weight=1)

        left_frame = Frame(root, width=200)
        left_frame.grid(column=0, row=0, sticky=E+W+N+S)
        left_frame.rowconfigure(1, weight=1)


        top_left_frame = Frame(left_frame, width=200,
                               padx=3, pady=3,
                               height=200)
        top_left_frame.grid(column=0, row=0, sticky=E+W+N)
        top_left_frame.columnconfigure(0, weight=1)

        mid_left_frame = Frame(left_frame, pady=3, padx=3)
        mid_left_frame.grid(column=0, row=1, stick=E+W)
        mid_left_frame.columnconfigure(0, weight=1)


        bottom_left_frame = Frame(left_frame, width=200, pady=3,
                                  padx=3)
        bottom_left_frame.grid(column=0, row=2, sticky=E+W+S)
        bottom_left_frame.columnconfigure(0, minsize=200, weight=0)

        bottom_left_frame.rowconfigure(0, weight=1)
        bottom_left_frame.rowconfigure(16, weight=1)

        right_frame = Frame(root, width=450, height=500, pady=3)
        right_frame.rowconfigure(0, weight=1)
        right_frame.grid(column=1, row=0, sticky=E+W+N+S)
        right_frame.columnconfigure(0, weight=1)
        right_frame.columnconfigure(1, weight=1)
        right_frame.columnconfigure(2, weight=1)
        right_frame.columnconfigure(3, weight=1)
        right_frame.columnconfigure(4, weight=1)
        right_frame.columnconfigure(5, weight=1)
        right_frame.columnconfigure(6, weight=1)
        right_frame.columnconfigure(7, weight=1)
        right_frame.columnconfigure(8, weight=1)

        # matplotlib graph for temperature and pressure
        fig, self.ax1 = plt.subplots()
        fig.set_size_inches(15, 10)
        self.ax2 = self.ax1.twinx()  # instantiate a second axes that shares
        # the
        # same x-axis
        self.canvas = FigureCanvasTkAgg(fig, master=right_frame)
        self.canvas.get_tk_widget().grid(column=0, row=0, columnspan=9)
        # canvas.show()
        self.draw_graph()

        # create list of stations
        self.tkvar1 = StringVar(self.master)
        # set choices of popupmenu
        stationchoices = getvallist("stationName", 1)
        # set default menuitem
        self.tkvar1.set(stationchoices[0])
        # make a popupmenu
        stationpu = OptionMenu(top_left_frame, self.tkvar1, *stationchoices,
                               command=self.selected_station)
        # place it in the grid
        stationpu.grid(sticky=N+E+W)

        self.tkvar2 = StringVar(self.master)
        timechoices = ["10min", "20min", "30min", "60min"]
        self.tkvar2.set(timechoices[0])
        # make a popupmenu
        timerpu = OptionMenu(top_left_frame, self.tkvar2, *timechoices,
                               command=self.selected_timer)
        # place it in the grid
        timerpu.grid(sticky=N+E+W)

        # show assignment data of other stations
        self.coldestlbl0.set(f"Koudste: {self.coldest[0]}°C")
        self.hottestlbl0.set(f"Heetste: {self.hottest[0]}°C")
        self.windiestlbl0.set(f"Max wind: {self.windiest[0]} Km/h")
        self.leastwindiestlbl0.set(f"Min wind: {self.leastwindiest[0]} Km/h")
        self.sunniestlbl0.set(f"Zonnigst: {self.sunniest[0]} W/m²")

        self.coldestlbl1.set(self.coldest[2])
        self.hottestlbl1.set(self.hottest[2])
        self.windiestlbl1.set(self.windiest[2])
        self.leastwindiestlbl1.set(self.leastwindiest[2])
        self.sunniestlbl1.set(self.sunniest[2])

        Label(mid_left_frame, textvariable=self.coldestlbl0, anchor=W).grid(
            sticky=EW)
        Label(mid_left_frame, textvariable=self.coldestlbl1, anchor=W).grid(
            sticky=EW)
        Label(mid_left_frame, text="").grid(sticky=EW)

        Label(mid_left_frame, textvariable=self.hottestlbl0, anchor=W).grid(
            sticky=EW)
        Label(mid_left_frame, textvariable=self.hottestlbl1, anchor=W).grid(
            sticky=EW)
        Label(mid_left_frame, text="").grid(sticky=EW)

        Label(mid_left_frame, textvariable=self.windiestlbl0, anchor=W).grid(
            sticky=EW)
        Label(mid_left_frame, textvariable=self.windiestlbl1, anchor=W).grid(
            sticky=EW)
        Label(mid_left_frame, text="").grid(sticky=EW)

        Label(mid_left_frame, textvariable=self.leastwindiestlbl0,
              anchor=W).grid(sticky=EW)
        Label(mid_left_frame, textvariable=self.leastwindiestlbl1, anchor=W).grid(
            sticky=EW)
        Label(mid_left_frame, text="").grid(sticky=EW)

        Label(mid_left_frame, textvariable=self.sunniestlbl0,
              anchor=W).grid(sticky=EW)
        Label(mid_left_frame, textvariable=self.sunniestlbl1, anchor=W).grid(
            sticky=EW)

        # Label(root, textvariable=self.test).grid(sticky=EW)

        # self.test.set("hoi")

        # creating a button instance
        quitbutton = Button(bottom_left_frame, text="Exit", command=self.client_exit)
        # placing the button on my window
        quitbutton.grid(sticky=SW)



        # selected station data
        # weather description, visibility, temperature, air pressure,
        # sun power, rain, wind-direction/power/gusts
        Label(right_frame, text="Huidig weer:").grid(column=0, row=1)
        Label(right_frame, textvariable=self.weatherlbl).grid(
            column=0, row=2)

        Label(right_frame, text="Zicht:").grid(column=1, row=1)
        Label(right_frame, textvariable=self.visibilitylbl, anchor=W).grid(
            column=1,
            row=2)

        Label(right_frame, text="Temperatuur:").grid(column=2, row=1)
        Label(right_frame, textvariable=self.temperaturelbl, anchor=W).grid(
            column=2,
            row=2)

        Label(right_frame, text="Luchtdruk:").grid(column=3, row=1)
        Label(right_frame, textvariable=self.pressurelbl, anchor=W).grid(
            column=3,
            row=2)

        Label(right_frame, text="Zonnekracht:").grid(column=4, row=1)
        Label(right_frame, textvariable=self.sunpowerlbl, anchor=W).grid(
            column=4,
            row=2)

        Label(right_frame, text="Regen laatste uur:").grid(column=5, row=1)
        Label(right_frame, textvariable=self.rainlbl, anchor=W).grid(column=5,
                                                                     row=2)

        Label(right_frame, text="Windrichting:").grid(column=6, row=1)
        Label(right_frame, textvariable=self.winddirectionlbl, anchor=W).grid(
            column=6,
            row=2)

        Label(right_frame, text="Windsnelheid:").grid(column=7, row=1)
        Label(right_frame, textvariable=self.windspeedlbl, anchor=W).grid(
            column=7,
            row=2)

        Label(right_frame, text="Windstoten:").grid(column=8, row=1)
        Label(right_frame, textvariable=self.windgustslbl, anchor=W).grid(
            column=8,
            row=2)

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

        # start timed updater
        self.onupdate()

    def client_exit(self):
        exit()

    def draw_graph(self):
        self.ax1.clear()
        self.ax2.clear()
        temperatures = []
        pressures = []
        timestamps = []
        with open('weatherdata.csv', 'r') as weatherfile:
            reader = csv.reader(weatherfile,    delimiter=';',
                                                quotechar='"',
                                                quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                if int(row[1]) == self.selectedstation:
                    timestamps.append(row[0])
                    temperatures.append(row[2])
                    pressures.append(row[3])

        color = 'tab:red'
        self.ax1.set_xlabel('Datum')
        self.ax1.set_ylabel('°C', color=color)
        self.ax1.plot(timestamps, temperatures, color=color)
        self.ax1.tick_params(axis='y', labelcolor=color)

        color = 'tab:blue'
        self.ax2.set_ylabel('hPa', color=color)
        self.ax2.plot(timestamps, pressures, color=color)
        self.ax2.tick_params(axis='y', labelcolor=color)
        self.canvas.draw()

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
                    self.selectedstation = i
                    print(i)
        self.right_frame_data()
        self.draw_graph()

    def selected_timer(self, value):
        # cancel te last timer because a new interval is set
        root.after_cancel(self.callback)
        # compare input to needed output
        if value == "10min":
            self.updatetime = 10 * 60 * 1000
        elif value == "20min":
            self.updatetime = 20 * 60 * 1000
        elif value == "30min":
            self.updatetime = 30 * 60 * 1000
        elif value == "60min":
            self.updatetime = 60 * 60 * 1000
        # run the onupdate function with new interval
        self.onupdate()

    def current_iso8601(self):
        return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

    def onupdate(self):
        # update displayed time
        print("new data")
        getweatherdata()
        self.left_frame_data()
        self.right_frame_data()
        # schedule update timer with callback to cancel
        self.callback = self.after(self.updatetime, self.onupdate)


def getweatherdata():
    # load json file
    # jsonraw = urllib.request.urlopen(
        # "https://data.buienradar.nl/2.0/feed/json")
    jsonraw = open('sample_json')
    weatherdata = json.load(jsonraw)["actual"]
    # create a timestamp
    time = datetime.now()
    timestamp = time.strftime("%b %d %Y %H:%M:%S")
    # clear data so there is room for fresh data
    stations.clear()
    index = 0

    for station in weatherdata["stationmeasurements"]:
        stations.append(WeatherStation(timestamp,
                                       index,
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
        index += 1


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


def datalist_from_csv(key):
    with open('weatherdata.csv', mode='r', newline='') as weatherfile:
        csv_reader = csv.reader(weatherfile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(
                    f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')


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
    pass


if __name__ == "__main__":
    stations = []
    getweatherdata()
    writecsv()
    main()
    root = Tk()
    app = Window(root)
    root.geometry('1000x750')
    root.mainloop()
