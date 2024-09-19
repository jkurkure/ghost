#!/usr/bin/env python3
import os, time, sys, platformdirs, subprocess

start = time.time()
data_dir = platformdirs.user_data_dir(appname="ghost", appauthor="r93817dn")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
file_path = os.path.join(data_dir, f"{start}.log")

if (len(sys.argv) > 1):
    print(f"{' '.join(sys.argv[1:])} has been scheduled to run every minute and logs can be found at {file_path}")

    command = f"{' '.join(sys.argv[1:])} >> {file_path}"
    script = f'''
import os, time
while True:
    os.system("echo " + str(time.ctime()) + " >> " + r"{file_path}")
    os.system(r"{command}")
    time.sleep(60.0 - ((time.time() - {start}) % 60.0))
    '''

    helper = os.path.join(data_dir, f"{start}.pyw")
    with open(helper, "w") as f:
        f.write(script)

    # spinlock until helper exists
    while not os.path.exists(helper):
        pass
    subprocess.Popen(["pythonw", helper])
