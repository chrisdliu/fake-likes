import sys, json


_, filepath = sys.argv

with open(filepath, 'r') as file:
	data = json.load(file)

nonerrors = []
for profile in data:
	if 'error' not in profile:
		nonerrors.append(profile)

with open(filepath, 'w') as file:
	json.dump(nonerrors, file)