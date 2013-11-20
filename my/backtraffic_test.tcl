


set val(chan)          Channel/WirelessChannel      ;# channel type
set val(prop)          Propagation/TwoRayGround     ;# radio-propagation model
set val(netif)         Phy/WirelessPhy/802_15_4     ;# network interface type
set val(mac)           Mac/802_15_4                 ;# MAC type
set val(ifq)           Queue/DropTail/PriQueue      ;# interface queue type
set val(ll)            LL/LL802_15_4                           ;# link layer type
# set val(ll)            LL                           ;# link layer type
set val(ant)           Antenna/OmniAntenna          ;# antenna model
set val(ifqlen)        2	         	    ;# max packet in ifq

set val(rp)            NOAH			    ;# protocol tye
set val(x)             10			    ;# X dimension of topography
set val(y)             10			    ;# Y dimension of topography
# set val(energymodel)   EnergyModel		    ;# Energy Model
set val(initialenergy) 100			    ;# value

set val(assocStart) 0.4
set val(assocTime) 1

Agent/NOAH set be_random_ 0


set argNN [lindex $argv 0]
set argSizeBack [lindex $argv 1]
set argIntervalBack [lindex $argv 2]
set argSize [lindex $argv 3]
# set argBO [lindex $argv 1]
# set argSO [lindex $argv 2]

set argBO ""
set argSO ""

set val(nn)  [expr {$argNN != "" ? $argNN : 2}]                ;# number of mobilenodes


# set val(operationStart) 1
set val(operationStart) [expr $val(assocStart) + $val(assocTime) * $val(nn)]
set val(stop)           [expr $val(operationStart) + 10.1]                ;# simulation period 

set val(bmsg-interval) 0.003      ;# 1/60
set val(bmsg-size)     [expr {$argSize != "" ? $argSize : 120}]              ;# 1..120
set val(bmsg-start)    $val(operationStart)
set val(bmsg-stop)    [expr $val(stop) - 0.1]

set val(pois-interval) [expr {$argIntervalBack != "" ? $argIntervalBack : 3}]
set val(pois-size)     [expr {$argSizeBack != "" ? $argSizeBack : 10}]              ;# 1..120
set val(pois-rate)     250
set val(pois-start)    $val(operationStart)
set val(pois-stop)    [expr $val(stop) - 0.1]

set val(BO) [expr {$argBO != "" ? $argBO : 3}]
set val(SO) [expr {$argSO != "" ? $argSO : 3}]
set val(beacon_enabled) 0
# set val(GTS_setting) 0xAE

set namtracename    backtraffic_test.nam

set ns        		[new Simulator]
set tracefd       	[open backtraffic_test.tr w]
set namtrace      	[open $namtracename w]

$ns trace-all $tracefd
$ns namtrace-all-wireless $namtrace $val(x) $val(y)

