from pprint import pprint

from ns2_parse import parse_log_file, parse_tr_file
from common import pairwise

from pylab import *

from itertools import tee, izip



def transmission_len(tx):
	data = []
	
	# for k,txn in tx.items():
	txn = tx[0]
	# pprint(txn)
	for a,b in pairwise(txn):
		data.append(b.t - a.t)

	# print (data)
	plt = figure().add_subplot()
	bp = boxplot(data,0,'',0)



def jitter(srcs, fig = None, pos = 0):
	
	def pairs(iterable):
		"s -> (s0,s1), (s1,s2), (s2, s3), ..."
		a, b = tee(iterable)
		next(b, None)
		return izip(a, b)

	data = []
	for txn in srcs:
		x = []
		for a,b in pairs(pairwise(txn)):
			# print(a, b)
			# print(a[0])
			# print(b[0])
			x.append(b[0].t - a[0].t)
		data.append(x)

	# pprint(data)

	# if not fig:
	# 	fig, ax = subplots()

	bp = boxplot(data,False,'',True)

	return fig


et = parse_log_file('log.txt')

# transmission_len(et.tx)
fig = jitter([et.tx[0]])
# jitter(et.rx[1], fig, 1)


grid()
show()