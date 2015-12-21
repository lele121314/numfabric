#!/usr/bin/python
import sys
import os
import numpy as np
import mp_solver_pfabric_link as solver

flow_start = "flow_start"
log_file = sys.argv[1]
method = sys.argv[2]
fid_index = 1
src_index = 6
dst_index = 7
fstart_index = 3
ecmp_hash_index = 3
weight_index = 3
fsize_index = 5

num_flow_index = 1
num_port_index = 1

numports = 0
numflows = 0

fh = open(log_file, "r")

sim = solver.Simulation()

for line in fh:
  l1 = line.rstrip();
  elems = l1.split(' ')
  if(len(elems) > 1):
    if(elems[0] == "num_flows"):
      numflows = int(elems[num_flow_index])
      # Allocate matrix now:
      f_matrix = np.zeros((numflows, numports))
      w = np.ones((numflows, 1)) # tbd
      c = np.ones((numports, 1))
      print("Allocated a matrix with %d rows and %d columns" %(numflows, numports))
    if(elems[0] == "num_ports"):
      numports = int(elems[num_port_index])
      sim.init_custom(numports, method)
    if(elems[0] == "flow_start" and len(elems) > 10): #or (elems[0] == "flow_stop")):
      # new flow, we need to insert into our matrix
      flow_id = int(elems[fid_index])
      src_id = int(elems[src_index]) -1
      dst_id = int(elems[dst_index]) -1
      flow_size = int(elems[fsize_index])
      flow_arrival = float(elems[fstart_index])
      weight = float(elems[weight_index])
      ecmp_hash = int(elems[ecmp_hash_index])

      if(elems[0] == "flow_start"):
        print("adding flow ...");
        sim.add_flow_list(src_id, dst_id, flow_id, flow_size, flow_arrival, weight, ecmp_hash)
        #f_matrix[flow_id, src_id] = 1
        #f_matrix[flow_id, dst_id] = 1
        #new_row = np.ones((numports, 0))
        #new_row[src_id] = 1
        #new_row[dst_id] = 1
        #add_row(new_row, flow_id, flow_size)
        #print("flow added (%d %d %d) A=" %(flow_id, src_id, dst_id))
        #print f_matrix
        #solver.main_solver(f_matrix, w, c, numports, numflows)
      #else:
        #f_matrix[flow_id, src_id] = 0
        #f_matrix[flow_id, dst_id] = 0
        #print("flow removed (%d %d %d) A=" %(flow_id, src_id, dst_id))
        #print f_matrix
        #solver.main_solver(f_matrix, w, c, numports/2.0, numflows)

#After everything...

sim.startSim()

