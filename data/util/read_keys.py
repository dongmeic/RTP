import json

def read_usr(path):
	with open(path, 'r') as f:
		keys = json.load(f)
	return keys['ArcGIS_Online']['usr']

def read_pwd(path):
	with open(path, 'r') as f:
		keys = json.load(f)
	return keys['ArcGIS_Online']['pwd']
