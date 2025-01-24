import frappe
from frappe.model.document import Document

class Soldador(Document):
    def onload(self):
        self.load_dashboard_info()

    def load_dashboard_info(self):
        homologacions = frappe.get_all("Homologacion", fields=["name"])
        
        active_homologacions = []
        
        for homologacion in homologacions:
            # Fetching the Homologar soldador records related to the current Soldador and Homologacion
            homologar_soldador = frappe.get_all("Homologar soldador", filters={
                "soldador": self.name,
                "homologación": homologacion["name"],
                "estado": "Activo"  # Checking for active state
            })
            
            # If we find any active homologar_soldador, set color to green, else red
            if homologar_soldador:
                color = "green"
            else:
                color = "red"
            
            # Append to the list with color based on the condition
            active_homologacions.append({
                "homologacion": homologacion["name"],
                "color": color
            })

        # Prepare dashboard information
        info = {
            "active_homologacions": active_homologacions
        }

        # Setting the onload data for the frontend
        self.set_onload("dashboard_info", info)
