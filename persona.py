"""
Módulo: models/persona.py
Clase base Persona - Herencia y Polimorfismo
"""

from abc import ABC, abstractmethod
from datetime import datetime
import re


class Persona(ABC):
    """
    Clase abstracta Persona que representa a cualquier persona en el sistema.
    
    Attributes:
        _id (int): Identificador único
        _nombre (str): Nombre completo
        _email (str): Correo electrónico
        _telefonо (str): Número de teléfono
        _fecha_registro (datetime): Fecha de registro en el sistema
    """
    
    # Variable de clase para generar IDs únicos automáticamente
    _contador_ids = 0
    
    def __init__(self, nombre: str, email: str, telefono: str):
        """
        Constructor de la clase Persona.
        
        Args:
            nombre (str): Nombre completo
            email (str): Correo electrónico
            telefono (str): Número de teléfono
            
        Raises:
            ValueError: Si email o teléfono no son válidos
        """
        # Encapsulamiento: atributos privados con _
        self._id = self._generar_id()
        self._nombre = nombre
        self._email = email if self._validar_email(email) else None
        self._telefono = telefono
        self._fecha_registro = datetime.now()
        
        if self._email is None:
            raise ValueError(f"Email inválido: {email}")
    
    @staticmethod
    def _generar_id() -> int:
        """Genera un ID único incrementando el contador de clase."""
        Persona._contador_ids += 1
        return Persona._contador_ids
    
    @staticmethod
    def _validar_email(email: str) -> bool:
        """
        Valida que el email tenga un formato correcto.
        
        Args:
            email (str): Email a validar
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    # ============ GETTERS (Encapsulamiento) ============
    
    @property
    def id(self) -> int:
        """Retorna el ID de la persona."""
        return self._id
    
    @property
    def nombre(self) -> str:
        """Retorna el nombre de la persona."""
        return self._nombre
    
    @property
    def email(self) -> str:
        """Retorna el email de la persona."""
        return self._email
    
    @property
    def telefono(self) -> str:
        """Retorna el teléfono de la persona."""
        return self._telefono
    
    @property
    def fecha_registro(self) -> datetime:
        """Retorna la fecha de registro."""
        return self._fecha_registro
    
    # ============ SETTERS (Encapsulamiento) ============
    
    @email.setter
    def email(self, nuevo_email: str):
        """
        Actualiza el email validando el formato.
        
        Args:
            nuevo_email (str): Nuevo email
            
        Raises:
            ValueError: Si el email es inválido
        """
        if self._validar_email(nuevo_email):
            self._email = nuevo_email
        else:
            raise ValueError(f"Email inválido: {nuevo_email}")
    
    @telefono.setter
    def telefono(self, nuevo_telefono: str):
        """Actualiza el teléfono."""
        self._telefono = nuevo_telefono
    
    # ============ MÉTODOS ABSTRACTOS (Polimorfismo) ============
    
    @abstractmethod
    def obtener_info(self) -> str:
        """
        Método abstracto que será implementado por las subclases.
        Retorna información de la persona.
        
        Returns:
            str: Información formateada de la persona
        """
        pass
    
    @abstractmethod
    def validar(self) -> bool:
        """
        Método abstracto para validar los datos de la persona.
        
        Returns:
            bool: True si es válido, False en caso contrario
        """
        pass
    
    # ============ MÉTODOS COMUNES ============
    
    def obtener_contacto(self) -> dict:
        """
        Retorna un diccionario con la información de contacto.
        
        Returns:
            dict: Información de contacto
        """
        return {
            'email': self._email,
            'telefono': self._telefono
        }
    
    def __str__(self) -> str:
        """Representación en string de la Persona."""
        return self.obtener_info()
    
    def __repr__(self) -> str:
        """Representación técnica de la Persona."""
        return f"Persona(id={self._id}, nombre='{self._nombre}', email='{self._email}')"
