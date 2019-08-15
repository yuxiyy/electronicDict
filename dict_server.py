"""
电子词典服务端代码
"""

from socket import *
from threading import Thread
import pymysql,os,sys

class Server:
    def __init__(self):
        # 创建套接字
        self.server = socket()
        self.server.bind(("0.0.0.0",8888))
        self.server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.server.listen(5)
        # 创建数据库连接对象,游标对象
        self.db, self.cur = self.connect_database()

    # 多线程处理客户端请求函数
    def handle(self,c):
        while True:
            data = c.recv(1024).decode()
            c.send("OK".encode())
            if data == "L":
                username = self.do_login(c)
            elif data == "R":
                self.do_register(c)
            elif data == "S":
                self.do_seekWord(c,username)
            elif data == "H":
                self.do_history(c)
            elif data == "E":
                break

    # 处理查看历史记录请求
    def do_history(self,c):
        c.recv(1024)
        sql = "select * from history"
        self.cur.execute(sql)
        resule = self.cur.fetchmany(10)
        for item in resule:
            for i in item:
                c.send(str(i).encode())
                c.recv(1024)
            c.send(b"end")
            c.recv(1024)
        c.send(b"#")

    # 处理查找单词请求
    def do_seekWord(self,c,username):
        while True:
            word=c.recv(1024).decode()
            if word == "#":
                c.send(b"OK")
                break
            sql = "select mean from words where word=%s"
            self.cur.execute(sql,[word])
            resule = self.cur.fetchone()
            if resule:
                c.send(resule[0].encode())
                sql = "insert into history(username,target_word) values(%s,%s)"
                self.cur.execute(sql,[username,word])
                self.db.commit()
            else:
                c.send("没有该单词".encode())

    # 处理注册请求
    def do_register(self,c):
        while True:
            username = c.recv(1024).decode()
            sql = "select password from user_message where username='%s'" % username
            self.cur.execute(sql)
            resule = self.cur.fetchone()
            if not resule:
                c.send("t".encode())
                email = c.recv(1024).decode()
                sql = "select password from user_message where email='%s'" %email
                self.cur.execute(sql)
                if not self.cur.fetchone():
                    c.send("t".encode())
                    password = c.recv(1024).decode()
                    c.send("OK".encode())
                    sql = "insert into user_message(username,password,email) values (%s,%s,%s)"
                    self.cur.execute(sql,[username,password,email])
                    self.db.commit()
                    break
                else:
                    c.send("f".encode())
            else:
                c.send("f".encode())

    # 处理登录请求
    def do_login(self,c):
        username = c.recv(1024).decode()
        sql = "select password from user_message where username='%s'" %username
        self.cur.execute(sql)
        resule = self.cur.fetchone()
        if resule:
            c.send("t".encode())
            password = c.recv(1024).decode()
            if password == resule[0]:
                c.send("t".encode())
            else:
                c.send("f".encode())
        else:
            c.send("f".encode())
        return username

    # 服务端主函数
    def main(self):
        while True:
            try:
                connfd,addr=self.server.accept()
                print("Connect from",addr)
                t = Thread(target=self.handle,args=(connfd,))
                t.setDaemon(True)
                t.start()
            except KeyboardInterrupt:
                sys.exit("服务器已退出")
            except Exception:
                sys.exit("出现未知错误,服务器已退出")

    # 连接数据库
    def connect_database(self):
        db = pymysql.connect(host='localhost',
                                  port=3306,
                                  user='root',
                                  password='123456',
                                  database='dict',
                                  charset='utf8')

        # 创建游标 (操作数据库语句,获取查询结果)
        cur = db.cursor()
        return db,cur

if __name__ == '__main__':
    server = Server()
    server.main()










