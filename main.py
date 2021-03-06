#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# CEROD - Currency Exchange Rate and Oil Price Daily

from tkinter import *
from tkinter import ttk, messagebox
from bs4 import BeautifulSoup
import requests, time, os, datetime
from io import BytesIO
from PIL import ImageTk, Image
import pytesseract, csv
from urllib.request import urlopen

##### DATA SCRAPPING #####

def Rate(event=None):
	initTable1 = table1.insert('', 'end', value=('-', '-', '-'))
	url = 'https://bcel.com.la/bcel/exchange-rate.html'
	try:
		progress1['value'] = 0
		root.update()
		rawdata = requests.get(url)
		progress1['value'] = 10
		root.update()	
		rawdata = rawdata.content
		progress1['value'] = 20
		root.update()	
		data = BeautifulSoup(rawdata, 'html.parser')
		progress1['value'] = 30
		root.update()
		currency = data.find_all('td', {'data-title':u'ປະເພດສະກຸນເງິນ'})
		progress1['value'] = 40
		root.update()
		codes = data.find_all('td', {'data-title':u'ລະຫັດສະກຸນເງິນ'})
		progress1['value'] = 50
		root.update()
		buy = data.find_all('td', {'data-title':'NOTE'})
		progress1['value'] = 60
		root.update()
		sell = data.find_all('td', {'data-title':u'ອັດຕາຂາຍ'})
		progress1['value'] = 70
		root.update()	
		result = []
		for cu, co, bu, se in zip(currency, codes, buy, sell):
			result.append({'currency': cu.text.strip(), 'codes': co.text.strip(), 'buy': bu.text.strip(), 'sell': se.text.strip()})
		progress1['value'] = 80
		root.update()	
		table1.delete(*table1.get_children())
		progress1['value'] = 90
		root.update()
		for r in result:
			final = table1.insert('', 'end', value=(r['currency'], r['buy'], r['sell']))
		progress1['value'] = 100
		root.update()
	except:
		table1.delete(*table1.get_children())
		final = table1.insert('', 'end', value=('-', '-', '-'))
		messagebox.showinfo('ເກີດຂໍ້ຜິດພາດ', 'ເກີດຂໍ້ຜິດພາດໃນການດຶງຂໍ້ມູນອັດຕາແລກປ່ຽນ ກະລຸນາກວດສອບການເຊື່ອມຕໍ່ອິນເຕີເນັດຂອງທ່ານແລ້ວລອງໃໝ່ອີກຄັ້ງ')

