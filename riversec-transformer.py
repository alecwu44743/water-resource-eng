import os
import csv
import json
import pandas as pd
from itertools import islice

from math import sqrt


def make_json(csvFilePath, jsonFilePath):
    data = {}
    
    with open(csvFilePath, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)

        for row in islice(csvReader, 0, None, 3):
            # print(row)
            row["point"] = row["point"].replace("淡", "")
            row["system"] = row["system"].replace(" ", "")
            
            #strat the process of Left Side of the River
            row["L-mode"] = row["L-mode"].replace(" ", "")
            if row["L-mode"] == "支距":
                row["L-mode"] = "distance"
            elif row["L-mode"] == "轉換":
                row["L-mode"] = "transform"
            
            row["L-Ordinate-N(Y)"] = row["L-Ordinate-N(Y)"].replace(" ", "")
            row["L-Ordinate-N(Y)"] = row["L-Ordinate-N(Y)"].replace(",", "")
            row["L-Abscissa-E(X)"] = row["L-Abscissa-E(X)"].replace(" ", "")
            row["L-Abscissa-E(X)"] = row["L-Abscissa-E(X)"].replace(",", "")
            
            row["L-Rel-0-points"] = row["L-Rel-0-points"].replace(" ", "")
            row["L-Rel-0-points"] = row["L-Rel-0-points"].replace(",", "")
            
            row["L-Elevation"] = row["L-Elevation"].replace(" ", "")
            row["L-Elevation"] = row["L-Elevation"].replace(",", "")
            
            #strat the process of Right Side of the River
            row["R-mode"] = row["R-mode"].replace(" ", "")
            if row["R-mode"] == "支距":
                row["R-mode"] = "distance"
            elif row["R-mode"] == "轉換":
                row["R-mode"] = "transform"
            
            row["R-Ordinate-N(Y)"] = row["R-Ordinate-N(Y)"].replace(" ", "")
            row["R-Ordinate-N(Y)"] = row["R-Ordinate-N(Y)"].replace(",", "")
            row["R-Abscissa-E(X)"] = row["R-Abscissa-E(X)"].replace(" ", "")
            row["R-Abscissa-E(X)"] = row["R-Abscissa-E(X)"].replace(",", "")
            
            row["R-Rel-0-points"] = row["R-Rel-0-points"].replace(" ", "")
            row["R-Rel-0-points"] = row["R-Rel-0-points"].replace(",", "")
            
            row["R-Elevation"] = row["R-Elevation"].replace(" ", "")
            row["R-Elevation"] = row["R-Elevation"].replace(",", "")
            
            
            key = row['point']
            data[key] = row
            dx = pow((float(row["R-Abscissa-E(X)"]) - float(row["L-Abscissa-E(X)"])), 2)
            dy = pow((float(row["R-Ordinate-N(Y)"]) - float(row["L-Ordinate-N(Y)"])), 2)
            data[key]['distance'] = pow((dx + dy), 0.5)
            
    with open(jsonFilePath, 'w', encoding='utf-8-sig') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


def readjson2Dict(jsonFilePath):
    global tamsui_json
    with open(jsonFilePath, 'r', encoding='utf-8-sig') as jsonf:
        tamsui_json = json.load(jsonf)


def print_preprocessed_data(x_ext, y_ext):
    print(f" -> after data processing: x_ext: {x_ext}")
    print(f" -> after data processing: y_ext: {y_ext}")


def fix_extdata(file_name, x_ext, y_ext):
    isAcceptable = True
    
    if len(x_ext) != len(y_ext):
        print(f" -> {file_name} data is not complete.")
        isAcceptable = False
    else:
        for list_index in range(len(x_ext)):
            x_ext[list_index] = round(x_ext[list_index], 2)
            y_ext[list_index] = round(y_ext[list_index], 2)
    
    return x_ext, y_ext, isAcceptable


def validate_data(new_x, ex_data, ny_data):
    if len(ex_data) != len(ny_data):
        print("Data is not complete.")
        return False # if the data is not complete
    
    for list_index in range(1, len(ex_data)):
        check_value = sqrt(pow((ex_data[list_index] - ex_data[0]), 2) + pow((ny_data[list_index] - ny_data[0]), 2))
        if abs(check_value - new_x[list_index]) > 0.2:
            print("Data is not correct.")
            return False # if the value is not correct
    
    return True #pass the validation


