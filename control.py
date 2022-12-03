#!C:\Users\kenny\AppData\Local\Programs\Python\Python37\python.exe
#print headers first
print("Content-Type: text/html; charset=utf-8\n")
#print("Content-type: application/json; charset: utf-8\n")

import json
from datetime import date, datetime
import cgi
import bidModel as bid


form = cgi.FieldStorage()
act=form.getvalue('act')

#we can start accessing DB now
if act=='getList': # 所有拍賣中的商品
	result=bid.getActiveList()
	print(json.dumps(result,ensure_ascii=True)) #dump json string to client
elif act=='getHistory': # 我的下標歷史紀錄
	uid=int(form.getvalue('uID'))
	result=bid.showHistory(uid)
	print(json.dumps(result,ensure_ascii=True))
elif act=='loadBid': # 我的下標狀態
	uid=int(form.getvalue('uID'))
	result=bid.loadBid(uid)
	print(json.dumps(result,ensure_ascii=True))
elif act=='getAuction': # 我的拍賣歷史紀錄(已結標)
	uid=int(form.getvalue('uID'))
	result=bid.getAuction(uid)
	print(json.dumps(result,ensure_ascii=True))
elif act=='getNowAuction': # 我的拍賣歷史紀錄(未結標)
	uid=int(form.getvalue('uID'))
	result=bid.getNowAuction(uid)
	print(json.dumps(result,ensure_ascii=True))
elif act=='detail': # 商品內容
	oid=int(form.getvalue('oID'))
	result=bid.getDetail(oid)
	print(json.dumps(result,ensure_ascii=True))
elif act=='bid':
	uid=int(form.getvalue('uID'))
	oid=int(form.getvalue('oID'))
	price=int(form.getvalue('price'))
	if bid.bid(uid,oid,price):
		print('{"msg":"OK"}')
	else:
		print('{"msg":"Invalid"}')
elif act=='add':
	#load the posted data
	try:
		uid=int(form.getvalue('uID'))
		jsonStr=form.getvalue('dat')
		dat = json.loads(jsonStr)
	except:
		print(jsonStr)
		exit()
	bid.add(uid,dat['text'],dat['name'])
#result=bid.getNowAuction(0)
#print(json.dumps(result,ensure_ascii=True))