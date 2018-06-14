import json
import subprocess
from time import sleep
import time
from multiprocessing import Process, Manager, Value
from ctypes import c_char_p
import sys
def complie(complier,extension,input_,result,output_):
    output = subprocess.check_output(
        complier+' main'+extension+' '+output_,
        shell=True,
        input=bytes(input_, 'utf-8'),
    )
    result.value = output.decode()
if __name__ == '__main__':
    outTime = 1
    manager = Manager()
    result = manager.Value(c_char_p, "")
    #테스트케이스 여는곳
    with open('testCase.json') as data_file:
        data = json.load(data_file)
    #어떤 파일인지 확인파일 여는곳
    with open('fileState.json') as data_file:
        file = json.load(data_file)
    #컴파일 돌리는곳
    totaltime = 0
    if file['compiler'] == 'javac':
        outTime = 3
    for i in range(1,data['caseNum']+1):
        try:
            t = Process(target=complie, args=(file['compiler'],file['extension'],data['case '+str(i)]['input'],result,file['output']))
            t.start()
            nowTime = time.time()
            t.join(outTime)
            totaltime += time.time() - nowTime
            if t.is_alive():
                t.terminate()
                sleep(0.1)
                print('TimeOut!!',end=' ')
                sys.exit(1)
            elif data['case '+str(i)]['output'] != result.value:
                print(data['case '+str(i)]['output'], result.value)
                print('Fail',end=' ')
                sys.exit(1)
        except Exception as e:
            print('Error\n',e,end=' ')
            sys.exit(1)
    totaltime_Result = totaltime / data['caseNum'] 
    totaltime_Result = int(totaltime_Result)
    print('success! Time :',totaltime_Result,'TotalTime :',totaltime,end=' ')