def Oil(event=None):
	initTable2 = table2.insert('', 'end', value=('-', '-', '-','-', '-', '-','-'))
	try:
		progress2['value'] = 0
		root.update()
		url = 'http://www.petrotradelaos.com/en/news/gas-price-data.html'
		rawdata = requests.get(url)
		progress2['value'] = 10
		root.update()
		rawdata = rawdata.content
		progress2['value'] = 20
		root.update()
		base = 'http://www.petrotradelaos.com/'
		imgsoup = BeautifulSoup(rawdata, 'html.parser')
		progress2['value'] = 30
		root.update()
		div = imgsoup.find('div', {'itemprop': 'articleBody'})
		progress2['value'] = 40
		root.update()
		imgtag = div.find('img')
		progress2['value'] = 50
		root.update()
		imgurl = base + imgtag['src'][1:]
		imgdate = imgtag['src'][8:18]
		date = imgtag['src'][8:18]
		date = f'ລາຄານ້ຳມັນວັນທີ {date}'
		progress2['value'] = 55
		root.update()
		resq = requests.get(imgurl)
		progress2['value'] = 60
		root.update()
		result = resq.content
		progress2['value'] = 70
		root.update()
		# ocrlao=pytesseract.image_to_string(Image.open(BytesIO(result)), lang='Laos')
		ocrlao=pytesseract.image_to_string(Image.open(BytesIO(result)), lang='lao')
		linebreak = ocrlao.split('\n')
		progress2['value'] = 80
		root.update()
		price=[]
		# pro = ['ນະຄອນຫລວງວຽງຈັນ', 'ຜົ້ງສາລີ', 'ຫລວງນ້ຳທາ', 'ອຸດົມໄຊ', 'ບໍ່ແກ້ວ', 'ຫລວງພຣະບາງ', 'ໄຊຍະບູລີ', 'ຫົວພັນ', 'ຊຽງຂວາງ', 'ວຽງຈັນ', 'ບໍລິຄຳໄຊ', 'ຄຳມ່ວນ', 'ສະຫວັນນະເຂດ', 'ສາລະວັນ', 'ຈຳປາສັກ', 'ເຊກອງ', 'ອັດຕະປື', 'ໄຊສົມບູນ']
		# pros = ['VT','PH','LM','OU','BK','LP','XA','HO','XI','VI','BL','KH','SV','SL','CH','XE','AT','XS',]
		for lb in linebreak:
			if len(list(lb))>57:
				pipe = lb.replace('|','')
				clean = pipe.split(' ')[-7:]
				if len(clean[1]) > 0:
					if clean[0] == 'ຫຼວງພະບາ]':
						clean[0] = 'ຫຼວງພຣະບາງ'
					elif clean[0] == 'ຫຼວງນໍາທາ':
						clean[0] = 'ຫຼວງນ້ຳທາ'
					elif clean[0] == 'ເຊກອງ]':
						clean[0] = 'ເຊກອງ'
					elif clean[0] == 'ຜົ່ງສາລີ' or clean[0] == 'ຜືງສາລີ':
						clean[0] = 'ຜົ້ງສາລີ'
					elif clean[0] == 'ຮັດຕະປື' or clean[0] == 'ຮ໌ດຕະປື':
						clean[0] = 'ອັດຕະປື'
					elif clean[0] == 'ໄຊສົມບຸນ':
						clean[0] = 'ໄຊສົມບູນ'
					elif clean[0] == 'ຊຽງຂວາ]' or clean[0] == 'ຊຽງຂວາງ]':
						clean[0] = 'ຊຽງຂວາງ'
					price.append({'pro':clean[0],'old95':clean[1],'new95':clean[2],'old91':clean[3],'new91':clean[4],'olddie':clean[5],'newdie':clean[6]})
		# for i,j in zip(pro, price):
		# 	j['pro'] = i
		# print(price)
		progress2['value'] = 90
		root.update()
		table2.delete(*table2.get_children())
		for p in price:
			final = table2.insert('', 'end', value=(p['pro'],p['old95'],p['new95'],p['old91'],p['new91'],p['olddie'],p['newdie']))
		progress2['value'] = 100
		root.update()
		return date
	except:
		table2.delete(*table2.get_children())
		final = table2.insert('', 'end', value=('-', '-', '-','-', '-', '-','-'))
		messagebox.showinfo('ເກີດຂໍ້ຜິດພາດ', 'ເກີດຂໍ້ຜິດພາດໃນການດຶງຂໍ້ມູນລາຄານ້ຳມັນ ກະລຸນາກວດສອບການເຊື່ອມຕໍ່ອິນເຕີເນັດຂອງທ່ານແລ້ວລອງໃໝ່ອີກຄັ້ງ')
# def Oil():
# 	url = 'http://www.petrotradelaos.com/en/news/gas-price-data.html'

# 	rawdata = requests.get(url)
# 	rawdata = rawdata.content

# 	base = 'http://www.petrotradelaos.com/'

# 	data = BeautifulSoup(rawdata, 'html.parser')
# 	div = data.find('div', {'itemprop': 'articleBody'})
# 	img = div.find('img')
# 	imgurl = base + img['src'][1:]
# 	date = img['src'][8:18]
# 	date = f'ລາຄານ້ຳມັນວັນທີ {date}'
# 	res = requests.get(imgurl)
# 	result = res.content
# 	return result, date

##### GUI #####
root = Tk()
root.geometry('1024x768')  # 1600x1200	4:3	# 1280x800 16:9	# 1280x720
root.title('CEROD')
root.iconbitmap('exchange.ico')

laofont = ('Defago Noto Sans', 14)
engfont = ('Times New Roman', 14)

