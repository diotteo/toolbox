#! /usr/bin/env python3

import sys
import re

def printUsage():
	print('Usage: {} <expr>'.format(sys.argv[0]))


def getIntNbLen(s):
	r = re.compile(r'^[+-]?((0x[0-9a-fA-F]+)|(\d+))')
	m = r.match(s)

	if (m == None):
		return 0
	else:
		return len(m.group())


def getFloatNbLen(s):
	r = re.compile(r'^[+-]?((\d+\.(\d*)?)|(\d*\.\d+))([Ee][+-]?\d+)?')
	m = r.match(s)

	if (m == None):
		return 0
	else:
		return len(m.group())


def getNb(s):
	nb = None
	nbLen = getFloatNbLen(s)
	if (nbLen > 0):
		nb = float(s[:nbLen])
	else:
		nbLen = getIntNbLen(s)
		if (nbLen > 0):
			nb = int(s[:nbLen], 0)

	return (nbLen, nb)


def getOperator(s):
	if (s[0:2] == '**'):
		return (2, '**') #OP.EXPONENT)
	elif (s[0] == '*'):
		return (1, '*') #OP.MULT)
	elif (s[0] == '/'):
		return (1, '/') #OP.DIV)
	elif (s[0] == '+'):
		return (1, '+') #OP.ADD)
	elif (s[0] == '-'):
		return (1, '-') #OP.SUB)
	return (0, None)


def getExpr(s):
	l = []
	exprlen = 0

	if (len(s) < 1):
		return (0, None)

	elif (s[0] == '('):
		subexpr = getExpr(s[1:])

		exprlen = 1 + subexpr[0] + 1
		l.append(subexpr[1])

		if (len(s) < exprlen):
			raise SyntaxError('Incomplete expression: missing closing parenthesis')
		elif (s[exprlen - 1] != ')'):
			raise SyntaxError('Bogus expression: expecting closing parenthesis at index ' + str(exprlen - 1))

	else:
		nb = getNb(s)
		if (nb[1] == None):
			raise SyntaxError('Bogus expression: "' + s + '" doesn\'t start with a number')

		l.append(nb[1])
		exprlen = exprlen + nb[0]

	op = None
	while (exprlen < len(s)):
		op = getOperator(s[exprlen:])

		if (op[0] == 0):
			break
		l.append(op[1])
		exprlen = exprlen + op[0]

		subexpr = getExpr(s[exprlen:])
		if (subexpr[0] == 0):
			raise SyntaxError('Incomplete expression ends with an operator (' + op[1] + ')')
		l.extend(subexpr[1])
		exprlen = exprlen + subexpr[0]

	return (exprlen, tuple(l))


def lex(s):
	expr = getExpr(s)

	if (len(s) > expr[0]):
		raise SyntaxError('Error: string longer than largest recognized expression (starting at index ' + str(expr[0]) + ')')

	return expr[1]

class OP:
	EXPONENT = 1
	MULT = 2
	DIV = 3
	ADD = 4
	SUB = 5


class TOKEN:
	EXPR = 1
	OP = 2


class Node:
	def __init__(self):
		self.parent = None
		self.tok = None
		self.lval = None
		self.rval = None
		self.indent = 0


	def __str__(self):
		if (self.indent > 0):
			prefix = ''
		else:
			prefix = 'tok: '

		if (type(self.tok) is not str):
			return prefix + str(self.tok)

		if (type(self.lval) is Node):
			self.lval.indent = self.indent + 2
			lvalstr = str(self.lval)
		else:
			lvalstr = str(self.lval)

		if (type(self.rval) is Node):
			self.rval.indent = self.indent + 2
			rvalstr = str(self.rval)
		else:
			rvalstr = str(self.rval)

		return prefix + self.tok + '\n' + (' ' * (self.indent + 2)) + 'lval: ' + lvalstr + '\n' + (' ' * (self.indent + 2)) + 'rval: ' + rvalstr


def parse(l):
	rootNode = Node()
	curNode = rootNode
	expectedTok = TOKEN.EXPR

	OPERATORS = ('**', '*', '/', '+', '-')
	for i in range(len(l)):
		tok = l[i]

		if (type(tok) is tuple):
			newNode = parse(tok)
			if (curNode.lval == None):
				curNode.lval = newNode
				newNode.parent = curNode
			elif (curNode.rval == None):
				curNode.rval = newNode
				newNode.parent = curNode
			else:
				raise RuntimeError('?!?')

		elif (tok in OPERATORS):
			if (curNode.tok == None):
				curNode.tok = tok
			else:
				newNode = Node()
				newNode.tok = tok

				# If the new operator has greater precedence than the former
				if (OPERATORS.index(curNode.tok) > OPERATORS.index(tok)):
					newNode.lval = curNode.rval
					curNode.rval = newNode
					newNode.parent = curNode
				else:
					curNode.parent.rval = newNode
					newNode.parent = curNode.parent
					curNode.parent = newNode
					newNode.lval = curNode

				curNode = newNode

		else:
			if (curNode.lval == None):
				curNode.lval = tok
			elif (curNode.rval == None):
				curNode.rval = tok
			else:
				raise RuntimeError('?!?')

	if (rootNode.tok == None):
		rootNode.tok = rootNode.lval
		rootNode.lval = None
	return rootNode


def evalExpr(tree):
	if (type(tree.lval) is Node):
		lval = evalExpr(tree.lval)
	else:
		lval = tree.lval

	if (type(tree.rval) is Node):
		rval = evalExpr(tree.rval)
	else:
		rval = tree.rval

	if (tree.tok == '**'):
		return lval ** rval
	elif (tree.tok == '*'):
		return lval * rval
	elif (tree.tok == '/'):
		return lval / rval
	elif (tree.tok == '+'):
		return lval + rval
	elif (tree.tok == '-'):
		return lval - rval
	else:
		return tree.tok


if (len(sys.argv) < 2):
	printUsage()
	exit(0)
s = sys.argv[1]

if (len(s) < 1):
	printUsage()
	exit(0)


l = lex(s)
tree = parse(l)
r = evalExpr(tree)

if (False):
	print(str(tree))
	print('full expr = ' + str(l))
	print('Result is: ' + str(r))
else:
	print(r)