$ns puts-nam-traceall {# nam4wpan #}       ;# inform nam that this is a trace file for wpan (special handling needed)

Mac/802_15_4 wpanCmd verbose on
Mac/802_15_4 wpanNam namStatus on       ;# default = off (should be turned on before other 'wpanNam' commands can work)
# Mac/802_15_4 wpanNam ColFlashClr gold      ;# default = gold

set dist(5m)  7.69113e-06
set dist(9m)  2.37381e-06
set dist(10m) 1.92278e-06
set dist(11m) 1.58908e-06
set dist(12m) 1.33527e-06
set dist(13m) 1.13774e-06
set dist(14m) 9.81011e-07
set dist(15m) 8.54570e-07
set dist(16m) 7.51087e-07
set dist(20m) 4.80696e-07
set dist(25m) 3.07645e-07
set dist(30m) 2.13643e-07
set dist(35m) 1.56962e-07
set dist(40m) 1.20174e-07
Phy/WirelessPhy set CSThresh_ $dist(40m)
Phy/WirelessPhy set RXThresh_ $dist(40m)

set topo       [new Topography]
$topo load_flatgrid $val(x) $val(y)

create-god $val(nn)

$ns node-config \
            -adhocRouting $val(rp) \
            -llType $val(ll) \
             -macType $val(mac) \
             -ifqType $val(ifq) \
             -ifqLen $val(ifqlen) \
             -antType $val(ant) \
             -propType $val(prop) \
             -phyType $val(netif) \
             -channel [new $val(chan)] \
             -topoInstance $topo \
             -agentTrace ON \
             -routerTrace ON \
             -macTrace  OFF \
             -movementTrace OFF \
             -initialEnergy $val(initialenergy) \
             -rxPower 35.28e-3 \
             -txPower 31.32e-3 \
         -idlePower 712e-6 \
         -sleepPower 144e-9  
         # -energyModel $val(energymodel) \



for {set i 0} {$i < $val(nn) } { incr i } {
        set mnode_($i) [$ns node]
}

proc setNodeGTS {node gts} {
    set mac [ [set node] getMac 0]
    puts $mac
    set ll [$mac up-target]
    puts $ll
    $ll set GTS_delivery_ $gts
}

if {[info exists val(GTS_setting)]} {
    setNodeGTS $mnode_(0) 1
}

# exit

set cmd "[$mnode_(0) set ragent_] routing $val(nn) 0 0"
for {set to 1} {$to < $val(nn) } {incr to} {
    set hop $to
    set cmd "$cmd $to $hop"
}
# puts "$cmd"
eval $cmd
# puts ""

for {set i 1} {$i < $val(nn) } {incr i} {
    set cmd "[$mnode_($i) set ragent_] routing $val(nn)"
    for {set to 0} {$to < $val(nn) } {incr to} {
        if {$to == $i} {
            set hop $to
        } else {
            set hop 0
        }
        set cmd "$cmd $to $hop"
    }
    # puts "$cmd"
    eval $cmd
    # puts ""
}



for {set i 1} {$i < $val(nn) } { incr i } {
    $mnode_($i) set X_ [ expr {$val(x) * rand()} ]
    $mnode_($i) set Y_ [ expr {$val(y) * rand()} ]
    $mnode_($i) set Z_ 0
}

# Position of Sink
$mnode_(0) set X_ [ expr {$val(x)/2} ]
$mnode_(0) set Y_ [ expr {$val(y)/2} ]
$mnode_(0) set Z_ 0.0
$mnode_(0) label "Sink"

for {set i 0} {$i < $val(nn)} { incr i } {
    $ns initial_node_pos $mnode_($i) 10
}

proc get_rand_time {first last number} {
    # puts "get_rand_time $first $last $number"
    set times ""
    set interval [expr $last - $first]
    set maxrval [expr pow(2,31)]
    set intrval [expr $interval/$maxrval]

    for { set i 0 } { $i < $number } { incr i } {
        set randtime [expr ([ns-random] * $intrval) + $first]
        # XXX include only 6 decimals (i.e. usec)
        lappend times [format "%.6f" $randtime]
    }
    # puts "$times"
    return $times
}


$ns at 0.0 "$mnode_(0) NodeLabel PAN Coor"
$ns at 0.0 "$mnode_(0) sscs startPANCoord $val(beacon_enabled) $val(BO) $val(SO)"

if {[info exists val(GTS_setting)]} {
    $ns at $val(assocStart) "$mnode_(0) sscs MLME_GTS_indication 0 [expr {$val(GTS_setting)}]"
}

# # set times [get_rand_time 0.5 5 $val(nn)]
# # puts $times
for {set i 1} {$i < $val(nn)} { incr i } {
    # set t [lindex $times $i]
    set t [expr $val(assocStart) + $val(assocTime) * ($i - 1)]
    puts "t = $t"
    $ns at $t "$mnode_($i) sscs startDevice $val(beacon_enabled) 0 0 $val(BO) $val(SO)"
}



# for {set i 0} {$i < $val(nn)} { incr i } {
#     set agent($i) [new Agent/Broadcastbase]
#     $mnode_($i) attach $agent($i) 250
#     $agent($i) set fid_ $i
#     set game($i) [new Application/BroadcastbaseApp] 
#     $game($i) set bsize_ $val(bmsg-size)
#     $game($i) set bmsg-interval_ $val(bmsg-interval)
#     $game($i) set propagate_ 0
#     $game($i) attach-agent $agent($i)     
# }
# $ns at $val(bmsg-start) "$game(0) start "
# $ns at $val(bmsg-stop)  "$game(0) stop "



proc poissontraffic { src dst } {
   global ns val mnode_
   set udp($src) [new Agent/UDP]
   eval $ns attach-agent \$mnode_($src) \$udp($src)
   set null($dst) [new Agent/Null]
   eval $ns attach-agent \$mnode_($dst) \$null($dst)
   set expl($src) [new Application/Traffic/Exponential]
   eval \$expl($src) set packetSize_ \$val(pois-size)
   eval \$expl($src) set burst_time_ 0
   eval \$expl($src) set idle_time_ [expr \$val(pois-interval)*1000.0-\$val(pois-size)*8/\$val(pois-rate)]ms    ;# idle_time + pkt_tx_time = interval
   eval \$expl($src) set rate_ \$val(pois-rate)k
   eval \$expl($src) attach-agent \$udp($src)
   eval $ns connect \$udp($src) \$null($dst)
   $ns at $val(pois-start) "$expl($src) start"
   $ns at $val(pois-stop) "$expl($src) stop"
}

for {set i 1} {$i < $val(nn)} { incr i } {
    poissontraffic $i 0
}



# #Setup a UDP connection
# set udp [new Agent/UDP]
# $ns attach-agent $mnode_(0) $udp
# set sink [new Agent/Null]
# $ns attach-agent $mnode_(1) $sink

# $ns connect $udp $sink
# $udp set fid_ 1

# #Setup a CBR over UDP connection
# set cbr [new Application/Traffic/CBR]
# $cbr attach-agent $udp
# $cbr set type_ CBR
# $cbr set packet_size_ $val(bmsg-size)
# $cbr set interval_ $val(bmsg-interval)
# set pktType cbr

# $ns at $val(bmsg-start) "$cbr start"
# $ns at $val(bmsg-stop) "$cbr stop"







# Telling nodes when the simulation ends
for {set i 0} {$i < $val(nn) } { incr i } {
    $ns at $val(stop) "$mnode_($i) reset;"
}


# ending nam and the simulation
$ns at $val(stop) "$ns nam-end-wireless $val(stop)"
$ns at $val(stop) "stop"
$ns at [expr $val(stop) + 0.01] "puts \"end simulation\"; $ns halt"
proc stop {} {
    global ns tracefd namtrace
    $ns flush-trace
    # close $tracefd
    # close $namtrace

    set hasDISPLAY 0
    foreach index [array names env] {
        puts "$index: $env($index)"
        if { ("$index" == "DISPLAY") && ("$env($index)" != "") } {
                set hasDISPLAY 1
        }
    }
    if { "$hasDISPLAY" == "1" } {
        exec nam $namtracename &
    }
}


$ns run


