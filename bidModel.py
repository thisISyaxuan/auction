#!C:\Users\kenny\AppData\Local\Programs\Python\Python37\python.exe
#print headers first
#print("Content-Type: text/html; charset=utf-8\n")
#print("Content-type: application/json; charset: utf-8\n")

import json
#import cgi
from datetime import datetime
from dbConfig import conn, cur


def add(uID, text, objName):
	sql ="insert into `object` (name,uID,expire,text ) values (%s,%s,now()+interval 1 minute,%s);" # 拍賣開啟10分鐘
	print(objName)
	cur.execute(sql,(objName, uID, text))
	conn.commit()
	conn.close()

def loadBid(uID):
	sql = "SELECT bid.oID,object.name,object.text,max(bid.price),object.expire FROM `bid`,`object` WHERE bid.uid = %s and bid.oid=object.oid and expire > now() group by oID;"
	cur.execute(sql,(uID,))
	record1 = cur.fetchall()
	sql ="SELECT bid.oid,bid.uid,object.name,max(bid.price) FROM `bid`,object WHERE bid.oid=object.oid and expire > now() group by oid;"
	cur.execute(sql,())
	record2 = cur.fetchall()
	result=[]
	for i in range(len(record1)):
		for j in range(len(record2)):
			if record1[i][0] == record2[j][0]:
				maxPrice = record2[j][3]
				if maxPrice > record1[i][3]:
					theMax = "否"
				else:
					theMax = "是"
		lessTime = (record1[i][4] - datetime.now()).seconds
		lessTime = str(lessTime//60)+"分"+str(lessTime%60)+"秒"
		temp={
			"oid":record1[i][0],
			"name":record1[i][1],
			"text":record1[i][2],
			"myPrice":record1[i][3],
			"maxPrice":maxPrice,
			"lessTime":lessTime,
			"theMax":theMax,
		}
		result.append(temp)
	return result
# def getMyObjList(uID):
# 	sql="""select object.oID,object.name,expire,max(price)
# 		from object,bid where object.oID=bid.oID and object.uID=%s
# 		group by object.oID
# 		"""
# 	cur.execute(sql,tuple(uID))
# 	records = cur.fetchall()
# 	result=[]
# 	for (oid,name, name, expire, price) in records:
# 		temp={
# 			"oid": oid,
# 			"name": name,
# 			"expire": expire.strftime('%Y-%m-%d %H:%M:%S'),
# 			"price": price
# 		}
# 		#print(temp)
# 		result.append(temp)
	
# 		#if isinstance(o, datetime):
# 		#	o=o.strftime('%Y-%m-%d %H:%M:%S')
# 		#elif isinstance(o, date):
# 		#	o=o.strftime('%Y-%m-%d')
# 	print(json.dumps(result,ensure_ascii=True))

def showHistory(uID):
	sql="""select object.oID,object.name,object.text,max(bid.price),object.expire
		from object,bid 
		where object.oID=bid.oID and bid.uID=%s and expire < now()
		group by object.oID
		"""
	cur.execute(sql,(uID,))
	record1 = cur.fetchall()
	sql ="SELECT bid.oid,bid.uid,object.name,max(bid.price) FROM `bid`,object WHERE bid.oid=object.oid and object.expire < now() group by oid;"
	cur.execute(sql,())
	record2 = cur.fetchall()
	result=[]
	for i in range(len(record1)):
		winner = uID
		for j in range(len(record2)):
			if record1[i][0] == record2[j][0]:
				maxPrice = record2[j][3]
				if maxPrice > record1[i][3]:
					theMax = "否"
					sql = "select uid from bid where oid = %s order by price desc;"
					cur.execute(sql,(record2[j][0],))
					winner = cur.fetchall()[0][0]
				else:
					theMax = "是"
		temp={
			"oid":record1[i][0],
			"name":record1[i][1],
			"text":record1[i][2],
			"closeTime":record1[i][4].strftime('%Y-%m-%d %H:%M:%S'),
			"myPrice":record1[i][3],
			"maxPrice":maxPrice,
			"theMax":theMax,
			"winner":winner
		}
		result.append(temp)
	return result
def getDetail(oID):
	sql = """select object.oid,object.name,object.text,object.expire,max(bid.price),object.uID
	from object,bid where object.oID = %s and bid.oID = object.oID;"""
	cur.execute(sql,(oID,))
	records = cur.fetchall()
	result= []
	price = records[0][4]
	if price == None:
		price = 0
	lessTime = (records[0][3] - datetime.now()).seconds
	lessTime = str(lessTime//60)+"分"+str(lessTime%60)+"秒"
	temp = {
		"oid": records[0][0],
		"name": records[0][1],
		"text": records[0][2],
		"expire": lessTime,
		"price": price,
		"uID": records[0][5]
	}
	result.append(temp)
	return result

def getAuction(uID):
	sql="""select bid.oID,bid.uID,bid.price,b.name,b.text,b.expire from bid,
	(select bid.oid,bid.uid,max(bid.price)c,a.name,a.text,a.expire from bid,
	(select object.oid,object.name,object.text,object.expire from object where object.uID = %s and object.expire < now())a
	where bid.oID = a.oID group by oID)b 
	where bid.price = b.c and bid.oID = b.oid order by oid;
	"""
	cur.execute(sql,(uID,))
	record1 = cur.fetchall()
	sql="""select object.oID,object.name, object.text, object.expire from object left join bid on object.oID=bid.oID
	where expire < now() and object.uID = %s and bid.price is NULL group by object.oID;
	"""
	cur.execute(sql,(uID,))
	record2 = cur.fetchall()
	result=[]
	for (oid,uid,price,name,text,expire) in record1:
		if price is None:
			price=0
		temp={
			"oid": oid,
			"uid":uid,
			"name": name,
			"expire": expire.strftime('%Y-%m-%d %H:%M:%S'),
			"price": price,
			"text":text
		}
		result.append(temp)
	for (oid,name,text,expire) in record2:
		temp={
			"oid": oid,
			"name": name,
			"expire": expire.strftime('%Y-%m-%d %H:%M:%S'),
			"price": "無人出價",
			"text":text,
			"uid": "無人出價"
		}
		result.append(temp)
	return result

def getNowAuction(uID):
	sql="""select object.oID,object.name, object.text, object.expire from object left join bid on object.oID=bid.oID
	where expire > now() and object.uID = %s and bid.price is NULL group by object.oID;
	"""
	cur.execute(sql,(uID,))
	record1 = cur.fetchall()
	sql="""select bid.oID,bid.uID,bid.price,b.name,b.text,b.expire from bid,
	(select bid.oid,bid.uid,max(bid.price)c,a.name,a.text,a.expire from bid,
	(select object.oid,object.name,object.text,object.expire from object where object.uID = %s and object.expire >= now())a
	where bid.oID = a.oID group by oID)b 
	where bid.price = b.c and bid.oID = b.oid order by oid;
	"""
	cur.execute(sql,(uID,))
	record2 = cur.fetchall()
	result=[]
	for (oid,name,text,expire) in record1:
		temp={
			"oid": oid,
			"name": name,
			"expire": expire.strftime('%Y-%m-%d %H:%M:%S'),
			"price": "無人出價",
			"text":text,
			"uid": "無人出價"
		}
		result.append(temp)
	for (oid,uid,price,name,text,expire) in record2:
		lessTime = (expire - datetime.now()).seconds
		lessTime = str(lessTime//60)+"分"+str(lessTime%60)+"秒"
		temp={
			"oid": oid,
			"uid": uid,
			"price": price,
			"name": name,
			"text":text,
			"expire": lessTime
		}
		result.append(temp)
	return result
#print(getNowAuction(0))
def getActiveList():
	sql="""select object.oID,object.name, object.expire
		from object where expire > now() group by object.oID;
		"""
	cur.execute(sql)
	records = cur.fetchall()
	result=[]
	for (oid,name,expire) in records:
		lessTime = (expire - datetime.now()).seconds
		lessTime = str(lessTime//60)+"分"+str(lessTime%60)+"秒"
		temp={
			"oid": oid,
			"name": name,
			"expire": lessTime
		}
		result.append(temp)
	return result

def bid(uID,oID,price):
	sql="select count(*) from bid,object where bid.oID=object.oID and bid.oID=%s and bid.price>=%s and expire>now();"
	cur.execute(sql,(oID,price))
	records = cur.fetchone()
	if records and records[0]>0:
		return False
	

	sql="""insert into bid (oID, uID,price) values (%s,%s,%s)
		"""
	cur.execute(sql,(oID,uID,price))
	conn.commit()
	conn.close()
	return True