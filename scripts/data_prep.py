import os, ast, argparse, json
import preprocessing

parser = argparse.ArgumentParser()
parser.add_argument('--raw_dept_data', type=str, default='departments.json', help='')
args = parser.parse_args()

def get_departments(root_dir: str, dept_data_file_name: str):
    dept_data_file_path = root_dir + "data/" + dept_data_file_name
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

    with open(root_dir + "data/" + f"{dept_data_file_name.split('.')[0]}_processed.json", 'w') as fp:
        json.dump(department_dict,fp)
            
    