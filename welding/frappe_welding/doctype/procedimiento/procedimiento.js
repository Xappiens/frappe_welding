frappe.ui.form.on("Procedimiento", {
	espesor_mínimo: function (frm) {
	  update_rango_de_espesor(frm);
	},
	espesor_máximo: function (frm) {
	  update_rango_de_espesor(frm);
	},
	material_base: function (frm) {
		set_filters_filling_materials(frm);
	},
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

function set_filters_filling_materials(frm){
	if(frm.doc.material_base){
		frappe.call({
			method: 'welding.frappe_welding.doctype.procedimiento.procedimiento.set_filling_materials',
			args: {
				 // Assuming "Base Material" is the DocType where your material info is stored
				 base_material: frm.doc.material_base       // The selected base material
			},
			callback: function(response) {
				// Check if the response contains the material details
				if (response.message) {
					// Extract the list of compatible filling materials
					let compatible_filling_materials = response.message;

					// Filter the filling materials based on the compatible ones
					frm.fields_dict['material_de_relleno'].get_query = function(doc) {
						return {
							filters: {
								'name': ['in', compatible_filling_materials.map(m => m.name)]  // Filter using names of compatible materials
							}
						};
					};
				}
			}
		});
	}
}
