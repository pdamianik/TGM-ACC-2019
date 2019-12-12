import os, sys, math
sys.path.append(os.path.abspath("."))
from ..CCio import CCParser

try:
	import colorama
	colorama.init()
	VISUALIZE = True # Change this line to enable/disable the visualization of the process. Note: Disabled will be much faster
except:
	VISUALIZE = False

LEVEL = 0

class Crater:
	def __init__(self, landingSpot):
		self.triangles = []
		self.landingSpot = landingSpot
		self.size = 0
		self.totalX = 0
		self.totalY = 0
		self.distance = .0
		self.weightpoint = [0, 0]
		self.points = []
	def appendField(self, point):
		self.totalX += point[0]
		self.totalY += point[1]
		self.size += 1
		self.distance = math.sqrt((self.landingSpot[0]-self.weightpoint[0])*(self.landingSpot[0]-self.weightpoint[0]) + (self.landingSpot[1]-self.weightpoint[1])*(self.landingSpot[1]-self.weightpoint[1]))
		self.points.append(point)
		self.weightpoint = [self.totalX/self.size, self.totalY/self.size]
	def __len__(self):
		return self.size
	def __ge__(self, otherCrater):
		return self.distance >= otherCrater.distance
	def __gt__(self, otherCrater):
		return self.distance > otherCrater.distance
	def __le__(self, otherCrater):
		return self.distance <= otherCrater.distance
	def __lt__(self, otherCrater):
		return self.distance < otherCrater.distance
	def __comp__(self, otherCrater):
		return self.distance - otherCrater.distance
	def __str__(self):
		return str(round(self.distance)) + " " + str(self.size)

class Height2DSurface:
	def __init__(self, surface, toCheck=None):
		self.surface = surface
		if VISUALIZE:
			self.renderData = [[[colorama.Style.RESET_ALL, colorama.Style.RESET_ALL]]*len(x) for x in surface]
			self._changes = []
		if toCheck == None:
			self.toCheck = [[True]*len(surface[0])]*len(surface)
		else:
			self.toCheck = toCheck
	def __getitem__(self, key):
		return self.surface[key]
	def __iter__(self):
		return self.surface.__iter__()
	def __len__(self):
		return len(self.surface)
	def setInitial(self, x, y):
		self.renderData[y][x] = [colorama.Style.RESET_ALL, colorama.Style.RESET_ALL]
		self._changes.append("\033["+str(y+3)+";"+str(4+4*x)+"H" + str(self.surface[y][x]).rjust(2))
	def setActive(self, x, y):
		self.renderData[y][x] = [colorama.Back.LIGHTBLACK_EX, colorama.Style.RESET_ALL]
		self._changes.append("\033["+str(y+3)+";"+str(4+4*x)+"H" + colorama.Back.LIGHTBLACK_EX + str(self.surface[y][x]).rjust(2) + colorama.Style.RESET_ALL)
	def setFound(self, x, y):
		self.renderData[y][x] = [colorama.Back.GREEN, colorama.Style.RESET_ALL]
		self._changes.append("\033["+str(y+3)+";"+str(4+4*x)+"H" + colorama.Back.GREEN + str(self.surface[y][x]).rjust(2) + colorama.Style.RESET_ALL)
	def setNotFound(self, x, y):
		self.renderData[y][x] = [colorama.Back.YELLOW + colorama.Fore.BLACK, colorama.Style.RESET_ALL]
		self._changes.append("\033["+str(y+3)+";"+str(4+4*x)+"H" + colorama.Back.YELLOW + colorama.Fore.BLACK + str(self.surface[y][x]).rjust(2) + colorama.Style.RESET_ALL)
	def renderChanges(self):
		changes, self._changes = self._changes, []
		return "".join(changes)
	def checked(self, x, y):
		self.toCheck[y][x] = False
	def findCrater(self, checkCoordinates, crater, previousHeight=None):
		checkHeight = self.surface[checkCoordinates[1]][checkCoordinates[0]]
		if checkHeight == None or not self.toCheck[checkCoordinates[1]][checkCoordinates[0]] or checkHeight > 20:
			if VISUALIZE and (checkHeight >= 20 or checkHeight == None): self.setNotFound(checkCoordinates[0], checkCoordinates[1])
			return None
		if previousHeight != None and abs(checkHeight-previousHeight) > 1:
			self.setNotFound(checkCoordinates[0], checkCoordinates[1])
			return None
		crater.appendField(checkCoordinates)
		self.checked(checkCoordinates[0], checkCoordinates[1])
		found = False

		offsets = [(x, 0) for x in (-1, 1)] + [(0, y) for y in (-1, 1)]

		for offset in offsets:
			x = checkCoordinates[0]+offset[0]
			y = checkCoordinates[1]+offset[1]
			if y < 0 or y > len(self.surface)-1 or x < 0 or x > len(self.surface[0])-1: continue
			tmpCrater = self.findCrater((x, y), crater, checkHeight)
			if tmpCrater != None:
				found = True
				crater = tmpCrater

		if VISUALIZE:
			if len(crater) > 1:
				self.setFound(checkCoordinates[0], checkCoordinates[1])
			else:
				self.setNotFound(checkCoordinates[0], checkCoordinates[1])

		if found or previousHeight == None and len(crater) > 1:
			return crater
		return None
	def __str__(self):
		result = " "*3 + "".join([str(x).rjust(2) + " "*2 for x in range(len(self.surface[0]))]) + "\n"
		for rowIndex in range(len(self.surface)):
			row = self.surface[rowIndex]
			tmp = []
			for columnIndex in range(len(row)):
				column = row[columnIndex]
				renderData = self.renderData[rowIndex][columnIndex]
				tmp.append(str(renderData[0]) + str(column).rjust(2) + str(renderData[1]))
			result += str(rowIndex).ljust(3) + ", ".join(tmp) + "\n"
		return result

