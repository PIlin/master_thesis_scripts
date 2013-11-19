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



with open("tps.data", "rb") as f:
	tps = pickle.load(f)

with open("jts.data", "rb") as f:
	jts = pickle.load(f)


# print(tps)

def new_figure():
	# figsize = (8,6)
	figsize = (6,4.5)

	f = plt.figure(figsize=figsize)

	# f.tight_layout(.5)

	return f


def draw_throughput(fig, data):
	x = range(1, len(data) + 1)

	print(len(x), len(data))

	d = [d / 1000 for d in data]

	fig.plot(x, d, 'k+-')
	fig.grid()

	fig.set_xlabel(u"Розмір корисного навантаження пакету, байт")
	fig.set_ylabel(u"Корисна пропускна здібність, Кбіт/с")





# print (f.get_size_inches())

f = new_figure()
ax = f.add_subplot(111)
draw_throughput(ax, tps)
f.savefig('fig.pdf')
f.savefig('fig.pgf')

# plt.show()