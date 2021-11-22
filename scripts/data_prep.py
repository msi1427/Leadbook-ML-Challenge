import os, sys, ast, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--raw_dept_data', type=str, default='departments.json', help='')
args = parser.parse_args()

def get_departments(root_dir: str,dept_data_file_name: str):
    dept_data_file_path = root_dir + "data/" + dept_data_file_name
    print(dept_data_file_path)
    with open(dept_data_file_path, 'r') as fp:
        departments = fp.read()
    departments = (departments[1:-2]+",").split("\n")

    dept_dict = {}
    for department in departments:
        dept_dict.update(ast.literal_eval(department)[0])

    return dept_dict

if __name__ == "__main__" : 
    dept_data_file_name = args.raw_dept_data
    root_dir = os.path.dirname(os.path.abspath(__file__)) + "/../"
    departments = get_departments(root_dir,dept_data_file_name)
    print(departments)