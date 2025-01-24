// Copyright (c) 2025, Xappiens and contributors
// For license information, please see license.txt

frappe.ui.form.on("WPS", {
	espesor_mínimo: function (frm) {
	  update_rango_de_espesor(frm);
	},
	espesor_máximo: function (frm) {
	  update_rango_de_espesor(frm);
	}
  });
  
  function update_rango_de_espesor(frm) {
	if (frm.doc.espesor_mínimo && frm.doc.espesor_máximo) {
	  frm.set_value(
		"rango_de_espesor",
		`${frm.doc.espesor_mínimo} - ${frm.doc.espesor_máximo}`
	  );
	} else {
	  frm.set_value("rango_de_espesor", "");
	}
  }
  