import urllib.request
import csv
import json
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import os


class WeatherDataFiles:
    # write all stations to csv file
    def writecsv(self):
        # go through all stations
        for i in range(0, len(self.stations)):
            # open the file
            with open('weatherdata.csv', mode='a', newline='') as weatherfile:
                # select which fieldnames to write
                fieldnames = ['time', 'index', 'temperature', 'airPressure',
                              'precipitation',
                              'sunPower', 'windSpeed']
                # create the actual writer with settings
                weather_writer = csv.DictWriter(weatherfile, fieldnames=fieldnames,
                                                delimiter=';',
                                                quotechar='"',
                                                extrasaction='ignore',
                                                quoting=csv.QUOTE_MINIMAL)
                # write the row
                weather_writer.writerow(self.stations[i].__dict__)
        return

    def writecsv_single(self, stationid):
        # write a single station to a file with stationName as filename, same as above but single
        with open(self.stations[stationid].stationName + '.csv', mode='a', newline='') as \
                weatherfile:
            # select which fields to write
            fieldnames = ['time', 'index', 'temperature', 'airPressure',
                          'precipitation',
                          'sunPower', 'windSpeed']
            weather_writer = csv.DictWriter(weatherfile, fieldnames=fieldnames,
                                            delimiter=';',
                                            quotechar='"',
                                            extrasaction='ignore',
                                            quoting=csv.QUOTE_MINIMAL)
            weather_writer.writerow(self.stations[stationid].__dict__)
        return

    def delete_csv(self):
        # delete the file containing all readings
        # check is file exists
        if os.path.isfile('weatherdata.csv'):
            # remove the file
            os.remove('weatherdata.csv')
            # create a new blank file
            open('weatherdata.csv', 'w')
            return
        else:
            return


class WeatherStation(WeatherDataFiles):
    # simple class containing all data from a single weatherstation
    def __init__(self, time, index, jsonid, stationid, stationname, lat, lon, region, timestamp,
                 weatherdescription, winddirection, airpressure, temperature, groundtemperature,
                 feeltemperature, visibility, windgusts, windspeed, windspeedbft, humidity,
                 precipitation, sunpower, rainfalllast24hour, rainfalllasthour,
                 winddirectiondegrees):
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


class WeatherDataFromInternet:
    def __init__(self):
        self.stations = []
        self.itemlist = []
        self.time = None
        self.index = None
        self.jsonraw = None
        self.weatherdata = None

    def getweatherdata(self):
        # load json file
        self.jsonraw = urllib.request.urlopen("https://data.buienradar.nl/2.0/feed/json")
        self.weatherdata = json.load(self.jsonraw)["actual"]
        # create a timestamp
        self.time = datetime.today().strftime("%d/%m/%Y - %H:%M:%S")
        # clear data so there is room for fresh data
        self.stations.clear()
        # reset the index
        self.index = 0

        # count the amount of stations in weatherraw and iterate through them
        for self.station in self.weatherdata["stationmeasurements"]:
            # add all data to new WeatherStation objects
            self.stations.append(WeatherStation(self.time,
                                                self.index,
                                                self.station.get("$id", "na"),
                                                self.station.get("stationid", "na"),
                                                self.station.get("stationname", "na"),
                                                self.station.get("lat", "na"),
                                                self.station.get("lon", "na"),
                                                self.station.get("regio", "na"),
                                                self.station.get("timestamp", "na"),
                                                self.station.get("weatherdescription", "na"),
                                                self.station.get("winddirection", "na"),
                                                self.station.get("airpressure", "na"),
                                                self.station.get("temperature", "na"),
                                                self.station.get("groundtemperature", "na"),
                                                self.station.get("feeltemperature", "na"),
                                                self.station.get("visibility", "na"),
                                                self.station.get("windgusts", "na"),
                                                self.station.get("windspeed", "na"),
                                                self.station.get("windspeedBft", "na"),
                                                self.station.get("humidity", "na"),
                                                self.station.get("precipitation", "na"),
                                                self.station.get("sunpower", "na"),
                                                self.station.get("rainFallLast24Hour", "na"),
                                                self.station.get("rainFallLastHour", "na"),
                                                self.station.get("winddirectiondegrees", "na")))
            # increase the numerical index to add to data
            self.index += 1
        return

    def is_number(self, s):
        # checks if input value is a number
        try:
            float(s)
            return True
        except ValueError:
            return False

    # gets all valid values from keystr with associated index
    def getvallist(self, keystr, size=3):
        self.itemlist = []
        # go through all stations
        for i in range(0, len(self.stations)):
            # get keys and values from station
            for key, val in self.stations[i].__dict__.items():
                # find desired key from keys
                if key.__contains__(keystr) and val != 'na':
                    if size == 1:
                        # check if value is a number
                        if self.is_number(val):
                            # append value and id to list if not 'na'
                            self.itemlist.append(float(val))
                        else:
                            self.itemlist.append(val)
                    elif size == 3:
                        if self.is_number(val):
                            # append value id and name to list if not 'na'
                            self.itemlist.append([float(val), i, self.stations[
                                i].__dict__.get("stationName")])
                        else:
                            self.itemlist.append([val, i, self.stations[i].__dict__.get(
                                "stationName")])
                    else:
                        if self.is_number(val):
                            # append value and id to list if not 'na'
                            self.itemlist.append([float(val), i])
                        else:
                            self.itemlist.append([val, i])
                else:
                    # don't do anything if value = 'na'
                    continue
        # return the list of items
        return self.itemlist

    def gethottest(self):
        # gets a list of all temperatures and returns the hottest one
        return max(self.getvallist('temperature'))

    def getcoldest(self):
        # see above
        return min(self.getvallist('temperature'))

    def getsunniest(self):
        # see above
        return max(self.getvallist('sunPower'))

    def getmostwindiest(self):
        # see above
        return max(self.getvallist('windSpeed'))

    def getleastwindiest(self):
        # see above
        return min(self.getvallist('windSpeed'))


