# Regression.py
# Ashish D'Souza and Stephen Brown
# July 26th, 2018
#    _____       __       _____ __          ____        __            ____               _           __
#   / ___/____ _/ /____  / / (_) /____     / __ \____ _/ /_____ _    / __ \_________    (_)__  _____/ /_
#   \__ \/ __ `/ __/ _ \/ / / / __/ _ \   / / / / __ `/ __/ __ `/   / /_/ / ___/ __ \  / / _ \/ ___/ __/
#  ___/ / /_/ / /_/  __/ / / / /_/  __/  / /_/ / /_/ / /_/ /_/ /   / ____/ /  / /_/ / / /  __/ /__/ /_
# /____/\__,_/\__/\___/_/_/_/\__/\___/  /_____/\__,_/\__/\__,_/   /_/   /_/   \____/_/ /\___/\___/\__/
#                                                                                 /___/

import tensorflow as tf
import numpy as np
from gmplot import gmplot
import os


def univariate_linear_regression(x_training_data, y_training_data, training_iterations):
    y = tf.constant(np.array(y_training_data), dtype=tf.float32, name="y")
    x = tf.constant(np.array(x_training_data), dtype=tf.float32, name="x")
    bias = tf.Variable(1.0, dtype=tf.float32, name="bias")
    weight = tf.Variable(1.0, dtype=tf.float32, name="weight")
    linear_model = weight * x + bias
    loss = tf.reduce_sum(tf.square(linear_model - y))
    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)
    optimizer = tf.train.GradientDescentOptimizer(0.01)
    training = optimizer.minimize(loss)
    for i in range(training_iterations):
        sess.run(training)
    return sess.run([tf.get_default_graph().get_tensor_by_name("bias:0"), tf.get_default_graph().get_tensor_by_name("weight:0")])


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


def predict(data, lat_array, lon_array, x, standard_deviations, spatial_resolution, map_name):
    gmap = gmplot.GoogleMapPlotter((lat_array[0] + lat_array[-1]) / 2, (lon_array[0] + lon_array[-1]) / 2, 3)

    predictions = []
    percentage = -1
    print("[-] Predicting data...")
    for lat in range(len(data[0])):
        predictions.append([])
        for lon in range(len(data[0][lat])):
            y_training_data = []
            for geo_slice in range(len(data)):
                y_training_data.append(data[geo_slice][lat][lon])
            prediction = univariate_linear_regression(list(range(len(y_training_data))), y_training_data, 100)
            predictions[lat].append(prediction[0] + prediction[1] * x)
            if exact_round(lat / (len(lat_array) - 1) * 100) != percentage:
                percentage = exact_round(lat / (len(lat_array) - 1) * 100)
                os.system("cls" if os.name == "nt" else "clear")
                if percentage != 100:
                    print("\t" + str(percentage) + "%\t [" + "=" * percentage + ">" + " " * (100 - percentage) + "]")
                else:
                    print("\t100% [" + "=" * 100 + ">]")
    print("[+] Data prediction finished.")
    print("[-] Extracting data...")
    standard_deviation = np.std(np.array(predictions))
    average = np.average(np.array(predictions))
    increment = 0
    maximum = 0
    datapoints = []
    percentage = -1
    for lat in range(len(predictions)):
        for lon in range(len(predictions[lat])):
            if predictions[lat][lon] <= standard_deviation * standard_deviations + average and predictions[lat][lon] > 0:
                datapoints.append([])
                datapoints[increment].append(lat)
                datapoints[increment].append(lon)
                if predictions[lat][lon] > maximum:
                    maximum = predictions[lat][lon]
                increment += 1
        if exact_round(lat / (len(lat_array) - 1) * 100) != percentage:
            percentage = exact_round(lat / (len(lat_array) - 1) * 100)
            os.system("cls" if os.name == "nt" else "clear")
            if percentage != 100:
                print("\t" + str(percentage) + "%\t [" + "=" * percentage + ">" + " " * (100 - percentage) + "]")
            else:
                print("\t100% [" + "=" * 100 + ">]")
    print("[+] Data extraction finished.")
    print("[-] Plotting data...")
    percentage = -1
    for i in range(len(datapoints)):
        if rgb(scale_max(predictions[datapoints[i][0]][datapoints[i][1]], maximum)) != [0, 0, 0]:
            gmap.scatter([predictions[lat_array][datapoints[i][0]]], [predictions[lon_array][datapoints[i][1]]], "#" + hex_color(rgb(scale_max(predictions[datapoints[i][0]][datapoints[i][1]], maximum))), size=sum(spatial_resolution) * 15000, marker=False)
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
