#! /usr/bin/env python3

import tempfile
import os


def loadPrimes(fname = None):
	if (fname is None):
		fname = os.path.dirname(__file__) + '/primes1.txt'

	f = open(fname, 'r', newline = '\r\n')

	# Skip the first two (header) lines
	for i in range(2):
		f.readline()

	plist = []
	for line in f:
		plist.extend(int(x) for x in line.split() if True)

	return plist


def primeFactorize(n, plist):
	flist = []

	i = 0
	p = plist[i]
	while p * p <= n:
		if (n % p == 0):
			power = 0
			while (n % p == 0):
				power = power + 1
				n = (int)(n / p)

			flist.append((p, power))

		if (p < plist[-1]):
			i = i + 1
			p = plist[i]
		elif (p > plist[-1]):
			raise RuntimeError("p (" + str(p) + ") is greater than plist[-1] (" + plist[-1] + ")")
		else:
			raise RuntimeError('Reached the end of the prime list: ' + str(p))

	if (n >= 1):
		flist.append((n, 1))
	return flist


def getDivisors(n, plist):
	divlist = []

	primeFactList = primeFactorize(n, plist)
	powList = [x[1] for x in primeFactList if True]

	while (True):
		d = 1
		for i in range(len(primeFactList)):
			pf = primeFactList[i][0]
			d = d * pf ** powList[i]

		if (d not in divlist):
			divlist.append(d)

		q = int(n / d)
		if (q not in divlist):
			divlist.append(q)

		i = len(powList) - 1
		while (powList[i] == 0 and i >= 0):
			powList[i] = primeFactList[i][1]
			i = i - 1

		if (i == -1):
			# Done
			break
		else:
			powList[i] = powList[i] - 1

	return divlist


def getProperDivisors(n, plist):
	divList = getDivisors(n, plist)
	divList.remove(n)
	return divList


#def loadPrimes(fname = 'prime.txt'):
#	f = open(fname, 'r')
#
#	plist = []
#	for line in f:
#		plist.append(int(line.rstrip()))
#
#	f.close()
#	return plist
#
#
#def savePrimes(plist, fname = 'prime.txt'):
#	f = tempfile.NamedTemporaryFile(mode = 'w+', delete = False)
#	tname = f.name
#
#	for p in plist:
#		f.write(str(p) + '\n')
#	f.close()
#
#	os.rename(tname, fname)
#
#
#def appendPrimes(plist, fname = 'prime.txt'):
#	f = open(fname, 'r+')
#
#	fplist = []
#	for line in f:
#		fplist.append(int(line.rstrip()))
#
#	if (len(plist) > len(fplist)):
#		for i in range(len(fplist), len(plist)):
#			f.write(str(plist[i]) + '\n')
#
#	f.close()


#def __mytest():
#	plist = loadPrimes()
#	print('plist = ' + str(plist))
#	plist.append(5)
#	print('plist = ' + str(plist))
#	savePrimes(plist)
