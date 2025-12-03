from app import app
from datetime import datetime,timedelta
from flask import session
# Filtro para formatear números con comas
def commafy(value):
    if value:
        return f"{round(value, 2):,}"
    else:
        return 0

# Filtro para formatear nombres de bases
def title_format(value):
    replacements = {
        "visualizacion": "visualización",
        "almacen": "almacén",
        "creacion": "creación",
        "descripcion": "descripción",
        "informacion": "información",
        "categoria": "categoría",
        "menu": "menú",
        "telefono": "teléfono",
        "razon": "razón",
        "metodo": "método",
        "transito": "tránsito",
        "periodico": "periódico",
        "genero":"género",
        "direccion":"dirección",
        "codigo":"código",
        "contratacion":"contratación",
        "numero":"número",
        "razon":"razón",
        "direccion":"dirección",
        "nomina":"nómina",
        "electronico":"electrónico",
        "ultimo":"último",
        "sesion":"sesión",
        "metodo":"método",
        "comision":"comisión",
        "codigo":"código",
        "actualizacion": "actualización",
        "ejecucion": "ejecución",
        "dias":"días",
        "transito": "tránsito",
        "interaccion":"interacción",
        "interacciones":"interacciones",
        "ultima":'última',
        "region":'región',
        "tipos_de_interacciones":"tipos de interacciones"
    }
    
    # First check for exact match
    if value in replacements:
        return replacements[value].capitalize()
    
    if value=='id_visualizacion':
        return "ID"

    # Replace underscores with spaces
    
    formatted = value.replace("_id_visualizacion","").replace("_nombre_empresa","").replace("_nombre_completo","").replace("_nombre","").replace("_", " ")
    # Remove "id " prefix if present
    if formatted.startswith("id "):
        formatted = formatted[3:]
    # Capitalize first letter
    formatted = formatted.capitalize()
    # Replace words with their accented versions if they exist
    for k, v in replacements.items():
        if k in formatted.lower():
            formatted = formatted.lower().replace(k, v.capitalize())
    return formatted.capitalize()

# Filtro para formatear nombres de bases
def money_format(value):
    return f"${round(value, 2):,}"

def remove_numbers(value):
    # Convert the value to a string (in case it's a number) and remove all digits
    return ''.join([char for char in str(value) if not char.isdigit()])
def date_format(value):
    if value:
        return value.strftime("%Y-%m-%d")
    else:
        return value
    
def can_access(path):
    return any(path.startswith(r) for r in session.get("accessible_routes", []))

def local_time(value):
    if not value:
        return ''
    try:
        if isinstance(value, str) and "Fecha hora: " in value:
            value=value.replace('Fecha hora: ', '').strip()
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            value=(value - timedelta(hours=6)).strftime('%Y-%m-%dT%H:%M')
            return 'Fecha hora: '+value
        else:
            return (value - timedelta(hours=6)).strftime('%Y-%m-%dT%H:%M')
    except Exception as e:
        return ''
    
app.jinja_env.globals['can_access'] = can_access

# Ejemplo de uso
app.jinja_env.filters["date_format"] = date_format
app.jinja_env.filters["commafy"] = commafy
app.jinja_env.filters["money_format"] = money_format
app.jinja_env.filters["title_format"] = title_format
app.jinja_env.filters["remove_numbers"] = remove_numbers
app.jinja_env.filters["local_time"] = local_time
