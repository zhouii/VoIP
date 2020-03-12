# Code by Bluecat
# https://github.com/zhouii/VoIP
import requests
import re
import time
import json
from datetime import datetime
import sys
import argparse

log_file='voip.log' # 填写日志保存路径
ip='192.168.1.1' # 填写光猫IP地址
telecomadmin_password='abcd1234' # 填写光猫超级管理员账户telecomadmin的密码

def log(txt):
	global f
	if f==None:
		f=open(log_file,'a')
	f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' '+txt+'\n')

def login():
	try:
		r=s.get('http://%s'%ip)
		token=re.findall('Frm_Logintoken"\)\.value = "(\S*?)"',r.text)[0]
		r=s.post('http://%s'%ip,data="frashnum=&action=login&Frm_Logintoken=%s&user_name=telecomadmin&Password=%s"%(token,telecomadmin_password),headers={'Content-Type': 'application/x-www-form-urlencoded'})
		if 'mainFrame' not in r.text:
			raise
	except Exception:
		log('Login failed! Exit!')
		raise
	else:
		log('Login success')

def logout():
	try:
		r=s.post('http://%s'%ip,data="logout=1",headers={'Content-Type': 'application/x-www-form-urlencoded'})
		if 'fLogin' not in r.text:
			raise
	except Exception:
		log('Logout failed! Exit!')
		print(-1, end = '')
		sys.exit(-1)
	else:
		log('Logout success')

def parse(html):
	global data
	for item in re.findall("Transfer_meaning\('(.*?)','(.*?)'\)",html):
		data[item[0]]=item[1].encode().decode('unicode-escape')

def getConfig():
	try:
		r=s.get('http://%s/getpage.gch?pid=1002&nextpage=app_voip_basic_t.gch'%ip)
		parse(r.text)
		if data['Enable0']!='1' and data['Enable0']!='2':
			raise
	except Exception:
		log('Get config failed! Exit!')
		raise
	else:
		log('Get config success')
		return data['Enable0']

def submit(enable0):
	try:
		global data
		HiddenPara=["PublishServer","Enable","Name","DigitMap","DigitMapEnable","AuthUserName","DigestUserName","AuthPassword","DisplayName","RegStatus","DNSStatus","TermID0","Enable0"]
		for para in HiddenPara:
			data[para]='NULL'
		data['IF_INDEX']='0'
		data["AuthUserName"]=data["AuthUserName0"]
		data["DigestUserName"]=data["DigestUserName0"]
		data["AuthPassword"]=data["AuthPassword0"]
		data['Enable0']=enable0
		data['IF_ACTION']='apply'
		r=s.post('http://%s/getpage.gch?pid=1002&nextpage=app_voip_basic_t.gch'%ip,data=data)
		parse(r.text)
		if data['Enable0']!=enable0:
			raise
	except Exception:
		log('Submit failed! Exit!')
		raise
	else:
		log('Submit %s success'%enable0)
		return data['Enable0']

def query():
	try:
		login()
		result=getConfig()
		logout()
	except Exception:
		return -1
	return int(result)

def enable():
	try:
		login()
		getConfig()
		result=submit('2')
		logout()
	except Exception:
		return -1
	return int(result)

def disable():
	try:
		login()
		getConfig()
		result=submit('1')
		logout()
	except Exception:
		return -1
	return int(result)

def switch():
	try:
		login()
		result=submit('2' if getConfig()=='1' else '1')
		logout()
	except Exception:
		return -1
	return int(result)

s=requests.session()
data={}
f=None

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Take an action to VoIP of F450G, then echo & return 2 if enabled and 1 if disabled after the action.\nIf failed, I will echo & return -1.',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("action", metavar='action', help="There are 4 allowed actions:\n query     Directly echo & return result.\n enable    Enable VoIP on modem.\n disable   Disable VoIP on modem.\n switch    Enable VoIP if disabled, vice versa.", choices=['query','enable','disable','switch'])
	parser.add_argument('-i','--ip',help='IP address of modem.')
	parser.add_argument('-p','--password',help='Password of telecomadmin account on modem.\nRefer to https://www.zhouii.com/2018/10/646.html if you do not have.')
	parser.add_argument('-l','--log',help='Place to store log file.')
	args = parser.parse_args()
	if args.ip!=None:
		ip=args.ip
	if args.password!=None:
		telecomadmin_password=args.password
	if args.log!=None:
		log_file=args.log
	f=open(log_file,'a')
	if args.action=='query':
		result=query()
		print(result, end = '')
		sys.exit(int(result))
	elif args.action=='enable':
		result=enable()
		print(result, end = '')
		sys.exit(int(result))
	elif args.action=='disable':
		result=disable()
		print(result, end = '')
		sys.exit(int(result))
	elif args.action=='switch':
		result=switch()
		print(result, end = '')
		sys.exit(int(result))
	else:
		sys.exit(-1)
