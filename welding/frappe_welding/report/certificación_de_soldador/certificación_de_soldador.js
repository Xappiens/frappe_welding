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
      label: __("Certificacion Estado"),
      fieldtype: "Select",
      options: "\nActivo\nVencido",
      width: 150,
    },
    {
      fieldname: "prueba_certificacion_status",
      label: __("Prueba Certificacion Estado"),
      fieldtype: "Select",
      options: "\nPendiente\nAprobar\nFallar",
      width: 150,
    },
    {
      "fieldname": "is_homologacion",
      "label": "Disponer de Homologación",
      "fieldtype": "Check",
      "default": 1,  
      "width": 120
  },
  ],

  // Formatter for 'status' column
  formatter: function (value, row, column, data, default_formatter) {
    value = default_formatter(value, row, column, data);

    var color_map = {
      Activo: "#28a745", // Green
      Vencido: "#dc3545", // Red
      Pendiente: "#ffc107",
      Aprobar:"#28a745",
      Fallar:"#dc3545",
    };

    if (column.fieldname == "status" && color_map[data.status]) {
      return `<div style='background-color:${color_map[data.status]}; color: white;'>${value}</div>`;
    }
    if (column.fieldname == "prueba_certificacion_status" && color_map[data.prueba_certificacion_status]) {
      return `<div style='background-color:${color_map[data.prueba_certificacion_status]}; color: white;'>${value}</div>`;
    }

    return value;
  },

  get_datatable_options(options) {
    return Object.assign(options, {
      checkboxColumn: true,
    });
  },

  // Function to handle loading the report and the button action
  onload: function () {
    frappe.query_report.page.add_inner_button(
      __("Assign Prueba Certificación"),
      function () {
        const selected_rows = getSelectedRows();
        if (selected_rows.length === 0) {
          frappe.msgprint(__("Seleccione al menos una fila."));
          return;
        }

        const dialog_fields = buildDialogFields(selected_rows);

        // Show the dialog with dynamic fields
        const dialog = new frappe.ui.Dialog({
          title: __("Assign Prueba Certificación"),
          fields: dialog_fields,
          primary_action_label: __("Assign"),
          primary_action: function (data) {
            assignTestToSoldador(selected_rows, data, dialog);
          },
        });

        dialog.show();
      }
    );
  },
};

// Function to get selected rows from the table
function getSelectedRows() {
  let selected_rows = [];
  $(".dt-scrollable")
    .find(":input[type=checkbox]")
    .each((idx, row) => {
      if (row.checked) {
        selected_rows.push(frappe.query_report.data[idx]);
      }
    });
  return selected_rows;
}

// Function to build dialog fields based on the selected rows
function buildDialogFields(selected_rows) {
  let dialog_fields = [
    {
      label: __("Homologación"),
      fieldname: "homologacion",
      fieldtype: "Link",
      options: "Homologacion",
      reqd: true,
    },
    {
      label: __("Fecha de Prueba"),
      fieldname: "fecha_de_prueba",
      fieldtype: "Date",
      reqd: true,
    },
    {
      label: __("Tipo de Prueba"),
      fieldname: "tipo_de_prueba",
      fieldtype: "Select",
      options: ["Destructivo Prueba(DT)", "Prueba No-Destructivas(NDT)"],
    },
  ];

  // If exactly one row is selected, add the "Soldador" field to the dialog
  if (selected_rows.length === 1) {
    dialog_fields.unshift({
      label: __("Soldador"),
      fieldname: "soldador",
      fieldtype: "Link",
      options: "Soldador",
      default: selected_rows[0].soldador,
      reqd: true,
    });
  }

  return dialog_fields;
}

// Function to handle assigning the test to the "Soldador"
function assignTestToSoldador(selected_rows, data, dialog) {
  frappe.call({
    method: "welding.frappe_welding.doctype.prueba_certificacion.prueba_certificacion.assign_prueba_certificacion",
    args: {
      rows: selected_rows,
      data: data,
    },
    callback: function (response) {
      if (!response.exc) {
        frappe.msgprint(__("Prueba Certificación asignada exitosamente."));
        dialog.hide();
      }
    },
  });
} 


