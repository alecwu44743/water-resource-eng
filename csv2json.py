import os
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
            
            row["L-mode"] = row["L-mode"].replace(" ", "")
            if row["L-mode"] == "支距":
                row["L-mode"] = "distance"
            elif row["L-mode"] == "轉換":
                row["L-mode"] = "transform"
            
            row["L-Ordinate-N(Y)"] = row["L-Ordinate-N(Y)"].replace(" ", "")
            row["L-Ordinate-N(Y)"] = row["L-Ordinate-N(Y)"].replace(",", "")
            row["L-Abscissa-E(X)"] = row["L-Abscissa-E(X)"].replace(" ", "")
            row["L-Abscissa-E(X)"] = row["L-Abscissa-E(X)"].replace(",", "")
            
            row["Rel-0-points"] = row["Rel-0-points"].replace(" ", "")
            row["Rel-0-points"] = row["Rel-0-points"].replace(",", "")
            
            row["R-mode"] = row["R-mode"].replace(" ", "")
            if row["R-mode"] == "支距":
                row["R-mode"] = "distance"
            elif row["R-mode"] == "轉換":
                row["R-mode"] = "transform"
            
            row["R-Ordinate-N(Y)"] = row["R-Ordinate-N(Y)"].replace(" ", "")
            row["R-Abscissa-E(X)"] = row["R-Abscissa-E(X)"].replace(" ", "")
            
            
            key = row['point']
            data[key] = row
            
    with open(jsonFilePath, 'w', encoding='utf-8-sig') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


def pos_transform(raw_data_path):
    if not os.path.exists(raw_data_path):
        print(f"The directory '{raw_data_path}' does not exist.")
        return
    
    if not os.path.isdir(raw_data_path):
        print(f"'{raw_data_path}' is not a directory.")
        return
    
    files = os.listdir(raw_data_path)
    print(f"Files in the directory '{raw_data_path}':")
    for file_name in files:
        print(file_name)
    
    # print(f"\n{len(files)} files in total.")



if __name__ == "__main__":
    dataFilePath = r"./data/"
    csvFilePath = r"tamsui.csv"
    jsonFilePath = r"tamsui.json"
    
    raw_data_path = "../river-prediction-nstc/result_non-duplicated"
    save_data_path = "../river-prediction-nstc/result_non-duplicated"
    
    # make_json(dataFilePath + csvFilePath, jsonFilePath)
    pos_transform(raw_data_path)