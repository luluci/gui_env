from os import truncate
import pathlib


if False:
	ciao_path = "D:/home/Tools/kazoeciao158"
	result_dir = "./result"

	p = pathlib.Path(ciao_path + "/" + result_dir)
	print(p)
	print(p.resolve())


if True:
	array = None
	if not array:
		print("空です.")
	array = []
	if not array:
		print("空です.")
