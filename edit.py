#import packages

import json
import os
from tabulate import tabulate
import textwrap
from utils import SAVEANDEXIT

#import other modules of the program
from datablocks import load_metadata, get_metadata_blocks



#globals 

DOWNLOADED_PATH = os.path.join(os.getcwd(), "JSON_metadata_downloads")
EDITED_PATH = os.path.join(os.getcwd(), "JSON_metadata_downloads_edited")

# Check if the output folder for edited files exists, if not, create it
if not os.path.exists(EDITED_PATH):
    os.makedirs(EDITED_PATH)




def save_exit(metadata:dict, filename:str,output_path):  
    global SAVEANDEXIT
    user_input = input(
        "Select Y to exit and save changes in your hard drive. Select N to continue editing: y/n").lower()
    print(f"User input: {user_input}")  # Add this line for debugging
    if user_input == 'y':
        filepath = os.path.join(output_path, filename)
        with open(filepath, "w") as f: 
            json.dump(metadata, f)
        print(f"Changes saved for {filepath}")
        SAVEANDEXIT = True
        
    else:
        SAVEANDEXIT = False
  #  return SAVEANDEXIT    

def select_option():
    while True:
        option = input("Select an option (Y/N): ").lower()
        if option in ['y', 'n']:
            return option
        else:
            print("Invalid option. Please select either Y, N ")


def select_row_or_column():
    while True:
        option = input("Select an option (R/C): ").lower()
        if option in ['r', 'c']:
            return option
        else:
            print("Invalid option. Please select either R or C.")


#Help functions to select and edit metadata

def select_data(metadata:dict, filename:str):
    citation, geo, science, lt_citation, lt_geo, lt_science, other = get_metadata_blocks(metadata)[:7]

    options = {
        "1": (citation, "Citation Metadata"),
        "2": (geo, "Geospatial Metadata"),
        "3": (science, "Social Science Metadata"),
        "4": (lt_citation, "LT Citation Metadata"),
        "5": (lt_geo, "LT Geospatial Metadata"),
        "6": (lt_science, "LT Social Science Metadata"),
        "7": (other, "Other Metadata Blocks")
    }
    print(f"Editing file: {filename}")

    while True:
        print("Please select which select_ you want to edit:")
        for key, (value, name) in options.items():
            print(f"{key}. {name}")

        choice = input("Enter your choice (1-7): ")
        selected = options.get(choice)

        if selected:
            print(f"You selected {selected[1]}.")
            return selected[0]

        print("Invalid choice. Please enter a number between 1 and 7.")


def edit_other_metadata(metadata: dict, filename: str):
    other, other_vars = get_metadata_blocks(metadata)[-2:]
    table_data = []
    for i, k in enumerate(other_vars):
        if k in other:
            value_wrapped = textwrap.fill(other[k], width=45)
            table_data.append([i, k, value_wrapped])
    print(tabulate(table_data, headers=[
          "Index", "Field", "Value (compound = multiple)"], tablefmt="grid"))
    select_row = int(
        input("Please enter the index of the row you want to edit: "))
    print("\nYou selected the following field:")
    print(tabulate([table_data[select_row]], headers=[
          "Index", "Field", "Value (compound = multiple)"], tablefmt="grid"))
    while True:
        to_continue = input(
            "If this is the correct field, select Y to continue. If not, select N to start again: Y / N: ").lower()
        if to_continue == "y":
            new_value = input("Please type in new value: ")
            print(f"New field value: {new_value}")
            to_save = input(
                "If this is correct, select Y to continue and save changes. If not, select N to start again: Y / N: ").lower()
            if to_save == "y":
                other[other_vars[select_row]] = new_value
                print(f"Updated field value: {other[other_vars[select_row]]}")
                break
            elif to_save == "n":
                continue
        elif to_continue == "n":
            edit_other_metadata(metadata, filename)




def get_typenames_1st_level(data):
    output = []
    for n, d in enumerate(data):
        type_class = d.get('typeClass', None)
        if type_class == 'primitive':
            output.append(
                {'index': n, 'typeName': d['typeName'], 'typeClass': d['value']})
        else:
            output.append(
                {'index': n, 'typeName': d['typeName'], 'typeClass': type_class})
    return output




def print_data(data):
    # Extract the data
    table_data = get_typenames_1st_level(data)
    # Prepare the table rows
    rows = []
    for row in table_data:
        # Use textwrap to break typeClass after 45 characters and align it to the right
        type_class_wrapped = textwrap.fill(str(row['typeClass']), width=80)
       # type_class_wrapped_1 = "\n".join(f"{' ' * 60}{val}" for val in type_class_wrapped.split("\n"))
        rows.append([row['index'], row['typeName'], type_class_wrapped])
    # Print the table using tabulate
    print(tabulate(rows, headers=[
          'index', 'typeName', 'Value (compound = multiple)']))




