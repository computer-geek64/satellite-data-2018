# Data.py
# Ashish D'Souza and Stephen Brown
# July 25th, 2018
#    _____       __       _____ __          ____        __            ____               _           __
#   / ___/____ _/ /____  / / (_) /____     / __ \____ _/ /_____ _    / __ \_________    (_)__  _____/ /_
#   \__ \/ __ `/ __/ _ \/ / / / __/ _ \   / / / / __ `/ __/ __ `/   / /_/ / ___/ __ \  / / _ \/ ___/ __/
#  ___/ / /_/ / /_/  __/ / / / /_/  __/  / /_/ / /_/ / /_/ /_/ /   / ____/ /  / /_/ / / /  __/ /__/ /_
# /____/\__,_/\__/\___/_/_/_/\__/\___/  /_____/\__,_/\__/\__,_/   /_/   /_/   \____/_/ /\___/\___/\__/
#                                                                                 /___/

import os
from selenium import webdriver
import time


def search(keywords: str) -> None:
    browser = webdriver.Chrome()
    browser.minimize_window()
    browser.get("https://disc.gsfc.nasa.gov/datasets?keywords=" + keywords.replace(" ", "%20") + "&page=1")
    time.sleep(5)
    pages = len(browser.find_elements_by_class_name("pagination-page"))
    names = []
    links = []
    disciplines = []
    sources = []
    temporal_resolution = []
    spatial_resolution = []
    process_level = []
    begin_date = []
    end_date = []
    count = 0
    for page in range(pages):
        browser.get("https://disc.gsfc.nasa.gov/datasets?keywords=" + keywords.replace(" ", "%20") + "&page=" + str(page + 1))
        time.sleep(5)
        results = browser.find_elements_by_css_selector("tr[ng-repeat]")
        for i in range(len(results)):
            names.append(results[i].find_element_by_class_name("rowCell-dataset").find_element_by_tag_name("a").text)
            links.append(results[i].find_element_by_class_name("rowCell-dataset").find_element_by_tag_name("a").get_attribute("href"))
            disciplines.append(results[i].find_element_by_class_name("rowCell-dataset").find_element_by_tag_name("span").text.split("- ")[1])
            sources.append(results[i].find_element_by_class_name("rowCell-source").text)
            temporal_resolution.append(results[i].find_element_by_class_name("rowCell-tempRes").text)
            spatial_resolution.append(results[i].find_element_by_class_name("rowCell-spatialRes").text)
            process_level.append(results[i].find_element_by_class_name("rowCell-processLevel").text)
            begin_date.append(results[i].find_element_by_class_name("rowCell-startDate").text)
            end_date.append(results[i].find_element_by_class_name("rowCell-endDate").text)
            print(str(count + 1) + ": " + names[i])
            print("\tDiscipline: " + disciplines[i])
            print("\tSource: " + sources[i])
            print("\tTemporal Resolution: " + temporal_resolution[i])
            print("\tSpatial Resolution: " + spatial_resolution[i])
            print("\tProcess Level: " + process_level[i])
            print("\tTime: " + begin_date[i] + " to " + end_date[i])
            count += 1

    if len(names) == 0:
        print("Internet connection error. Exiting...")
        browser.close()
        exit(0)
    selection = int(input("Please select a dataset to download:\n"))
    browser.get(links[selection - 1])
    time.sleep(5)
    link = browser.find_element_by_css_selector("a[title*=HTTP].btn").get_attribute("href")
    print("Downloading from source: " + link)
    download("C:/Users/skillsusa/Documents/SatelliteData/Websites", link, "", True)
    if link.split("/")[-1] != "":
        folder = link.split("/")[-1]
    else:
        folder = link.split("/")[-2]
    if not os.path.exists("C:/Users/skillsusa/Documents/SatelliteData/Data/" + folder):
        os.mkdir("C:/Users/skillsusa/Documents/SatelliteData/Data/" + folder)
    download("C:/Users/skillsusa/Documents/SatelliteData/Data/" + folder, link, "-A .nc,.nc4,.hdf,.he5 -nd -R .tmp", True)
    os.system("del /S /Q *.tmp")
    print("Download completed successfully.")
    browser.close()


# Downloads the dataset using filepath and url parameters, and returns the absolute filename of the downloaded dataset
def download(filepath: str, url: str, options: str, recursive: bool) -> str:
    # Changes working directory
    os.chdir(filepath)
    # Cookie authentication
    wget =  "C:/Users/skillsusa/Documents/wget.exe"
    cookies_file = "C:/Users/skillsusa/Documents/SatelliteData/Cookies/.urs_cookies"
    if recursive:
        os.system(wget + " "[:len(options)] + options + " -r -np --load-cookies " + cookies_file + " --save-cookies " + cookies_file + " --keep-session-cookies --content-disposition \"" + url + "\"")
    else:
        os.system(wget + " "[:len(options)] + options + " --load-coookies " + cookies_file + " --save-cookies " + cookies_file + " --keep-session-cookies --content-disposition \"" + url + "\"")
    # Alternative method without using cookies
    # os.system("wget --user=ashish.dsouza --ask-password \"" + url + "\")

    # Returns a string representation of the downloaded file, using a combination of the filepath and url
    return filepath + "/" + url.split("/")[-1]


search(input("Keyword search:\n"))
