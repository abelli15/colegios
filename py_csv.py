import csv

def read_csv(file_name):
    with open(file_name, "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        data = list(reader)
    return data
def write_csv(file_name, headers, data):
    with open(file_name, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
def write_csv_from_list(file_name, data):
    with open(file_name, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        for item in data:
            writer.writerow([item])