# style1 = ttk.Style()
# style1.theme_create('pastel', settings={
#     ".": {
#         "configure": {
#             "background": '#ddd',  # All except tabs
#             "font": 'red'
#         }
#     },
#     "TNotebook": {
#         "configure": {
#             "background": '#848a98',  # Your margin color
#             "tabmargins": [2, 5, 0, 0],  # margins: left, top, right, separator
#         }
#     },
#     "TNotebook.Tab": {
#         "configure": {
#             "background": '#d9ffcc',  # tab color when not selected
#             # [space between text and horizontal tab-button border, space between text and vertical tab_button border]
#             "padding": [10, 2],
#             "font": laofont
#         },
#         "map": {
#             "background": [("selected", '#ccffff')],  # Tab color when selected
#             "expand": [("selected", [1, 1, 1, 0])]  # text margins
#         }
#     },
# })
# style1.theme_use('pastel')

dollar = PhotoImage(file='dollar.png')
oil = PhotoImage(file='oil.png')

# def About():
# 	messagebox.showinfo('About','This app is use for checking the exchange rate and oil price, for personal use only.')

# menubar = Menu(root)
# root.config(menu=menubar)
# filemenu = Menu(menubar, tearoff=0)
# menubar.add_cascade(label='File', menu=filemenu)
# filemenu.add_command(label='Import CSV')
# filemenu.add_command(label='Import Excel')
# helpmenu = Menu(menubar, tearoff=0)
# menubar.add_cascade(label='Help', menu=helpmenu)
# helpmenu.add_command(label='About', command=About)
# donatemenu = Menu(menubar)
# menubar.add_cascade(label='Donate', menu=donatemenu)

tab = ttk.Notebook(root)
t1 = Frame(tab)
tab.add(t1, text=f'{"ອັດຕາແລກປ່ຽນ":^{20}}', image=dollar, compound='left')
t2 = Frame(tab)
tab.add(t2, text=f'{"ລາຄານ້ຳມັນ":^{20}}', image=oil, compound='left')
tab.pack(fill=BOTH, expand=1)
style1 = ttk.Style(tab)
style1.configure("TNotebook.Tab", font=laofont)

pstyle1 = ttk.Style(root)
pstyle1.theme_use('alt')
pstyle1.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
progress1 = ttk.Progressbar(t1, length=500, cursor='spider', mode="determinate", orient=HORIZONTAL, style="green.Horizontal.TProgressbar")
progress1.pack(pady=5)

pstyle2 = ttk.Style(root)
pstyle2.theme_use('alt')
pstyle2.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
progress2 = ttk.Progressbar(t2, length=500, cursor='spider', mode="determinate", orient=HORIZONTAL, style="green.Horizontal.TProgressbar")
progress2.pack(pady=5)

b1 = ttk.Button(t1, text='Refresh', command=Rate)
b1.pack(pady=5, ipadx=10, ipady=5)
v_l1 = StringVar()
v_l1.set('ກົດປຸ່ມ Refresh ຫລື F5 (ເທິງແປ້ນພິມ) ເພື່ອອັບເດດອັດຕາແລກປ່ຽນລ່າສຸດ')
l1 = Label(t1, textvariable=v_l1, font=laofont)
l1.pack()
# l1 = Label(t1, text='ກົດປຸ່ມ Refresh ຫລື F5 (ເທິງແປ້ນພິມ) ເພື່ອອັບເດດອັດຕາແລກປ່ຽນລ່າສຸດ', font=laofont)
# l1.pack()

f1 = Frame(t1)
f1.pack(ipady = 10, pady=5)

header1 = ['currency', 'buy', 'sell']
table1 = ttk.Treeview(f1, height=18, column=header1, show='headings')
table1.pack(pady=5)
style2 = ttk.Style(f1)
style2.configure("Treeview.Heading", font=laofont)
style2.configure("Treeview", font=engfont, rowheight=25)
table1.heading('currency', text='ສະກຸນເງິນ')
table1.column('currency', width=500)
table1.heading('buy',text='ລາຄາຊື້')
table1.column('buy', width=200, anchor="e")
table1.heading('sell',text='ລາຄາຂາຍ')
table1.column('sell', width=200, anchor="e")

