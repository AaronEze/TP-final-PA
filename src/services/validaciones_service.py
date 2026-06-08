import re
from datetime import datetime

class ValidacionesService:
    
    @staticmethod
    def validar_email(email: str) -> bool:
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None

    @staticmethod
    def validar_telefono(telefono: str) -> bool:
        patron = r'^[\d\s\-\+\(\)]{7,}$'
        return re.match(patron, telefono) is not None

    @staticmethod
    def validar_hora(hora: str) -> bool:
        try:
            datetime.strptime(hora, '%H:%M')
            return True
        except ValueError:
            return False

    @staticmethod
    def validar_puntuacion(puntuacion: float) -> bool:
        return 0 <= puntuacion <= 100

    @staticmethod
    def validar_anos_experiencia(anos: int) -> bool:
        return anos >= 0

    @staticmethod
    def validar_salario(salario_min: float, salario_max: float) -> bool:
        return salario_min > 0 and salario_max > 0 and salario_min <= salario_max