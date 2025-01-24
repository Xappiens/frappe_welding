# Copyright (c) 2025, Xappiens and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Procedimiento(Document):
    def on_update(self):
        print("on_update", self.name)
        # Ensure 'WPS' is linked to this Procedimiento
        wps = frappe.get_doc({
                'doctype': 'WPS',
                'procedimiento': self.name,	
            })
        wps.insert()

@frappe.whitelist()
def set_filling_materials(base_material):
    # Get the Configuracion de Materiales document
    configuracion_materiales = frappe.get_doc('Configuracion de Materiales', "Configuracion de Materiales")
    
    # Initialize an empty list to store compatible filling materials
    compatible_filling_materials = []

    # Loop through the compatibility rules in Configuracion de Materiales
    for material in configuracion_materiales.reglas_compatibilidad_materiales:
        # Print the current material and its base group for debugging
        print("Checking material:", material)
        print("Base material group:", material.grupo_de_base_material)

        # Check if the material matches the base material
        if material.grupo_de_base_material == frappe.db.get_value("Material base",base_material,"grupo_de_material"):
            # If a match is found, get the compatible filling materials
            compatible_filling_materials = frappe.get_list(
                'Material de Relleno', 
                filters={'grupo_de_material': material.grupo_de_relleno_material}
            )
            print("Compatible filling materials found:", compatible_filling_materials)
            break  # Exit the loop once the match is found
    
    # Return the list of compatible filling materials
    return compatible_filling_materials


    