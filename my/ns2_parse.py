
import re

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
tr_re_r = re.compile('r ' + tr_std_part('AGT'))
tr_re_s = re.compile('s ' + tr_std_part('AGT'))
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

Event = namedtuple('Event', ['e','t','i', 'ip','type'])

EventTypes = namedtuple('EventTypes', ['tx', 'rx', 'drops'])
def addNode(self, node):
	self.tx[node] = []
	self.rx[node] = []
	self.drops[node] = []
EventTypes.addNode = addNode
def lastNode(self):
	return max(self.tx.iterkeys())
EventTypes.lastNode = lastNode

	
# tx = {i:[] for i in range(0, nodes)}
# rx = {i:[] for i in range(0, nodes)}
# drops = {i:[] for i in range(0, nodes)}
# tx = {}
# rx = {}
# drops = {}

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


def parse_log_mo(r, m, et):
	md = m.groupdict()
	node = int(md['node'])

	if not node in et.tx:
		et.addNode(node)

	time = float(md['time'])
	infos = md['info']
	infod = parse_log_info(infos)

	if r == phy_send:
		et.tx[node].append(Event(t = time, e = 1, i = infos, ip = infod, type = 'send'))
	elif r == phy_sendOver:
		et.tx[node].append(Event(t = time, e = 0, i = infos, ip = infod, type = 'sendOver'))
	if r == phy_recv:
		et.rx[node].append(Event(t = time, e = 1, i = infos, ip = infod, type = 'recv'))
	elif r == phy_recvOver:
		et.rx[node].append(Event(t = time, e = 0, i = infos, ip = infod, type = 'recvOver'))
	elif r == phy_recvOverDrop:
		et.rx[node].append(Event(t = time, e = 0, i = infos, ip = infod, type = 'phy_recvOverDrop'))
		et.drops[node].append(Event(t = time, e = 1, i = infos, ip = infod, type = 'drop'))
		et.drops[node].append(Event(t = time + 0.0001, e = 0, i = infos, ip = infod, type = 'drop'))
	elif r == mac_drop:
		et.drops[node].append(Event(t = time, e = 1, i = infos, ip = infod, type = 'drop'))
		et.drops[node].append(Event(t = time + 0.0001, e = 0, i = infos, ip = infod, type = 'drop'))



def parse_log_line(l, et):
	# print (l)
	for r in rs_log:
		m = r.search(l)
		# print (m)
		if m:
			parse_log_mo(r, m, et)
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

def parse_tr_mo(r, m, et):
	md = m.groupdict()
	node = int(md['node'])

	if not node in et.tx:
		et.addNode(node)

	time = float(md['time'])
	infos = md['info']
	infod = parse_tr_info(infos)

	if r == tr_re_r:
		if node == 0:
			return
		et.rx[node].append(Event(t = time, e = 1, i = infos, ip = infod, type = 'r'))
		et.rx[node].append(Event(t = time+0.0005, e = 0, i = infos, ip = infod, type = 'r'))
		# pprint(rx)
	elif r == tr_re_s:
		et.tx[node].append(Event(t = time, e = 1, i = infos, ip = infod, type = 's'))
		et.tx[node].append(Event(t = time+0.0005, e = 0, i = infos, ip = infod, type = 's'))
		# pprint(tx)
	elif r == tr_re_D:
		et.drops[node].append(Event(t = time, e = 1, i = infos, ip = infod, type = 'D'))
		et.drops[node].append(Event(t = time+0.0005, e = 0, i = infos, ip = infod, type = 'D'))
		# pprint(drops)


def parse_tr_line(l, et):
	for r in rs_tr:
		# print (l)
		m = r.search(l)
		# print (m)
		if m:
			parse_tr_mo(r, m, et)
			return

# parse_log_line(phy_recvOverDrop_test)
# print(rx)


def parse_log_file(fname):
	et = EventTypes({}, {}, {})

	with open(fname) as f:
		for line in f:
			parse_log_line(line, et)

	return et

def parse_tr_file(fname):
	et = EventTypes({}, {}, {})

	with open(fname) as f:
		for line in f:
			parse_tr_line(line, et)

	return et


 