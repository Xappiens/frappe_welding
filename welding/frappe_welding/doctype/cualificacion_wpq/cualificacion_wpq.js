frappe.ui.form.on('Cualificacion WPQ', {
    homologación: function(frm) {
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

                // Set query for the 'wps' field to filter based on the 'wps_names' array
                frm.set_query('wps', function() {
                    return {
                        filters: {
                            'name': ['in', wps_names] // Filter to only show WPS in 'wps_names' array
                        }
                    };
                });
            }
        });
    },
	refresh: function(frm) {
		if (!frm.doc.__islocal && !frm.doc.wpqr) {
        // Add a custom button to create a WPQR
        frm.add_custom_button(__('Create WPQR'), function() {
            // Call function to create WPQR
            frm.trigger('create_wpqr');
        });
	}
    },

    create_wpqr: function(frm) {
        // Function to create a new WPQR (Weld Procedure Qualification Record)
        
        // Check if the WPQ is valid and has the necessary information
        if (!frm.doc.wps || !frm.doc.name) {
            frappe.msgprint(__('Please ensure that the WPQ has valid WPS and other necessary details.'));
            return;
        }

        // Create a new WPQR document (without saving it)
        let wpqr = frappe.model.get_new_doc('Ensayo WPQR');  // Get a new WPQR document, not saving it yet

        // Populate the WPQR fields with values from the current WPQ
        wpqr.wps = frm.doc.wps;
        wpqr.wpq = frm.doc.name;

        // Redirect the user to the newly created WPQR form
        frappe.set_route('form', 'Ensayo WPQR', wpqr.name);
    }
});


