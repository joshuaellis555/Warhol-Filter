
import sys
import multiprocessing as mp
import marshal
import types
import inspect

import time

def _work(DataQ, ReturnQ,fun):
    try:
        args,k = DataQ.get()
        ReturnQ.put((k,fun(*args)))
        return True
    except Exception as e:
        print('\nERROR!:')
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("\n"+str(exc_tb.tb_lineno)+" "+str(exc_obj)+" "+str(exc_tb),"\n")
        ReturnQ.put((k,e))
        return True

def _worker(JobsDoneQ, NofJobs, NofWorkers, ReturnQ, DataQ,fun):
    # Worker loop
    working = True
    if not inspect.isclass(fun):
        fun = types.FunctionType(marshal.loads(fun), globals(), "fun")
    while working:
        jobNo = JobsDoneQ.get()
        _work(DataQ, ReturnQ,fun)
        if NofJobs-jobNo <= NofWorkers-1:
            working = False

class Buddy():

    def __new__(self,fun,jobsD):
        resultsQ=mp.Queue()

        if not inspect.isclass(fun):
            fun = marshal.dumps(fun.__code__)
        
        JobLen=len(jobsD)
        CORES = min(mp.cpu_count(),JobLen)

        JobsDoneQ=mp.Queue()
        ReturnQ=mp.Queue()
        ReadRequestQ=mp.Queue()
        DataQ=mp.Queue()
        DataBuffer=min(CORES*2,JobLen)
        keys=list(jobsD.keys())
        
        for i in range(JobLen):
            JobsDoneQ.put(i+1)
            ReadRequestQ.put(1)
        
        for i in range(DataBuffer):
            k=keys[i]
            DataQ.put((jobsD[k],k))
            ReadRequestQ.get()
            ReadRequestQ.put(0)
                

        p = {}
        for core in range(CORES):
            p[core] = mp.Process(target=_worker,
                              args=[JobsDoneQ, JobLen, CORES, ReturnQ, DataQ, fun])
            p[core].start()

        results={}
        
        #Read returned data from workers, add new read reqests
        for i in range(DataBuffer, JobLen+DataBuffer):
            r=ReturnQ.get()
            results[r[0]]=r[1]
            #print(iCompound,cType)
            if ReadRequestQ.get():
                k=keys[i]
                DataQ.put((jobsD[k],k))

        return results

