from io import FileIO

class CCParser(FileIO):
	def __iter__(self):
		for line in self.parse(): yield line
	def __getitem__(self, item):
		return list(self)[item]
	def parseline(self, modifierFunction=int):
		return [modifierFunction(x) for x in self.readline().decode('utf-8').split()]
	def parse(self, modifierFunction=int):
		return [[modifierFunction(y) for y in x.split()] for x in self.read().decode('utf-8').split('\n')]

def main():
	f = open('./testData.in', 'w')
	f.write("""0 1
0 0 0 0 1 1 2 2 2 3 4""")
	f.close()
	with CCParser('./testData.in') as f:
		print(f.parseline(), end='\n\n')
		f.seek(0)
		print(f.parse(), end='\n\n')
		f.seek(0)
		print(f.parseline())
		print(f.parseline(), end='\n\n')
		f.seek(0)
		print(f[0])

if __name__ == "__main__":
	main()