import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, getdate

class Homologarsoldador(Document):
    
    def on_update(self):
        self.update_prueba_certificacion(self.name)
	
    def update_prueba_certificacion(self, homologar_soldador_name):
        # Get the related welder (soldador) 
        soldador = frappe.get_doc("Soldador", self.soldador)
        
        # Check if the Soldador already has a certificate in historial_certificacion
        existing_certificate = None
        for entry in soldador.historial_certificacion:
            if entry.prueba_certificacion == self.prueba_certificacion:
                existing_certificate = entry
                break

        # If there is an existing certificate, we can either update it or skip adding
        if existing_certificate:
            # If you want to update the existing entry, you can modify its fields here
            existing_certificate.certificación = homologar_soldador_name
            existing_certificate.tipo_de_certificación = self.tipo_de_certificación
            existing_certificate.status = self.estado
            existing_certificate.fecha_de_certificación = self.fecha_de_certificación
            existing_certificate.fecha_de_vencimiento_de_la_certificación = self.fecha_de_vencimiento_de_la_certificación
       
        
        # Save the updated Soldador document
        soldador.save()




# def check_certification_expiry():
#     # Get all HomologarSoldador records
#     homologar_soldador_records = frappe.get_all("Homologar soldador", fields=["name", "fecha_de_certificación", "fecha_de_vencimiento_de_la_certificación", "estado"])
    
#     for record in homologar_soldador_records:
#         fecha_de_certificacion = getdate(record.fecha_de_certificación)
#         fecha_de_vencimiento = getdate(record.fecha_de_vencimiento_de_la_certificación)
        
#         # Get today's date
#         today = getdate(nowdate())
        
#         # Check if today's date is outside the certification range
#         if today < fecha_de_certificacion or today > fecha_de_vencimiento:
#             # Update the status to "Expired" if the current date is not within the range
#             if record.estado != "Vencido":  # Only update if the status is not already "Expired"
#                 frappe.db.set_value("Homologar soldador", record.name, "estado", "Vencido")
#         else:
#             frappe.db.set_value("Homologar soldador", record.name, "estado", "Vencido")
#         frappe.db.commit() 
#     frappe.log_error(f"Certification expired for {record.name}", "Certification Expiry")
