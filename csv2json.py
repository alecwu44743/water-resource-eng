import csv
import json
import pandas as pd
from itertools import islice


def make_json(csvFilePath, jsonFilePath):
    data = {}
    
    read_csv = pd.read_csv(csvFilePath)
    csv_line = read_csv.shape[0]
    
    with open(csvFilePath, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)

        for row in islice(csvReader, 0, None, 3):
            # print(row)
            row["point"] = row["point"].replace("淡", "")
            row["system"] = row["system"].replace(" ", "")
            row["mode"] = row["mode"].replace(" ", "")
            
            if row["mode"] == "支距":
                row["mode"] = "distance"
            elif row["mode"] == "轉換":
                row["mode"] = "transform"
            
            row["Ordinate-N(Y)"] = row["Ordinate-N(Y)"].replace(" ", "")
            row["Abscissa-E(X)"] = row["Abscissa-E(X)"].replace(" ", "")
            
            
            key = row['point']
            data[key] = row
            
    with open(jsonFilePath, 'w', encoding='utf-8-sig') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


dataFilePath = r"./data/"
csvFilePath = r"tamsui - LEFT.csv"
jsonFilePath = r"tamsui-left.json"

make_json(dataFilePath + csvFilePath, jsonFilePath)