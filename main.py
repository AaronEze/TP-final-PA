"""Sistema de turnos de entrevistas laborales - VERSIÓN SIMPLIFICADA"""

from datetime import datetime, date, timedelta
from candidato import Candidato, EstadoCandidato
from busqueda import Busqueda, EstadoBusqueda
from evaluacion import Evaluacion
from turno import Turno
from calendario import Calendario


class SistemaEntrevistas:
    """Sistema de gestión de turnos de entrevistas"""
    
    def __init__(self):
        self._calendario = Calendario()
        self._candidatos = []
        self._busquedas = []
        self._evaluaciones = []
        self._turnos = []
    
    # ===== CANDIDATOS =====
    
    def registrar_candidato(self, nombre: str, email: str, telefono: str,
                           anos_experiencia: int, cv: str) -> Candidato:
        try:
            candidato = Candidato(nombre, email, telefono, anos_experiencia, cv)
            self._candidatos.append(candidato)
            print(f"✅ Candidato '{nombre}' registrado")
            return candidato
        except ValueError as e:
            print(f"❌ Error: {e}")
            return None
    
    def agregar_habilidades_candidato(self, candidato_id: int, habilidades: list) -> bool:
        cand = next((c for c in self._candidatos if c.id == candidato_id), None)
        if cand:
            cand.agregar_multiples_habilidades(habilidades)
            return True
        return False
    
    def listar_candidatos(self):
        if not self._candidatos:
            print("No hay candidatos registrados")
            return
        print("\n" + "="*60)
        print("LISTA DE CANDIDATOS")
        print("="*60)
        for i, cand in enumerate(self._candidatos, 1):
            print(f"{i}. {cand.nombre} (ID: {cand.id})")
            print(f"   Experiencia: {cand.anos_experiencia} años")
            print(f"   Habilidades: {', '.join(cand.habilidades)}")
            print(f"   Email: {cand.email}\n")
    
    # ===== BÚSQUEDAS =====
    
    def crear_busqueda(self, titulo: str, descripcion: str, salario_min: float,
                      salario_max: float, skills: list, exp_min: int) -> Busqueda:
        busqueda = Busqueda(titulo, descripcion, salario_min, salario_max, skills, exp_min)
        self._busquedas.append(busqueda)
        print(f"✅ Búsqueda '{titulo}' creada")
        return busqueda
    
    def listar_busquedas(self):
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
            print(f"   Salario: {busq.obtener_rango_salario()}\n")
    
    # ===== EVALUACIONES =====
    
    def evaluar_candidato(self, candidato_id: int, busqueda_id: int,
                         evaluador: str, resultado: str, puntuacion: float,
                         comentarios: str = "") -> Evaluacion:
        cand = next((c for c in self._candidatos if c.id == candidato_id), None)
        busq = next((b for b in self._busquedas if b.id == busqueda_id), None)
        
        if not cand or not busq:
            print("❌ Error: Candidato o búsqueda no encontrados")
            return None
        
        try:
            evaluacion = Evaluacion(cand, busq, evaluador)
            evaluacion.evaluar(resultado, puntuacion, comentarios)
            self._evaluaciones.append(evaluacion)
            
            if resultado.lower() == "aprobado":
                cand.estado = EstadoCandidato.APROBADO
            else:
                cand.estado = EstadoCandidato.RECHAZADO
            
            print(f"✅ Evaluación guardada: {resultado}")
            return evaluacion
        except ValueError as e:
            print(f"❌ Error: {e}")
            return None
    
    def listar_evaluaciones(self, estado: str = "todas"):
        if estado == "pendientes":
            evals = [e for e in self._evaluaciones if e.esta_pendiente()]
        elif estado == "aprobadas":
            evals = [e for e in self._evaluaciones if e.es_aprobado()]
        elif estado == "rechazadas":
            evals = [e for e in self._evaluaciones if e.es_rechazado()]
        else:
            evals = self._evaluaciones
        
        if not evals:
            print(f"No hay evaluaciones {estado}")
            return
        
        print("\n" + "="*60)
        print(f"EVALUACIONES ({estado.upper()})")
        print("="*60)
        for eval_obj in evals:
            print(f"ID: {eval_obj.id}")
            print(f"Candidato: {eval_obj.candidato.nombre}")
            print(f"Puesto: {eval_obj.busqueda.titulo_puesto}")
            print(f"Resultado: {eval_obj.resultado.value}")
            print(f"Puntuación: {eval_obj.puntuacion}/100\n")
    
    # ===== TURNOS =====
    
    def agendar_turno(self, evaluacion_id: int, fecha: str, hora: str,
                     entrevistador: str, sala: str) -> Turno:
        eval_obj = next((e for e in self._evaluaciones if e.id == evaluacion_id), None)
        
        if not eval_obj:
            print("❌ Evaluación no encontrada")
            return None
        
        try:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            turno = Turno(eval_obj, fecha_obj, hora, entrevistador, sala)
            
            if self._calendario.agregar_turno(turno):
                self._turnos.append(turno)
                print(f"✅ Turno agendado para {fecha} a las {hora}")
                return turno
            else:
                print("❌ Horario no disponible")
        except ValueError:
            print("❌ Formato de fecha inválido (usar YYYY-MM-DD)")
        
        return None
    
    def cancelar_turno(self, turno_id: int, motivo: str = "") -> bool:
        turno = next((t for t in self._turnos if t.id == turno_id), None)
        if turno:
            self._calendario.eliminar_turno(turno)
            turno.cancelar(motivo)
            print(f"✅ Turno {turno_id} cancelado")
            return True
        return False
    
    def listar_turnos(self, tipo: str = "proximos"):
        if tipo == "proximos":
            turnos = self._calendario.obtener_turnos_proximos(20)
            titulo = "PRÓXIMOS TURNOS"
        else:
            turnos = self._calendario.obtener_todos_turnos()
            titulo = "TODOS LOS TURNOS"
        
        if not turnos:
            print("No hay turnos")
            return
        
        print("\n" + "="*60)
        print(titulo)
        print("="*60)
        for t in turnos:
            print(f"ID: {t.id}")
            print(f"Candidato: {t.evaluacion.candidato.nombre}")
            print(f"Puesto: {t.evaluacion.busqueda.titulo_puesto}")
            print(f"Fecha: {t.fecha.strftime('%d/%m/%Y')}")
            print(f"Hora: {t.hora}")
            print(f"Entrevistador: {t.entrevistador}")
            print(f"Sala: {t.sala}")
            print(f"Estado: {t.estado.value}\n")
    
    def obtener_slots_disponibles(self, fecha: str) -> list:
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            return self._calendario.obtener_slots_libres(fecha)
        except ValueError:
            print("❌ Formato de fecha inválido")
            return []
    
    # ===== REPORTES =====
    
    def generar_reportes(self):
        print("\n" + "="*60)
        print("REPORTES DEL SISTEMA")
        print("="*60)
        
        print("\n📋 CANDIDATOS")
        print(f"  Total: {len(self._candidatos)}")
        print(f"  Aprobados: {len([c for c in self._candidatos if c.estado == EstadoCandidato.APROBADO])}")
        print(f"  Rechazados: {len([c for c in self._candidatos if c.estado == EstadoCandidato.RECHAZADO])}")
        
        print("\n📋 EVALUACIONES")
        print(f"  Total: {len(self._evaluaciones)}")
        print(f"  Aprobadas: {len([e for e in self._evaluaciones if e.es_aprobado()])}")
        print(f"  Rechazadas: {len([e for e in self._evaluaciones if e.es_rechazado()])}")
        print(f"  Pendientes: {len([e for e in self._evaluaciones if e.esta_pendiente()])}")
        
        print("\n📋 TURNOS")
        print(f"  Total: {len(self._turnos)}")
        print(f"  Próximos: {len(self._calendario.obtener_turnos_proximos())}")


