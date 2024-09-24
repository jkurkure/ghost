#!/usr/bin/env python3
import os, time, sys, platformdirs, subprocess, random, pickle

start = time.time()
data_dir = platformdirs.user_data_dir(appname="ghost", appauthor="jkurkure")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

file_path = os.path.join(data_dir, f"{start}.log")
data_path = os.path.join(data_dir, "ghost.dat")


if "--kill" in sys.argv:
    name = sys.argv[sys.argv.index("--kill") + 1]
    with open(data_path, "rb") as file:
        registry = pickle.load(file)
    if name in registry:
        os.kill(registry[name], 9)
        del registry[name]
        with open(data_path, "wb") as file:
            pickle.dump(registry, file)
    else:
        print(f"Job with name {name} not found")
elif "--list" in sys.argv:
    with open(data_path, "rb") as file:
        registry = pickle.load(file)
    for name, pid in registry.items():
        print(f"{name}: {pid}")

elif (len(sys.argv) > 1):
    print(f"{' '.join(sys.argv[1:])} has been scheduled to run every minute and logs can be found at {file_path}\n")

    command = f"{' '.join(sys.argv[1:])} >> {file_path} 2>&1"
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
    p = subprocess.Popen(["python3", helper])
    
    name = input("Give your scheduled job a name: ")
    if os.path.exists(data_path):
        with open(data_path, "rb") as file:
            registry = pickle.load(file)
    else:
        registry = {}

    if name in registry:
        while name in registry:
            name = input("Name already exists, please choose another name: ")
    registry[name] = p.pid

    with open(data_path, "wb") as file:
        pickle.dump(registry, file)
