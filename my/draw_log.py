
import sys
import re

from pprint import pprint

import matplotlib.pyplot as plt 


from collections import namedtuple

from ns2_parse import parse_log_file, parse_tr_file
from common import pairwise

et = parse_log_file('log.txt')
# et = parse_tr_file('t4.tr')
tx = et.tx
rx = et.rx
drops = et.drops
nodes = et.lastNode()
# print (tx)



lines = {}

def draw(src, ax, color):
	bt = []
	for a,b in pairwise(src):
		# assert(a.e == 1)
		# assert(b.e == 0)
		# bt.append((a.t, b.t-a.t))
		l = ax.fill_between([a.t, b.t], [0.2, 0.8], color = color, picker=True)
		lines[l] = a
	# print(bt)



def draw_annot(srcs, ax, colors):
	arr = []
	X = namedtuple('X', ['e', 'node', 'c', 'type'])
	i = 0
	for sc in izip(srcs, colors):
		pprint(sc)
		print(type(sc[0]))
		for k,v in sc[0].items():
			for e in v:
				arr.append(X(e, k, sc[1], i))
		i = i + 1

	# pprint(arr)
	arr.sort(key = lambda x: x.e.t)
	pprint (arr)

	def y_gen(a,b,c):
		cur = a
		while True:
			yield cur
			cur = cur + c
			if cur > b: cur = cur - (b - a)

	yg = [y_gen(0.1, 0.8, 0.2) for i in range(0, len(ax))]

	for x in arr:
		if x.e.e == 1:
			y = yg[x.node].next()
			print (x)
			ax[x.node].annotate('%.5f,%s' % (x.e.t, x.e.i), xy=(x.e.t, y), xytext=(x.e.t, y+0.1),
					arrowprops=dict(facecolor=x.c, shrink=0.05), color = x.c)


f,ax = plt.subplots(nodes, sharex = True)
for i in range(0,nodes):
	ax[i].set_ylim(0, 1)
	draw(tx[i], ax[i], 'black')
	draw(rx[i], ax[i], 'blue')
	draw(drops[i], ax[i], 'red')
	ax[i].grid()

# draw_annot([tx, rx, drops], ax, ['black', 'blue', 'red'])

pprint(drops)


def onpick(event):
	# print(event.artist)
	if event.artist in lines:
		a = lines[event.artist]
		print(a)
	pass

	
f.canvas.mpl_connect('pick_event', onpick)

plt.show()

