frappe.ui.form.on("Cualificacion WPQ", {
  // homologación: function (frm) {
  //   frappe.call({
  //     method: "frappe.client.get",
  //     args: {
  //       doctype: "Homologacion",
  //       filters: { name: frm.doc.homologación },
  //     },
  //     callback: function (response) {
  //       var homologation = response.message;

  //       if (!homologation || !Array.isArray(homologation.procedimiento)) {
  //         frappe.msgprint(__("No valid procedimiento found."));
  //         return;
  //       }

  //       // Map out the procedimiento names
  //       var wps_names = homologation.procedimiento.map(
  //         (item) => item.procedimiento
  //       );

  //       // Set query for the 'wps' field to filter based on the 'wps_names' array
  //       frm.set_query("wps", function () {
  //         return {
  //           filters: {
  //             name: ["in", wps_names], // Filter to only show WPS in 'wps_names' array
  //           },
  //         };
  //       });
  //     },
  //   });
  // },
});
