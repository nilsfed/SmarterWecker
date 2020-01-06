import requests
import api_keys
from tkinter import *
import os
import io
# allows for image formats other than gif
from PIL import Image, ImageTk
import tkinter as tk
from urllib.request import urlopen

#cities = ["London,uk", "Porto,pt", "Paris,fr"]
#weather_dict = {}

def city_forecast(city):
  response = requests.get(
          "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+api_keys.open_weather_key+"&units=metric"
  )
  print("request")
  return response.json()

#for city in cities:
#  weather_dict[city] = city_forecast(city)

city_of_interest = "Karlsruhe,de"

forecast = city_forecast(city_of_interest)
print(forecast)
icon_id = forecast["weather"][0]["icon"]
url = "https://openweathermap.org/img/wn/"+icon_id+"@2x.png"


root = Tk()
root.title("Weather v1")
root.geometry("800x480")

city_label = Label(root, font=('times', 32, 'bold'), bg='black', fg="white")
city_label["text"] = city_of_interest
city_label.pack()
canvas = Canvas(root, width=500, height=300, bg="grey")
canvas.pack()

image_bytes = urlopen(url).read()
# internal data file
data_stream = io.BytesIO(image_bytes)
# open as a PIL image object
pil_image = Image.open(data_stream)

tk_image = ImageTk.PhotoImage(pil_image)

canvas.create_image(250, 250, image=tk_image)

weather_label = Label(root, font=('times', 32, 'bold'), bg='black', fg="white")
weather_label["text"] = forecast["weather"][0]["description"]
weather_label.pack()

root.mainloop()