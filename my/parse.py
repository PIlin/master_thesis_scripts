
import sys
import re

from pprint import pprint

import matplotlib.pyplot as plt 

from itertools import izip
from collections import namedtuple


phy_recv_test = r"[wpan/p802_15_4phy.cc::recv][0.000320](node 0) incoming pkt: type = M_CM7_Bcn-Req, src = 0, dst = -1, uid = 0, mac_uid = 0, size = 8"
phy_recv = re.compile('.*p802_15_4phy.cc::recv\]\[(?P<time>.*)\]\(node (?P<node>.*)\) incoming pkt: (?P<info>.*)')

phy_recvOver_test = r"[wpan/p802_15_4phy.cc::recvOverHandler][0.000768](node 2) incoming pkt: type = M_CM7_Bcn-Req, src = 0, dst = -1, uid = 0, mac_uid = 0, size = 8 --> PD_DATA_indication()"
phy_recvOver = re.compile('.*p802_15_4phy.cc::recvOverHandler\]\[(?P<time>.*)\]\(node (?P<node>.*)\) incoming pkt: (?P<info>.*)')

phy_recvOverDrop_test = r"[D][ERR][wpan/p802_15_4phy.cc::recvOverHandler::779][5.090404](node 1) dropping pkt: type = tcp, src = 0, dst = -1, uid = 0, mac_uid = 50, size = 7"
phy_recvOverDrop = re.compile('\[D\]\[(?P<reason>.*?)\].*p802_15_4phy.cc::recvOverHandler:{0,2}(?P<line>.*)\]\[(?P<time>.*)\]\(node (?P<node>.*)\) dropping pkt: (?P<info>.*)')

phy_send_test = r"[wpan/p802_15_4phy.cc::recv][0.000320](node 0) outgoing pkt: type = M_CM7_Bcn-Req, src = 0, dst = -1, uid = 0, mac_uid = 0, size = 8"
phy_send = re.compile('.*p802_15_4phy.cc::recv\]\[(?P<time>.*)\]\(node (?P<node>.*)\) outgoing pkt: (?P<info>.*)')

phy_sendOver_test = r"[wpan/p802_15_4phy.cc::sendOverHandler][0.000768](node 0) sending over: type = M_CM7_Bcn-Req, src = 0, dst = -1, uid = 0, mac_uid = 0, size = 14"
phy_sendOver = re.compile('.*p802_15_4phy.cc::sendOverHandler\]\[(?P<time>.*)\]\(node (?P<node>.*)\) sending over: (?P<info>.*)')

mac_drop_test = r"[D][APS][wpan/p802_15_4mac.cc::recv::1204][0.664063](node 2) dropping pkt: type = M_CM7_Bcn-Req, src = 1, dst = -1, uid = 0, mac_uid = 3, size = 8"
mac_drop = re.compile('\[D\]\[(?P<reason>.*?)\].*p802_15_4mac.cc::recv:{0,2}(?P<line>.*)\]\[(?P<time>.*)\]\(node (?P<node>.*)\) dropping pkt: (?P<info>.*)')

rs_log = (phy_recv, phy_recvOver, phy_recvOverDrop, phy_send, phy_sendOver, mac_drop)


"s 5.000427946 _0_ RTR  --- 0 undefined 120 [0 0 0 0] ------- [0:250 -1:250 32 0] "
tr_std_part = lambda src: '(?P<time>.*) _(?P<node>.*)_ %s .*?--- (?P<info>.*?) \[' % (src,)
tr_re_r = re.compile('r ' + tr_std_part('RTR'))
tr_re_s = re.compile('s ' + tr_std_part('RTR'))
tr_re_D = re.compile('D ' + tr_std_part('IFQ'))

rs_tr = (tr_re_r, tr_re_s, tr_re_D)


info_src = re.compile(r'src = ([-\d]*)')
info_dst = re.compile(r'dst = ([-\d]*)')
info_type = re.compile(r'type = ([-\d]*)')
info_size = re.compile(r'size = ([-\d]*)')

info_fields = ['src', 'dst', 'type', 'size']
info_re = {}
for f in info_fields:
	info_re[f] = re.compile('%s = ([-\d]*)' % (f,))



