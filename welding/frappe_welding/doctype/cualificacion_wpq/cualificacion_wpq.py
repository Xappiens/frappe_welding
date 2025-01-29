# Copyright (c) 2025, Xappiens and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
class CualificacionWPQ(Document):
    def on_update(self):
        update_prueba_certificacion(self.prueba_certificacion,self.wps, self.name , self.status)
        
def update_prueba_certificacion(prueba_certificacion_name, wps_name, wpq_name, status):
    # Fetch the "Prueba Certificacion" document
    prueba_certificacion = frappe.get_doc("Prueba Certificacion", prueba_certificacion_name)
    # Check if detalles_de_la_prueba_de_soldadura exists
    if prueba_certificacion and prueba_certificacion.detalles_de_la_prueba_de_soldadura:
        # Loop through the child table "detalles_de_la_prueba_de_soldadura"
        for row in prueba_certificacion.detalles_de_la_prueba_de_soldadura:
            # Check if the wps is set and matches the given wps_name
            if row.wps == wps_name:
                # Link the WPQ to the current row
                row.wpq = wpq_name
                row.status = status

        # Save the updated "Prueba Certificacion" document after linking WPQ
        try:
            prueba_certificacion.save()
            frappe.db.commit()
            return _("Prueba Certificacion details updated successfully.")
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Error saving Prueba Certificacion")
            return _("Error while saving the document: {0}".format(str(e)))
    else:
        return _("No valid detalles_de_la_prueba_de_soldadura found.")
