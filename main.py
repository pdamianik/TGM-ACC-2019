import os, sys, traceback, levels
from importlib import reload, import_module

def run(level):
	if "levels.level" + str(level) not in sys.modules:
		import_module("levels.level" + str(level) + ".main", ".")
		sys.modules["levels.level" + str(level) + ".main"].main()
	else:
		reload(sys.modules["levels.level" + str(level)])
		reload(sys.modules["levels.level" + str(level) + ".main"])
		sys.modules["levels.level" + str(level) + ".main"].main()

if __name__ == '__main__':
	level = None
	while level != "":
		try:
			level = input("Level: ")
			if level.strip() in ("", "exit", "exit"):
				break
			elif level.strip() in ("test"):
				if "test" in sys.modules:
					reload(sys.modules["test"])
					sys.modules["test"].test()
				else:
					import_module("test")
					sys.modules["test"].test()
			else:
				run(level)
		except:
			traceback.print_exc()