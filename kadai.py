import apache_log_parser
from pprint import pprint
from datetime import datetime
import glob
import os.path
import sys
if len(sys.argv)==1:
    sys.stderr.write('ログファイルを指定してください')
    exit()
with open("joindata.txt", 'wb') as saveFile:
    for i in range(len(sys.argv)-1):
        data = open(sys.argv[i+1], "rb").read()
        saveFile.write(data)
        border='\n'.encode()
        saveFile.write(border)
        saveFile.flush()
line_parser = apache_log_parser.make_parser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")


def read_apache_log(ifn, logformat='%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'):
    parser = apache_log_parser.make_parser(logformat)
    P = []
    E = []
    with open(ifn) as f:
        for line in f:
            try:
                parsed_line = parser(line)
                P.append(parsed_line)
            except ValueError:
                E.append(line)

    pprint('=== Read Summary ===')
    pprint('Parsed     : {0}'.format(len(P)))
    pprint('ValueError : {0}'.format(len(E)))
    pprint('====================')

    return P
host = []
hostcount={}
time=[]
timecount={}
for i in range(24):
    timecount[str(i)+"時"]=0
ifn = 'joindata.txt'
log=read_apache_log(ifn)
for i in log:
    host.append(i['remote_host'])

for i in host:
    if i in hostcount:
        hostcount[i]=hostcount[i]+1
    else:
        hostcount[i]=1
host_sorted= sorted(hostcount.items(), key=lambda x:x[1],reverse=True)
for i in log:
    time.append(i['time_received_datetimeobj'].hour)
for i in time:
    timecount[str(i)+'時']=timecount[str(i)+'時']+1

print("ホスト別アクセス件数",host_sorted)
print("時間帯別アクセス",timecount)