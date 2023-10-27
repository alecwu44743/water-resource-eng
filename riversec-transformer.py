import os
import csv
import json
import pandas as pd
from itertools import islice

from math import sqrt
#test


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
        # print(f"The delta is {check_value} - {new_x[list_index]} = {abs(check_value - new_x[list_index])} at pos: {list_index}")
        if abs(check_value - new_x[list_index]) > 0.2:
            print("Data is not correct. ")
            # print(f"The delta is {check_value} - {new_x[list_index]} = {abs(check_value - new_x[list_index])}")
            return False # if the value is not correct
    
    return True #pass the validation

def axis_predict_formula(curr_rel_0, last_rel_0, first_axis, last_axis):
    r = (round(curr_rel_0, 2) * (last_axis - first_axis) + (last_rel_0 * first_axis)) / last_rel_0
    # print(f"({round(curr_rel_0, 2)} * ({last_axis} - {first_axis}) + ({last_rel_0} * {first_axis})) / {last_rel_0}")
    # print(f"The result of predict: {r}")
    return round((round(curr_rel_0, 2) * (last_axis - first_axis) + (last_rel_0 * first_axis)) / last_rel_0, 4) # the formula to predict next value of axis(x or y)


def tr_write_csv(filename, elevation, ex_data, ny_data):
    transform_df = pd.DataFrame()
    
    transform_df['elevation'] = elevation
    
    transform_df['ex_data'] = ex_data
    transform_df['ny_data'] = ny_data

    # if filename[1] != 1:
    #     part1 = filename[:3]
    #     part2 = filename[3:6]
    #     part3 = filename[6:]

    filename = "./TRANSFORM/" + "TRANSFORM_" + filename
    
    pd.set_option('display.float_format', '{:.5f}'.format)
    
    print(transform_df)
    transform_df.to_csv(filename, index=False)


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
    Correct_list = []
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
                    
                    print(f" -> x_ext: {x_ext} len: {len(x_ext)}")
                    print(f" -> y_ext: {y_ext} len: {len(y_ext)}")

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
                    
                    if R_rel_0_points in x_ext: # find the value (Right side)
                        print(f" -> {x_ext[x_ext.index(R_rel_0_points)]} is the R-Rel-0-points.")
                        found = True
                        pos = x_ext.index(R_rel_0_points)

                        for list_index in range(len(x_ext)-1): 
                            if(x_ext[list_index] == x_ext[pos] and y_ext[list_index] == R_elevation):
                                pos = list_index # the currect position of rel_0
                                continue
                            elif(x_ext[list_index] == x_ext[pos]): # remove the duplicated rel_0
                                x_ext.remove(x_ext[list_index])
                                y_ext.remove(y_ext[list_index])

                            if(x_ext[list_index] > x_ext[pos]):
                                break
                        
                        point_found = False # the flag of finding the correct index with correct rel_0 and elevation
                        for list_value in x_ext[:]:
                            list_index = x_ext.index(list_value)
                            print(f" -> check {list_index}'s {list_value} {R_rel_0_points} at {y_ext[list_index]} {round(R_elevation,2)}")
                            if(list_value == R_rel_0_points):
                                if(y_ext[list_index] == round(R_elevation,2)):
                                    pos = list_index # the currect position of rel_0
                                    point_found = True # find the correct index
                                    print(f" -> {list_value} at {list_index} is the corrert value")
                                    continue 
                                else: # remove the duplicated rel_0
                                    x_ext.remove(list_value)
                                    y_ext.remove(y_ext[list_index])

                            if(list_value > R_rel_0_points):
                                break
                        
                        if(not point_found): # not find the correct index -> using forced insertion
                            print(f" -> Forced inserting {R_rel_0_points} {round(R_elevation,2)} to list")
                            x_ext.insert(pos,R_rel_0_points)
                            y_ext.insert(pos,round(R_elevation,2))
                            point_found = True 

                        x_ext = x_ext[:pos+1]
                        y_ext = y_ext[:pos+1]

                        print(f" -> pos: {pos}")
                        # print_preprocessed_data(x_ext, y_ext)
                    
                    if not found: # Insert values (Right side)
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

                                x_ext = x_ext[:pos+2]
                                y_ext = y_ext[:pos+2]

                                break
                        
                        if found:
                            pos = x_ext.index(R_rel_0_points)
                            print(f" -> pos: {pos+1}")
                            # print_preprocessed_data(x_ext, y_ext)
                        else:
                            print(f" -> {R_rel_0_points} is NOT between {x_ext[0]} and {x_ext[-1]}.")
                            print(f" -> Appending {R_rel_0_points}, {R_elevation} to the end of x_ext and y_ext list ...")
                            x_ext.append(R_rel_0_points)
                            y_ext.append(R_elevation)
                    
                    found = False # Reset found to false for left side
                    
                    if L_rel_0_points in x_ext: # find the value (Left side)
                        print(f" -> {x_ext[x_ext.index(L_rel_0_points)]} is the L-Rel-0-points.")
                        found = True
                        pos = x_ext.index(L_rel_0_points)
            
                        point_found = False # the flag of finding the correct index with correct rel_0 and elevation
                        for list_value in x_ext[:]:
                            list_index = x_ext.index(list_value)
                            print(f" -> check {list_index}'s {list_value} {L_rel_0_points} at {y_ext[list_index]} {round(L_elevation,2)}")
                            if(list_value == L_rel_0_points):
                                if(y_ext[list_index] == round(L_elevation,2)):
                                    pos = list_index # the currect position of rel_0
                                    point_found = True # find the correct index
                                    print(f" -> {list_value} at {list_index} is the corrert value")
                                    continue 
                                else: # remove the duplicated rel_0
                                    x_ext.remove(list_value)
                                    y_ext.remove(y_ext[list_index])

                            if(list_value > L_rel_0_points):
                                break
                        
                        if(not point_found): # not find the correct index -> using forced insertion
                            print(f" -> Forced inserting {L_rel_0_points} {round(L_elevation,2)} to list")
                            x_ext.insert(pos,L_rel_0_points)
                            y_ext.insert(pos,round(L_elevation,2))
                            point_found = True   

                        x_ext = x_ext[pos:]
                        y_ext = y_ext[pos:]

                        print(f" -> pos: {pos}")
                    
                    if not found: # Insert values (Left side)
                        not_found_dict = {file_name: L_rel_0_points}
                        not_found_rel0points.append(not_found_dict)
                        
                        print(f" -> {L_rel_0_points} is NOT found.")
                        # print(f" -> x_ext : {x_ext}")
                        for list_index in range(len(x_ext)-1):
                            if x_ext[list_index] < L_rel_0_points and L_rel_0_points < x_ext[list_index+1]:
                                pos = list_index
                                found = True
                                
                                print(f" -> {file_name} insert value.")
                                x_ext.insert(pos+1, L_rel_0_points)
                                y_ext.insert(pos+1, L_elevation)

                                x_ext = x_ext[pos+1:]
                                y_ext = y_ext[pos+1:]
                                break
                        
                        if found:
                            pos = x_ext.index(L_rel_0_points)
                            print(f" -> pos: {pos+1}")
                        else:
                            print(f" -> {L_rel_0_points} is NOT between {x_ext[0]} and {x_ext[-1]}.")
                            print(f" -> Inserting {L_rel_0_points}, {L_elevation} to the head of x_ext and y_ext list ...")
                            x_ext.insert(0,L_rel_0_points)
                            y_ext.insert(0,L_elevation)

                    print(f" -> x_ext: {x_ext} len: {len(x_ext)}")
                    print(f" -> y_ext: {y_ext} len: {len(y_ext)}")

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
                    for list_index in range(1, len(x_ext)-1):
                        if x_ext[list_index] != now:
                            xtemp.append(x_ext[list_index])
                            ytemp.append(y_ext[list_index])
                        now = x_ext[list_index]
                    xtemp.append(x_ext[-1])
                    ytemp.append(y_ext[-1])

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

                    print(f" -> after removing duplicated data: x_ext: {x_ext} len: {len(x_ext)}")
                    print(f" -> after removing duplicated data: y_ext: {y_ext} len: {len(y_ext)}")
                    
                    L_Ordinate_N_Y = tamsui_json[river_section]["L-Ordinate-N(Y)"]
                    L_Ordinate_N_Y = float(L_Ordinate_N_Y) # first Y
                    L_Abscissa_E_X = tamsui_json[river_section]["L-Abscissa-E(X)"]
                    L_Abscissa_E_X = float(L_Abscissa_E_X) # first X
                    R_Ordinate_N_Y = tamsui_json[river_section]["R-Ordinate-N(Y)"]
                    R_Ordinate_N_Y = float(R_Ordinate_N_Y) # last Y
                    R_Abscissa_E_X = tamsui_json[river_section]["R-Abscissa-E(X)"]
                    R_Abscissa_E_X = float(R_Abscissa_E_X) # last X
                    axis_x_predict_list = []
                    axis_y_predict_list = []
                    print(f" -> Computing the value of axis in {file_name}.")
                    axis_x_predict_list.append(L_Abscissa_E_X)
                    axis_y_predict_list.append(L_Ordinate_N_Y)
                    x_ext[-1] -= x_ext[0]
                    
                    for index in range(1,len(x_ext)-1):
                        x_ext[index] -= x_ext[0]
                        # parameter => curr_rel_0, last_rel_0, first_axis, last_axis
                        predict_x = axis_predict_formula(x_ext[index],x_ext[-1],L_Abscissa_E_X,round(R_Abscissa_E_X,3))
                        predict_y = axis_predict_formula(x_ext[index],x_ext[-1],L_Ordinate_N_Y,round(R_Ordinate_N_Y,3))
                        axis_x_predict_list.append(predict_x)
                        axis_y_predict_list.append(predict_y)
                    axis_x_predict_list.append(R_Abscissa_E_X)
                    axis_y_predict_list.append(R_Ordinate_N_Y)
                    
                    x_ext[0] = 0
                    isVaild = validate_data(x_ext, axis_x_predict_list, axis_y_predict_list)
                    if(isVaild):
                        Correct_list.append(river_section)
                        print(" -> Data is correct.")
                        print(f" -> Writing the data to csv file in {file_name}.")
                        tr_write_csv(file_name, y_ext, axis_x_predict_list, axis_y_predict_list)
                        
                        print(f" -> {file_name} is all done.\n")
                    
                    print(f" -> Process of {file_name} is all done.\n")
            else:
                print(f" -> {river_section} is DECLINED.\n")
                declined_list.append(river_section)
            
            break
    
    print(f"Correct list: {Correct_list}")
    print(f"Total correct: {len(Correct_list)}") 
    print()
    print(f"Declined list: {declined_list}")
    print(f"Total declined: {len(declined_list)}") # 4898
    print()
    #print Not found Rel-0-points line by line
    # for not_found in not_found_rel0points:
    #     print(f"Not found Rel-0-points: {not_found}")
    # print(f"Total not found Rel-0-points: {len(not_found_rel0points)}")
    
    # print(f"\n{len(files)} files in total.")


