import json
import csv
import os
import new_directory
from new_directory import creating_new_directory

def test_file_generator(data, folder):
    file_paths = []

    with open(data, 'r') as f:
        data = json.load(f)
    total_files = 0
    
    if isinstance(data, list):
        for index, item in enumerate(data):
            file_name = f"test_case_{index}.json"
            file_path = os.path.join(os.getcwd(),folder, file_name)
            with open(file_path, 'w') as f:
                f.write(json.dumps(item)) 
            file_paths.append(file_path)
            total_files = index + 1

    else:
        print("🚨❌🚨❌🚨❌no array❌🚨❌🚨❌🚨")
    print("Total Test Cases are {}".format(total_files))
    save_paths_to_csv(file_paths)


def save_paths_to_csv(file_paths):
    csv_file = 'file_paths.csv'
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['File Path'])
        for path in file_paths:
            writer.writerow([path])

    print(f"Saved to {csv_file}")


input_data = 'new-busines-set5.json'
new_folder = creating_new_directory(input_data)
test_file_generator(input_data, new_folder)
