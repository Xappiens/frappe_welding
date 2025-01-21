frappe.ui.form.on('Prueba Certificacion', {
    homologación: function(frm) {
        // If no homologation is selected, clear the table and refresh
        if (!frm.doc.homologación) {
            frm.clear_table('procedimiento_wps');
            frm.refresh_field('procedimiento_wps');
            return;
        }

        // Fetch the relevant WPS related to the Prueba Certificación (test certification)
        frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'Homologacion',
                filters: { 'name': frm.doc.homologación }
            },
            callback: function(response) {
                var homologation = response.message;

                if (!homologation || !Array.isArray(homologation.procedimiento_wps)) {
                    frappe.msgprint(__('No valid procedimiento_wps found.'));
                    return;
                }

                // Map out the procedimiento names
                var wps_names = homologation.procedimiento_wps.map(item => item.procedimiento);

                // Clear and populate the procedimiento_wps table if the field exists
                if (frm.fields_dict['detalles_de_la_prueba_de_soldadura']) {
                    frm.clear_table('detalles_de_la_prueba_de_soldadura');
                    wps_names.forEach(function(wps_name) {
                        var row = frm.add_child('detalles_de_la_prueba_de_soldadura');
                        row.wps = wps_name;
                    });
                    frm.refresh_field('detalles_de_la_prueba_de_soldadura');
                } else {
                    console.error('No "procedimiento_wps" field found in the form.');
                }
            }
        });
    },
    detalles_de_la_prueba_de_soldadura: function(frm) {
        // Check if all rows in the "detalles_de_la_prueba_de_soldadura" table have estado as "Aprobar"
        var allApproved = frm.doc.detalles_de_la_prueba_de_soldadura.every(function(row) {
            return row.status === "Aprobar";
        });

        // If all rows have estado "Aprobar", set the parent document's estado to "Aprobar"
        if (allApproved) {
            frm.set_value('status', 'Aprobar');
        } else {
            frm.set_value('status', 'Pending');  // Or any other status you want when not all are "Aprobar"
        }
    },
    refresh: function(frm) {
        if (!frm.doc.__islocal) {
        // Add a button to the form
        frm.add_custom_button(__('Create WPQ'), function() {
            // Show the modal dialog for selecting WPS
            show_wps_dialog(frm);
        });
    }
    }
});


function show_wps_dialog(frm) {
    var dialog = new frappe.ui.Dialog({
        title: __('Select WPS'),
        fields: [
            {
                fieldname: 'wps_select',
                label: __('WPS'),
                fieldtype: 'Link',
                options: 'Procedimiento WPS',  // Link to the WPS doctype
                reqd: 1,
                get_query: function() {
                    // Get the list of WPS names from the detalles_de_la_prueba_de_soldadura table
                    var wps_names = frm.doc.detalles_de_la_prueba_de_soldadura.map(function(item) {
                        return item.wps;
                    });

                    return {
                        filters: {
                            'name': ['in', wps_names]  // Filter by WPS names
                        }
                    };
                }
            }
        ],
        primary_action_label: __('Create'),
        primary_action: function() {
            var selected_wps = dialog.get_values().wps_select;
            if (selected_wps) {
                // Call function to create WPQ
                create_wpq(frm, selected_wps);
                dialog.hide();
            }
        }
    });

    dialog.show();
}

// Function to create WPQ document
function create_wpq(frm, selected_wps) {
    let wpq = frappe.model.get_new_doc('Cualificacion WPQ');  // Get a new WPQR document, not saving it yet

        // Populate the WPQR fields with values from the current WPQ
        wpq.prueba_certificacion = frm.doc.name;
        wpq.wps = selected_wps;

        // Redirect the user to the newly created WPQR form
        frappe.set_route('form', 'Cualificacion WPQ', wpq.name);
}