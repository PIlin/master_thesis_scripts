# -*- coding: utf-8 -*-



# import cairocffi as cairo

import sys
import pickle

import numpy as np

from pprint import pprint

import matplotlib
matplotlib.use('Qt4Agg')
# matplotlib.use('pgf')

from matplotlib.backends.backend_pgf import FigureCanvasPgf
matplotlib.backend_bases.register_backend('pdf', FigureCanvasPgf)

pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": [
         r"\usepackage[utf8]{inputenc}",
         r"\usepackage[T2A]{fontenc}",
         r"\usepackage{pscyr}",
         ],
    "font.family": "serif"
}
matplotlib.rcParams.update(pgf_with_pdflatex)


import matplotlib.pyplot as plt 


data = {}
files = ('tps', 'dls', 'deliv')
for fn in files:
	fname = fn + '.data'
	with open(fname, "rb") as f:
		data[fn] = pickle.load(f)




# print(tps)

def new_figure(figsize = (6,4)):
	# figsize = (8,6)
	# figsize = (6,4.5)

	f = plt.figure(figsize=figsize)

	f.set_tight_layout(1)

	return f


def draw_throughput(ax, data, xdata, style, label):
	x = range(1, len(data) + 1)

	print(len(x), len(data))

	# d = [d / 1000 for d in data]
	d = data

	ax.plot(xdata, d, style, markersize = 4, label = label)

	# plt.xticks(xdata)

	ax.set_xlabel(u"Середній час між відправками пакету вузлом, с")
	# ax.set_ylabel(u"Успішно доставлених пакетів, %")
	ax.set_ylabel(u"Пропускна здібність, Кбіт/с")

def draw_delay(ax, data):

	print(len(data))

	# idx = [0]
	# idx.extend(range(19,120,20))


	print(idx)

	# d = [[x * 1000 for x in data[i]] for i in idx]

	bp = ax.boxplot(d,0,'')
	plt.xticks(range(1, len(idx) + 1), [i + 1 for i in idx])

	# pprint(bp)

	plt.setp(bp['boxes'], color = 'black')
	plt.setp(bp['whiskers'], color = 'black')
	plt.setp(bp['medians'], color = 'black')

	ax.set_xlabel(u"Розмір корисного навантаження пакету, байт")
	ax.set_ylabel(u"Затримка передачі, мс")




# print (f.get_size_inches())


tps = data['tps']
dls = data['dls']
deliv = data['deliv']
pprint(len(dls))
# dls_s = dls[0]
# dls_f = dls[1]
pprint(deliv)

# sys.exit()



# f = new_figure()
# ax = f.add_subplot(111)
# style = {5:'o-', 50:'>--', 100:'s-', 7:'*-'}
# # ss = sorted([0.005, 
# # 	0.01, 0.015, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.075, 0.09, 
# # 	0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 1])
# ss = sorted([1, 0.75, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1, 0.01])
# for count in [5,50,100]:
# 	d =[]
# 	for s in ss:
# 		# d.append(tps[('%d' % (count,),'10','%f'%(s,))][0] / 1000)
# 		d.append(tps[('%d' % (count,),'10','%f'%(s,))][1] / 1000)
# 	print(d)
# 	draw_throughput(ax, d, ss, 'k'+style[count], u'nn = %d' % count)

# ax.legend(loc = 0)
# ax.grid()
# ax.set_xscale('log')
# ticks = []
# # ticks.extend(np.arange(0.005, 0.01, 0.001).tolist())
# ticks.extend(np.arange(0.01, 0.1, 0.01).tolist())
# ticks.extend(np.arange(0.1, 1, 0.1).tolist())
# ticks.extend([1])
# print(ticks)
# plt.xticks(ticks)
# # ax.set_xlim(0.005, 1)
# # ax.set_ylim(0, 30)
# # f.savefig('tp.pdf')
# # f.savefig('tp.pgf')



