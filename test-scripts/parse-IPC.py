from collections import defaultdict
import os, glob
import pandas as pd


def find_files(dat_addr, inst, indx):
    source = os.getcwd()
    f=[]
    os.chdir(dat_addr)
    st="redis-"
    if indx:
        st=st+"reorder"
    else:
        st=st+"original"
    for file in glob.glob(st+"-"+inst+"*"):
        f1 = os.path.splitext(file)[0]
        f.append(f1)
    os.chdir(source)
    return f

def read_file(addr):
    with open(addr) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

def get_stat(stat, content, inst):
    leng=len(content)
    i=0
    while i<leng:
        spl=content[i].split()
        if len(spl)<5:
            i+=1
            continue
        if spl[1]=="instructions":
            i+=1
            stat[inst].append(float(spl[3]))
            return
        i+=1


folders=["./original/", "./reorder/"]
commands={1:"PING", 2:"SET", 3:"GET", 4:"INCR",
            5:"LPUSH", 6:"RPUSH", 7:"LPOP", 8:"RPOP", 9:"SADD", 10:"HSET", 11:"SPOP", 12:"LRANGE", 13:"MSET"}
def main():
    for i in range(2):
        stat=defaultdict(list)
        for j in range(1,14):
            files=find_files(folders[i], commands[j], i)
            for file in files:
                content=read_file(folders[i]+file+".txt")
                get_stat(stat, content, commands[j])

        df=pd.DataFrame(columns=list(stat.keys())+["file"])
        df2=pd.DataFrame(columns=list(stat.keys())+["metric"])

        for item in stat:
            df[item]=stat[item]
            mean=df[item].mean()
            std=df[item].std()
            df2[item]=[mean, std]
        df2["metric"]=["avg", "std"]
        df2=df2.set_index("metric")
        df["file"]=[1,2,3, 4,5]
        df=df.set_index("file")
        result=pd.concat([df, df2])
        result.to_csv(file+".csv")

if __name__=="__main__":
    main()