def pos_transform(raw_data_path):
    if not os.path.exists(raw_data_path):
        print(f"The directory '{raw_data_path}' does not exist.")
        return
    
    if not os.path.isdir(raw_data_path):
        print(f"'{raw_data_path}' is not a directory.")
        return
    
    files = os.listdir(raw_data_path)
    print(f"Files in the directory '{raw_data_path}':")
    
    month_id = ["120", "100", "050"]
    status = "pass"
    declined_list = []
    not_found_rel0points = []
    for file_name in files:
        #message for processing the file
        print(f"Processing '{file_name}'...", end="")
        
        for month in month_id:
            if file_name.find(month) == -1:
                continue
            
            mid_index = file_name.find(month)
            year = file_name[1:mid_index]
            river_section = file_name[mid_index+2:]
            river_section = river_section.replace("csv", "")
            river_section = river_section.replace(".", "")
            
            print(f" -> year: {year}, month: {month}, river_section: {river_section}")
            
            if river_section in list(tamsui_json.keys()):
                print(f" -> {river_section} is ACCEPTED.")
                
                to_open = raw_data_path + "/" + file_name
                with open(to_open, 'r', encoding='utf-8-sig') as csvf:
                    print(f" -> {file_name} is opened.")
                    
                    #read the csv file
                    csv_reader = pd.read_csv(csvf)
                    
                    # Define the column to extract
                    extracted_x = "x"
                    extracted_y = "y"
                    
                    # Extract data using a list comprehension
                    x_ext = csv_reader[extracted_x].tolist()
                    y_ext = csv_reader[extracted_y].tolist()
                    
                    # print(f" -> Extracted data: {extracted_data}")
                    if len(x_ext) == 0 or len(y_ext) == 0:
                        print(f" -> {file_name} data is empty.")
                        break
                    elif len(x_ext) != len(y_ext):
                        print(f" -> {file_name} data is not complete.")
                        break
                    else:
                        print(f" -> {file_name} data is complete.")
                    
                    if x_ext[0] > x_ext[-1]:
                        print(f" -> range check failed. [{x_ext[0]}, {x_ext[-1]}]")
                    
                    # print(f" -> x_ext: {x_ext}")
                    # print(f" -> y_ext: {y_ext}")
                    
                    R_rel_0_points = tamsui_json[river_section]["R-Rel-0-points"] # checking -96.55
                    R_rel_0_points = float(R_rel_0_points)
                    R_elevation = tamsui_json[river_section]["R-Elevation"]
                    R_elevation = float(R_elevation)
                    L_rel_0_points = tamsui_json[river_section]["L-Rel-0-points"] # checking -96.55
                    L_rel_0_points = float(L_rel_0_points)
                    L_elevation = tamsui_json[river_section]["L-Elevation"]
                    L_elevation = float(L_elevation)
                    found = False
                    pos = -1
                    
                    if R_rel_0_points in x_ext: # find the value
                        print(f" -> {x_ext[x_ext.index(R_rel_0_points)]} is the R-Rel-0-points.")
                        found = True
                        pos = x_ext.index(R_rel_0_points)
                        x_ext = x_ext[pos:]
                        
                        print(f" -> pos: {pos}")
                        # print_preprocessed_data(x_ext, y_ext)
                    
                    if not found: # Insert values
                        not_found_dict = {file_name: R_rel_0_points}
                        not_found_rel0points.append(not_found_dict)
                        
                        print(f" -> {R_rel_0_points} is NOT found.")
                        
                        for list_index in range(len(x_ext)-1):
                            if x_ext[list_index] < R_rel_0_points and R_rel_0_points < x_ext[list_index+1]:
                                pos = list_index
                                found = True
                                
                                print(f" -> {file_name} insert value.")
                                x_ext.insert(pos+1, R_rel_0_points)
                                y_ext.insert(pos+1, R_elevation)
                                break
                        
                        if found:
                            print(f" -> {R_rel_0_points} is between {x_ext[pos]} and {x_ext[pos+2]}.")
                            print(f" -> pos: {pos+1}")
                            # print_preprocessed_data(x_ext, y_ext)
                        else:
                            print(f" -> {R_rel_0_points} is NOT between {x_ext[0]} and {x_ext[-1]}.")
                    
                    if L_rel_0_points in x_ext: # find the value
                        print(f" -> {x_ext[x_ext.index(L_rel_0_points)]} is the L-Rel-0-points.")
                        found = True
                        pos = x_ext.index(L_rel_0_points)
                        x_ext = x_ext[:pos]
                        
                        print(f" -> pos: {pos}")
                        # print_preprocessed_data(x_ext, y_ext)
                    
                    if not found: # Insert values
                        not_found_dict = {file_name: L_rel_0_points}
                        not_found_rel0points.append(not_found_dict)
                        
                        print(f" -> {L_rel_0_points} is NOT found.")
                        
                        for list_index in range(len(x_ext)-1):
                            if x_ext[list_index] < L_rel_0_points and L_rel_0_points < x_ext[list_index+1]:
                                pos = list_index
                                found = True
                                
                                print(f" -> {file_name} insert value.")
                                x_ext.insert(pos+1, L_rel_0_points)
                                y_ext.insert(pos+1, L_elevation)
                                break
                        
                        if found:
                            print(f" -> {L_rel_0_points} is between {x_ext[pos]} and {x_ext[pos+2]}.")
                            print(f" -> pos: {pos+1}")
                            # print_preprocessed_data(x_ext, y_ext)
                        else:
                            print(f" -> {L_rel_0_points} is NOT between {x_ext[0]} and {x_ext[-1]}.")
                    
                    

                    print(f" -> {file_name} is doing fixing.")
                    x_ext, y_ext, isAcceptable = fix_extdata(file_name, x_ext, y_ext)
                    
                    if not isAcceptable:
                        print(f" -> ERROR occurred in {file_name}.")
                        break
                    
                    # print(f" -> after fixing - round(numebr, 2): x_ext: {x_ext}")
                    # print(f" -> after fixing - round(numebr, 2): y_ext: {y_ext}")
                    
                    print(f" -> removing duplicated data in {file_name}.")
                    xtemp = []
                    ytemp = []
                    now = x_ext[0]
                    xtemp.append(x_ext[0])
                    ytemp.append(y_ext[0])
                    for list_index in range(1, len(x_ext)):
                        if x_ext[list_index] != now:
                            xtemp.append(x_ext[list_index])
                            ytemp.append(y_ext[list_index])
                        now = x_ext[list_index]
                    
                    if len(xtemp) != len(ytemp):
                        print(f" -> ERROR occurred in the process of removing duplicated data in {file_name}.")
                        break
                    
                    x_ext = xtemp
                    y_ext = ytemp
                    
                    del xtemp
                    del ytemp
                    
                    '''
                    This is a exmple for using the function of validate_data(new_x, ex_data, ny_data)
                    
                    90A:
                    test_new_x = [0.0000, 4.7300, 12.1500, 14.3600]
                    test_ex_data = [275470.255, 275474.1711, 275480.3151, 275482.1451]
                    test_ny = [2746480.522, 2746477.8695, 2746473.7094, 2746472.4703]
                    
                    if validate_data(test_new_x, test_ex_data, test_ny):
                        print(" -> Data is correct.")
                    else:
                        print(f" -> A validation error occurred in the process of removing duplicated data in {file_name}.")
                        break
                    '''
                    
                    
                    
                    # print(f" -> after removing duplicated data: x_ext: {x_ext}")
                    # print(f" -> after removing duplicated data: y_ext: {y_ext}")
                    
                    print(f" -> Process of {file_name} is all done.\n")
            else:
                print(f" -> {river_section} is DECLINED.\n")
                declined_list.append(river_section)
            
            break
    
    print(f"Declined list: {declined_list}")
    print(f"Total declined: {len(declined_list)}") # 4898
    print()
    #print Not found Rel-0-points line by line
    # for not_found in not_found_rel0points:
    #     print(f"Not found Rel-0-points: {not_found}")
    # print(f"Total not found Rel-0-points: {len(not_found_rel0points)}")
    
    # print(f"\n{len(files)} files in total.")



if __name__ == "__main__":
    dataFilePath = r"./data/"
    csvFilePath = r"tamsui_new.csv"
    jsonFilePath = r"tamsui.json"
    
    raw_data_path = "./result_all" #Today is a good day xD

    nonduplicated_data_path = "./result_non-duplicated"
    save_data_path = "./result_non-duplicated" #commit
    
    # make_json(dataFilePath + csvFilePath, jsonFilePath) #make json file
    readjson2Dict(jsonFilePath) #read json
    
    pos_transform(raw_data_path)
    
    # print(tamsui_json)