f = new_figure()
ax = f.add_subplot(111)
style = {5:'o-', 50:'>--', 100:'s-', 7:'*-'}
ss = sorted([1, 0.75, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1, 0.01])
for count in [5,50,100]:
	succ=[]
	fail=[]
	for s in ss:
		# print(len(dls[('%d' % (count,),'10','%f'%(s,))]))
		dls_s = dls[('%d' % (count,),'10','%f'%(s,))][0]
		dls_f = dls[('%d' % (count,),'10','%f'%(s,))][1]
		# d.append(dls_s[('%d' % (count,),'10','%f'%(s,))])
		succ.append(len(dls_s))
		fail.append(len(dls_f))
	

	succ = np.array(succ, dtype=np.float)
	fail = np.array(fail, dtype=np.float)

	# print(succ)
	# print(fail)
	total = succ + fail
	fail_rate = np.divide(fail, total) * 100
	succ_rate = np.divide(succ, total) * 100

	# print(total)
	# print(fail_rate)
	# sys.exit()

	draw_throughput(ax, succ_rate, ss, 'k'+style[count], u'nn = %d' % count)
	# draw_throughput(ax, fail, ss, 'k'+style[count], u'nn = %d' % count)

	# draw_delay(ax, d)

ax.legend(loc = 0)
ax.grid()
ax.set_xscale('log')
ticks = []
# ticks.extend(np.arange(0.005, 0.01, 0.001).tolist())
ticks.extend(np.arange(0.01, 0.1, 0.01).tolist())
ticks.extend(np.arange(0.1, 1, 0.1).tolist())
ticks.extend([1])
print(ticks)
plt.xticks(ticks)
# ax.set_xlim(0.005, 1)
# ax.set_ylim(0, 30)
f.savefig('succ_rate.pdf')
f.savefig('succ_rate.pgf')




f = new_figure()
ax = f.add_subplot(111)
style = {5:'o-', 50:'>--', 100:'s-', 7:'*-'}
# ss = sorted([0.005, 
# 	0.01, 0.015, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.075, 0.09, 
# 	0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 1])
ss = sorted([1, 0.75, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1, 0.01])
for count in [5,50,100]:
	d =[]
	for s in ss:
		# d.append(tps[('%d' % (count,),'10','%f'%(s,))][0] / 1000)
		d.append(deliv[('%d' % (count,),'10','%f'%(s,))][2] * 100)
	print(d)
	draw_throughput(ax, d, ss, 'k'+style[count], u'nn = %d' % count)

ax.legend(loc = 0)
ax.grid()
ax.set_xscale('log')
ticks = []
# ticks.extend(np.arange(0.005, 0.01, 0.001).tolist())
ticks.extend(np.arange(0.01, 0.1, 0.01).tolist())
ticks.extend(np.arange(0.1, 1, 0.1).tolist())
ticks.extend([1])
print(ticks)
plt.xticks(ticks)
# ax.set_xlim(0.005, 1)
# ax.set_ylim(0, 30)
# f.savefig('deliv.pdf')
# f.savefig('deliv.pgf')




# f = new_figure()
# ax = f.add_subplot(111)
# draw_throughput(ax, data['tps_ack'], 'ko-', u'Із ACK')
# draw_throughput(ax, data['tps_noack'], 'k^-', u'Без ACK')
# ax.legend(loc = 0)
# ax.grid()
# f.savefig('tp.pdf')
# f.savefig('tp.pgf')

# f = new_figure((4,4))
# ax = f.add_subplot(111)
# draw_jitter(ax, data['jts_ack'])
# ax.set_ylim(0,16)
# f.savefig('jts_ack.pdf')
# f.savefig('jts_ack.pgf')


# f = new_figure((4,4))
# ax = f.add_subplot(111)
# draw_jitter(ax, data['jts_noack'])
# ax.set_ylim(0,16)
# f.savefig('jts_noack.pdf')
# f.savefig('jts_noack.pgf')


plt.show()