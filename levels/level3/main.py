import time

LEVEL = 3

cacheS = {0: 290797}
cacheSMax = 0
result = 290797

def S(n):
	global cacheS, cacheSMax, result
	if n > cacheSMax:
		for i in range(n-cacheSMax):
			result = (result*result)%50515093
			cacheS[cacheSMax+i+1] = result
		cacheSMax = n
	return cacheS[n]

def A(i,j):
	global cacheS
	minS = S(i)
	for x in range(i+1, j+1):
		if not x in cacheS:
			S(x)
		s = cacheS[x]
		if s < minS:
			minS = s
	return minS

def M(N):
	sumA = 0
	for j in range(1, N+1):
		for i in range(1, j+1):
			sumA += A(i,j)
	return sumA

def main():
	start = time.time()
	print(M(500))
	end = time.time()
	print(end-start)