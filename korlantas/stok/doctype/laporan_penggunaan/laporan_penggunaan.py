# -*- coding: utf-8 -*-
# Copyright (c) 2018, Bobby and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import cint

class LaporanPenggunaan(Document):
	def validate(self):
		if self.source:
			#check kartu stock
			for row in self.items:
				ks = frappe.db.sql("""select name, document,stok from `tabKartu Stok` where gudang="{}" and document="{}" """.format(self.gudang,row.document),as_list=1)
				ada=0
				for n in ks:
					ada=1
					if n[2]<row.stok:
						frappe.throw("Document {} stok kurang {}".format(row.document,cint(n[2])-cint(row.stok)))
				if ada==0:
					doc = frappe.get_doc({
						"doctype": "Kartu Stok",
						"document":row.document,
						"stok":0,
						"gudang":self.gudang
						})
					doc.insert()
	def on_submit(self):
		#check kartu stock
		for row in self.items:
			if self.source:
				ks = frappe.db.sql("""update `tabKartu Stok` set stok=stok-{} where gudang="{}" and document="{}" """.format(self.jumlah,self.gudang,row.document),as_list=1)
				doc = frappe.get_doc({
					"doctype": "Mutasi Stok",
					"tanggal":self.tanggal,
					"document":row.document,
					"stok":row.jumlah*-1,
					"gudang":self.gudang,
					"beli":row.beli,
					"pnbp":row.pnbp,
					"type":"Laporan Penggunaan",
					"link_to":self.name
					})
				doc.insert()
	def on_cancel(self):
		for row in self.items:
			if self.gudang:
				ks = frappe.db.sql("""update `tabKartu Stok` set stok=stok+{} where gudang="{}" and document="{}" """.format(self.jumlah,self.gudang,row.document),as_list=1)
		frappe.db.sql("""delete from `tabMutasi Stok` where link_to="{}" """.format(self.name),as_list=1)

