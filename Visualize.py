# Visualize.py
# Ashish D'Souza and Stephen Brown
# July 25th, 2018
#    _____       __       _____ __          ____        __            ____               _           __
#   / ___/____ _/ /____  / / (_) /____     / __ \____ _/ /_____ _    / __ \_________    (_)__  _____/ /_
#   \__ \/ __ `/ __/ _ \/ / / / __/ _ \   / / / / __ `/ __/ __ `/   / /_/ / ___/ __ \  / / _ \/ ___/ __/
#  ___/ / /_/ / /_/  __/ / / / /_/  __/  / /_/ / /_/ / /_/ /_/ /   / ____/ /  / /_/ / / /  __/ /__/ /_
# /____/\__,_/\__/\___/_/_/_/\__/\___/  /_____/\__,_/\__/\__,_/   /_/   /_/   \____/_/ /\___/\___/\__/
#                                                                                 /___/

import netCDF4
import numpy as np
from gmplot import gmplot
import os


# ----- Variables ----- #
# filename = "C:/Users/skillsusa/Downloads/dataset.nc"
# lat_name = "lat"
# lon_name = "lon"
# dataset_name = "CH4_FLX_CA_TOT"
# map_name = "Map.html"
filename = "C:/Users/skillsusa/Downloads/dataset2.nc"
lat_name = "Lat"
lon_name = "Lon"
dataset_name = "emissions"
map_name = "C:/Users/skillsusa/Documents/SatelliteData/Maps/Map.html"
spatial_resolution = [0.5, 0.667]
standard_deviations = 3


def scale(value, array):
    scaled_value = float(1275 / array.max()) * value
    if scaled_value - int(scaled_value) < 0.5:
        scaled_value = int(scaled_value)
    else:
        scaled_value = int(scaled_value) + 1
    return scaled_value


def scale_max(value, maximum):
    scaled_value = float(1275 / maximum) * value
    if scaled_value - int(scaled_value) < 0.5:
        scaled_value = int(scaled_value)
    else:
        scaled_value = int(scaled_value) + 1
    return scaled_value


def rgb(raw_value):
    red = 0
    green = 0
    blue = 0
    if raw_value == 0:
        return [0, 0, 0]
    elif raw_value < 256:
        red = 255 - raw_value
        blue = 255
    elif raw_value < 511:
        green = raw_value - 255
        blue = 255
    elif raw_value < 766:
        green = 255
        blue = 765 - raw_value
    elif raw_value < 1021:
        red = raw_value - 765
        green = 255
    elif raw_value < 1276:
        red = 255
        green = 1275 - raw_value
    return [red, green, blue]


def hex_color(rgb):
    hex_strings = [hex(rgb[0])[2:], hex(rgb[1])[2:], hex(rgb[2])[2:]]
    for i in range(len(hex_strings)):
        if len(hex_strings[i]) == 1:
            hex_strings[i] = "0" + hex_strings[i]
        elif len(hex_strings[i]) == 0:
            hex_strings[i] = "00"
    return "".join(hex_strings).upper()


def exact_round(a):
    if a - int(a) < 0.5:
        return int(a)
    else:
        return int(a) + 1


def visualize(filename, dataset_name, lat_name, lon_name, spatial_resolution, standard_deviations, map_name):
    dataset = netCDF4.Dataset(filename, "r")

    gmap = gmplot.GoogleMapPlotter((dataset.variables[lat_name][0] + dataset.variables[lat_name][-1]) / 2, (dataset.variables[lon_name][0] + dataset.variables[lon_name][-1]) / 2, 3)

    standard_deviation = np.std(np.array(dataset.variables[dataset_name]))
    average = np.average(np.array(dataset.variables[dataset_name]))
    increment = 0
    maximum = 0
    datapoints = []
    percentage = -1
    print("[-] Extracting data...")
    for lat in range(len(dataset.variables[dataset_name][0])):
        for lon in range(len(dataset.variables[dataset_name][0][lat])):
            if dataset.variables[dataset_name][0][lat][lon] > standard_deviation * standard_deviations + average or dataset.variables[dataset_name][0][lat][lon] < 1:
                continue
            else:
                datapoints.append([])
                datapoints[increment].append(lat)
                datapoints[increment].append(lon)
                if dataset.variables[dataset_name][0][lat][lon] > maximum:
                    maximum = dataset.variables[dataset_name][0][lat][lon]
                increment += 1
        if exact_round(lat / (len(dataset.variables[lat_name]) - 1) * 100) != percentage:
            percentage = exact_round(lat / (len(dataset.variables[lat_name]) - 1) * 100)
            os.system("cls" if os.name == "nt" else "clear")
            if percentage != 100:
                print("\t" + str(percentage) + "%\t [" + "=" * percentage + ">" + " " * (100 - percentage) + "]")
            else:
                print("\t100% [" + "=" * 100 + ">]")
    print("[+] Data extraction finished.")
    print("[-] Plotting data...")
    percentage = -1
    for i in range(len(datapoints)):
        if rgb(scale_max(dataset.variables[dataset_name][0][datapoints[i][0]][datapoints[i][1]], maximum)) != [0, 0, 0]:
            gmap.scatter([dataset.variables[lat_name][datapoints[i][0]]], [dataset.variables[lon_name][datapoints[i][1]]], "#" + hex_color(rgb(scale_max(dataset.variables[dataset_name][0][datapoints[i][0]][datapoints[i][1]], maximum))), size=sum(spatial_resolution) * 15000, marker=False)
        if exact_round(i / (len(datapoints) - 1) * 100) != percentage:
            percentage = exact_round(i / (len(datapoints) - 1) * 100)
            os.system("cls" if os.name == "nt" else "clear")
            if percentage != 100:
                print("\t" + str(percentage) + "%\t [" + "=" * percentage + ">" + " " * (100 - percentage) + "]")
            else:
                print("\t100% [" + "=" * 100 + ">]")
    print("[+] Data plotting finished.")
    print("[-] Rendering map...")
    gmap.draw(map_name)
    print("[+] Map rendering finished.")
    os.system(map_name)
    return map_name


visualize(filename, dataset_name, lat_name, lon_name, spatial_resolution, standard_deviations, map_name)