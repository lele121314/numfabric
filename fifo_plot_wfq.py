import sys
import os
import matplotlib;
matplotlib.use('Agg');
del matplotlib;
import matplotlib.pyplot as plt;

f = open(sys.argv[1]+".out")
pre = sys.argv[1];
dir = sys.argv[1]

if not os.path.exists(dir):
  os.makedirs(dir)

xy = []
x = {}
y = {}

rtime = []
trate = []

stimes = {}
srates = {}
dtimes = {}
drates = {}
crates = {}


start_times = {}
finish_times = {}
stime_xaxis = {}
finish_xaxis = {}

total_capacity=10000*2.0;

qtimes = {}
fifo_1_qsizes = {}
fifo_2_qsizes = {}
qprices = {}

qwaittimes = {}
qfwaits  ={}

q0times = {}
q0deadlines = {}
q1times = {}
q1deadlines = {}
rincrements = {}
qvirtual_times = []
qvirtualtimes_times = []

dctcp_alphas = {}
dctcp_times = {}

def ewma(values, g=1.0/8):
    ret = []
    prev = 0
    for v in values:
        prev = prev * (1.0 - g) + v * g
        ret.append(prev)
    return ret

num_flows=1

for line in f:
  l1 = line.rstrip();
  xy = l1.split(' ');
  if(len(xy) > 1 and xy[0]=="num_flows"):
    num_flows=int(xy[1])
  if(xy[0] == "Rate"):
    sflow_id=int(xy[2])
    st1 = float(xy[3])
    srate=float(xy[4])

    if(sflow_id not in stimes):
      stimes[sflow_id] = []
      srates[sflow_id] = []

    stimes[sflow_id].append(st1)
    srates[sflow_id].append(srate)
  
  if(xy[0] == "DestRate"):
    flow_id=int(xy[2])
    t1 = float(xy[3])
    rate=float(xy[4])
    csfq_rate = float(xy[5])

    if(flow_id not in dtimes and (flow_id == 1 or flow_id == 2 or flow_id == 3 or flow_id == 4)): 
    #if(flow_id not in dtimes):
      dtimes[flow_id] = []
      drates[flow_id] = []
      crates[flow_id] = []

    if((flow_id == 1 or flow_id == 2 or flow_id == 3 or flow_id == 4)): 
        dtimes[flow_id].append(t1)
        drates[flow_id].append(rate)
        crates[flow_id].append(csfq_rate)

  if(len(xy)> 2 and xy[1] == "TotalRate"):
    rtime.append(float(xy[0]))
    trate.append(float(xy[2])/total_capacity)

  if(xy[0] == "start_time"):
    fid = int(xy[2])
    stime = float(xy[3])
    curtime = float(xy[4])
    if(fid not in start_times):
      start_times[fid] = []
      stime_xaxis[fid] = []
    start_times[fid].append(stime)
    stime_xaxis[fid].append(curtime)
 
  if(xy[0] == "finish_time"):
    fid = int(xy[2])
    stime = float(xy[3])
    curtime = float(xy[4])
    if(fid not in finish_times):
      finish_times[fid] = []
      finish_xaxis[fid] = []
    finish_times[fid].append(stime)
    finish_xaxis[fid].append(curtime)
 
  # example FIFO_QueueStats 
  #if(xy[0] == "QueueStats"):
  #  queue_id = xy[1]
  #  qtime = float(xy[2])
  #  qsize = float(xy[3])
  #  
  #  if(queue_id not in qtimes):
  #    qtimes[queue_id] = []
  #    qsizes[queue_id] = []
  #  
  #  qtimes[queue_id].append(qtime)
  #  qsizes[queue_id].append(qsize)

  if(len(xy) > 5):
    if(xy[3] == "DCTCP_DEBUG"):
      dctcp_nid = xy[10]
      dctcp_time = float(xy[0])
      dctcp_alpha = float(xy[7])
      if(dctcp_nid not in dctcp_times):
        dctcp_times[dctcp_nid] = []
        dctcp_alphas[dctcp_nid] = []
      (dctcp_times[dctcp_nid]).append(dctcp_time)
      (dctcp_alphas[dctcp_nid]).append(dctcp_alpha) 
  
  # new example line: QueueStats 0_0_1 1.499 fifo_2_size 70032 fifo_1_size 0 0
  if(xy[0] == "QueueStats"):
    queue_id = xy[1]
    qtime = float(xy[2])
    fifo_1_qsize = float(xy[6])
    fifo_2_qsize = float(xy[4])
    
    if(queue_id not in qtimes):
      qtimes[queue_id] = []
      fifo_1_qsizes[queue_id] = []
      fifo_2_qsizes[queue_id] = []
    
    qtimes[queue_id].append(qtime)
    fifo_1_qsizes[queue_id].append(fifo_1_qsize)
    fifo_2_qsizes[queue_id].append(fifo_2_qsize)
  
  
  #if(xy[0] == "QueueStats1"):
  #  queue_id = xy[1]
  #  qtime = float(xy[2])
  #  qfid = int(xy[3])
  #  qfdeadline = float(xy[4])
  #  qvirtual_time = float(xy[5])
