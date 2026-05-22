"""
Módulo: main.py
Aplicación principal - Sistema de turnos de entrevistas laborales
"""

from datetime import datetime, date, timedelta
from models.candidato import Candidato, EstadoCandidato
from models.busqueda import Busqueda, EstadoBusqueda
from models.evaluacion import Evaluacion
from models.turno import Turno
from models.calendario import Calendario
from services.servicios import (ServicioEvaluacion, ServicioCalendario, 
                                ServicioCandidato)


class SistemaEntrevistas:
    """
    Clase principal que orquesta todo el sistema.
    Contiene todos los servicios e implementa el menú de la aplicación.
    """
    
    def __init__(self):
        """Inicializa el sistema con todos los servicios."""
        self._calendario = Calendario()
        self._servicio_evaluacion = ServicioEvaluacion()
        self._servicio_calendario = ServicioCalendario(self._calendario)
        self._servicio_candidato = ServicioCandidato()
        self._candidatos = []
        self._busquedas = []
    
    # ============ MÉTODOS DE CANDIDATOS ============
    
    def registrar_candidato(self, nombre: str, email: str, telefono: str,
                           anos_experiencia: int, cv: str) -> Candidato:
        """
        Registra un nuevo candidato.
        
        Args:
            nombre, email, telefono, anos_experiencia, cv
            
        Returns:
            Candidato: Candidato creado
        """
        try:
            candidato = Candidato(nombre, email, telefono, anos_experiencia, cv)
            if self._servicio_candidato.registrar_candidato(candidato):
                self._candidatos.append(candidato)
                print(f"✅ Candidato '{nombre}' registrado exitosamente")
                return candidato
        except ValueError as e:
            print(f"❌ Error: {e}")
        return None
    
    def agregar_habilidades_candidato(self, candidato_id: int, habilidades: list) -> bool:
        """
        Agrega habilidades a un candidato.
        
        Args:
            candidato_id (int): ID del candidato
            habilidades (list): Lista de habilidades
            
        Returns:
            bool: True si se agregaron
        """
        candidato = self._servicio_candidato.obtener_candidato_por_id(candidato_id)
        if candidato:
            candidato.agregar_multiples_habilidades(habilidades)
            return True
        return False
    
    def listar_candidatos(self):
        """Lista todos los candidatos registrados."""
        candidatos = self._servicio_candidato.obtener_todos_candidatos()
        if not candidatos:
            print("No hay candidatos registrados")
            return
        
        print("\n" + "="*60)
        print("LISTA DE CANDIDATOS")
        print("="*60)
        for i, cand in enumerate(candidatos, 1):
            print(f"{i}. {cand.nombre} (ID: {cand.id})")
            print(f"   Experiencia: {cand.anos_experiencia} años")
            print(f"   Habilidades: {', '.join(cand.habilidades)}")
            print(f"   Email: {cand.email}")
            print()
    
    # ============ MÉTODOS DE BÚSQUEDAS ============
    
    def crear_busqueda(self, titulo: str, descripcion: str, salario_min: float,
                      salario_max: float, skills: list, exp_min: int) -> Busqueda:
        """
        Crea una nueva búsqueda de empleo.
        
        Args:
            titulo, descripcion, salario_min, salario_max, skills, exp_min
            
        Returns:
            Busqueda: Búsqueda creada
        """
        busqueda = Busqueda(titulo, descripcion, salario_min, salario_max, 
                           skills, exp_min)
        self._busquedas.append(busqueda)
        print(f"✅ Búsqueda '{titulo}' creada exitosamente")
        return busqueda
    
    def listar_busquedas(self):
        """Lista todas las búsquedas abiertas."""
        if not self._busquedas:
            print("No hay búsquedas activas")
            return
        
        print("\n" + "="*60)
        print("BÚSQUEDAS DISPONIBLES")
        print("="*60)
        for i, busq in enumerate(self._busquedas, 1):
            print(f"{i}. {busq.titulo_puesto} (ID: {busq.id})")
            print(f"   Descripción: {busq.descripcion}")
            print(f"   Experiencia requerida: {busq.experiencia_minima} años")
            print(f"   Skills: {', '.join(busq.skills_requeridos)}")
            print(f"   Salario: {busq.obtener_rango_salario()}")
            print()
    
    # ============ MÉTODOS DE EVALUACIÓN ============
    
    def evaluar_candidato(self, candidato_id: int, busqueda_id: int,
                         evaluador: str, resultado: str, puntuacion: float,
                         comentarios: str = "") -> Evaluacion:
        """
        Evalúa un candidato para una búsqueda.
        
        Args:
            candidato_id, busqueda_id, evaluador, resultado, puntuacion, comentarios
            
        Returns:
            Evaluacion: Evaluación creada
        """
        candidato = self._servicio_candidato.obtener_candidato_por_id(candidato_id)
        busqueda = next((b for b in self._busquedas if b.id == busqueda_id), None)
        
        if not candidato or not busqueda:
            print("❌ Error: Candidato o búsqueda no encontrados")
            return None
        
        evaluacion = self._servicio_evaluacion.crear_evaluacion(candidato, busqueda, evaluador)
        
        if self._servicio_evaluacion.evaluar_candidato(evaluacion, resultado, 
                                                       puntuacion, comentarios):
            # Actualizar estado del candidato
            if resultado.lower() == "aprobado":
                candidato.estado = EstadoCandidato.APROBADO
            else:
                candidato.estado = EstadoCandidato.RECHAZADO
            
            print(f"✅ Evaluación guardada: {resultado}")
            return evaluacion
        
        return None
    
    def listar_evaluaciones(self, estado: str = "todas"):
        """
        Lista evaluaciones según el estado.
        
        Args:
            estado (str): "todas", "pendientes", "aprobadas", "rechazadas"
        """
        if estado == "pendientes":
            evaluaciones = self._servicio_evaluacion.obtener_evaluaciones_pendientes()
        elif estado == "aprobadas":
            evaluaciones = self._servicio_evaluacion.obtener_evaluaciones_aprobadas()
        elif estado == "rechazadas":
            evaluaciones = self._servicio_evaluacion.obtener_evaluaciones_rechazadas()
        else:
            evaluaciones = self._servicio_evaluacion.obtener_todas_evaluaciones()
        
        if not evaluaciones:
            print(f"No hay evaluaciones {estado}")
            return
        
        print("\n" + "="*60)
        print(f"EVALUACIONES ({estado.upper()})")
        print("="*60)
        for eval_obj in evaluaciones:
            print(f"ID: {eval_obj.id}")
            print(f"Candidato: {eval_obj.candidato.nombre}")
            print(f"Puesto: {eval_obj.busqueda.titulo_puesto}")
            print(f"Resultado: {eval_obj.resultado.value}")
            print(f"Puntuación: {eval_obj.puntuacion}/100")
            print()
    
    # ============ MÉTODOS DE TURNOS ============
    
    def agendar_turno(self, evaluacion_id: int, fecha: str, hora: str,
                     entrevistador: str, sala: str) -> Turno:
        """
        Agenda un turno para una evaluación aprobada.
        
        Args:
            evaluacion_id, fecha (YYYY-MM-DD), hora (HH:MM), entrevistador, sala
            
        Returns:
            Turno: Turno creado
        """
        evaluacion = self._servicio_evaluacion.obtener_evaluacion_por_id(evaluacion_id)
        
        if not evaluacion:
            print("❌ Evaluación no encontrada")
            return None
        
        try:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            turno = self._servicio_calendario.crear_turno(evaluacion, fecha_obj, 
                                                         hora, entrevistador, sala)
            if turno:
                print(f"✅ Turno agendado para {fecha} a las {hora}")
                return turno
        except ValueError:
            print("❌ Formato de fecha inválido (usar YYYY-MM-DD)")
        
        return None
    
    def cancelar_turno(self, turno_id: int, motivo: str = "") -> bool:
        """
        Cancela un turno.
        
        Args:
            turno_id (int): ID del turno
            motivo (str): Motivo de cancelación
            
        Returns:
            bool: True si se canceló
        """
        if self._servicio_calendario.cancelar_turno(turno_id, motivo):
            print(f"✅ Turno {turno_id} cancelado")
            return True
        return False
    
    def listar_turnos(self, tipo: str = "proximos"):
        """
        Lista turnos.
        
        Args:
            tipo (str): "proximos" o "todos"
        """
        if tipo == "proximos":
            turnos = self._servicio_calendario.obtener_turnos_proximos(20)
            titulo = "PRÓXIMOS TURNOS"
        else:
            turnos = self._servicio_calendario.obtener_todos_turnos()
            titulo = "TODOS LOS TURNOS"
        
        if not turnos:
            print("No hay turnos")
            return
        
        print("\n" + "="*60)
        print(titulo)
        print("="*60)
        for turno in turnos:
            print(f"ID: {turno.id}")
            print(f"Candidato: {turno.evaluacion.candidato.nombre}")
            print(f"Puesto: {turno.evaluacion.busqueda.titulo_puesto}")
            print(f"Fecha: {turno.fecha.strftime('%d/%m/%Y')}")
            print(f"Hora: {turno.hora}")
            print(f"Entrevistador: {turno.entrevistador}")
            print(f"Sala: {turno.sala}")
            print(f"Estado: {turno.estado.value}")
            print()
    
    def obtener_slots_disponibles(self, fecha: str) -> list:
        """
        Obtiene slots disponibles para una fecha.
        
        Args:
            fecha (str): Fecha en formato YYYY-MM-DD
            
        Returns:
            list: Horarios disponibles
        """
        try:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            return self._servicio_calendario.obtener_slots_disponibles(fecha_obj)
        except ValueError:
            print("❌ Formato de fecha inválido")
            return []
    
    # ============ REPORTES ============
    
    def generar_reportes(self):
        """Genera reportes del sistema."""
        print("\n" + "="*60)
        print("REPORTES DEL SISTEMA")
        print("="*60)
        
        # Reporte de candidatos
        rep_cand = self._servicio_candidato.generar_reporte_candidatos()
        print("\n📋 CANDIDATOS")
        for clave, valor in rep_cand.items():
            print(f"  {clave}: {valor}")
        
        # Reporte de evaluaciones
        rep_eval = self._servicio_evaluacion.generar_reporte_evaluaciones()
        print("\n📋 EVALUACIONES")
        for clave, valor in rep_eval.items():
            print(f"  {clave}: {valor}")
        
        # Reporte de turnos
        rep_turn = self._servicio_calendario.generar_reporte_turnos()
        print("\n📋 TURNOS")
        for clave, valor in rep_turn.items():
            print(f"  {clave}: {valor}")