def merge_csv(files_path):
    files = os.listdir(files_path)
    
    month_id = ["120", "100", "050"]
    last_year = ""
    merged_data = pd.DataFrame()
    
    for file_name in files:
        for month in month_id:
            if file_name.find(month) == -1:
                continue
    
            mid_index = file_name.find(month)
            year = file_name[10:mid_index]

            if year != last_year :
                if last_year == "":
                    print(f"./MERGE  is not a directory.")
                    last_year = year

                elif not merged_data.empty:
                    output_file = "./MERGE/" + "MERGE_" + last_year + ".csv"
                    print(last_year)
                    merged_data.to_csv(output_file, index=False)

                merge_files = os.listdir("./MERGE")
                for merge_file_name in merge_files:
                    mid_index = merge_file_name.find(".")
                    merge_year = merge_file_name[6:mid_index]
                    # print(merge_year)
                    if merge_year == year:
                        last_year = year
                        # print("Already exists: " + year)
                        merged_data = pd.read_csv(os.path.join("./MERGE", merge_file_name), encoding='utf-8-sig')
                        break
                    else:
                        last_year = year
                        merged_data = pd.DataFrame()
                        # print("New: " + year)
                    
            # print(f" -> year: {year} last_year: {last_year}")

            to_open = files_path + "/" + file_name
            with open(to_open, 'r', encoding='utf-8-sig') as csvf:
                    csv_reader = pd.read_csv(csvf)
                    merged_data = merged_data._append(csv_reader, ignore_index=True)

    if not merged_data.empty:
        output_file = "./MERGE/" + "MERGE_" + last_year + ".csv"
        merged_data.to_csv(output_file, index=False)






if __name__ == "__main__":
    dataFilePath = r"./data/"
    csvFilePath = r"tamsui_new.csv"
    jsonFilePath = r"tamsui.json"
    mergeCsvPath = r"./merge/"
    
    raw_data_path = "/Users/wufangyi/result_all" #Today is a good day xD

    nonduplicated_data_path = "/Users/wufangyi/result_non-duplicated"
    save_data_path = "/Users/wufangyi/result_non-duplicated" #commit
    
    transformed_data_path = "/Users/wufangyi/TRANSFORM"
    
    
    # make_json(dataFilePath + csvFilePath, jsonFilePath) #make json file
    # readjson2Dict(jsonFilePath) #read json
    
    # os.mkdir("./TRANSFORM")
    # pos_transform(raw_data_path)
    
    os.mkdir("./MERGE")
    # merge the csv files of each year
    merge_csv(transformed_data_path)
    
    # print(tamsui_json)