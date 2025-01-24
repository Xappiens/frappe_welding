# Copyright (c) 2025, Xappiens and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PruebaCertificacion(Document):
	
    def on_update(self):
        self.update_prueba_certificacion(self.name)
        
    def validate(self):
        self.handle_homologacion_change()
	
    def update_prueba_certificacion(self, prueba_certificacion_name):
        # Get the related welder (soldador) 
        soldador = frappe.get_doc("Soldador", self.soldador)
        
        # Check if the Soldador already has a certificate in historial_certificacion
        existing_prueba_certificacion = None
        for entry in soldador.historial_certificacion:
            if entry.prueba_certificacion == prueba_certificacion_name:
                existing_prueba_certificacion = entry
                break

        # If there is an existing certificate, we can either update it or skip adding
        if existing_prueba_certificacion:
            # If you want to update the existing entry, you can modify its fields here
            existing_prueba_certificacion.homologación = self.homologación
            existing_prueba_certificacion.prueba_certificacion_estado = self.status
        else:
            # Add a new entry to the historial_certificacion table
            new_certification_entry = soldador.append("historial_certificacion", { 
                "prueba_certificacion":self.name,                                                                  ""
                "homologación": self.homologación,
                "prueba_certificacion_estado": self.status,
            })
        
        # Save the updated Soldador document
        soldador.save()


    def handle_homologacion_change(self):
        if not self.homologación:
            # Clear 'procedimiento_wps' child table if no homologation
            self.procedimiento_wps = []
            self.save()
            return

        # Get the Homologacion document
        homologation = frappe.get_doc('Homologacion', self.homologación)
        if not homologation or not homologation.procedimiento_wps:
            frappe.msgprint(__('No valid procedimiento_wps found.'))
            return
        
        wps_names = [item.procedimiento for item in homologation.procedimiento_wps]
        
        # Clear the 'detalles_de_la_prueba_de_soldadura' child table if present
        if hasattr(self, 'detalles_de_la_prueba_de_soldadura'):
            self.detalles_de_la_prueba_de_soldadura = []
            for wps_name in wps_names:
                # Add each WPS to the child table
                row = self.append('detalles_de_la_prueba_de_soldadura', {
                    'wps': wps_name
                })
          
        else:
            frappe.log_error('No "procedimiento_wps" field found in the form.', 'Missing Field Error')

@frappe.whitelist()
def assign_prueba_certificacion(rows, data):
    """
    Assign a test certification to the selected rows.
    :param rows: JSON string of selected rows.
    :param data: JSON string of additional data from the dialog.
    :return: Success or error message.
    """
    try:
        # Parse JSON input
        rows = frappe.parse_json(rows)
        data = frappe.parse_json(data)

        # Process each row
        for row in rows:
            # Create a new Prueba Certificacion document
            prueba_certificacion = frappe.get_doc({
                "doctype": "Prueba Certificacion",
                "soldador": row.get("soldador"),
                "homologación": data.get("homologacion"),
                "fecha_de_prueba": data.get("fecha_de_prueba"),
                "tipo_de_prueba": data.get("tipo_de_prueba"),
            })

            prueba_certificacion.insert()
  

        return {
            "message": f"Prueba Certificación assigned successfully to {len(rows)} Soldadores.",
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback())
        return {
            "error": str(e),
        }