def menu_principal():
    """Menú principal de la aplicación."""
    sistema = SistemaEntrevistas()
    
    while True:
        print("\n" + "="*60)
        print("SISTEMA DE TURNOS DE ENTREVISTAS LABORALES")
        print("="*60)
        print("1. Registrar candidato")
        print("2. Listar candidatos")
        print("3. Crear búsqueda de empleo")
        print("4. Listar búsquedas")
        print("5. Evaluar candidato")
        print("6. Listar evaluaciones")
        print("7. Agendar turno")
        print("8. Listar turnos")
        print("9. Cancelar turno")
        print("10. Ver disponibilidad de horarios")
        print("11. Generar reportes")
        print("12. Ejecutar demo completa")
        print("0. Salir")
        print("="*60)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            nombre = input("Nombre: ")
            email = input("Email: ")
            telefono = input("Teléfono: ")
            anos = int(input("Años de experiencia: "))
            cv = input("CV/Descripción: ")
            cand = sistema.registrar_candidato(nombre, email, telefono, anos, cv)
            if cand:
                habilidades = input("Habilidades (separadas por coma): ").split(",")
                sistema.agregar_habilidades_candidato(cand.id, 
                                                     [h.strip() for h in habilidades])
        
        elif opcion == "2":
            sistema.listar_candidatos()
        
        elif opcion == "3":
            titulo = input("Título del puesto: ")
            desc = input("Descripción: ")
            sal_min = float(input("Salario mínimo: "))
            sal_max = float(input("Salario máximo: "))
            skills = input("Skills requeridos (separados por coma): ").split(",")
            exp_min = int(input("Experiencia mínima (años): "))
            sistema.crear_busqueda(titulo, desc, sal_min, sal_max, 
                                  [s.strip() for s in skills], exp_min)
        
        elif opcion == "4":
            sistema.listar_busquedas()
        
        elif opcion == "5":
            sistema.listar_candidatos()
            cand_id = int(input("ID del candidato: "))
            sistema.listar_busquedas()
            busq_id = int(input("ID de la búsqueda: "))
            evaluador = input("Nombre del evaluador: ")
            resultado = input("Resultado (aprobado/rechazado): ")
            puntuacion = float(input("Puntuación (0-100): "))
            comentarios = input("Comentarios: ")
            sistema.evaluar_candidato(cand_id, busq_id, evaluador, resultado, 
                                     puntuacion, comentarios)
        
        elif opcion == "6":
            estado = input("Filtro (todas/pendientes/aprobadas/rechazadas): ")
            sistema.listar_evaluaciones(estado)
        
        elif opcion == "7":
            eval_id = int(input("ID de evaluación: "))
            fecha = input("Fecha (YYYY-MM-DD): ")
            slots = sistema.obtener_slots_disponibles(fecha)
            print(f"Horarios disponibles: {slots}")
            hora = input("Hora (HH:MM): ")
            entrevistador = input("Nombre del entrevistador: ")
            sala = input("Sala: ")
            sistema.agendar_turno(eval_id, fecha, hora, entrevistador, sala)
        
        elif opcion == "8":
            tipo = input("Tipo (proximos/todos): ")
            sistema.listar_turnos(tipo)
        
        elif opcion == "9":
            turno_id = int(input("ID del turno: "))
            motivo = input("Motivo de cancelación: ")
            sistema.cancelar_turno(turno_id, motivo)
        
        elif opcion == "10":
            fecha = input("Fecha (YYYY-MM-DD): ")
            slots = sistema.obtener_slots_disponibles(fecha)
            print(f"Horarios disponibles para {fecha}: {slots}")
        
        elif opcion == "11":
            sistema.generar_reportes()
        
        elif opcion == "12":
            ejecutar_demo_completa(sistema)
        
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida")


