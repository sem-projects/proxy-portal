from datetime import datetime, date
import pandas as pd
import numpy as np
import os
import subprocess
import sqlite3

'''ts = int("1541768332")

# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try `ts /= 1000` in that case
print(datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))'''

data = pd.read_csv("/var/log/squid/access.log",delimiter=r"\s+")
data.columns = ['timestamp', 'data_size', 'ip', 'protocol', 'no_idea', 'method', 'site', 'user', 'no_idea2', 'no_idea3']
print(data[:5])

conn = sqlite3.connect('students.sqlite3')
cur = conn.cursor()
date1 = datetime.now()

subprocess.call('cp /var/log/squid/access.log /etc/squid/squidReports/',shell=True)
subprocess.call('echo "" > /var/log/squid/access.log',shell=True)
subprocess.call('mv /etc/squid/squidReports/access.log /etc/squid/squidReports/'+str(date.today())+'_access.log',shell=True)

data2 = data.groupby(['user']).sum().reset_index()
#print(data2.iloc[0]['user'])
for i in range(0,len(data2)):
	cur.execute("INSERT into DailyData (id,useremail,curr_date,data_size) VALUES (?,?,?,?)",(str(date1)+str(data2.iloc[i]['user']),str(data2.iloc[i]['user'])+"@iiita.ac.in",date1,int(data2.iloc[i]['data_size'])))
	conn.commit()
	#print (data2.iloc[i]['user'],data2.iloc[i]['data_size'])


time_basis_data = [0 for i in range(24)]
for index,row in data.iterrows():
	#print(row['timestamp'])
	a = int(row['timestamp'])
	b = int(datetime.fromtimestamp(a).strftime('%H'))
	time_basis_data[b] += int(row['data_size'])

for i in range(24):
	cur = conn.cursor()
	cur.execute("INSERT into HourlyAllData (id,hour,curr_date,data_size) VALUES (?,?,?,?)",(str(date1)+" "+str(i),i,date1,time_basis_data[i]))
	conn.commit()


conn.close()
