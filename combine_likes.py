import sys, json


_, datapath, likespath = sys.argv

with open(datapath, 'r') as datafile:
	data = json.load(datafile)

with open(likespath, 'r') as likesfile:
	likes = json.load(likesfile)


for like in likes:
	for fb_id, num in like.items():
		for profile in data:
			if profile['id'] == fb_id:
				profile['parsed']['#page_likes'] = num
				break

with open(datapath, 'w') as datafile:
	json.dump(data, datafile)