class WeatherDisplay(Frame, WeatherDataFromInternet, WeatherDataFiles):

    def __init__(self, master=None):
        self.stations = []
        self.weatherdata = WeatherDataFromInternet
        self.weatherdata.getweatherdata(self)
        self.tkvar1 = None
        self.tkvar2 = None
        Frame.__init__(self, master)
        self.master = master
        self.selectedstation = 0

        self.callback = None
        self.canvas = None
        # set default time interval
        self.updatetime = 10 * 60 * 1000

        self.coldest = WeatherDataFromInternet.getcoldest(self)
        self.hottest = WeatherDataFromInternet.gethottest(self)
        self.windiest = WeatherDataFromInternet.getmostwindiest(self)
        self.leastwindiest = WeatherDataFromInternet.getleastwindiest(self)
        self.sunniest = WeatherDataFromInternet.getsunniest(self)

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
        # updates all values in the left sidebar
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
        # updates all values of the current station under the graph
        self.weatherlbl.set(f"{self.stations[self.selectedstation].weatherDescription}")
        self.visibilitylbl.set(f"{self.stations[self.selectedstation].visibility}m")
        self.temperaturelbl.set(f"{self.stations[self.selectedstation].temperature}°C")
        self.pressurelbl.set(f"{self.stations[self.selectedstation].airPressure}hPa")
        self.sunpowerlbl.set(f"{self.stations[self.selectedstation].sunPower}W/m²")
        self.rainlbl.set(f"{self.stations[self.selectedstation].rainFallLastHour}mm")
        self.winddirectionlbl.set(f"{self.stations[self.selectedstation].windDirection}")
        self.windspeedlbl.set(f"{self.stations[self.selectedstation].windSpeed}Km/h")
        self.windgustslbl.set(f"{self.stations[self.selectedstation].windGusts}Km/h")

    def init_window(self):
        # changing the title of the master window
        self.master.title("Weerstation")
        # setting a grid
        root.grid_rowconfigure(0, weight=1)
        # left elements don't have to scale
        root.grid_columnconfigure(0, weight=0)
        # right elements have to scale (graph) when resizing window
        root.grid_columnconfigure(1, weight=1)

        # adding a 200 pixel wide left frame containing all elements of the left side
        left_frame = Frame(root, width=200)
        # make this stick to all sides
        left_frame.grid(column=0, row=0, sticky=E+W+N+S)
        # make only the middle row grow when scaling
        left_frame.rowconfigure(1, weight=1)

        # create a top left frame inside left frame for selecting station and interval
        top_left_frame = Frame(left_frame, width=200, padx=3, pady=3, height=200)
        top_left_frame.grid(column=0, row=0, sticky=E+W+N)
        top_left_frame.columnconfigure(0, weight=1)

        # create a middle left frame for highest, lowest etc
        mid_left_frame = Frame(left_frame, pady=3, padx=3)
        mid_left_frame.grid(column=0, row=1, stick=E+W)
        mid_left_frame.columnconfigure(0, weight=1)

        # create a bottom left frame for an exit button
        bottom_left_frame = Frame(left_frame, width=200, pady=3, padx=3)
        bottom_left_frame.grid(column=0, row=2, sticky=E+W+S)
        bottom_left_frame.columnconfigure(0, minsize=200, weight=0)

        # create the right frame for graph and data of current station
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
        # create a figure for the plot two plot which share the X axis (time)
        fig, self.ax = plt.subplots(2, 1, sharex=True)
        # set the size of this figure
        fig.set_size_inches(20, 10)
        # set the bg color to match the window
        fig.patch.set_facecolor('#F0F0F0')
        # create a canvas which houses the figure
        self.canvas = FigureCanvasTkAgg(fig, master=right_frame)
        # place the figure on the grid
        self.canvas.get_tk_widget().grid(column=0, row=0, columnspan=8)
        # draw the graph in a function so it's able to update later
        self.draw_graph()

        # create list of all stationsstations
        self.tkvar1 = StringVar(self.master)
        # set choices of popupmenu
        stationchoices = self.getvallist("stationName", 1)
        # set default menuitem
        self.tkvar1.set(stationchoices[0])
        # make a popupmenu for stationselect which exectutes selected_station when changed
        stationpu = OptionMenu(top_left_frame, self.tkvar1, *stationchoices,
                               command=self.selected_station)
        # place it in the grid
        stationpu.grid(sticky=N+E+W)

        # create another popupmenu for setting the time interval
        # make some choices
        self.tkvar2 = StringVar(self.master)
        timechoices = ["10min", "20min", "30min", "60min"]
        # set the default one
        self.tkvar2.set(timechoices[0])
        # make a popupmenu which executes selected_timer when changed
        timerpu = OptionMenu(top_left_frame, self.tkvar2, *timechoices, command=self.selected_timer)
        # place it in the grid
        timerpu.grid(sticky=N+E+W)

        # create labels for all left frame data (hottest, coldests, etc)
        Label(mid_left_frame, textvariable=self.coldestlbl0, anchor=W).grid(sticky=EW)
        Label(mid_left_frame, textvariable=self.coldestlbl1, anchor=W).grid(sticky=EW)
        Label(mid_left_frame, text="").grid(sticky=EW)

        Label(mid_left_frame, textvariable=self.hottestlbl0, anchor=W).grid(sticky=EW)
        Label(mid_left_frame, textvariable=self.hottestlbl1, anchor=W).grid(sticky=EW)
        Label(mid_left_frame, text="").grid(sticky=EW)

        Label(mid_left_frame, textvariable=self.windiestlbl0, anchor=W).grid(sticky=EW)
        Label(mid_left_frame, textvariable=self.windiestlbl1, anchor=W).grid(sticky=EW)
        Label(mid_left_frame, text="").grid(sticky=EW)

        Label(mid_left_frame, textvariable=self.leastwindiestlbl0,anchor=W).grid(sticky=EW)
        Label(mid_left_frame, textvariable=self.leastwindiestlbl1, anchor=W).grid(sticky=EW)
        Label(mid_left_frame, text="").grid(sticky=EW)

        Label(mid_left_frame, textvariable=self.sunniestlbl0, anchor=W).grid(sticky=EW)
        Label(mid_left_frame, textvariable=self.sunniestlbl1, anchor=W).grid(sticky=EW)

        # creating a quit button
        quitbutton = Button(bottom_left_frame, text="Exit", command=self.client_exit)
        # placing the button
        quitbutton.grid(sticky=SW)

        # selected station data labels under graph
        Label(right_frame, text="Huidig weer:").grid(column=0, row=1)
        Label(right_frame, textvariable=self.weatherlbl).grid(column=0, row=2)

        Label(right_frame, text="Zicht:").grid(column=1, row=1)
        Label(right_frame, textvariable=self.visibilitylbl, anchor=W).grid(column=1, row=2)

        Label(right_frame, text="Temperatuur:").grid(column=2, row=1)
        Label(right_frame, textvariable=self.temperaturelbl, anchor=W).grid(column=2, row=2)

        Label(right_frame, text="Luchtdruk:").grid(column=3, row=1)
        Label(right_frame, textvariable=self.pressurelbl, anchor=W).grid(column=3, row=2)

        Label(right_frame, text="Zonnekracht:").grid(column=4, row=1)
        Label(right_frame, textvariable=self.sunpowerlbl, anchor=W).grid(column=4, row=2)

        Label(right_frame, text="Regen laatste uur:").grid(column=5, row=1)
        Label(right_frame, textvariable=self.rainlbl, anchor=W).grid(column=5, row=2)

        Label(right_frame, text="Windrichting:").grid(column=6, row=1)
        Label(right_frame, textvariable=self.winddirectionlbl, anchor=W).grid(column=6, row=2)

        Label(right_frame, text="Windsnelheid:").grid(column=7, row=1)
        Label(right_frame, textvariable=self.windspeedlbl, anchor=W).grid(column=7, row=2)

        Label(right_frame, text="Windstoten:").grid(column=8, row=1)
        Label(right_frame, textvariable=self.windgustslbl, anchor=W).grid(column=8, row=2)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)
        # create the file object
        file = Menu(menu, tearoff=False)
        # add all options to the file menu and link their commands
        file.add_command(label="Verwijder CSV", command=self.delete_csv)
        file.add_command(label="Exit", command=self.client_exit)
        # added "file" to our menu
        menu.add_cascade(label="File", menu=file)
        # create another file object for the about menu
        edit = Menu(menu, tearoff=False)
        # make about call the about subwindow
        edit.add_command(label="About", command=self.about_window)
        # added "file" to our menu
        menu.add_cascade(label="Help", menu=edit)
        # start timed updater for data
        self.onupdate()

    def client_exit(self):
        # stops the current timer and closes the program
        root.after_cancel(self.callback)
        exit()

    def draw_graph(self):
        # clear the current graph and it's variables
        self.ax[0].clear()
        self.ax[1].clear()
        temperatures = []
        pressures = []
        timestamps = []
        # open the weatherdata file
        with open('weatherdata.csv', 'r') as weatherfile:
            # create a reader object with settings
            reader = csv.reader(weatherfile,    delimiter=';',
                                                quotechar='"',
                                                quoting=csv.QUOTE_MINIMAL)
            # got through all rows in the csv file
            for row in reader:
                # check if it's our selected station
                if int(row[1]) == self.selectedstation:
                    # convert timestamp to date object and add to list
                    timestamps.append(datetime.strptime(row[0], "%d/%m/%Y - %H:%M:%S"))
                    # check if values from this row are numbers or 'na' and append either value or 0
                    if self.is_number(row[2]):
                        temperatures.append(float(row[2]))
                    else:
                        temperatures.append(0)
                    if self.is_number(row[3]):
                        pressures.append(float(row[3]))
                    else:
                        pressures.append(0)

        # set color, labels, axisdata and ticks of top plot
        color = 'tab:red'
        self.ax[0].set_xlabel('Tijd')
        self.ax[0].set_ylabel('°C', color=color)
        self.ax[0].plot(timestamps, temperatures, color=color)
        self.ax[0].tick_params(axis='y', labelcolor=color)

        # set color, labels, axisdata and ticks of bottom plot
        color = 'tab:blue'
        self.ax[1].set_ylabel('hPa', color=color)
        self.ax[1].plot(timestamps, pressures, color=color)
        self.ax[1].tick_params(axis='y', labelcolor=color)
        plt.ticklabel_format(useOffset=False, axis='y')

        # compact layout
        plt.tight_layout(5)
        # make time axis nicer with autoformatting dates
        plt.gcf().autofmt_xdate()
        # update the graph
        self.canvas.draw()

    def about_window(self):
        # create a subwindow above root
        sub = Toplevel()
        sub.title("About")
        sub.geometry("250x60")
        # make it not resizeable
        sub.resizable(width=False, height=False)
        sub.columnconfigure(0, weight=1)
        sub.rowconfigure(0, weight=1)
        sub.rowconfigure(1, weight=1)
        # add developer labels and disclaimer
        Label(sub, text="Developed by: Paul de Groot").grid(sticky=E+W)
        Label(sub, text="Using data provided by www.buienradar.nl").grid(sticky=E+W)

    def selected_station(self, value):
        # get the id of the chosen station and set this as selectedstation
        # go through all stations
        for i in range(0, len(self.stations)):
            # go through key and value of current station
            for k, v in self.stations[i].__dict__.items():
                # compare stationName to value and set selected station to i if true
                if k == "stationName" and v == value:
                    self.selectedstation = i
                    break
        # update the graph and it's subdata
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

    def onupdate(self):
        # update displayed time
        try:
            # check if weatherdata.csv is writeable
            open('weatherdata.csv', 'a')
        except PermissionError:
            # if not show a messagebox displaying the error with which needs to be fixed
            messagebox.showerror("Error", "weatherdata.csv is geopend, sluit dit bestand.")
            # try again
            self.onupdate()
            return
        try:
            # check if currently selected station data .csv is writeable
            open(self.stations[self.selectedstation].stationName + '.csv', 'a')
        except PermissionError:
            # if not show a messagebox displaying the error with which needs to be fixed
            messagebox.showerror("Error", f'{self.stations[self.selectedstation].stationName}'
                                          f'.csv is geopend, sluit dit bestand.')
            # try again
            self.onupdate()
            return
        else:
            # data is writeable so go ahead
            # get some new data and update everything on screen
            self.getweatherdata()
            self.left_frame_data()
            self.right_frame_data()
            self.draw_graph()

            # write the new data
            self.writecsv()
            # write only the currently selected station
            self.writecsv_single(self.selectedstation)

            # schedule update timer for next update with callback to cancel
            self.callback = self.after(self.updatetime, self.onupdate)


if __name__ == "__main__":
    # initialize tkinter
    root = Tk()
    # create app object
    app = WeatherDisplay(root)
    # set some parameters
    root.geometry('1200x750')
    root.minsize(1200, 400)
    # run our GUI
    root.mainloop()
