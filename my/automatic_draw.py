# -*- coding: utf-8 -*-



# import cairocffi as cairo

import sys
import pickle

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
files = ('tps',)
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


def draw_throughput(ax, data, style, label):
	x = range(1, len(data) + 1)

	print(len(x), len(data))

	d = [d / 1000 for d in data]

	ax.plot([1,50,100,120], d, style, markersize = 3, label = label)

	plt.xticks([0,50,100,120])

	ax.set_xlabel(u"Розмір корисного навантаження пакету, байт")
	ax.set_ylabel(u"Корисна пропускна здібність, Кбіт/с")

def draw_jitter(ax, data):

	print(len(data))

	idx = [0]
	idx.extend(range(19,120,20))


	print(idx)

	d = [[x * 1000 for x in data[i]] for i in idx]

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
pprint(tps)

f = new_figure()
ax = f.add_subplot(111)
style = {1:'o-', 3:'^--', 5:'s-.', 7:'*-'}
for bo in [1,3,5,7]:
	d =[]
	for s in [1,50,100,120]:
		d.append(tps[(s,bo,bo)])
	print(d)

	draw_throughput(ax, d, 'k'+style[bo], u'BO=SO=%d' % bo)

ax.legend(loc = 0)
ax.grid()
f.savefig('tp.pdf')
f.savefig('tp.pgf')

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


# plt.show()