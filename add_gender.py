import sys, json


_, filepath = sys.argv

with open(filepath, 'r') as file:
    data = json.load(file)

for profile in data:
    profile['parsed']['?gender_male'] = 0
    profile['parsed']['?gender_female'] = 0
    profile['parsed']['?gender_other'] = 0
    gender = profile['raw']['gender']
    if raw['gender'].lower() == 'male':
        profile['parsed']['?gender_male'] = 1
    elif raw['gender'].lower() == 'female':
        profile['parsed']['?gender_female'] = 1
    else:
        profile['parsed']['?gender_other'] = 1

with open(filepath, 'w') as file:
    json.dump(data, filepath)