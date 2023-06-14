import json
import csv
import os

def save_paths_to_csv(file_paths):
    csv_file = 'file_paths.csv'
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['File Path'])
        for path in file_paths:
            writer.writerow([path])

    print(f"Saved to {csv_file}")
