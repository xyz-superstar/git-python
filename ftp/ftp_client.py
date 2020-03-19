from socket import *
import sys,time

#基本功能操作
class FtpClient(object):
    def __init__(self,sockfd):
        self.sockfd = sockfd
#显示文件清单
    def do_list(self):
        self.sockfd.send(b'L')#发送请求
        data = self.sockfd.recv(1024).decode()
        if data == 'ok':
            data = self.sockfd.recv(4096).decode()
            files = data.split('#')
            for file in files:
                print(file)
            print('文件列表展示完毕\n')
        else:
            #由服务器发送失败原因
            print(data.decode())
#下载文件
    def do_get(self,filename):
        self.sockfd.send((b'G ' + filename).encode())
        data = self.sockefd.recv(1024).decode()
        if data == 'ok':
            fd = open(filename,'wb')
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break
                fd.write(data)
            fd.close()
            print('%s下载完毕\n'%filename)
        else:
            print(data.decode())
            
#退出程序
    def do_quit(self):
        self.sockfd.send(b'Q')

#上传文件
    def do_put(self,filename):
        try:
            fd = open(filenam,'rb')
        except:
            print('没有找到文件')
            return
        self.sockfd.send((b'P ' + filename).encode())
        data = self.sockefd.recv(1024).decode()
        if data == 'ok':
            while True:
                data = fd.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b'##')
                    fd.close()
                    print('\n%s上传完毕\n'%filename)
                    break
                else:
                    self.sockfd.send(data)
        else:
            print(data.decode())
            
                
    
def main():
    if len(sys.argv) < 3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,ADDR)
    
    sockfd = socket()
    try:
        sockefd.connect(ADDR)
    except:
        print('连接失败')
        return
        
    ftp = FtpClient(sockfd)#功能类对象
        
    while True:
        print('====================命令 选项===================')
        print('==================== list =====================')
        print('==================== get file==================')
        print('==================== put file==================')
        print('===============================================')
        
        cmd = input('请输入命令>>')
        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd[:3] == 'get':
            filename = cmd.split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[:3] =='put':
            filename = cmd.split(' ')[-1]
            ftp.do_put(filename)
        elif cmd.strip() == 'quit':
            ftp.do_quit()
            sockfd.close()
            print('感谢使用')
        else:
            print("命令输入错误，请重新输入")
            sys.exit()
    

if __name__ == '__main__':
    main()
