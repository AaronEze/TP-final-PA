"""
Módulo: utils/validaciones.py
Funciones de validación reutilizables
"""

import re
from datetime import datetime, date, time


def validar_email(email: str) -> bool:
    """
    Valida que el email tenga un formato correcto.
    
    Args:
        email (str): Email a validar
        
    Returns:
        bool: True si es válido
    """
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None


def validar_telefono(telefono: str) -> bool:
    """
    Valida que el teléfono sea válido.
    
    Args:
        telefono (str): Teléfono a validar
        
    Returns:
        bool: True si es válido
    """
    # Acepta números, espacios y caracteres especiales comunes
    patron = r'^[\d\s\-\+\(\)]{7,}$'
    return re.match(patron, telefono) is not None


def validar_fecha(fecha: date) -> bool:
    """
    Valida que la fecha sea válida y futura.
    
    Args:
        fecha (date): Fecha a validar
        
    Returns:
        bool: True si es válida
    """
    try:
        if not isinstance(fecha, date):
            return False
        return fecha >= date.today()
    except:
        return False


def validar_hora(hora: str) -> bool:
    """
    Valida que la hora tenga formato correcto (HH:MM).
    
    Args:
        hora (str): Hora a validar
        
    Returns:
        bool: True si es válida
    """
    try:
        datetime.strptime(hora, '%H:%M')
        return True
    except ValueError:
        return False


def validar_puntuacion(puntuacion: float) -> bool:
    """
    Valida que la puntuación esté entre 0 y 100.
    
    Args:
        puntuacion (float): Puntuación a validar
        
    Returns:
        bool: True si es válida
    """
    return 0 <= puntuacion <= 100


def validar_anos_experiencia(anos: int) -> bool:
    """
    Valida que los años de experiencia sean válidos.
    
    Args:
        anos (int): Años a validar
        
    Returns:
        bool: True si es válido
    """
    return anos >= 0


def validar_nombre(nombre: str) -> bool:
    """
    Valida que el nombre sea válido.
    
    Args:
        nombre (str): Nombre a validar
        
    Returns:
        bool: True si es válido
    """
    return len(nombre.strip()) > 0 and len(nombre) <= 100


def validar_salario(salario_min: float, salario_max: float) -> bool:
    """
    Valida que los salarios sean válidos.
    
    Args:
        salario_min (float): Salario mínimo
        salario_max (float): Salario máximo
        
    Returns:
        bool: True si son válidos
    """
    return salario_min > 0 and salario_max > 0 and salario_min <= salario_max
