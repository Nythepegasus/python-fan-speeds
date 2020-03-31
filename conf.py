import csv

def conf_read(conf="default.csv"):
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
    gen_yn = input("Generate config file [Y/n]?")
    if gen_yn.lower() == "y" or gen_yn == "":
        print("This is going to loop, to break the loop and write the output to the file, you have to type 'q' and hit enter")
        conf_dict = {}
        first_loop = True
        t, r = "", ""
        while t != "q" or r != "q":
            if first_loop:
                t = input("Input first temperature: ")
                r = input("Input rpm for first interval: ")
                first_loop = False
            else:
                t = input("Input next temperature for interval: ")
                r = input("Input next rpm interval: ")
            conf_dict[t] = r
        try:
            conf_dict.pop("q")
        except KeyError:
            pass
        file_name = input("Input file name (note, csv extension is added automagically): ")
        with open(f"{file_name}.csv", "w") as f:
            writer = csv.writer(f)
            for item in conf_dict.keys():
                writer.writerow([item, conf_dict[item]])

    else:
        print("Exited")
        return 1
