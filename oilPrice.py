from bs4 import BeautifulSoup
import requests, time, os, datetime
from io import BytesIO
from PIL import ImageTk, Image
import pytesseract, csv

def Oil():
	url = 'http://www.petrotradelaos.com/en/news/gas-price-data.html'

	rawdata = requests.get(url)
	rawdata = rawdata.content
	base = 'http://www.petrotradelaos.com/'
	imgsoup = BeautifulSoup(rawdata, 'html.parser')
	div = imgsoup.find('div', {'itemprop': 'articleBody'})
	imgtag = div.find('img')
	imgurl = base + imgtag['src'][1:]
	imgdate = imgtag['src'][8:18]
	resq = requests.get(imgurl)
	result = resq.content
	# image = Image.open(BytesIO(result))

	ocrlao=pytesseract.image_to_string(Image.open(BytesIO(result)), lang='Laos')
	# ocrlao=pytesseract.image_to_string(Image.open('../asset/oil.jpg'), lang='Laos')
	linebreak = ocrlao.split('\n')
	price=[]
	pro = ['ນະຄອນຫລວງວຽງຈັນ', 'ຜົ້ງສາລີ', 'ຫລວງນ້ຳທາ', 'ອຸດົມໄຊ', 'ບໍ່ແກ້ວ', 'ຫລວງພຣະບາງ', 'ໄຊຍະບູລີ', 'ຫົວພັນ', 'ຊຽງຂວາງ', 'ວຽງຈັນ', 'ບໍລິຄຳໄຊ', 'ຄຳມ່ວນ', 'ສະຫວັນນະເຂດ', 'ສາລະວັນ', 'ຈຳປາສັກ', 'ເຊກອງ', 'ອັດຕະປື', 'ໄຊສົມບູນ']
	pros = ['VT','PH','LM','OU','BK','LP','XA','HO','XI','VI','BL','KH','SV','SL','CH','XE','AT','XS',]
	for lb in linebreak:
		if len(list(lb))>57:
			pipe = lb.replace('|','')
			clean = pipe.split(' ')[-7:]
			if len(clean[1]) > 0:
				price.append({'pro':clean[0],'old95':clean[1],'new95':clean[2],'old91':clean[3],'new91':clean[4],'olddie':clean[5],'newdie':clean[6]})
				# price.append(clean)
	for i,j in zip(pro, price):
		j['pro'] = i
	return price
	# for p in price:
	# 	print(p)

print(Oil())