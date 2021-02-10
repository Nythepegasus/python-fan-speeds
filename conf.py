import csv

def conf_read(conf="default.csv"):
    with open(conf, "r") as csv_file:
        first = csv_file.readline()
        csv_reader = csv.reader(csv_file)
        gend = "".join([f"if temp <= {first[0]}:" + "\n\twith open(f\"{path}fan1_output\", \"w\") as f:\n\t\t" + f"f.write(\"{first[1]}\")"] + [f"\nelif temp <= {line[0]}:\n\twith open(f\"{{path}}fan1_output\", \"w\") as f:\n\t\tf.write(\"{line[1]}\")" for line in csv_reader])
    return gend

def conf_write():
    """Needs made, but configs can be used right now"""
    gen_yn = input("Generate config file [Y/n]?")
    if gen_yn.lower() in ["y", ""]:
        print("This is going to loop, to break the loop and write the output to the file, you have to type 'q' and hit enter")
        conf_dict = {}
        while (t := input("Input (temperature, rpm) pair: ")).lower() != "q":
            d = t.split(", ")
            if len(d) != 2:
                print('Error: Must be input like "temp, rpm"!')
                pass
            conf_dict[d[0]] = d[1]
        with open(f"{input('Input file name (note, csv extension is added automagically): ')}.csv", "w") as f:
            writer = csv.writer(f)
            for item in conf_dict.keys():
                writer.writerow([item, conf_dict[item]])
    else:
        print("Exited")
        return 1
