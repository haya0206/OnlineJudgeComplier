import docker
from io import BytesIO
import tarfile
import time
import json
from flask import request, Flask
#보낼 파일 만드는 함수
def tarMake(fileState, testCase, inDocker):
    
    tarstream = BytesIO()
    tar = tarfile.TarFile(fileobj=tarstream, mode='w')
    
    file_data = fileState['source'].encode('utf8')
    tarinfo = tarfile.TarInfo(name='main'+fileState['extension'])
    tarinfo.size = len(file_data)
    tarinfo.mtime = time.time()
    tar.addfile(tarinfo, BytesIO(file_data))
    
    file_data2 = testCase.encode('utf8')
    tarinfo2 = tarfile.TarInfo(name='testCase.json')
    tarinfo2.size = len(file_data2)
    tarinfo2.mtime = time.time()
    tar.addfile(tarinfo2, BytesIO(file_data2))
    
    file_data3 = inDocker.encode('utf8')
    tarinfo3 = tarfile.TarInfo(name='inDocker.py')
    tarinfo3.size = len(file_data3)
    tarinfo3.mtime = time.time()
    tar.addfile(tarinfo3, BytesIO(file_data3))
    
    fileState = json.dumps(fileState)
    file_data4 = fileState.encode('utf8')
    tarinfo4 = tarfile.TarInfo(name='fileState.json')
    tarinfo4.size = len(file_data4)
    tarinfo4.mtime = time.time()
    tar.addfile(tarinfo4, BytesIO(file_data4))
    
    tar.close()
    return tarstream
    
def compilerSet(num):
    fileState = {}
    num = int(num)
    if num == 1:
        fileState = {
            "compiler":"gcc",
            "extension":".c",
            "output" : "-o a.out -lm --static -std=c99 && ./a.out"
        }
    elif num == 2:
        fileState = {
            "compiler":"g++",
            "extension":".cc",
            "output" : "-o a.out && ./a.out"
        }
    elif num == 3:
        fileState = {
            "compiler":"javac",
            "extension":".java",
            "output" : "&& java main"
        }
    elif num == 4:
        fileState = {
            "compiler":"python",
            "extension":".py",
            "output" : ""
        }
    elif num == 5:
        fileState = {
            "compiler":"python3",
            "extension":".py",
            "output" : ""
        }
    return fileState
app = Flask(__name__)
@app.route('/', methods=['POST'])
def mainF():
    if request.method == 'POST':
        
        with open(request.form['qnum']+'.json') as data_file:    
            data = json.load(data_file)
        
        with open('inDocker.py', 'r') as data_file:    
            inDocker = data_file.read()
        
        fileState = compilerSet(int(request.form['languege']))
        fileState["source"] = request.form['source']
        data = json.dumps(data)
        tarstream = tarMake(fileState , data, inDocker)
        
        client = docker.from_env()
        a = client.containers.run("haya0206/ubuntu:basic", detach=True, tty=True)
        tarstream.seek(0)
        a.put_archive(path='/',data=tarstream)
        result = a.exec_run('python3 inDocker.py').output.decode()
        print(result)
        return result
        a.stop()
if __name__ == '__main__':
    app.run(host='0.0.0.0')
