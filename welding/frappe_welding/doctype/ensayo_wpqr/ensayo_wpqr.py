# Copyright (c) 2025, Xappiens and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
class EnsayoWPQR(Document):
    def on_update(self):
        # Call the function to handle status update
        on_update_status_to_aprobar(self)
    def after_insert(self):
        update_prueba_certificacion(self.prueba_certificacion,self.wpq, self.name)
        
def update_prueba_certificacion(prueba_certificacion_name, wpq_name, wpqr_name):
    # Fetch the "Prueba Certificacion" document
    prueba_certificacion = frappe.get_doc("Prueba Certificacion", prueba_certificacion_name)
    # Check if detalles_de_la_prueba_de_soldadura exists
    if prueba_certificacion and prueba_certificacion.detalles_de_la_prueba_de_soldadura:
        # Loop through the child table "detalles_de_la_prueba_de_soldadura"
        for row in prueba_certificacion.detalles_de_la_prueba_de_soldadura:
            # Check if the wps is set and matches the given wps_name
            if row.wpq == wpq_name:
                # Link the WPQ to the current row
                row.wpqr = wpqr_name

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
def on_update_status_to_aprobar(doc):
    if doc.status == 'Aprobar':
        # Fetch the related "Prueba Certificacion" document
        prueba_certificacion = frappe.get_doc("Prueba Certificacion", doc.prueba_certificacion)
        frappe.db.set_value("Cualificacion WPQ",doc.wpq,"status", doc.status)
        if prueba_certificacion:
            # Loop through the child table "detalles_de_la_prueba_de_soldadura"
            for row in prueba_certificacion.detalles_de_la_prueba_de_soldadura:
                if row.wps == doc.wps and row.wpq == doc.wpq:
                    # Update the status of the row in detalles_de_la_prueba_de_soldadura
                    row.status = 'Aprobar'
            
            # Save the changes in Prueba Certificacion
            prueba_certificacion.save()
            frappe.db.commit()  # Ensure changes are committed to the database

        frappe.msgprint(_('WPQR status and related details updated successfully.'))
