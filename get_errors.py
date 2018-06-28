import sys, json


_, filepath = sys.argv

with open(filepath, 'r') as file:
	data = json.load(file)

errors = []
for profile in data:
	if 'error' in profile:
		errors.append(profile['id'])

with opne('errors.json', 'w') as file:
	json.dump(errors, file)