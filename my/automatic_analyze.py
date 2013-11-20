#!/usr/bin/env python2

import pickle
from pylab import *

import numpy as np

from pprint import pprint

from common import pairwise
from itertools import tee, izip

def read_results_file(fname):
	print(fname)
	with open(fname, 'rb') as f:
		return pickle.load(f)

def filter_starts(rx):
	return tuple([e for e in rx if e.e == 1])


def troughput(rx):
	if not rx:
		return 0

	start_time = rx[0].t
	stop_time = rx[-1].t
	bytes = 0
	for e in rx:
		bytes += e.ip['size']


	bits = bytes * 8
	print ("=== throughput ===")
	print (start_time, stop_time, bytes, bits)

	tp = bits / (stop_time - start_time)
	print (tp)
	return tp

def jitter(rx):
	def pairs(iterable):
		"s -> (s0,s1), (s1,s2), (s2, s3), ..."
		a, b = tee(iterable)
		next(b, None)
		return izip(a, b)

	x = []
	for a,b in pairs(pairwise(rx)):
		x.append(b[0].t - a[0].t)

	print('=== jitter ===')
	minj = min(x)
	maxj = max(x)
	meanj = np.mean(x)
	stdj = np.std(x)

	print(minj, maxj, meanj, stdj)

	return x
def delay(trace, rx0):

	# print(trace)

	rt = {}
	tt = {}
	dt = {}

	def build_dic(dic, arr):
		for p in arr:
			# pprint(p)
			dic[p.ip['number']] = p.t

	def build_dic_from_trace(dic, trace):
		for number,tnode in trace.iteritems():
			if number == 0:
				continue
			ft = filter_starts(tnode)
			build_dic(dic, ft)


	build_dic(rt,rx0)
	build_dic_from_trace(tt, trace.tx)
	build_dic_from_trace(dt, trace.drops)


	suc = []
	fail = []

	print('=== delay ===')

	# pprint(trace.drops)
	print(len(tt), len(dt), len(rt))
	# assert(len(tt) == len(dt) + len(rt))

	for k,vt in tt.iteritems():
		if k in rt:
			vr = rt[k]
			assert(vr > vt)
			suc.append(vr - vt)
			# print(vr, vt, vr - vt)
		elif k in dt:
			vd = dt[k]
			assert(vd > vt)
			fail.append(vd - vt)
		else:
			print('unknown dorp', k)
			# pprint(rx0)
			assert(False)


	if suc:
		print('suc')
		minj = min(suc)
		maxj = max(suc)
		meanj = np.mean(suc)
		stdj = np.std(suc)
		print(minj, maxj, meanj, stdj)

	if fail:
		print('fail')
		minj = min(fail)
		maxj = max(fail)
		meanj = np.mean(fail)
		stdj = np.std(fail)

		print(minj, maxj, meanj, stdj)

	return (suc, fail)



# =======================================

files = ('tps', 'jts', 'dls')
data = {}

def read_data_file(fn):
	try:
		fname = fn + '.data'
		with open(fname, "rb") as f:
			data[fn] = pickle.load(f)
	except:
		print(sys.exc_info())
		pass

for fn in files:
	data[fn] = {}
	read_data_file(fn)


# pprint(data['tps'])

# sys.exit()


def get_result_fname(tf, opts):
	filename = "test_" + tf + "_"
	for v in opts:
		filename = filename + v + "_"
	filename = filename + ".data"
	return filename

# for inter in [0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.07, 0.075, 0.09, 0.1, 0.2, 0.5, 1]:
for inter in [0.05, 0.06, 0.15, 0.3, 0.4]:
	for size in [5,50,100]:
	# for size in [100]:
		opts = tuple(("%d 10 %f" % (size, inter)).split())
		# print(opts)
		fname = get_result_fname('backtraffic_test', opts)
		info = read_results_file(fname)
		tr = info[0]

		r0 = filter_starts(tr.rx[0] if tr.rx else [])

		t = troughput(r0)
		data['tps'][opts] = t

		# j = jitter(r0)
		# data['jts'][opts] = j

		d = delay(tr, r0)
		data['dls'][opts] = d

		print('\n\n')

# print(dls)

# sys.exit()

for fn in files:
	fname = fn + '.data'
	with open(fname, "wb") as f:
		pickle.dump(data[fn], f)
		# eval('pickle.dump(%s, f)' % (fn,))
		
# with open("jts.data", "wb") as f:
# 	pickle.dump(jts, f)
# with open("dls.data", "wb") as f:
# 	pickle.dump(dls, f)