nodes = 3
Event = namedtuple('Event', ['e','t','i', 'ip','type'])
tx = {i:[] for i in range(0, nodes)}
rx = {i:[] for i in range(0, nodes)}
drops = {i:[] for i in range(0, nodes)}
# print(tx)

def try_int(val):
	try:
		return int(val)
	except ValueError:
		return val

def parse_log_info(info):
	ip = {}
	for k,v in info_re.items():
		m = v.search(info)
		if m:
			ip[k] = try_int(m.group(1))
	# print (ip)
	return ip


def parse_log_mo(r, m):
	md = m.groupdict()
	node = int(md['node'])

	if node >= nodes:
		return

	time = float(md['time'])
	infos = md['info']
	infod = parse_log_info(infos)

	if r == phy_send:
		tx[node].append(Event(t = time, e = 1, i = infos, ip = infod, type = 'send'))
	elif r == phy_sendOver:
		tx[node].append(Event(t = time, e = 0, i = infos, ip = infod, type = 'sendOver'))
	if r == phy_recv:
		rx[node].append(Event(t = time, e = 1, i = infos, ip = infod, type = 'recv'))
	elif r == phy_recvOver:
		rx[node].append(Event(t = time, e = 0, i = infos, ip = infod, type = 'recvOver'))
	elif r == phy_recvOverDrop:
		rx[node].append(Event(t = time, e = 0, i = infos, ip = infod, type = 'phy_recvOverDrop'))
		drops[node].append(Event(t = time, e = 1, i = infos, ip = infod, type = 'drop'))
		drops[node].append(Event(t = time + 0.0001, e = 0, i = infos, ip = infod, type = 'drop'))
	elif r == mac_drop:
		drops[node].append(Event(t = time, e = 1, i = infos, ip = infod, type = 'drop'))
		drops[node].append(Event(t = time + 0.0001, e = 0, i = infos, ip = infod, type = 'drop'))



def parse_log_line(l):
	# print (l)
	for r in rs_log:
		m = r.search(l)
		# print (m)
		if m:
			parse_log_mo(r, m)
			return

def parse_tr_info(info):
	ip = {}
	# print (info)
	il = info.split()
	
	ip['number'] 	= try_int(il[0])
	ip['type']		= 		  il[1]
	ip['size'] 		= try_int(il[2])

	# print(ip)
	return ip

def parse_tr_mo(r, m):
	md = m.groupdict()
	node = int(md['node'])

	if node >= nodes:
		return

	time = float(md['time'])
	infos = md['info']
	infod = parse_tr_info(infos)

	if r == tr_re_r:
		if node == 0:
			return
		rx[node].append(Event(t = time, e = 1, i = infos, ip = infod, type = 'r'))
		rx[node].append(Event(t = time+0.0005, e = 0, i = infos, ip = infod, type = 'r'))
		# pprint(rx)
	elif r == tr_re_s:
		tx[node].append(Event(t = time, e = 1, i = infos, ip = infod, type = 's'))
		tx[node].append(Event(t = time+0.0005, e = 0, i = infos, ip = infod, type = 's'))
		# pprint(tx)
	elif r == tr_re_D:
		drops[node].append(Event(t = time, e = 1, i = infos, ip = infod, type = 'D'))
		drops[node].append(Event(t = time+0.0005, e = 0, i = infos, ip = infod, type = 'D'))
		# pprint(drops)


def parse_tr_line(l):
	for r in rs_tr:
		# print (l)
		m = r.search(l)
		# print (m)
		if m:
			parse_tr_mo(r, m)
			return


# fname = 'log.txt'
fname = 't4.tr'
with open(fname) as f:
	for line in f:
		# parse_log_line(line)
		parse_tr_line(line)

print (tx)

# parse_log_line(phy_recvOverDrop_test)
# print(rx)
# sys.exit()

def pairwise(iterable):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)

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


	# ax.broken_barh(bt, (0,0.99), facecolors=color, picker=True)

	# yg = y_gen(0.1, 0.8, 0.2)
	# for e in src:
	# 	if e.e == 1:
	# 		print (e)
	# 		y = yg.next()
	# 		ax.annotate(e.i, xy=(e.t, y), xytext=(e.t, y+0.1),
	# 			arrowprops=dict(facecolor=color, shrink=0.05),)

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

