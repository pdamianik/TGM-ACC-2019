import os, traceback
from main import run

expectedResults = {
	1: {
		"example.out": "2\n" +
		"1 7\n" +
		"7 4"
	},
	2: {
		"example.out": "2\n"+
		"2 2\n"+
		"2 5",
		"example2.out": "3\n"+
		"2 3\n"+
		"2 3\n"+
		"2 2"
	}
}

if __name__ == "__main__":
	for key in expectedResults:
		outputFiles = expectedResults[key]
		levelPath = os.path.abspath("." + os.sep + "levels" + os.sep + "level" + str(key)) + os.sep
		try:
			run(key)
		except:
			traceback.print_exc()
		for filename in outputFiles:
			expectedResult = outputFiles[filename]
			with open(levelPath + filename, "r") as f:
				data = f.read()
				print("[*] Expected data: " + expectedResult)
				print("[*] Result data: " + data)
				assert expectedResult == data