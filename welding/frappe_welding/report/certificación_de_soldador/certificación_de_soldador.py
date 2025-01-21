import frappe

def execute(filters=None):
    if filters is None:
        filters = {}

    # Define filter conditions
    conditions = []
    if filters.get("soldador"):
        conditions.append("Soldador.name = %(soldador)s")
    if filters.get("homologacion"):
        conditions.append("certification.homologación = %(homologacion)s")
    if filters.get("empleado"):
        conditions.append("Soldador.empleado = %(empleado)s")
    if filters.get("compañia"):
        conditions.append("Soldador.compañía = %(compañia)s")
    if filters.get("status"):
        conditions.append("certification.status = %(status)s")
    if filters.get("certification_name"):
        conditions.append("certification.certificación = %(certification_name)s")
   
    
    # Combine conditions into a WHERE clause
    where_clause = " AND ".join(conditions)
    if where_clause:
        where_clause = "WHERE " + where_clause

    # Query to fetch data
    data = frappe.db.sql(f"""
        SELECT
            Soldador.name AS soldador,
            Soldador.empleado AS empleado,
            Soldador.compañía AS compañia,
            certification.certificación AS certification_name,
            certification.homologación AS homologacion,
            certification.tipo_de_certificación AS tipo_de_certificacion,
            certification.status AS status,
            certification.fecha_de_certificación AS fecha_de_certificacion,
            certification.fecha_de_vencimiento_de_la_certificación AS fecha_de_vencimiento
        FROM
            `tabSoldador` AS Soldador
        JOIN
            `tabHistorial Certificacion` AS certification
            ON Soldador.name = certification.parent
        {where_clause}
    """, filters, as_dict=True)

    # Format data to apply color
    # for record in data:
    #     if record['status'] == 'Active':
    #         record['status_color'] = 'green'
    #     elif record['status'] == 'Expired':
    #         record['status_color'] = 'red'

    # Columns for the report
    columns = [	 	
        {"fieldname": "soldador", "label": "Soldador", "fieldtype": "Link", "options": "Soldador", "width": 150},
        {"fieldname": "empleado", "label": "Empleado", "fieldtype": "Link", "options": "Employee", "width": 100},
        {"fieldname": "compañia", "label": "Compañía", "fieldtype": "Link", "options": "Company", "width": 100},
        {"fieldname": "homologacion", "label": "Homologación", "fieldtype": "Link", "options": "Homologacion", "width": 100},
        {"fieldname": "tipo_de_certificacion", "label": "Tipo de certificación", "fieldtype": "Data", "width": 150},
        {"fieldname": "certification_name", "label": "Certificación", "fieldtype": "Link", "options": "Homologar soldador", "width": 150},
        {"fieldname": "status", "label": "Estado", "fieldtype": "Data", "width": 100, "align":"center"},  
        {"fieldname": "fecha_de_certificacion", "label": "Fecha de certificación", "fieldtype": "Date", "width": 120},
        {"fieldname": "fecha_de_vencimiento", "label": "Fecha de vencimiento de la certificación", "fieldtype": "Date", "width": 120}
    ]

    return columns, data
