'''
ftp文件服务器
'''

from socket import *
import sys,os,time
import signal

def class FtpServer(object):
    def __init__(self,conffd):
        self.connfd = conffd
        
        
    def do_list(self):
        file_list = os.listdir(FILE_PATH)
        if not file_list:
            self.conffd.send('文件为空'.encode())
            return
        else:
            self.conffd.send(b'ok')
            time.sleep(0.1)
            files = ''
            for file in file_list:
                if file[0] != '.' and \
                os.path.isfile(FILE_PATH + file):
                    files = files + file + '#'
                self.conffd.sendall(files.encode())
    
    def do_get(self,filename):
        try:
            fd = open(FILE_PATH + filename,'rb')
        except:
            self.conffd.send('文件不存在'.encode())
            return
        self.conffd.send(b'ok')
        time.sleep(0.1)
        
        while True:
            data = f.read(1024)
            if not data:
                time.sleep(0.1)
                self.conffd.send(b'##')
                break
            self.conffd.send(data)
        print('文件发送完毕')
    
    def do_put(self.filename):
        try:
            fd = open(FILE_PATH + filename,'wb')
        except:
            self.conffd.send('上传失败'.encode())
            return
        self.conffd.send(b'ok')
        whiel True:
            data = self.conffd.recv(2048)
            if data == '##':
                break
            else:
                fd.write(data)
        fd.close()
        print('上传完毕')
                
        
            

#文件库路径
FILE_PATH = "C:\Users\Administrator\Desktop\ftpFile\\"
HOST = ''
PORT = 8000
ADDR = (HOST,PORT)

#将文件服务器功能写在类中

class FtpServer(object):
    pass
    
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    
    #处理子进程退出
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print('Listen the port 8000.....')
    
    whle True:
        try:
            conffd,addr = s.accept()
        except KeyboardInterrupt:
            s.colose()
            sys.exit('服务器退出')
        except Exception as e:
            print('服务器异常：',e)
        print('已连接客户端：'，addr)
        
        #创建子进程
        pid = os.fork()
        if pid == 0:
            s.close()
            ftp = FtpServer(conffd)
            while True:
                data = conffd.recv(1024).decode()
                if not data or data[0] == 'Q':
                    conffd.close()
                    sys.exit('客户端退出')
                elif data[0] == 'L':
                    ftp.do_list()
                elif data[0] =='G':
                    filename = data.split(' ')[-1]
                    ftp.do_get(filename)
                elif data[0] == 'P':
                    filrname = data.split(' ')[-1]
                    fdp.do_put(filename)
        else:
            conffd.close()
            continue
            
    
if __name__ == '__main__':
    main()



