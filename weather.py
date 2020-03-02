import requests
import api_keys
import os
import io
from tkinter import *
# allows for image formats other than gif
from PIL import Image, ImageTk
import tkinter as tk
from urllib.request import urlopen


def city_forecast(city):
  response = requests.get(
          "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+api_keys.open_weather_key+"&units=metric"
  )
  print("request")
  return response.json()

def weather_icon(icon_id):
    print (icon_id)

    url = "https://openweathermap.org/img/wn/"+icon_id+"@2x.png"
    image_bytes = urlopen(url).read()
    # internal data file
    data_stream = io.BytesIO(image_bytes)
    # open as a PIL image object
    pil_image = Image.open(data_stream)

    #tk_image = ImageTk.PhotoImage(pil_image)
    #pil_image.show()
    return pil_image