def menu_principal():
    """Menú principal de la aplicación"""
    sistema = SistemaEntrevistas()
    
    while True:
        print("\n" + "="*60)
        print("SISTEMA DE TURNOS DE ENTREVISTAS")
        print("="*60)
        print("1. Registrar candidato")
        print("2. Listar candidatos")
        print("3. Crear búsqueda")
        print("4. Listar búsquedas")
        print("5. Evaluar candidato")
        print("6. Listar evaluaciones")
        print("7. Agendar turno")
        print("8. Listar turnos")
        print("9. Cancelar turno")
        print("10. Ver disponibilidad")
        print("11. Generar reportes")
        print("12. Demo completa")
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
                sistema.agregar_habilidades_candidato(cand.id, [h.strip() for h in habilidades])
        
        elif opcion == "2":
            sistema.listar_candidatos()
        
        elif opcion == "3":
            titulo = input("Título del puesto: ")
            desc = input("Descripción: ")
            sal_min = float(input("Salario mínimo: "))
            sal_max = float(input("Salario máximo: "))
            skills = input("Skills requeridos (separados por coma): ").split(",")
            exp_min = int(input("Experiencia mínima (años): "))
            sistema.crear_busqueda(titulo, desc, sal_min, sal_max, [s.strip() for s in skills], exp_min)
        
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
            sistema.evaluar_candidato(cand_id, busq_id, evaluador, resultado, puntuacion, comentarios)
        
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
            ejecutar_demo(sistema)
        
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida")


