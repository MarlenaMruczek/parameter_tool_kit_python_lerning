
import json
import csv
from pathlib import Path
import sys

def load_params(path):
    """
    Load parameters from a JSON file. Validate the structure after loading.

    Args:
        path (str): The path to the JSON file containing parameters.
     """
    with open(path, "r") as f:
        data = json.load(f)

    has_errors = False
    for para in data:
        for key in ["name", "unit", "min", "max"]:
            if key not in para:
                print(f"❗Parameter {para.get('name', 'Unknown')} missing '{key}' key: {para}❗")
                has_errors = True
        if "value" not in para and "points" not in para:
            print(f"❗Parameter {para.get('name', 'Unknown')} missing 'value' or 'points' key: {para}❗")
            has_errors = True

    if has_errors:
        print("⚠️ERROR: One or more parameters are missing required keys. Please check the input files and correct parameters listed above.⚠️")
        sys.exit(1)

    return data

def validate(params):
    """
    Validate the parameters loaded from the JSON file.

    Args:
        params (list): A list of parameter dictionaries to validate.
        """
    for para in params:
        if "value" in para and not (para["min"] <= para["value"] <= para["max"]):
            print(f"❗Parameter value {para['value']} is out of bounds for {para['name']}.❗")
        elif "points" in para:
            for point in para["points"]:
                if not (para["min"] <= point["y"] <= para["max"]):
                    print(f"❗Point value {point['y']} is out of bounds for {para['name']}.❗")
        
                
    print("All parameters are checked.")

def diff(old_params, new_params):
    """
    Compare two parameter sets and return the differences.

    Args:
        old_params (list): The list of parameters from the old set.
        new_params (list): The list of parameters from the new set.

    Returns:
        dict: A dictionary containing the differences and json report of the differences.
    """
    old_dict = {para["name"]: para for para in old_params}
    new_dict = {para["name"]: para for para in new_params}

    differences = {"removed": [], "added": [], "modified": []}
    for name in old_dict:
        if name not in new_dict:
            differences["removed"].append(f"{name}")

    for name, new_para in new_dict.items():
        if name not in old_dict:
            differences["added"].append(f"{name}")
        else:
            old_para = old_dict[name]
            if "value" in old_para and "value" in new_para:
                key = "value"
            elif "points" in old_para and "points" in new_para:
                key = "points"
            else:
                key = False  # This will trigger the else clause below

            if key and old_para[key] != new_para[key]:
                differences["modified"].append({
                    "name": name,
                    "old": old_para[key],
                    "new": new_para[key]
                })
            elif not key:
                differences["modified"].append({
                    "name": name,
                    "old": "compareing single value with points",
                    "new": "compareing single value with points"
                })


    return differences

def report(diffs):
    """
    Print a report of the differences between two parameter sets.

    Args:
        diffs (dict): A dictionary containing the differences.
    """
    for param in diffs["modified"]:

        if param["old"] != 0 and isinstance(param["old"], (int, float)):
          param["percentage_change"] = round((param["new"] - param["old"]) / param["old"] * 100, 2)
        else:
            param["percentage_change"] = "N/A"

    diffs["modified"].sort(key=lambda x: abs(x["percentage_change"]) if isinstance(x["percentage_change"], (int, float)) else 0, reverse=True)

    with open("report.csv","w",newline ="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=diffs["modified"][0].keys())
        writer.writeheader()
        writer.writerows(diffs["modified"])


input_dir=Path("input")
#searching for all files with the suffix "_new.json" and "_old.json" in the input directory
files_new = list(input_dir.glob("*_new.json"))
files_old = list(input_dir.glob("*_old.json"))

if len(files_new) == 0 or len(files_old) == 0:
    print("⚠️ERROR:No '_new.json' or '_old.json' files found in the input directory.⚠️")
elif len(files_new) > 1 or len(files_old) > 1:
    print("⚠️ERROR:Multiple '_new.json' or '_old.json' files found in the input directory. Please ensure there is only one of each.⚠️")
else:
    print(f"Found files: {files_new[0].name} and {files_old[0].name}")
    print(f"Loading and validating parameters for {files_new[0].name}")
    new_data = load_params(input_dir / files_new[0].name)
    
    validate(new_data)
    

    print(f"Loading and validating parameters for {files_old[0].name}")
    old_data = load_params(input_dir / files_old[0].name)
    validate(old_data)

    
    differences = diff(old_data, new_data)
    if differences == {"removed": [], "added": [], "modified": []}:
        print("No differences found between the two parameter sets.")
    else:
        report(differences)
        print("Report generated: report.csv")

       

