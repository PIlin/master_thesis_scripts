#!/usr/bin/env python2

import pickle
from pylab import *

import numpy as np

from pprint import pprint

from common import pairwise
from itertools import tee, izip

def read_file(fname):
	print(fname)
	with open(fname, 'rb') as f:
		return pickle.load(f)

def filter_starts(rx):
	return tuple([e for e in rx if e.e == 1])


def troughput(rx):
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


	pprint(trace.drops)
	print(len(tt), len(dt), len(rt))
	# assert(len(tt) == len(dt) + len(rt))

	for k,vt in tt.iteritems():
		if k in rt:
			vr = rt[k]
			assert(vr > vt)
			suc.append(vr - vt)
			print(vr, vt, vr - vt)
		elif k in dt:
			vd = dt[k]
			assert(vd > vt)
			fail.append(vd - vt)
		else:
			print('unknown dorp', k)
			# pprint(rx0)
			assert(False)

	print('=== delay ===')

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





tps = {}
jts = {}
dls = {}

def get_result_fname(tf, opts):
	filename = "test_" + tf + "_"
	for v in opts:
		filename = filename + v + "_"
	filename = filename + ".data"
	return filename

for inter in [1, 0.1, 0.01]:
	for size in [5,50,100]:
		opts = tuple(("%d 10 %f" % (size, inter)).split())
		# print(opts)
		fname = get_result_fname('backtraffic_test', opts)
		info = read_file(fname)
		tr = info[0]

		r0 = filter_starts(tr.rx[0])

		t = troughput(r0)
		tps[opts] = t

		# j = jitter(r0)
		# jts[opts] = j

		d = delay(tr, r0)
		dls[opts] = d

print(dls)

with open("tps.data", "wb") as f:
	pickle.dump(tps, f)

with open("jts.data", "wb") as f:
	pickle.dump(jts, f)

with open("dls.data", "wb") as f:
	pickle.dump(dls, f)