def ejecutar_demo_completa(sistema: SistemaEntrevistas):
    """
    Ejecuta una demostración completa del sistema con datos de ejemplo.
    
    Args:
        sistema (SistemaEntrevistas): Instancia del sistema
    """
    print("\n" + "="*60)
    print("EJECUTANDO DEMO COMPLETA")
    print("="*60)
    
    # Registrar candidatos
    print("\n📝 REGISTRANDO CANDIDATOS...")
    cand1 = sistema.registrar_candidato(
        "Alice Johnson", "alice@email.com", "1111111111", 6, 
        "Senior Developer with 6 years experience"
    )
    sistema.agregar_habilidades_candidato(cand1.id, ["Python", "JavaScript", "SQL", "AWS"])
    
    cand2 = sistema.registrar_candidato(
        "Bob Smith", "bob@email.com", "2222222222", 3,
        "Full Stack Developer"
    )
    sistema.agregar_habilidades_candidato(cand2.id, ["Python", "React", "PostgreSQL"])
    
    cand3 = sistema.registrar_candidato(
        "Carol White", "carol@email.com", "3333333333", 8,
        "Technical Lead"
    )
    sistema.agregar_habilidades_candidato(cand3.id, ["Python", "JavaScript", "AWS", "Docker", "Kubernetes"])
    
    # Crear búsquedas
    print("\n🔍 CREANDO BÚSQUEDAS...")
    busq1 = sistema.crear_busqueda(
        "Senior Python Developer", "Buscamos desarrollador senior",
        80000, 120000, ["Python", "AWS", "SQL"], 5
    )
    
    busq2 = sistema.crear_busqueda(
        "Full Stack Developer", "Desarrollador full stack junior-mid",
        40000, 70000, ["Python", "React", "PostgreSQL"], 2
    )
    
    # Evaluar candidatos
    print("\n📊 EVALUANDO CANDIDATOS...")
    eval1 = sistema.evaluar_candidato(
        cand1.id, busq1.id, "Juan Manager", "aprobado", 95,
        "Excelente perfil, cumple todos los requisitos"
    )
    
    eval2 = sistema.evaluar_candidato(
        cand2.id, busq2.id, "Juan Manager", "aprobado", 88,
        "Buen candidato, tiene experiencia suficiente"
    )
    
    eval3 = sistema.evaluar_candidato(
        cand3.id, busq1.id, "Juan Manager", "aprobado", 98,
        "Perfecto match, muy recomendado"
    )
    
    # Agendar turnos
    print("\n📅 AGENDANDO TURNOS...")
    fecha_mañana = (date.today() + timedelta(days=2)).strftime('%Y-%m-%d')
    fecha_pasado = (date.today() + timedelta(days=5)).strftime('%Y-%m-%d')
    
    turno1 = sistema.agendar_turno(
        eval1.id, fecha_mañana, "09:30", "Luis Recruiter", "Sala A"
    )
    
    turno2 = sistema.agendar_turno(
        eval2.id, fecha_mañana, "10:00", "Luis Recruiter", "Sala B"
    )
    
    turno3 = sistema.agendar_turno(
        eval3.id, fecha_pasado, "14:00", "Maria HR", "Sala C"
    )
    
    # Mostrar resultados
    print("\n" + "="*60)
    print("RESUMEN DE LA DEMO")
    print("="*60)
    
    sistema.listar_candidatos()
    sistema.listar_busquedas()
    sistema.listar_evaluaciones("todas")
    sistema.listar_turnos("todos")
    sistema.generar_reportes()
    
    print("\n✅ DEMO COMPLETADA\n")


if __name__ == "__main__":
    menu_principal()
