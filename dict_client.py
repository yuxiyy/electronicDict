"""
电子词典客户端代码
"""

from socket import *
import pymysql,os
from getpass import getpass

class Client:
    def __init__(self):
        self.client = socket()
        self.client.connect(("127.0.0.1",8888))

    # 主函数
    def main(self):
        while True:
            self.firstView()
            self.secondView()

    def firstView(self):  # 一级界面
        while True:
            print("""-----------------------Menu---------------------------
1.登录
2.注册
3.退出""")
            n = input()
            if n=="1":
                self.client.send("L".encode())
                self.client.recv(1024)
                if self.login():
                    break
            elif n=="2":
                self.client.send("R".encode())
                self.client.recv(1024)
                self.register()
            elif n=="3":
                self.client.send("E".encode())
                print("谢谢使用")
                os._exit(0)
            else:
                print("没有该功能")

    def secondView(self):  # 二级界面
        while True:
            print("""-----------------------Menu---------------------------
1.查单词
2.历史记录
3.注销""")
            n = input()
            if n=="1":
                self.client.send("S".encode())
                self.client.recv(1024)
                self.seekWord()
            elif n=="2":
                self.client.send("H".encode())
                self.client.recv(1024)
                self.history()
            elif n=="3":
                break
            else:
                print("没有该功能")

    # 查单词
    def seekWord(self):
        while True:
            inWord = input("请输入要查询的单词(输入#退出):")
            self.client.send(inWord.encode())
            if inWord == "#":
                self.client.recv(1024)
                break
            wordMean = self.client.recv(1024).decode()
            print("单词解释:",wordMean)

    # 查看历史记录
    def history(self):
        print("最近10条历史记录为:")
        self.client.send("history".encode())
        while True:
            data = self.client.recv(1024).decode()
            if data == "end":
                self.client.send(b"ok")
                print()
                continue
            elif data == "#":
                break
            self.client.send(b"ok")
            print(data,end="    ")

    # 登录
    def login(self):
        username = input("请输入用户名:")
        password = getpass()
        self.client.send(username.encode())
        if self.client.recv(1024).decode()=="t":
            self.client.send(password.encode())
            if self.client.recv(1024).decode()=="t":
                print("登录成功")
                return True
        print("您的用户名或密码输入错误")
        return False

    # 注册
    def register(self):
        while True:
            username = input("请输入用户名:")
            password = getpass()
            email = input("请输入邮箱:")
            self.client.send(username.encode())
            if self.client.recv(1024).decode()=="t":
                self.client.send(email.encode())
                if self.client.recv(1024).decode()=="t":
                    self.client.send(password.encode())
                    self.client.recv(1024)
                    print("注册成功")
                    break
            print("您的用户名或邮箱已存在,请重新输入")

if __name__ == '__main__':
    client = Client()
    client.main()

















