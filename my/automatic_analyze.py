#!/usr/bin/env python2

import pickle
from pylab import *

import numpy as np

from pprint import pprint

from common import pairwise
from itertools import tee, izip

def read_file(fname):
	with open(fname, 'rb') as f:
		return pickle.load(f)

def filter_receives(rx):
	return [e for e in rx if e.e == 1]


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



tps = []
jts = []

for i in range(1,120):
	info = read_file('test_speed_test_%d_.data' % (i,))
	tr = info[0]

	r1 = filter_receives(tr.rx[1])

	t = troughput(r1)
	tps.append(t)

	j = jitter(r1)
	jts.append(j)

with open("tps.data", "wb") as f:
	pickle.dump(tps, f)

with open("jts.data", "wb") as f:
	pickle.dump(jts, f)
