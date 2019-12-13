import os, sys
sys.path.append(os.path.abspath("."))
from ..CCio import CCParser

LEVEL = 0

def run(path):
	print("[*] Parsing input file: " + path)

	resultData = ""
	with CCParser(path) as f:
		data = f.parse()

	print("[+] Successfully parsed input file: " + path)
	print("[#] Data:", str(data), sep="\n")

	print()
	print("[*] Starting to process...")

	try:
		# here goes the main code
		pass
	except:
		print("[-] Failed to process... Aborting.")
		sys.exit(1)

	print("[+] Finished to process!")
	print()
	print("[#] Result:", resultData, sep="\n")

	with open(path[:-2] + "out", "w") as f:
		f.write(resultData)

	return resultData

def main():
	[run(os.path.abspath(os.path.dirname(__file__)) + os.sep + path) if path.endswith(".in") else path for path in os.listdir(os.path.abspath(os.path.dirname(__file__)))]
