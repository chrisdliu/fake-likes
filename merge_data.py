import sys, json


_, fp1, fp2 = sys.argv

with open(fp1, 'r') as file1:
	data1 = json.load(file1)

with open(fp2, 'r') as file2:
	data2 = json.load(file2)

result = data1 + data2

with open('merged.json', 'w') as file:
	json.dump(result, file)