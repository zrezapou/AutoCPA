
import os
import time
import subprocess
from subprocess import check_output
from paramiko.client import SSHClient
import paramiko


client = SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())




addr="/home/zahra/"
folder=["redis-original", "redis-reorder"]
commands={1:"PING", 2:"SET", 3:"GET", 4:"INCR",
            5:"LPUSH", 6:"RPUSH", 7:"LPOP", 8:"RPOP", 9:"SADD", 10:"HSET", 11:"SPOP", 12:"LRANGE", 13:"MSET"}
os.chdir(addr)
for i in range(1, 14):
    for j in range(2):
        for k in range(3):
            print("i, j, k= ", i, j, k)
            stdin, output, stderr = client.exec_command('cpuset -l 0 pmc stat -- '+addr+folder[j]+'/src/redis-server '+ addr+folder[j]+'/redis.conf --protected-mode no')
            while True:
                try:
                    time.sleep(1)
                    result = subprocess.run([folder[j]+'/src/redis-cli', '-h', '129.97.75.35', '-p', '6379', 'ping'], stdout=subprocess.PIPE)
                    if result.stdout.decode('UTF-8')=="PONG\n":
                        print("Server is ready!")
                        break
                except:
                    continue
            for x in range(3):
                print(x+1, " run...")
                with open(os.devnull, "w") as trash:
                        subprocess.call(['cpuset', '-l', '0' ,folder[j]+'/src/redis-benchmark', '-h', '129.97.75.35', '-p', '6379', '-r', '100000000', '-n', '2000000', '-d', '100', '-c', '5', '-t', commands[i]], stdout=trash)
            subprocess.call([folder[j]+'/src/redis-cli', '-h', '129.97.75.35', '-p', '6379', 'shutdown', 'NOSAVE'])
            fileName=addr+folder[j]+"-"+commands[i]+str(k+1)+".txt"
            with open(fileName, "w") as f:
                output=stderr.readlines()
                st="".join(output)
                f.write(st)
            f.close()
