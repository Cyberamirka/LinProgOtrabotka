import csv


data = [
    ["Spam","Spam","Spam"],
    [1, 2, 3],
    [3, 4, 5]
]

with open("123.csv", 'w', encoding="utf-8") as f:
    csv_w = csv.writer(f, delimiter=";")
    for i in data:
        csv_w.writerow(i)