import socket   #导入socket模块
import re
from multiprocessing import Process #导入进程模块
from index import html1,html2,html3
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiderman.spiders.spider import MySpider
from urllib import parse

#设置静态文件根目录
HTML_ROOT_DIR='./html'
def handle_client(client_socket):
    """处理客户端连接请求"""
    request_data=client_socket.recv(1024)
    print(request_data)
    request_lines=request_data.splitlines()
    for line in request_lines:
        print(line)
    #'GET / HTTP/1.1'
    request_start_line=request_lines[0].decode("utf-8")
 
    print("*"*10)
    print(request_start_line)
     
    #提取用户请求的文件名

    file_name=re.match(r"\w+ +(/[^ ]*) ",str(request_start_line)).group(1)
    

    
    if "/" == file_name:#open the index file
        file_name='/index.html'
        response_start_line="HTTP/1.1 200 ok\r\n"
        response_heads="Server: My server\r\n"
        response_body=html1+html3
    
    elif '?' in file_name:
        params=parse.parse_qs( parse.urlparse( file_name ).query) #search the profs.
        response_start_line="HTTP/1.1 200 ok\r\n"
        response_heads="Server: My server\r\n"
        crawl(' '.join(params['query']), client_socket=client_socket,response_heads=response_start_line+response_heads,response_body=[html1,html2,html3])
        return 
    else:# open the other files
        try:
            file=open(HTML_ROOT_DIR+file_name,"rb")
        except IOError:
            response_start_line="HTTP/1.1 404 Not Found\r\n"
            response_heads="Server: My server\r\n"
            response_body="The file:{0} not found!".format(file_name)
        else:
            file_data=file.read()
            file.close()
    
            response_start_line="HTTP/1.1 200 ok\r\n"
            response_heads="Server: My server\r\n"
            if file_name.endswith('jpg'):
                response_heads="Content-Type: image/png\r\n"
                response_heads="cache: no-cache\r\n"
                response_heads="Content-Length: {0}\r\n".format(len(file_data))
                response_body=file_data
            else:
                response_body=file_data.decode("utf-8")

    response=response_start_line+response_heads+"\r\n"+response_body
    print("response data:",response)
    client_socket.send(bytes(response,"utf-8"))
    client_socket.close()


def crawl(keywords='',client_socket='',response_heads='',response_body=''):
    '''
        response
    '''
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    process.crawl(MySpider,{'keywords':keywords,'client_socket':client_socket,'response_heads':response_heads,'response_body':response_body})
    process.start()

 
if __name__=="__main__":         #如果直接运行本文件，那么__name__为__main__(此时才运行下面的程序)，否则为对应包名
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # 创建socket对象
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    #host = socket.gethostname()  # 获取本地主机名
    port = 1212  #
    #print(host)
    s.bind(("", port))  # 绑定端口
    s.listen(5)
 
    while True:
        c,addr=s.accept()   #建立客户端连接
        print('连接地址',addr)
        handle_client_process=Process(target=handle_client,args=(c,))   #ALT+ENTER快捷键生成函数
        handle_client_process.start()
        c.close()