# #   qnid = int(xy[5])

  #  if(queue_id == "0_0_1"):
  #    if(qfid not in q0times):
  #      q0times[qfid] = []
  #      q0deadlines[qfid] = []
  #    q0times[qfid].append(qtime)
  #    q0deadlines[qfid].append(qfdeadline)
  #    qvirtual_times.append(qvirtual_time)
  #    qvirtualtimes_times.append(qtime)
  
  if(xy[0] == "QWAIT"):
    qtime = float(xy[2])
    qfid = xy[3]
    qfwait = float(xy[5])
    queue_id = xy[1]

    if(queue_id == "0_0_1"):
      if(qfid not in qwaittimes):
        qwaittimes[qfid] = []
        qfwaits[qfid] = []
      qwaittimes[qfid].append(qtime)
      qfwaits[qfid].append(qfwait)
    
plt.figure(1)
plt.title("Unknown QueueOccupancy (FIFO 1)")
colors = ['r','b','g', 'm', 'c', 'y','k']
i=0
for key in fifo_1_qsizes:
    if(key == "0_0_1" or key == "2_2_0" or key == "3_3_0" or key == "1_1_4" or key == "1_1_5"):
      plt.plot(qtimes[key], ewma(fifo_1_qsizes[key], 1.0), colors[i], label=str(key)) 
      i = (i+1)%len(colors)
plt.xlabel('Time in seconds')
plt.ylabel('Unknown Queue occupancy in Bytes (FIFO 1)')
plt.legend(loc='lower right')
plt.savefig('%s/%s.%s.png' %(pre,pre,"known_fifo_1_queue_occupancy"))


plt.figure(8)
plt.title("Known QueueOccupancy (FIFO 2)")
colors = ['r','b','g', 'm', 'c', 'y','k']
i=0
for key in fifo_2_qsizes:
    if(key == "0_0_1" or key == "2_2_0" or key == "3_3_0" or key == "1_1_4" or key == "1_1_5"):
      plt.plot(qtimes[key], ewma(fifo_2_qsizes[key], 1.0), colors[i], label=str(key)) 
      i = (i+1)%len(colors)
plt.xlabel('Time in seconds')
plt.ylabel('Known Queue occupancy in Bytes (FIFO 2)')
plt.legend(loc='lower right')
plt.savefig('%s/%s.%s.png' %(pre,pre,"known_fifo_2_queue_occupancy"))
plt.draw()


plt.figure(2)
plt.title("Sum of all unknown sending rates / total sending capacity (ewma 0.01)")
plt.plot(rtime, ewma(trate, 0.01), colors[i]) 
plt.xlabel('Time in seconds')
plt.ylabel('Fraction of total capacity')
plt.legend(loc='upper right')
plt.savefig('%s/%s.%s.png' %(pre,pre,"unknown_load"))
plt.draw()

plt.figure(3)
plt.title("Sending rates at sender")
i=0
for key in stimes:
  plt.plot(stimes[key], ewma(srates[key], 1.0), colors[i]) 
  i = (i+1)%len(colors)

plt.xlabel('Time in seconds')
plt.ylabel('Rates in Mbps')
plt.legend(loc='upper right')
plt.savefig('%s/%s.%s.png' %(pre,pre,"rates"))
plt.draw()

plt.figure(6)
plt.title("Sending rates at destination")
i=0
for key in dtimes:
  plt.plot(dtimes[key], ewma(drates[key], 1.0), colors[i], label=str(key)) 
  i = (i+1)%len(colors)

plt.xlabel('Time in seconds')
plt.ylabel('Rates in Mbps')
plt.legend(loc='upper right')
plt.savefig('%s/%s.%s.png' %(pre,pre,"destination_rates"))
plt.draw()


plt.figure(7)
plt.title("Sending rates at destination (per-packet exponential averaged)")
i=0
for key in dtimes:
  plt.plot(dtimes[key], ewma(crates[key], 1.0), colors[i]) 
  i = (i+1)%len(colors)

plt.xlabel('Time in seconds')
plt.ylabel('Rates in Mbps')
plt.legend(loc='upper right')
plt.savefig('%s/%s.%s.png' %(pre,pre,"destination_rates_perpacket"))
plt.draw()

plt.show()

