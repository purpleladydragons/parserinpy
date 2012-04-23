from pyparsing import *
import operator
import re


exprstack = []

def pushFirst(strg, loc, toks):
	exprstack.append(toks[0])

num = Word(nums)
plus = Literal('+')
mult = Literal('*')
sub = Literal('-')
div = Literal('/')
addop = plus|sub
multop = mult|div
lpar = Literal("(").suppress()
rpar = Literal(")").suppress()


expr = Forward()
atom = num.setParseAction(pushFirst)|(lpar+expr.suppress()+rpar)
factor = atom

term = factor + ZeroOrMore((multop+factor).setParseAction(pushFirst))

expr << term + ZeroOrMore((addop+term).setParseAction(pushFirst))

ops = {	'+':operator.add,
		'*':operator.mul,
		'-':operator.sub,
		'/':operator.truediv
}

def evalstack(stack):
	op = stack.pop()
	if op in "+-*/^":
		op2 = evalstack(stack)
		op1 = evalstack(stack)
		return ops[op](op1,op2)
	elif re.search('[0-9]+',op):  #the magic line, difference vs elif op == num?
		return int(op)

t = "8*(7+(2*3))"

l = expr.parseString(t)

res = evalstack(exprstack)
print res
