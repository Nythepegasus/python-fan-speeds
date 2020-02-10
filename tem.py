#!/usr/bin/env python3
import glob, re, os, sys, subprocess, csv
from time import sleep
from decimal import Decimal

# Config Stuffs
DEBUG = False
path = "/sys/devices/platform/applesmc.768/"
files = [re.search(r'\d+', filepath.strip(path)).group(0) for filepath in glob.iglob(f"{path}temp*_input") if re.search(r'\d+', filepath.strip(path))]
temps, screwy = dict(), dict()
sensor_names = {
    "TCXC" : "PECI CPU",
    "TH0x" : "",
    "Ts1S" : "",
    "TB1T" : "Battery 1",
    "TPCD" : "PCH Die",
    "TC1C" : "CPU Core 1",
    "TH0a" : "",
    "Ts0P" : "Palm Rest 1",
    "TH0A" : "",
    "Ts2S" : "",
    "TB2T" : "Battery 2",
    "TCGC" : "PECI GPU",
    "TH0b" : "",
    "Ts0S" : "Memory Proximity",
    "TA0P" : "Airflow 1",
    "TH0B" : "",
    "TM0P" : "Mem Bank A1",
    "TBXT" : "Battery (???)",
    "TH0V" : "",
    "Th1H" : "Heatpipe 2",
    "TCSA" : "PECI SA",
    "TC0P" : "CPU 1 Proximity",
    "TH0c" : "",
    "Ts1P" : "Palm Rest 2",
    "TB0T" : "Battery TS_MAX",
    "TH0C" : ""
}

# Debug UID
if DEBUG:
    print(f"Current UID: {os.getuid()}\n")

# Function defs
def conf_read(conf="test.csv"):
    gend = ""
    with open(conf, "r") as csv_file:
        first = csv_file.readline()
        t, r = first[0], first[1]
        woowee = f"if temp <= {t}:" + "\n\twith open(f\"{path}fan1_output\", \"w\") as f:\n\t\t" + f"f.write(\"{r}\")"
        gend += woowee
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            t, r = line[0], line[1]
            woowee = "\n" + f"elif temp <= {t}:" + "\n\twith open(f\"{path}fan1_output\", \"w\") as f:\n\t\t" + f"f.write(\"{r}\")"
            gend += woowee
    return gend

def conf_write():
    """Needs made, but configs can be used right now"""
    pass

def user_main():
    """All of these things can be ran as any user, because you can read from every file, the tricky bit is being able to write to any file."""
    with open(f"{path}fan1_input", "r") as f:
        fanspeed = int(f.read().strip("\n"))
        print(f"Current fan speed: {fanspeed} rpm\n")
    for i in files:
        with open(f"{path}temp{i}_input", "r") as t, open(f"{path}temp{i}_label", "r") as l:
            temp, label = float(t.read().strip("\n"))/1000, l.read().strip("\n")
            if temp > 0:
                print(f"{label}:\t\t +{Decimal(temp).quantize(Decimal(10) ** -2)}°C\t\t\t{sensor_names[label]}")
                temps.update({label : temp})
            else:
                screwy.update({label : temp})
    temp = temps['TC1C']
    if DEBUG:
        print(f"DEBUG INFO:\nThe average overall temp: {round(sum(temps.values())/len(temps), 2)}°C\nCPU Temp: {temp}")
        print("\nScrewy labels:\n"+"\n".join(f"{i}: {Decimal(screwy[i]).quantize(Decimal(10) ** -2)}°C" for i in screwy))
    return temp

def root_main():
    """This runs the fan control section of this script. You must be root to write to the necessary files for fan control."""
    temp = user_main()
    with open(f"{path}fan1_manual", "r") as f:
        manual = f.read().strip("\n")
        if DEBUG:
            print(f"Fan manual {manual}")
        if manual == "0":
            write = True
        else:
            write = False
    if write:
        with open(f"{path}fan1_manual", "w") as f:
            f.write("1")
    else:
        if DEBUG:
            print("All good!")
    exec(gend)
    return 0

gend = conf_read()

# CLI options
if len(sys.argv) == 1:
    pass
else:
    if "h" in sys.argv[1]:
        print("You have to put options together (ex. -dc).\n\n-d\t\t\tSet debug flag\n-c\t\t\tSet config file (ex. tem.py -c [configfile])\n-h\t\t\tThis help menu")
        exit()
    if "d" in sys.argv[1]:
        DEBUG = True
    if "c" in sys.argv[1] and os.getuid() == 0:
        try:
            config = sys.argv[2]
            gend = conf_read(config)
        except IndexError:
            print("Error: No config file provided.")
    elif "c" in sys.argv[1] and os.getuid() != 0:
        print("Error: Must be root to use config files.")

# Finally, run the script
if os.getuid() == 0:
    while True:
        root_main()
        sleep(1.2)
        os.system("clear")
else:
    while True:
        user_main()
        sleep(1.2)
        os.system("clear")
