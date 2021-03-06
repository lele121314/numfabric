#!/usr/bin/python
import sys
import os
import subprocess
from subprocess import Popen, PIPE

arguments = {}

if(len(sys.argv) < 2):
    print("Usage : python run_config.py <executable> <config_file>")
    sys.exit()
plot_script=""
f=open(sys.argv[2], 'r')
for line in f:
    if(len(line) < 3):
        continue
    str1=(line.strip()).split('=')
    arg_key=str1[0]
    if(arg_key[0] == '#'):
        continue;
    arg_val=str1[1]
    if(arg_key == "plot_script"):
        plot_script=arg_val
        continue;
    arguments[arg_key] = arg_val

orig_prefix=arguments["prefix"]

# key components:

for deadline_mean in (10.0, 15.0):
    for load_val in (0.80, 1.0):
        for scheduler_mode in ('true', 'false'):
            arguments["load"] = str(load_val)
            arguments["deadline_mean"]=str(deadline_mean)
            arguments["scheduler_mode_edf"]=str(scheduler_mode)

            prefix_str=orig_prefix
            prefix_str=prefix_str+"_"+arguments["load"]+"_"+arguments["deadline_mean"]+"_"+arguments["scheduler_mode_edf"]
            arguments["prefix"] = prefix_str

            final_args=""
            for arg_key in arguments:
                final_args = final_args+" --"+arg_key+"=\""+arguments[arg_key]+"\""

            cmd_line="./waf --run \""+sys.argv[1]+final_args+"\""+" > "+prefix_str+".out "+" 2> "+prefix_str+".err"
            print(cmd_line)
            subprocess.call(cmd_line, shell="False")

#cmd_line="python "+plot_script+" "+prefix_str
#print(cmd_line)
#subprocess.call(cmd_line, shell="False")
f.close()
