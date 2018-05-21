// Copyright (c) 2018, Bobby and contributors
// For license information, please see license.txt

frappe.ui.form.on('Laporan Penggunaan', {
	refresh: function(frm) {
		cur_frm.add_fetch("document", "beli", "beli");
		cur_frm.add_fetch("document", "jual", "pnbp");
	}
});
