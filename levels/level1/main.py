import os, sys
from ..CCio import CCParser # Don't worry if you see an error here; just run the main.py in the root directory and enter this levels number (1)

LEVEL = 1
try:
	import colorama
	colorama.init()
	VISUALIZE = True # Change this line to enable/disable the visualization of the process. Note: Disabled will be much faster
except:
	VISUALIZE = False

class LandingSpot:
	_offsets = [[x, 0] for x in [1, -1]] + [[0, y] for y in [1, -1]]

	def __init__(self, x, y, height2DSurface):
		self.x = x
		self.y = y
		self.surface = height2DSurface
		self.centerHeight = height2DSurface[1][1]
		self.allowedHeightRange = tuple(range(self.centerHeight - 1, self.centerHeight + 2))
	def __ge__(self, otherLandingSpot):
		if self.x == otherLandingSpot.x:
			return self.y >= otherLandingSpot.y
		return self.x > otherLandingSpot.x
	def __gt__(self, otherLandingSpot):
		if self.x == otherLandingSpot.x:
			return self.y > otherLandingSpot.y
		return self.x > otherLandingSpot.x
	def __le__(self, otherLandingSpot):
		if self.x == otherLandingSpot.x:
			return self.y >= otherLandingSpot.y
		return self.x > otherLandingSpot.x
	def __lt__(self, otherLandingSpot):
		if self.x == otherLandingSpot.x:
			return self.y > otherLandingSpot.y
		return self.x > otherLandingSpot.x
	def __comp__(self, otherLandingSpot):
		if self.x == otherLandingSpot.x:
			return self.y - otherLandingSpot.y
		return self.x - otherLandingSpot.x
	def __str__(self):
		return str(self.x) + " " + str(self.y)
	def canLand(self):
		for offset in self._offsets:
			if self.surface[1 + offset[0]][1 + offset[1]] not in self.allowedHeightRange:
				return False
		return True

class Height2DSurface:
	def __init__(self, surface):
		self.surface = surface
		if VISUALIZE:
			self.renderData = [[[colorama.Style.RESET_ALL, colorama.Style.RESET_ALL]]*len(x) for x in surface]
			self._changes = []
	def __getitem__(self, key):
		return self.surface[key]
	def __iter__(self):
		return self.surface.__iter__()
	def __len__(self):
		return len(self.surface)
	def getLandingSpotAt(self, x, y):
		surface = []
		for offsetY in range(-1, 2):
			surface.append(self.surface[offsetY + y][x-1:x+2])
		return LandingSpot(x, y, Height2DSurface(surface))
	def setInitial(self, x, y):
		self.renderData[y][x] = [colorama.Style.RESET_ALL, colorama.Style.RESET_ALL]
	def setActive(self, x, y):
		self.renderData[y][x] = [colorama.Back.LIGHTBLACK_EX, colorama.Style.RESET_ALL]
	def setFound(self, x, y):
		self.renderData[y][x] = [colorama.Back.GREEN, colorama.Style.RESET_ALL]
	def setNotFound(self, x, y):
		self.renderData[y][x] = [colorama.Back.YELLOW + colorama.Fore.BLACK, colorama.Style.RESET_ALL]
	def renderChanges(self):
		changes, self._changes = self._changes, []
		return str(changes)
	def __str__(self):
		result = " "*3 + "".join([str(x).rjust(2) + " "*2 for x in range(len(self.surface[0]))]) + "\n"
		for rowIndex in range(len(self.surface)):
			row = self.surface[rowIndex]
			tmp = []
			for columnIndex in range(len(row)):
				column = row[columnIndex]
				renderData = self.renderData[rowIndex][columnIndex]
				tmp.append(str(renderData[0]) + str(column) + str(renderData[1]))
			result += str(rowIndex).ljust(3) + ", ".join(tmp) + "\n"
		return result

def main(path):
	print("[*] Parsing input file: " + path)

	resultData = ""
	with CCParser(path) as f:
		rawData = f.parse()

	print("[+] Successfully parsed input file: " + path)
	print()
	print("[#] Data:", "\n".join([str(x) for x in rawData]), sep="\n")
	print()
	print("[*] Starting to process...")

	try:
		results = []
		surface = Height2DSurface(rawData[1:])
		if VISUALIZE: print(surface)
		total = (len(surface)-2) * (len(surface[0])-2)
		current = 0
		sys.stdout.write("\033[2J")
		for rowIndex in range(1, len(surface) - 1):
			row = surface[rowIndex]
			for columnIndex in range(1, len(row) - 1):
				if VISUALIZE: surface.setActive(columnIndex, rowIndex)
				landingSpot = surface.getLandingSpotAt(columnIndex, rowIndex)
				if landingSpot.canLand():
					if VISUALIZE: surface.setFound(columnIndex, rowIndex)
					results.append(landingSpot)
				else:
					if VISUALIZE: surface.setNotFound(columnIndex, rowIndex)
				if VISUALIZE:
					sys.stdout.write("\033[;H")
					print("[#] Process (" + str(round(current/total*100, 2)) + "%): ")
				else:
					print("[#] Process: " + str(round(current/total*100, 2)) + "%", end="\r")
				if VISUALIZE: sys.stdout.write(str(surface))
				current += 1
		if VISUALIZE:
			sys.stdout.write("\033[;H")
			print("[+] Process (100%):  ")
			sys.stdout.write(str(surface))
		else:
			print("[+] Process: 100%  ")
		resultData = str(len(results)) + "\n" + "\n".join([str(x) for x in sorted(results, reverse=True)])
	except Exception as e:
		print("[-] Exception " + str(e) + " Aborting.")
		raise e

	print("[+] Finished to process!")
	print()
	print("[#] Result:", resultData, sep="\n")

	with open(path[:-2] + "out", "w") as f:
		f.write(resultData)

	return resultData

[main(os.path.abspath(os.path.dirname(__file__)) + os.sep + path) if path.endswith(".in") else path for path in os.listdir(os.path.abspath(os.path.dirname(__file__)))]
