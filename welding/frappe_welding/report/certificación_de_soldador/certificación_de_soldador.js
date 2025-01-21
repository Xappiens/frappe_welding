frappe.query_reports["Certificación de Soldador"] = {
	filters: [
	  {
		fieldname: "soldador",
		label: __("Soldador"),
		fieldtype: "Link",
		options: "Soldador",
		width: 150,
	  },
	  {
		fieldname: "homologacion",
		label: __("Homologacion"),
		fieldtype: "Link",
		options: "Homologacion",
		width: 150,
	  },
	  {
		fieldname: "empleado",
		label: __("Empleado"),
		fieldtype: "Link",
		options: "Employee",
		width: 150,
	  },
	  {
		fieldname: "compañia",
		label: __("Compañia"),
		fieldtype: "Link",
		options: "Company",
		width: 150,
	  },
	  {
		fieldname: "status",
		label: __("Estado"),
		fieldtype: "Select",
		options: "\nActivo\nVencido",
		width: 150,
	  },
	],
  
	formatter: function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
	
		// Define the color mapping for status field
		var color_map = {
		  "Activo": "#28a745",  // Green
		  "Vencido": "#dc3545", // Red
		};
	
		// Dynamically apply color to the 'status' field based on the value
		if (column.fieldname == "status" && color_map[data.status]) {
		  return `<div style='background-color:${color_map[data.status]}; color: white;'>${value}</div>`;
		}
	
		return value;
	  }	
  };
  