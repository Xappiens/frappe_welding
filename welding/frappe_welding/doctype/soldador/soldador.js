frappe.ui.form.on('Soldador', {
    refresh: function(frm) {
        // Apply custom styling on refresh
        setRowColor(frm);
    },
    historial_certificacion: function(frm) {
        // Apply custom styling when a row is added to the historial_certificacion table
        setRowColor(frm);
    }
});

function setRowColor(frm) {
    frm.fields_dict['historial_certificacion'].grid.wrapper.on('click', '.grid-row', function(event) {
        // Loop through each row in the 'historial_certificacion' table
        frm.fields_dict['historial_certificacion'].grid.grid_rows.forEach(function(row) {
            // Get the status value from the current row
            var status = row.doc.status;
            var $statusCell = $(row.$row).find('[data-fieldname="status"]');
            
            // Apply color based on the status value
            if (status === 'Activo') {
                $statusCell.css("color", "green");
            } else if (status === 'Vencido') {
                $statusCell.css("color", "red");
            } else {
                $statusCell.css("color", "black");
            }
        });
    });
}
