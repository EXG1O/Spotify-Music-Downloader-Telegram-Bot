import os

def if_find_folder_or_file(directory: str, name: str) -> bool:
	for _name in os.listdir(directory):
		if _name == name:
			return True
	return False