def main(path):
	print("[*] Parsing input file: " + path)

	resultData = ""
	with CCParser(path) as f:
		data = f.parse()

	grid = Height2DSurface(data[2:], [[height < 20 for height in row] for row in data[2:]])
	landingSpot = tuple(data[0])
	craters = []

	print("[+] Successfully parsed input file: " + path)
	print("[#] Data:", str(data), sep="\n")

	print()
	print("[*] Starting to process...")

	try:
		# here goes the main code
		total = (len(grid)) * (len(grid[0]))
		current = 0
		if VISUALIZE:
			print(grid)
			sys.stdout.write("\033[2J")
			sys.stdout.write("\033[2;H")
			sys.stdout.write(str(grid))
			sys.stdout.write("\033[;H")
		for y in range(len(grid)):
			row = grid[y]
			for x in range(len(row)):
				#height = row[x]
				crater = grid.findCrater((x,y), Crater(landingSpot))
				if crater != None:
					craters.append(crater)
				if VISUALIZE:
					sys.stdout.write("\033[;H")
					sys.stdout.write("[#] Process (" + str(round(current/total*100, 2)) + "%): ")
					sys.stdout.write(grid.renderChanges())
					pass
				else:
					print("[#] Process: " + str(round(current/total*100, 2)) + "%", end="\r")
				current += 1
		if VISUALIZE:
			sys.stdout.write("\033[;H")
			print("[+] Process (100%):  ")
			sys.stdout.write("\033["+str(3+len(grid))+";H")
			pass
		else:
			print("[+] Process: 100%  ")
		resultData = str(len(craters)) + "\n" +  "\n".join([str(x) for x in sorted(craters, reverse=True)])
	except Exception as e:
		print("[-] Exception " + str(e) + " Aborting.")
		raise e
	print()

	print("[+] Finished to process!")
	print()
	print("[#] Result:", resultData, sep="\n")

	with open(path[:-2] + "out", "w") as f:
		f.write(resultData)

	return resultData

[main(os.path.abspath(os.path.dirname(__file__)) + os.sep + path) if path.endswith(".in") else path for path in os.listdir(os.path.abspath(os.path.dirname(__file__)))]