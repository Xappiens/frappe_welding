import frappe

def execute(filters=None):
    if filters is None:
        filters = {}

    # Define filter conditions
    conditions = []
    inner_conditions = []
    
    # Basic conditions for Soldador
    if filters.get("soldador"):
        conditions.append("Soldador.name = %(soldador)s")
    if filters.get("empleado"):
        conditions.append("Soldador.empleado = %(empleado)s")
    if filters.get("compañia"):
        conditions.append("Soldador.compañía = %(compañia)s")
    
    # Additional conditions for homologación
    if filters.get("is_homologacion") == 1:
        if filters.get("status"):
            conditions.append("prueba_certificacion.status = %(status)s")
        if filters.get("prueba_certificacion_status"):
            conditions.append("prueba_certificacion.status = %(prueba_certificacion_status)s")
        if filters.get("certification_name"):
            conditions.append("prueba_certificacion.certificación = %(certification_name)s")
        if filters.get("homologacion"):
            conditions.append("prueba_certificacion.homologación = %(homologacion)s")
    else:
        if filters.get("homologacion"):
            inner_conditions.append("homologación IN (%(homologacion)s)")  # Properly add homologacion filter
    
    # Combine conditions
    where_clause = " AND ".join(conditions)
    inner_conditions_clause = " AND ".join(inner_conditions)
    
    # Define query based on the `is_homologacion` flag
    if filters.get("is_homologacion") == 0 or filters.get("is_homologacion") is None:
        query = f"""
            SELECT
                Soldador.name AS soldador,
                Soldador.empleado AS empleado,
                Soldador.compañía AS compañia
            FROM
                `tabSoldador` AS Soldador
            LEFT JOIN
                `tabHistorial Certificacion` AS prueba_certificacion
                ON Soldador.name = prueba_certificacion.parent
            WHERE
                (prueba_certificacion.homologación IS NULL OR 
                Soldador.name NOT IN (
                    SELECT DISTINCT parent
                    FROM `tabHistorial Certificacion`
                    {"WHERE " + inner_conditions_clause if inner_conditions_clause else ""}
                ))
                {"AND " + where_clause if where_clause else ""}
        """
    else:
        query = f"""
            SELECT
                Soldador.name AS soldador,
                Soldador.empleado AS empleado,
                Soldador.compañía AS compañia,
                prueba_certificacion.certificación AS certification_name,
                prueba_certificacion.prueba_certificacion AS prueba_certificacion,
                prueba_certificacion.homologación AS homologacion,
                prueba_certificacion.tipo_de_certificación AS tipo_de_certificacion,
                prueba_certificacion.status AS status,
                prueba_certificacion.prueba_certificacion_estado AS prueba_certificacion_status,
                prueba_certificacion.fecha_de_certificación AS fecha_de_certificacion,
                prueba_certificacion.fecha_de_vencimiento_de_la_certificación AS fecha_de_vencimiento
            FROM
                `tabSoldador` AS Soldador
            LEFT JOIN
                `tabHistorial Certificacion` AS prueba_certificacion
                ON Soldador.name = prueba_certificacion.parent
            {"WHERE " + where_clause if where_clause else ""}
        """
    # Execute the query
    data = frappe.db.sql(query, filters, as_dict=True)
    if filters.get("is_homologacion") == 0 or filters.get("is_homologacion") is None:
    # Columns for the report
        columns = [    
            {"fieldname": "soldador", "label": "Soldador", "fieldtype": "Link", "options": "Soldador", "width": 130},
            {"fieldname": "empleado", "label": "Empleado", "fieldtype": "Link", "options": "Employee", "width": 130},
            {"fieldname": "compañia", "label": "Compañía", "fieldtype": "Link", "options": "Company", "width": 90},
        ]
    else :
        columns = [    
            {"fieldname": "soldador", "label": "Soldador", "fieldtype": "Link", "options": "Soldador", "width": 130},
            {"fieldname": "empleado", "label": "Empleado", "fieldtype": "Link", "options": "Employee", "width": 100},
            {"fieldname": "homologacion", "label": "Homologación", "fieldtype": "Link", "options": "Homologacion", "width": 100},
            {"fieldname": "prueba_certificacion", "label": "Prueba Certificacion", "fieldtype": "Link", "options": "Prueba Certificacion", "width": 150},
            {"fieldname": "prueba_certificacion_status", "label": "Prueba Certificacion Estado", "fieldtype": "Data", "width": 100, "align": "center"},
            {"fieldname": "tipo_de_certificacion", "label": "Tipo de certificación", "fieldtype": "Data", "width": 120},
            {"fieldname": "certification_name", "label": "Certificación", "fieldtype": "Link", "options": "Homologar soldador", "width": 140},
            {"fieldname": "status", "label": "Certificacion Estado", "fieldtype": "Data", "width": 100, "align": "center"},
            {"fieldname": "fecha_de_certificacion", "label": "Fecha de certificación", "fieldtype": "Date", "width": 120},
            {"fieldname": "fecha_de_vencimiento", "label": "Fecha de vencimiento de la certificación", "fieldtype": "Date", "width": 120},
            {"fieldname": "compañia", "label": "Compañía", "fieldtype": "Link", "options": "Company", "width": 90},
        ]

    return columns, data
    