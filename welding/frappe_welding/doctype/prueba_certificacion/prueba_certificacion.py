# Copyright (c) 2025, Xappiens and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class PruebaCertificacion(Document):
	
    def on_update(self):
        self.update_prueba_certificacion(self.name)
    def after_insert(self):
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
                "prueba_certificacion":self.name,               
                "homologación": self.homologación,
                "prueba_certificacion_estado": self.status,
            })
        
        # Save the updated Soldador document
        soldador.save()


    def handle_homologacion_change(self):
        if not self.homologación:
            # Clear 'procedimiento_wps' child table if no homologation
            self.detalles_de_la_prueba_de_soldadura = []
            self.save()
            return

        # Get the Homologacion document
        homologation = frappe.get_doc('Homologacion', self.homologación)
        if not homologation or not homologation.procedimiento:
            frappe.msgprint(_('No valid procedimientos found in Homologacion.'))
            return

        # List of procedimientos from Homologacion
        procedimientos = [item.procedimiento for item in homologation.procedimiento]
        
        # Clear existing child table entries
        self.detalles_de_la_prueba_de_soldadura = []

        for procedimiento in procedimientos:
            # Fetch WPS documents linked to the procedimiento
            wps_list = frappe.get_all('WPS', filters={'procedimiento': procedimiento}, fields=['name'])
            
            if not wps_list:
                frappe.msgprint(__('No WPS found for procedimiento {0}.').format(procedimiento))
                continue
            
            for wps in wps_list:
                # Add each WPS to the 'procedimiento_wps' child table
                row = self.append('detalles_de_la_prueba_de_soldadura', {
                    'procedimiento': procedimiento,
                    'wps': wps['name']
                })
        



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

