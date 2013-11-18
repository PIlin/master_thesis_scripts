import subprocess as sp
import itertools as it

from pprint import pprint

import pickle

import StringIO


from ns2_parse import parse_log_file, parse_tr_file, parse_log_stream, parse_tr_stream


def call(command):
	print (command)

	child = sp.Popen(command, stdout = sp.PIPE, stderr=sp.PIPE)
	streamdata_out, streamdata_err = child.communicate()
	rc = child.returncode

	return rc, streamdata_out, streamdata_err


ns = "ns".split()
# make = "make".split()
# prog = "./profiling/hough_profiling".split()
# calls = ['50']

# cmake_opts = "-DHOMP_HOUGH_BUILD_LOOP_OMP_3=ON -DHOMP_HOUGH_BUILD_LOOP_ACC_ROW=ON .".split()
# make_opts = []


# pprint(possible_options)

def call_ns(ns_opts):
	print(ns_opts)
	rc, out, err = call(ns + ns_opts)
	# pprint(out)
	# pprint(err)
	# pprint(rc)

	# print(rc, err)

	return rc, out, err

# def combine_opts(build_options):
# 	res = []
# 	for i in range(1+len(build_options)):

# 		for c in it.combinations(build_options, i):
# 			d = {k:False for (k) in build_options }

# 			for k in c:
# 				d[k] = True

# 			# print(i,c, d)
# 			res.append(d)

# 	return res

# def get_cmake_opts(comb):
# 	o = ""
# 	# print(comb)
# 	for k,v in comb.iteritems():
# 		o = o + "-D" + k + "=" + ("ON" if v else "OFF") + " "
# 	return o

# def test(file, serial=False):
# 	command = prog + file + (['0'] if serial else ['1']) + calls
# 	print (command)
# 	rc,out,err = call(command)
# 	# pprint(out)
# 	# pprint(err)
# 	# pprint(rc)
# 	return rc, out

# def test_and_parse(file, serial=False):
# 	print(file)
# 	rc,out = test(file, serial)
# 	# rc,out = 0, '0.884521, 0.813743, 0.767085, 0.776789, 0.743436, 0.73228\n0.73228, 0.736669, 0.73977, 0.747103, 0.761356, 0.767085, 0.771617, 0.795577, 0.83191, 0.884521, \n'

# 	print(rc, out)

# 	if rc != 0:
# 		return False, [], []

# 	out = out.splitlines()

# 	out = [filter(lambda v: v.strip(), arr.split(',')) for arr in out ]
# 	# print(out)
# 	# print(out[1] )
# 	infos = [float(v) for v in out[0]]
# 	times = [float(v) for v in out[1]]
# 	# print(infos)
# 	# print(times)

# 	return True, infos, times

# opts_combinations = combine_opts(build_options)
# pprint(opts_combinations)
# print(get_cmake_opts({'HOMP_HOUGH_BUILD_LOOP_OMP_3': False, 'HOMP_HOUGH_BUILD_LOOP_OMP_2': True, 'HOMP_LOCAL_MAXIMA_LOOP_OMP_3': False, 'HOMP_LOCAL_MAXIMA_LOOP_OMP_2': True, 'HOMP_HOUGH_BUILD_LOOP_ACC_ROW': True, 'HOMP_RADIUSES_LOOP': True}))
# pprint(build("-DHOMP_HOUGH_BUILD_LOOP_OMP_3=ON -DHOMP_HOUGH_BUILD_LOOP_ACC_ROW=OFF .".split()))

# test()
# print(test_and_parse())


def parse_result(tr_fname, log_data):
	tr = parse_tr_file(tr_fname)
	# pprint(tr)

	# print(log_data)

	log = None
	# log = parse_log_stream(StringIO.StringIO(log_data))
	# pprint(log)
	return (tr, log)


def save(tf, opts, data):
	filename = "test_" + tf + "_"
	for v in opts:
		filename = filename + v + "_"
	# for k,v in opts.iteritems():
	# 	if v:
	# 		filename = filename + shortcuts[k] + "_"

	filename = filename + ".data"
	print(filename)
	with open(filename, "wb") as f:
		pickle.dump(data, f)


# def do_test_parallel(po):
# 	opts_combinations = po if po else combine_opts(build_options)
# 	for opts in opts_combinations:
# 		brc, bout = build(get_cmake_opts(opts).split())
# 		for fk, fv in test_files.iteritems():
# 			tr = False
# 			tinfos = []
# 			ttimes = []
# 			if brc == 0:
# 				tr, tinfos, ttimes = test_and_parse(fv.split(), serial=False)

# 			save(fk, opts, [brc, bout, tinfos, ttimes, opts], False)
# 			pass
# 		pass
# 	return

def do_test(name):
	for size in range(1,121):
		opts = ["%d" % (size,)]
		brc, bout, berr = call_ns(['%s.tcl' % (name,)] + opts)



		res = parse_result('%s.tr' % (name,), bout)

		save(name, opts, res)








do_test('speed_test')
# do_test_parallel(possible_options)