def ejecutar_demo(sistema: SistemaEntrevistas):
    """Demo del sistema con datos de ejemplo"""
    print("\n" + "="*60)
    print("EJECUTANDO DEMO")
    print("="*60)
    
    # Candidatos
    print("\n📝 Registrando candidatos...")
    c1 = sistema.registrar_candidato("Alice Johnson", "alice@email.com", "1111111111", 6, "Senior Dev")
    sistema.agregar_habilidades_candidato(c1.id, ["Python", "JavaScript", "SQL", "AWS"])
    
    c2 = sistema.registrar_candidato("Bob Smith", "bob@email.com", "2222222222", 3, "Full Stack Dev")
    sistema.agregar_habilidades_candidato(c2.id, ["Python", "React", "PostgreSQL"])
    
    # Búsquedas
    print("\n🔍 Creando búsquedas...")
    b1 = sistema.crear_busqueda("Senior Python Developer", "Dev Senior", 80000, 120000, ["Python", "AWS", "SQL"], 5)
    b2 = sistema.crear_busqueda("Full Stack Developer", "Dev Full Stack", 40000, 70000, ["Python", "React", "PostgreSQL"], 2)
    
    # Evaluaciones
    print("\n📊 Evaluando candidatos...")
    e1 = sistema.evaluar_candidato(c1.id, b1.id, "Manager", "aprobado", 95, "Excelente perfil")
    e2 = sistema.evaluar_candidato(c2.id, b2.id, "Manager", "aprobado", 88, "Buen candidato")
    
    # Turnos
    print("\n📅 Agendando turnos...")
    fecha = (date.today() + timedelta(days=2)).strftime('%Y-%m-%d')
    sistema.agendar_turno(e1.id, fecha, "09:30", "Recruiter", "Sala A")
    sistema.agendar_turno(e2.id, fecha, "10:00", "Recruiter", "Sala B")
    
    # Mostrar resultados
    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    sistema.listar_candidatos()
    sistema.listar_busquedas()
    sistema.listar_evaluaciones("todas")
    sistema.listar_turnos("todos")
    sistema.generar_reportes()
    print("\n✅ DEMO COMPLETADA\n")


if __name__ == "__main__":
    menu_principal()
