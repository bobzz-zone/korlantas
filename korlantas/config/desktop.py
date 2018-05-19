# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Master",
			"color": "grey",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("Master")
		},
		{
			"module_name": "Harga",
			"color": "grey",
			"icon": "octicon octicon-repo",
			"type": "module",
			"label": _("Harga")
		},
		{
			"module_name": "Stok",
			"color": "grey",
			"icon": "octicon octicon-package",
			"type": "module",
			"label": _("Stok")
		}
	]
