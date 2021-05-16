#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# CEROD - Currency Exchange Rate and Oil Price Daily

from tkinter import *
from tkinter import ttk, messagebox
from bs4 import BeautifulSoup
import requests, time, os, datetime
from io import BytesIO
from PIL import ImageTk, Image

##### DATA SCRAPPING #####

def Rate(event=None):
	url = 'https://bcel.com.la/bcel/exchange-rate.html'
	try:
		rawdata = requests.get(url)
		rawdata = rawdata.content

		data = BeautifulSoup(rawdata, 'html.parser')
		currency = data.find_all('td', {'data-title':u'ປະເພດສະກຸນເງິນ'})
		codes = data.find_all('td', {'data-title':u'ລະຫັດສະກຸນເງິນ'})
		buy = data.find_all('td', {'data-title':'NOTE'})
		sell = data.find_all('td', {'data-title':u'ອັດຕາຂາຍ'})
		result = []
		for cu, co, bu, se in zip(currency, codes, buy, sell):
			result.append({'currency': cu.text.strip(), 'codes': co.text.strip(), 'buy': bu.text.strip(), 'sell': se.text.strip()})
		table.delete(*table.get_children())
		for r in result:
			final = table.insert('', 'end', value=(r['currency'], r['buy'], r['sell']))
	except:
		table.delete(*table.get_children())
		final = table.insert('', 'end', value=('-', '-', '-'))
		messagebox.showinfo('ເກີດຂໍ້ຜິດພາດ', 'ເກີດຂໍ້ຜິດພາດໃນການດຶງຂໍ້ມູນ ກະລຸນາກວດສອບການເຊື່ອມຕໍ່ອິນເຕີເນັດຂອງທ່ານແລ້ວລອງໃໝ່ອີກຄັ້ງ')
def Oil():
	url = 'http://www.petrotradelaos.com/en/news/gas-price-data.html'

	rawdata = requests.get(url)
	rawdata = rawdata.content

	base = 'http://www.petrotradelaos.com/'

	data = BeautifulSoup(rawdata, 'html.parser')
	div = data.find('div', {'itemprop': 'articleBody'})
	img = div.find('img')
	imgurl = base + img['src'][1:]
	date = img['src'][8:18]
	date = f'ລາຄານ້ຳມັນວັນທີ {date}'
	res = requests.get(imgurl)
	result = res.content
	return result, date

##### GUI #####
root = Tk()
root.geometry('1024x768')  # 1600x1200	4:3	# 1280x800 16:9	# 1280x720
root.title('CEROD')
root.iconbitmap('dollar.png')

laofont = ('Defago Noto Sans', 20)
engfont = ('Times New Roman', 20)

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

tab = ttk.Notebook(root)
t1 = Frame(tab)
tab.add(t1, text=f'ອັດຕາແລກປ່ຽນ:^{20}', image=dollar, compound='left')
t2 = Frame(tab)
tab.add(t2, text=f'ລາຄານ້ຳມັນ:^{20}', image=oil, compound='left')
tab.pack(fill=BOTH, expand=1)

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

header = ['currency', 'buy', 'sell']
table = ttk.Treeview(f1, height=18, column=header, show='headings')
table.pack(pady=5)
style2 = ttk.Style(f1)
style2.configure("Treeview.Heading", font=laofont)
style2.configure("Treeview", font=engfont, rowheight=25)
table.heading('currency', text='ສະກຸນເງິນ')
table.column('currency', width=500)
table.heading('buy',text='ລາຄາຊື້')
table.column('buy', width=200, anchor="e")
table.heading('sell',text='ລາຄາຂາຍ')
table.column('sell', width=200, anchor="e")

Rate()

f2 = Frame(t2)
f2.pack()

try:
	v_oil_date = StringVar()
	rawimg = Oil()
	tkimage = ImageTk.PhotoImage(Image.open(BytesIO(rawimg[0])))
	v_oil_date.set(rawimg[1])
	l3 = Label(t2, textvariable=v_oil_date, font=laofont).pack()
	l4 = Label(t2, image=tkimage).pack()
except:
	now = datetime.datetime.now()
	days = {
            'Mon': 'ວັນຈັນ',
            'Teu': 'ອັງຄານ',
            'Wed': 'ພຸດ',
            'Thu': 'ພະຫັນ',
            'Fri': 'ສຸກ',
            'Sat': 'ເສົາ',
            'Sun': 'ອາທິດ',
        }
	d = now.strftime("%a")
	log = days[d] + '-' + now.strftime("%x")
	v_oil_date.set(log)
	l3 = Label(t2, textvariable=v_oil_date, font=laofont).pack()
	l3 = Label(t2, text="ເກີດຂໍ້ຜິດພາດໃນການດຶງຂໍ້ມູນ ກະລຸນາກວດສອບການເຊື່ອມຕໍ່ອິນເຕີເນັດຂອງທ່ານແລ້ວລອງໃໝ່ອີກຄັ້ງ", font=laofont).pack()
	defaultPNG = PhotoImage(file='default.png')
	l4 = Label(t2, image=defaultPNG).pack()

root.bind('<Escape>', lambda x: root.destroy())
root.bind('<F5>', Rate)
root.mainloop()
