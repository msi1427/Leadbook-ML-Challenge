import os, ast, argparse, json
import preprocessing
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--raw_dept_data', type=str, default='departments.json', help='')
args = parser.parse_args()

def get_departments(root_dir: str, dept_data_file_name: str):
    dept_data_file_path = f"{root_dir}data/{dept_data_file_name}"
    with open(dept_data_file_path, 'r') as fp:
        departments = fp.read()
    departments = (departments[1:-2]+",").split("\n")

    dept_dict = {}
    for department in departments:
        dept_dict.update(ast.literal_eval(department)[0])

    return dept_dict

def preprocess_data(phrase_list: list):
    phrase_list = preprocessing.replace_and_or(phrase_list)
    phrase_list = preprocessing.lowercasing(phrase_list)
    return phrase_list

def construct_train_data(department_dict : dict):
    data = []

    for key,phrase1_list in department_dict.items():
        for rep_key,phrase2_list in department_dict.items():
            score = 0.0
            if key == rep_key : score = 0.9
            else : score = 0.1
            triplet_dict = [{"phrase1" : phrase1, "phrase2": phrase2, "score": score} for phrase1 in phrase1_list for phrase2 in phrase2_list if phrase1 != phrase2]
            data.extend(triplet_dict)
    
    df = pd.DataFrame(data=data,columns=["phrase1","phrase2","score"])
    return df

if __name__ == "__main__" : 
    dept_data_file_name = args.raw_dept_data
    root_dir = os.path.dirname(os.path.abspath(__file__)) + "/../"
    departments = get_departments(root_dir,dept_data_file_name)

    department_dict = {}
    for key, value_list in departments.items():
        phrase_list = [value for value in value_list]
        phrase_list.append(key)
        phrase_list = preprocess_data(phrase_list)
        department_dict[key] = phrase_list

    with open(f"{root_dir}data/{dept_data_file_name.split('.')[0]}_processed.json", 'w') as fp:
        json.dump(department_dict,fp)
    
    df = construct_train_data(department_dict)
    df.to_csv(f"{root_dir}data/data/train.csv",index=False)