b2 = ttk.Button(t2, text='Refresh', command=Oil)
b2.pack(pady=5, ipadx=10, ipady=5)
v_l2 = StringVar()
l2 = Label(t2, textvariable=v_l2, font=laofont)
l2.pack()
# l1 = Label(t1, text='ກົດປຸ່ມ Refresh ຫລື F5 (ເທິງແປ້ນພິມ) ເພື່ອອັບເດດອັດຕາແລກປ່ຽນລ່າສຸດ', font=laofont)
# l1.pack()

f2 = Frame(t2)
f2.pack(ipady = 10, pady=5)

header2 = ['pro','old95','new95','old91','new91','olddie','newdie']
table2 = ttk.Treeview(f2, height=18, column=header2, show='headings')
table2.pack(pady=5)
style3 = ttk.Style(f2)
style3.configure("Treeview.Heading", font=laofont)
style3.configure("Treeview", font=laofont, rowheight=25)
table2.heading('pro', text='ແຂວງ/ນະຄອນ')
table2.column('pro', width=250)
table2.heading('old95',text='ແອັດຊັງ 95 ເກົ່າ')
table2.column('old95', width=120, anchor="e")
table2.heading('new95',text='ແອັດຊັງ 95 ໃໝ່')
table2.column('new95', width=120, anchor="e")
table2.heading('old91',text='ແອັດຊັງ 91 ເກົ່າ')
table2.column('old91', width=120, anchor="e")
table2.heading('new91',text='ແອັດຊັງ 91 ໃໝ່')
table2.column('new91', width=120, anchor="e")
table2.heading('olddie',text='ກາຊວນ ເກົ່າ')
table2.column('olddie', width=120, anchor="e")
table2.heading('newdie',text='ກາຊວນ ໃໝ່')
table2.column('newdie', width=120, anchor="e")

def Connection():
	try:
		check = urlopen('http://www.google.com', timeout=1).read()
		r = Rate()
		o = Oil()
		v_l2.set(f'ກົດປຸ່ມ Refresh ຫລື F6 (ເທິງແປ້ນພິມ) ເພື່ອອັບເດດລາຄານ້ຳມັນລ່າສຸດ ({o})')
	except:
		messagebox.showerror('ເກີດຂໍ້ຜິດພາດ', 'ບໍ່ສາມາດເຊື່ອມຕໍ່ອິນເຕີເນັດໄດ້ ກະລຸນາກວດສອບການເຊື່ອມຕໍ່ອິນເຕີເນັດຂອງທ່ານ')
# print(Connection())
Connection()

# try:
# 	v_oil_date = StringVar()
# 	rawimg = Oil()
# 	tkimage = ImageTk.PhotoImage(Image.open(BytesIO(rawimg[0])))
# 	v_oil_date.set(rawimg[1])
# 	l3 = Label(t2, textvariable=v_oil_date, font=laofont).pack()
# 	l4 = Label(t2, image=tkimage).pack()
# except:
# 	now = datetime.datetime.now()
# 	days = {
#             'Mon': 'ວັນຈັນ',
#             'Teu': 'ອັງຄານ',
#             'Wed': 'ພຸດ',
#             'Thu': 'ພະຫັນ',
#             'Fri': 'ສຸກ',
#             'Sat': 'ເສົາ',
#             'Sun': 'ອາທິດ',
#         }
# 	d = now.strftime("%a")
# 	log = days[d] + '-' + now.strftime("%x")
# 	v_oil_date.set(log)
# 	l3 = Label(t2, textvariable=v_oil_date, font=laofont).pack()
# 	l3 = Label(t2, text="ເກີດຂໍ້ຜິດພາດໃນການດຶງຂໍ້ມູນ ກະລຸນາກວດສອບການເຊື່ອມຕໍ່ອິນເຕີເນັດຂອງທ່ານແລ້ວລອງໃໝ່ອີກຄັ້ງ", font=laofont).pack()
# 	defaultPNG = PhotoImage(file='default.png')
# 	l4 = Label(t2, image=defaultPNG).pack()

root.bind('<Escape>', lambda x: root.destroy())
root.bind('<F5>', Rate)
root.bind('<F6>', Oil)
root.mainloop()
