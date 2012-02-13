#!/usr/bin/env python2
# encoding: utf-8
#
# A simple video memory usage calculator
#
# Copyright © 2011 Intel Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice (including the next
# paragraph) shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
# Authors:
#   Eugeni Dodonov <eugeni.dodonov@intel.com>
#

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
