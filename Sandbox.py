# Sandbox.py
# Ashish D'Souza and Stephen Brown
# July 26th, 2018
#    _____       __       _____ __          ____        __            ____               _           __
#   / ___/____ _/ /____  / / (_) /____     / __ \____ _/ /_____ _    / __ \_________    (_)__  _____/ /_
#   \__ \/ __ `/ __/ _ \/ / / / __/ _ \   / / / / __ `/ __/ __ `/   / /_/ / ___/ __ \  / / _ \/ ___/ __/
#  ___/ / /_/ / /_/  __/ / / / /_/  __/  / /_/ / /_/ / /_/ /_/ /   / ____/ /  / /_/ / / /  __/ /__/ /_
# /____/\__,_/\__/\___/_/_/_/\__/\___/  /_____/\__,_/\__/\__,_/   /_/   /_/   \____/_/ /\___/\___/\__/
#                                                                                 /___/

import netCDF4
import Regression


data = []
lat_array = []
lon_array = []
for i in range(1, 13):
    string = str(i)
    if i < 10:
        string = "0" + string
    dataset = netCDF4.Dataset("C:/Users/skillsusa/Downloads/CH4/CH4_flux_2010" + string + "01.nc", "r")
    data.append(dataset.variables["emissions"][0])
    lat_array = dataset.variables["Lat"]
    lon_array = dataset.variables["Lon"]
Regression.predict(data, lat_array, lon_array, 13, 3, [0.5, 0.667], "C:/Users/skillsusa/Downloads/Map.html")