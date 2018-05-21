# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe.utils import cint, now
def updatePrice():
	ppl = frappe.db.sql("""select name from `tabHarga Material` where from <= NOW() and docstatus=1 order by from desc limit 0,1 """,as_list=1)
	idx = ""
	for row in ppl:
		idx=row[0]
	if idx:
		pl = frappe.db.sql("""select document,harga from `tabTabel Harga` where parent="{}" """.format(idx),as_list=1)
		for row in pl:
			frappe.db.sql("""update `tabDocument Type` set beli={} where name="{}" """.format(row[1],row[0]),as_list=1)

	ppl = frappe.db.sql("""select name from `tabStandard PNBP` where from <= NOW() and docstatus=1 order by from desc limit 0,1 """,as_list=1)
	idx = ""
	for row in ppl:
		idx=row[0]
	if idx:
		pl = frappe.db.sql("""select document,harga from `tabTabel Pendapatan` where parent="{}" """.format(idx),as_list=1)
		for row in pl:
			frappe.db.sql("""update `tabDocument Type` set jual={} where name="{}" """.format(row[1],row[0]),as_list=1)
def bufferCheck():
	total_request={}
	#not done yet should check from buffer item
	ks = frappe.db.sql("""select gudang,document,stok from `tabKartu Stok` """,as_list=1)
	#stock perlu di add dari request yg belum ter realisasi
	ri = frappe.db.sql("""select p.gudang,d.document,sum(d.jumlah-d.diterima) from `tabTabel Request` d left join `tabRequest Barang` p on d.parent = p.name where docstatus=1 group by p.gudang,d.document """,as_list=1)
	for row in ks:
		ppl = frappe.db.sql("""select d.jumlah,d.request,p.type from `tabTabel Buffer Stok` d 
			left join `tabBuffer Stok` p on d.parent=p.name 
			where p.tanggal <= NOW() and  p.gudang="{}" and docstatus=1
			order by p.tanggal desc limit 0,1 """,as_list=1)
		req = 0
		for x in ri:
			if x[0]==row[0] and x[1]==row[1]:
				req=cint(row[2])
		for n in ppl:
			if cint(row[2])+req<cint(n[0]):
				#gudang, document, request
				if total_request[row[0]]:
					total_request[row[0]].append(row[1],n[1],n[2]])
				else:
					total_request[row[0]]=[]
					total_request[row[0]].append(row[1],n[1],n[2]])
	
	for key in total_request:
		items=[]
		gudang = key:
		for row in total_request[key]:
			items.append({"document":row[0],"jumlah":row[1]})
			doc = frappe.get_doc({
				"doctype": "Request Barang",
				"gudang":gudang,
				"type":row[2],
				"catatan":"Otomatis dari minimum stok buffer",
				"tanggal":now(),
				"items":items
				})
			doc.insert()
			doc.submit()