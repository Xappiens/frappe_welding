frappe.ui.form.on("Prueba Certificacion", {
    homologación: function (frm) {
        handle_homologacion_change(frm);
    },
    // on_update: function (frm) {
    //     handle_homologacion_change(frm);
    // },
    on_update: function (frm) {
        update_parent_status_based_on_child(frm);
    },
    refresh: function (frm) {
        if (!frm.doc.__islocal) {
            add_create_wpq_button(frm);
        }
    },
});

// Function to handle changes in the 'homologación' field
function handle_homologacion_change(frm) {
    if (!frm.doc.homologación) {
        frm.clear_table("detalles_de_la_prueba_de_soldadura");
        frm.refresh_field("detalles_de_la_prueba_de_soldadura");
        return;
    }

    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Homologacion",
            name: frm.doc.homologación,
        },
        callback: function (response) {
            const homologation = response.message;

            if (!homologation || !Array.isArray(homologation.procedimiento)) {
                frappe.msgprint(__("No valid procedimiento found."));
                return;
            }

            frm.clear_table("detalles_de_la_prueba_de_soldadura"); // Clear the table before populating it.

            // Iterate through each procedimiento in Homologacion
            homologation.procedimiento.forEach((proc_item) => {
                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "WPS",
                        filters: { procedimiento: proc_item.procedimiento },
                        fields: ["name"],
                    },
                    callback: function (wps_response) {
                        const wps_data = wps_response.message;

                        if (wps_data && wps_data.length) {
                            wps_data.forEach((wps) => {
                                const row = frm.add_child("detalles_de_la_prueba_de_soldadura");
                                row.procedimiento = proc_item.procedimiento;
                                row.wps = wps.name;
                            });
                        } else {
                            frappe.msgprint(
                                __("No WPS found for procedimiento {0}", [
                                    proc_item.procedimiento,
                                ])
                            );
                        }

                        frm.refresh_field("detalles_de_la_prueba_de_soldadura"); // Refresh after adding rows.
                    },
                });
            });
        },
    });
}


// Function to update parent status based on child table rows
function update_parent_status_based_on_child(frm) {
    if (!frm.doc.detalles_de_la_prueba_de_soldadura) return;

    const allApproved = frm.doc.detalles_de_la_prueba_de_soldadura.every(
        (row) => row.status === "Aprobar"
    );
    frm.set_value("status", allApproved ? "Aprobar" : "Pending");
}

// Function to add a custom button for creating WPQ
function add_create_wpq_button(frm) {
    frm.add_custom_button(__("Create WPQ"), function () {
        show_wps_dialog(frm);
    });
}

// Function to display a dialog for selecting WPS
function show_wps_dialog(frm) {
    const dialog = new frappe.ui.Dialog({
        title: __("Select WPS"),
        fields: [
            {
                fieldname: "wps_select",
                label: __("WPS"),
                fieldtype: "Link",
                options: "WPS",
                reqd: 1,
                get_query: function () {
                    const wps_names = frm.doc.detalles_de_la_prueba_de_soldadura.map(
                        (item) => item.wps
                    );
                    return {
                        filters: {
                            name: ["in", wps_names],
                        },
                    };
                },
            },
        ],
        primary_action_label: __("Create"),
        primary_action: function () {
            const selected_wps = dialog.get_values().wps_select;
            if (selected_wps) {
                create_wpq(frm, selected_wps);
                dialog.hide();
            }
        },
    });

    dialog.show();
}

// Function to create a WPQ document
function create_wpq(frm, selected_wps) {
    frappe.model.with_doctype("Cualificacion WPQ", function () {
        const wpq = frappe.model.get_new_doc("Cualificacion WPQ");
        wpq.prueba_certificacion = frm.doc.name;
        wpq.wps = selected_wps;

        frappe.set_route("form", "Cualificacion WPQ", wpq.name);
    });
}
