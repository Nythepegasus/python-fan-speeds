import glob, re, os, sys, subprocess
from decimal import Decimal

# Script Option # TODO: Set this as a cli option
DEBUG = True

# Config Stuffs
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

if DEBUG:
    print(f"Current UID: {os.getuid()}\n")

def user_main():
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
    print(f"\nThe average overall temp: {round(sum(temps.values())/len(temps), 2)}°C\n")
    temp = temps['TC1C']
    print(f"CPU Temp: {temp}")
    print("Screwy labels:\n"+"\n".join(f"{i}: {Decimal(screwy[i]).quantize(Decimal(10) ** -2)}°C" for i in screwy))
    return temp

def root_main():
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
    if temp <= 55.0:
        with open(f"{path}fan1_output", "w") as f:
            f.write("1300")
    elif 55.0 <= temp <= 60.0:
        with open(f"{path}fan1_output", "w") as f:
            f.write("2200")
    elif 60.0 <= temp <= 75.0:
        with open(f"{path}fan1_output", "w") as f:
            f.write("4500")
    elif 75.0 <= temp <= 95.0:
        with open(f"{path}fan1_output", "w") as f:
            f.write("5500")
    elif 95.0 <= temp:
        with open(f"{path}fan1_output", "w") as f:
            f.write("6199")
    return 0

if os.getuid() == 0:
    root_main()
else:
    user_main()
