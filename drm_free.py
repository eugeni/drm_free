#!/usr/bin/python

import sys

def calc_video_memory():
    data = open("/proc/dri/0/vma").readlines()
    processes = {}
    for line in data[1:]:
        line = line.strip()
        if not line:
            continue
        pid, mem, flags, addr = line.split()
        mem_start, mem_end = mem.split('-')
        size = int(mem_end, 16) - int(mem_start, 16)
        if pid not in processes:
            cmd = "unknown"
            with open("/proc/%s/stat" % pid, "r") as fd:
                tmp = fd.readline()
                cmd = tmp.split()[1]
            processes[pid] = {"cmd": cmd, "pages": [], "total": 0}
        processes[pid]["total"] += size
        processes[pid]["pages"].append((addr, size))
    return processes


if __name__ == "__main__":
    verbose = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "-v":
            verbose = True
    processes = calc_video_memory()
    for pid in processes:
        total = processes[pid]["total"]
        total_m = total / (1024.0 * 1024)
        print "PID %s %s: total %.4fM" % (pid, processes[pid]["cmd"], total_m)
        if verbose:
            for addr, size in processes[pid]["pages"]:
                print "\t%s: %d" % (addr, size)
