import os, sys, traceback, levels
from importlib import reload, import_module

def run(level):
	if "levels.level" + str(level) not in sys.modules:
		import_module("levels.level" + str(level) + ".main", ".")
	else:
		reload(sys.modules["levels.level" + str(level)])
		reload(sys.modules["levels.level" + str(level) + ".main"])

if __name__ == '__main__':
	level = None
	while level != "":
		try:
			level = input("Level: ")
			if level.strip() in ("", "exit", "exit"):
				break
			run(level)
		except:
			traceback.print_exc()