# -*- coding: UTF-8 -*-

import subprocess
import os
import glob
import time
import sys

def spawn_scripts(path, script, files_pattern):
    processes = []
    print path, script, files_pattern
    for infile in glob.glob( os.path.join(path, files_pattern) ):
        print infile
        to_start = "/usr/bin/python " + script + " " + infile
        print to_start
        processes.append(subprocess.Popen(["python", script, infile]))
    return processes

def wait_processes(processes):
    while len(processes):
        for p in processes:
            if p.poll() is not None:
                print "Process finished."
                processes.remove(p)
        time.sleep(10)

def usage():
    print """
    python multiproc_dir.py <script to run> <path/to/files> <begin_of_filenames»

    Example:
        python multiproc_dir.py script.py /home/plop/logs/ split-

    Will run script.py on each files which begin with split- in /home/plop/logs/

    """

if __name__ == '__main__':
    if len(sys.argv) == 4:
        script = sys.argv[1]
        path = sys.argv[2]
        files_pattern = sys.argv[3] + "*"
    else:
        usage()

    p = spawn_scripts(path, script, files_pattern)
    wait_processes(p)
    print "All processes finished."

