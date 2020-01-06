from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

import time, datetime

import audio_alarm, weather
import threading

# Initial Values

city_of_interest = "Karlsruhe,de"
alarm_time_hrs = 11
alarm_time_min = 00
alarm_setting = False

#default forecast for debugging/offline
forecast = {'coord': {'lon': 8.4, 'lat': 49.01}, 'weather': [{'id': 701, 'main': 'Mist', 'description': 'sun', 'icon': '50n'}], 'base': 'stations', 'main': {'temp': 1.37, 'feels_like': -1.11, 'temp_min': -0.56, 'temp_max': 4, 'pressure': 1027, 'humidity': 100}, 'visibility': 1400, 'wind': {'speed': 1}, 'clouds': {'all': 90}, 'dt': 1578326220, 'sys': {'type': 1, 'id': 1314, 'country': 'DE', 'sunrise': 1578295188, 'sunset': 1578325422}, 'timezone': 3600, 'id': 2892794, 'name': 'Karlsruhe', 'cod': 200}

# ------------------FUNCTIONS-----------------------

# ---- CLOCK ----
def tick():
    global alarm_time_hrs, alarm_time_min, alarm_setting
    current_time = time.strftime('%H:%M:%S') 
    if current_time != clock_label["text"]:
        clock_label["text"] = current_time
    now = datetime.datetime.now()
    if alarm_setting == True:
        if ((alarm_time_hrs == now.hour) & (alarm_time_min == now.minute)):
            audio_alarm.play()
            messagebox.showinfo("ALARM!", "It's {:02d}:{:02d}".format(alarm_time_hrs, alarm_time_min))
            audio_alarm.stop()
            alarm_setting = False
            update_alarm()
    
    clock_label.after(200, tick)

def update_alarm():
    global alarm_time_hrs
    global alarm_time_min
    
    alarm_string= "Alarm:\n{:02d}:{:02d}".format(alarm_time_hrs, alarm_time_min)
    alarm_label["text"] = alarm_string
    if alarm_setting == True:
        but_enable_alarm["text"] = "enabled"
    else:
        but_enable_alarm["text"] = "disabled"
    
def inc_hrs():
    global alarm_time_hrs
    alarm_time_hrs =(alarm_time_hrs + 1)% 24
    update_alarm()

def dec_hrs():
    global alarm_time_hrs
    alarm_time_hrs = (alarm_time_hrs - 1)% 24
    update_alarm()

def inc_min():
    global alarm_time_min
    alarm_time_min =(alarm_time_min + 1)% 60
    update_alarm()
    
def dec_min():
    global alarm_time_min
    alarm_time_min =(alarm_time_min - 1)% 60
    update_alarm()

def toggle_alarm():
    global alarm_setting
    alarm_setting = not alarm_setting
    update_alarm()

# ---- AUDIO ----
# imported from audi_alarm.py



# ---- WEATHER ----
# imported from weather.py

def update_weather():
	global forecast

	try:
		forecast = weather.city_forecast(city_of_interest)
	except:
		"no new weather data received"
	

	weather_label["text"] = "Description: "+ forecast["weather"][0]["description"]
	temperature_label["text"] = "Temperature: {:.1f}°C   Max: {:.1f}°C   Min: {:.1f}°C".format(forecast["main"]["temp"], forecast["main"]["temp_max"], forecast["main"]["temp_min"])
	icon_id = forecast["weather"][0]["icon"]
	icon_url = "https://openweathermap.org/img/wn/"+icon_id+"@2x.png"
	threading.Timer(3600, update_weather).start()

# ------------------GUI-----------------------

root = Tk()
root.title("Smart Clock v1")
root.geometry("800x480")

# create the main sections of the layout, 
# and lay them out
top = Frame(root, bg="black")
top.pack(side=TOP, fill=BOTH, expand=True)

bottom = Frame(root, bg="black")
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

clock_label = Label(root, font=('TkDefaultFont', 32, 'bold'), bg='black', fg="white")
clock_label.pack(in_=top, fill=BOTH, expand=1)

alarm_settings = Frame(bottom, bg="black")
alarm_settings.pack(fill = BOTH, expand=True, side=BOTTOM)

alarm_settings_hrs = Frame(alarm_settings, bg="black")
alarm_settings_hrs.pack(fill = BOTH, expand=True, side=LEFT)

alarm_settings_min = Frame(alarm_settings, bg="black")
alarm_settings_min.pack(fill = BOTH, expand=True, side=RIGHT)

alarm_label = Label(root, font=('TkDefaultFont', 24, 'bold'), bg='black', fg="white")
alarm_label.pack (in_=bottom, fill= BOTH, expand=1)


but_inc_min = Button(root, text="+ min",bg='black', fg="white", width=10, height=2, command=inc_min)
but_dec_min = Button(root, text="- min",bg='black', fg="white", width=10, height=2, command=dec_min)
but_inc_hrs = Button(root, text="+ hrs",bg='black', fg="white", width=10, height=2, command=inc_hrs)
but_dec_hrs = Button(root, text="- hrs",bg='black', fg="white", width=10, height=2, command=dec_hrs)

but_inc_min.pack(in_=alarm_settings_min)
but_dec_min.pack(in_=alarm_settings_min)
but_inc_hrs.pack(in_=alarm_settings_hrs)
but_dec_hrs.pack(in_=alarm_settings_hrs)

but_enable_alarm = Button(root, text="disabled",bg='black', fg="white", width=20, height=2, command=toggle_alarm)
but_enable_alarm.pack(in_=alarm_settings)

city_label = Label(root, bg='black', fg="white",font=('TkDefaultFont', 18))
city_label["text"] = "Weather in: " + city_of_interest
city_label.pack(in_=top)

temperature_label = Label(root, bg='black', fg="white",font=('TkDefaultFont', 18))
temperature_label.pack(in_=top)

weather_label = Label(root, bg='black', fg="white", font=('TkDefaultFont', 18))
weather_label.pack(in_=top)

tick()
update_alarm()
update_weather()

root.mainloop()