def edit_primitive_data(i, data):
    if i < 0 or i >= len(data):
        print("Invalid index.")
        return

    if 'value' not in data[i]:
        print("Value not found in the data.")
        return

    print(f"Current field value(s): {data[i]['value']}")
    
    # Check if the value is a list or a single value
    if isinstance(data[i]['value'], list):
        value_list = data[i]['value']
        # Print a numbered list of the values
        for j, value in enumerate(value_list):
            print(f"{j}. {value}")
        
        # Prompt the user to select a value to edit
        while True:
            try:
                selection = int(input("Enter the number of the value you want to edit: "))
                value_to_edit = value_list[selection]
                break
            except (ValueError, IndexError):
                    print("Invalid selection. Please enter a valid number.")



        value_to_edit = value_list[selection]
    else:
        # If the value is not a list, simply print it as is
        value_to_edit = data[i]['value']
    
    # Prompt the user to edit the selected value
    new_value = input(f"Enter a new value for '{value_to_edit}': ")
    print(f"New field value: {new_value}")
    
    # Prompt the user to confirm the new value
    to_save = input("If this is the correct field, select Y to save changes. If not, select N to discard changes: Y / N: ").lower()
    if to_save == "y":
        # Update the value in the data dictionary
        if isinstance(data[i]['value'], list):
            value_list[selection] = new_value
            data[i]['value'] = value_list
        else:
            data[i]['value'] = new_value
        print(f"Updated field value: {data[i]['value']}")
    else:
        print("Changes discarded.")



def get_compound_table(i: int, data):
    table_data = [[v['value'] for v in d.values()] for d in data[i]['value']]
    headers = list(data[i]['value'][0].keys())
    print(tabulate(table_data, headers=headers, tablefmt ="grid", showindex='always'))
    return table_data



def edit_compound_by_row(i, j, data):
    keys = list(data[i]['value'][0])
    print(*[f"{k}: {keys[k]}" for k in range(len(keys))], sep="\n")
    index = int(
        input("Please select which field you want to edit. Enter index number here: "))
    current_value = data[i]['value'][j][keys[index]]['value']
    print(f"Current value in this field: {current_value}")
    while True:
        new_value = input("Please type in new value: ")
        print(f"New value: {new_value}")
        continue_yn = input(
            "Is this correct? Y to continue, N to retype new value: Y/N ")
        if continue_yn.lower() == "y":
            data[i]['value'][j][keys[index]]['value'] = new_value
            #save_exit()
            break
        elif continue_yn.lower() == "n":
            edit_compound_by_row(i, j, data)


def edit_compound_by_typeName(data, i):
    keys = data[i]['value'][0].keys()
    print(*[f"{k}: {v['value']}" for k, v in data[i]
          ['value'][0].items()], sep='\n')

    while True:
        index = int(
            input(f"Please select which field you want to edit (0-{len(keys)-1}): "))
        if index < len(keys):
            break
        print(
            f"Invalid input. Please enter an index between 0 and {len(keys) - 1}.")

    field_values = [row[keys[index]]['value'] for row in data[i]['value']]
    print("Current multiple values in this field: ", *field_values, sep='\n')

    while True:
        new_value = input(
            "Please type in new value. Remember, that this will overwrite all multiple values in this column: ")
        print("New value:", new_value)
        continue_yn = input(
            "Is this correct? Y to continue, N to restart ").lower()
        if continue_yn == "y":
            for row in data[i]['value']:
                row[keys[index]]['value'] = new_value
            break
        elif continue_yn != "n":
            edit_compound_by_typeName(data, i)
    return data[i]['value']



def edit_metadata(metadata: dict, filename: str, output_path:str):
    #global SAVEANDEXIT
    other = get_metadata_blocks(metadata)[-2]
    selected_metadata = select_data(metadata, filename)

    if selected_metadata == other:
        edit_other_metadata(metadata, filename)
   
        pass

    if selected_metadata != other:
        metadata_1st_lvl = get_typenames_1st_level(selected_metadata)

        print_data(metadata_1st_lvl)
        index_field = int(
            input("Please enter the index of the field you want to edit: "))

        print("\nYou selected the following field:")
        print(metadata_1st_lvl[index_field]['index'],
              metadata_1st_lvl[index_field]['typeName'], metadata_1st_lvl[index_field]['typeClass'])
        print("\nIf it is correct and you want to continue, press Y. Otherwise, N to restart: ")
        to_continue = select_option()
        if to_continue == 'n':
            edit_metadata(metadata, filename, output_path)

        selected_field = selected_metadata[index_field]
        if selected_field["typeClass"] == "primitive":
            edit_primitive_data(index_field, selected_metadata)
        elif selected_field["typeClass"] == "controlledVocabulary":
            edit_primitive_data(index_field, selected_metadata)
        else:
            selected_typename = selected_field["typeName"]
            compound_table = get_compound_table(index_field, selected_metadata)
            print("*" * 150)
            print("You can select a column or a row to edit. If you select a row (for example, a single author)",
                  " you will be able to change value  fields one-by-one. If you select a column, you will overwrite all values in that column",
                  "(for example authorAffiliation) with a new single value")
            row_or_col = select_row_or_column()
            if row_or_col == "r":
                index_compound_row = int(
                    input("Please enter the index of the row you want to edit: "))
                if index_compound_row < len(selected_field["value"]):
                    edit_compound_by_row(
                        index_field, index_compound_row, selected_metadata)
                    print("\nThis is the updated compound field:")
                    get_compound_table(index_field, selected_metadata)
                    print(
                        "Do you want to save changes to your hard drive and quit? Y to save and quit N to continue editing")
                    edit_yn = select_option()
                    if edit_yn == "y":
                        save_exit(metadata, filename, output_path)
                else:
                    print(
                        "Invalid index. Please select an index within the range.")
            elif row_or_col == "c":
                edit_compound_by_typeName(
                    selected_metadata, index_field)
            else:
                print("Invalid option. Please select either R or C.")
   # save_exit(metadata, filename, output_path)











def main():

    
    file_name = "CV3D2B.json" #change this to edit different file
    metadata_test = load_metadata(os.path.join(DOWNLOADED_PATH,file_name))
    while not SAVEANDEXIT:
        edit_metadata(metadata_test, file_name, EDITED_PATH)



if __name__ == "__main__":
    main()
