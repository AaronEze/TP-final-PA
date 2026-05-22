"""
DIAGRAMA UML - SISTEMA DE ENTREVISTAS LABORALES

Este archivo contiene el diagrama de clases en formato ASCII.
Para una representación visual completa, usar herramientas como:
- Draw.io (https://draw.io)
- Lucidchart (https://lucidchart.com)
- PlantUML (http://plantuml.com)
- Diagrams.net
"""

UML_DIAGRAM = """
╔════════════════════════════════════════════════════════════════════════════════════════╗
║                    DIAGRAMA DE CLASES - SISTEMA DE ENTREVISTAS                       ║
╚════════════════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           <<abstract>>                                                  │
│                              PERSONA                                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Atributos:                                                                              │
│  - _id: int                                                                             │
│  - _nombre: str                                                                         │
│  - _email: str ◄─── [ENCAPSULAMIENTO]                                                 │
│  - _telefono: str                                                                       │
│  - _fecha_registro: datetime                                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Métodos:                                                                                │
│  + id: property                                                                         │
│  + nombre: property                                                                     │
│  + email: property (setter con validación)                                              │
│  + telefono: property (setter)                                                          │
│  + obtener_contacto(): dict                                                             │
│  + _validar_email(email): bool [static]                                                │
│  + obtener_info(): str [abstract] ◄─── [POLIMORFISMO]                                 │
│  + validar(): bool [abstract] ◄─── [POLIMORFISMO]                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                      △
                                      │ [HERENCIA]
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                             CANDIDATO                                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Atributos:                                                                              │
│  - _anos_experiencia: int                                                               │
│  - _habilidades: list[str]                                                              │
│  - _cv: str                                                                             │
│  - _estado: EstadoCandidato [enum]                                                      │
│  - _fecha_postulacion: datetime                                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Métodos:                                                                                │
│  + anos_experiencia: property                                                           │
│  + habilidades: property (read-only copy)                                               │
│  + estado: property                                                                     │
│  + agregar_habilidad(habilidad: str): None                                              │
│  + agregar_multiples_habilidades(habilidades: list): None                               │
│  + eliminar_habilidad(habilidad: str): bool                                             │
│  + tiene_experiencia_minima(anos: int): bool                                            │
│  + tiene_habilidad(habilidad: str): bool                                                │
│  + tiene_todas_habilidades(habilidades: list): bool                                     │
│  + obtener_info(): str [override] ◄─── [POLIMORFISMO]                                 │
│  + validar(): bool [override] ◄─── [POLIMORFISMO]                                     │
│  + obtener_info_compacta(): dict                                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              BUSQUEDA                                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Atributos:                                                                              │
│  - _id: int                                                                             │
│  - _titulo_puesto: str                                                                  │
│  - _descripcion: str                                                                    │
│  - _salario_min: float                                                                  │
│  - _salario_max: float                                                                  │
│  - _skills_requeridos: list[str]                                                        │
│  - _experiencia_minima: int                                                             │
│  - _estado: EstadoBusqueda [enum]                                                       │
│  - _fecha_creacion: datetime                                                            │
│  - _fecha_cierre: datetime [nullable]                                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Métodos:                                                                                │
│  + id, titulo_puesto, descripcion: property                                             │
│  + salario_min, salario_max, skills_requeridos: property                                │
│  + estado: property (setter)                                                            │
│  + obtener_requisitos(): dict                                                           │
│  + candidato_cumple_requisitos(candidato: Candidato): dict                              │
│  + cerrar_busqueda(): None                                                              │
│  + reabrirt_busqueda(): None                                                            │
│  + obtener_rango_salario(): str                                                         │
│  + obtener_info(): str                                                                  │
│  + obtener_info_compacta(): dict                                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            EVALUACION                                                   │
│                        [COMPOSICIÓN - Candidato + Búsqueda]                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Atributos:                                                                              │
│  - _id: int                                                                             │
│  - _candidato: Candidato [COMPOSICIÓN] ◄────────┐                                      │
│  - _busqueda: Búsqueda [COMPOSICIÓN] ◄─────────┐│                                      │
│  - _evaluador: str                              │                                      │
│  - _resultado: ResultadoEvaluacion [enum]       │                                      │
│  - _puntuacion: float (0-100)                   │                                      │
│  - _comentarios: str                            │                                      │
│  - _fecha_evaluacion: datetime [nullable]       │                                      │
├─────────────────────────────────────────────────┼──────────────────────────────────────┤
│ Métodos:                                        │                                      │
│  + id, candidato, busqueda: property            │                                      │
│  + resultado, puntuacion, comentarios: property │                                      │
│  + evaluar(resultado, puntuacion, comentarios): bool                                    │
│  + es_aprobado(): bool                          │                                      │
│  + es_rechazado(): bool                         │                                      │
│  + esta_pendiente(): bool                       │                                      │
│  + obtener_analisis(): dict                     │                                      │
│  + obtener_info(): str                          │                                      │
│  + obtener_info_compacta(): dict                │                                      │
└─────────────────────────────────────────────────┼──────────────────────────────────────┘
                                                  │
                        ┌─────────────────────────┘
                        │
        ┌───────────────┴─────────────────┐
        │                                 │
        ▼                                 ▼
   CANDIDATO                         BÚSQUEDA


┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              TURNO                                                       │
│                      [COMPOSICIÓN - Evaluación]                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Atributos:                                                                              │
│  - _id: int                                                                             │
│  - _evaluacion: Evaluacion [COMPOSICIÓN] ◄──────┐                                      │
│  - _fecha: date                                  │                                      │
│  - _hora: str (HH:MM)                            │                                      │
│  - _entrevistador: str                           │                                      │
│  - _sala: str                                    │                                      │
│  - _estado: EstadoTurno [enum]                   │                                      │
│  - _observaciones: str                           │                                      │
│  - _fecha_creacion: datetime                     │                                      │
│  - _fecha_cancelacion: datetime [nullable]       │                                      │
├──────────────────────────────────────────────────┼──────────────────────────────────────┤
│ Métodos:                                         │                                      │
│  + id, evaluacion, fecha, hora: property         │                                      │
│  + entrevistador: property (setter)              │                                      │
│  + sala: property (setter)                       │                                      │
│  + estado: property                              │                                      │
│  + agendar(): bool                               │                                      │
│  + cancelar(motivo): bool                        │                                      │
│  + completar(observaciones): bool                │                                      │
│  + marcar_no_presentado(observaciones): bool     │                                      │
│  + es_disponible(): bool                         │                                      │
│  + es_futuro(): bool                             │                                      │
│  + obtener_datetime(): datetime                  │                                      │
│  + obtener_datos_candidato(): dict               │                                      │
│  + obtener_datos_puesto(): dict                  │                                      │
│  + obtener_info(): str                           │                                      │
│  + obtener_info_compacta(): dict                 │                                      │
└──────────────────────────────────────────────────┼──────────────────────────────────────┘
                                                   │
                            ┌──────────────────────┘
                            │
                            ▼
                        EVALUACION


┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            CALENDARIO                                                   │
│                      [AGREGACIÓN - Turno[]]                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Atributos:                                                                              │
│  - _id: int                                                                             │
│  - _horarios_disponibles: Dict[str, List[str]]                                          │
│  - _turnos_agendados: List[Turno] [AGREGACIÓN] ◄────┐                                 │
│  - _salas_disponibles: List[str]                      │                                │
│  - _fecha_inicio_calendario: date                     │                                │
│  - _fecha_fin_calendario: date                        │                                │
├─────────────────────────────────────────────────────┤│                                │
│ Métodos:                                            │                                │
│  + id, turnos_agendados, salas_disponibles: property │                                │
│  + obtener_slots_libres(fecha): List[str]           │                                │
│  + esta_disponible(fecha, hora): bool               │                                │
│  + reservar_slot(fecha, hora): bool                 │                                │
│  + liberar_slot(fecha, hora): None                  │                                │
│  + agregar_turno(turno): bool [AGREGACIÓN]          │                                │
│  + eliminar_turno(turno): bool [AGREGACIÓN]         │                                │
│  + obtener_turnos_del_dia(fecha): List[Turno]       │                                │
│  + obtener_turnos_proximos(cantidad): List[Turno]   │                                │
│  + obtener_turnos_por_evaluacion(eval_id): List     │                                │
│  + obtener_info(): str                              │                                │
│  + obtener_info_compacta(): dict                     │                                │
└─────────────────────────────────────────────────────┼────────────────────────────────┘
                                                      │
                          ┌───────────────────────────┘
                          │
                          ▼
                       TURNO[] (colección)


╔════════════════════════════════════════════════════════════════════════════════════════╗
║                              SERVICIOS (SEPARACIÓN DE RESPONSABILIDADES)               ║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                        ║
│  ┌─────────────────────────────────────────────────────────────────────────────────┐  │
│  │                     SERVICIO_CANDIDATO                                          │  │
│  ├─────────────────────────────────────────────────────────────────────────────────┤  │
│  │ Métodos:                                                                        │  │
│  │  + registrar_candidato(candidato): bool                                         │  │
│  │  + obtener_candidato_por_id(id): Candidato                                      │  │
│  │  + obtener_candidatos_por_habilidad(habilidad): List[Candidato]                │  │
│  │  + obtener_candidatos_por_experiencia(anos): List[Candidato]                   │  │
│  │  + obtener_todos_candidatos(): List[Candidato]                                 │  │
│  │  + filtrar_candidatos(habilidad, anos_exp): List[Candidato]                    │  │
│  │  + generar_reporte_candidatos(): dict                                           │  │
│  └─────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                        │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐  │
│  │                     SERVICIO_EVALUACION                                         │  │
│  ├─────────────────────────────────────────────────────────────────────────────────┤  │
│  │ Métodos:                                                                        │  │
│  │  + crear_evaluacion(candidato, busqueda, evaluador): Evaluacion                │  │
│  │  + evaluar_candidato(eval, resultado, puntuacion): bool                        │  │
│  │  + obtener_evaluaciones_pendientes(): List[Evaluacion]                         │  │
│  │  + obtener_evaluaciones_aprobadas(): List[Evaluacion]                          │  │
│  │  + obtener_evaluaciones_rechazadas(): List[Evaluacion]                         │  │
│  │  + obtener_evaluacion_por_id(id): Evaluacion                                   │  │
│  │  + obtener_todas_evaluaciones(): List[Evaluacion]                              │  │
│  │  + generar_reporte_evaluaciones(): dict                                        │  │
│  └─────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                        │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐  │
│  │                     SERVICIO_CALENDARIO                                         │  │
│  ├─────────────────────────────────────────────────────────────────────────────────┤  │
│  │ Métodos:                                                                        │  │
│  │  + crear_turno(evaluacion, fecha, hora, entrevistador, sala): Turno           │  │
│  │  + agendar_turno(turno): bool                                                  │  │
│  │  + cancelar_turno(turno_id, motivo): bool                                      │  │
│  │  + completar_turno(turno_id, observaciones): bool                              │  │
│  │  + obtener_turno_por_id(id): Turno                                             │  │
│  │  + obtener_turnos_proximos(cantidad): List[Turno]                              │  │
│  │  + obtener_turnos_del_dia(fecha): List[Turno]                                  │  │
│  │  + obtener_slots_disponibles(fecha): List[str]                                 │  │
│  │  + obtener_todos_turnos(): List[Turno]                                         │  │
│  │  + generar_reporte_turnos(): dict                                              │  │
│  └─────────────────────────────────────────────────────────────────────────────────┘  │
║                                                                                        ║
╚════════════════════════════════════════════════════════════════════════════════════════╝


═══════════════════════════════════════════════════════════════════════════════════════════
LEYENDA:
═══════════════════════════════════════════════════════════════════════════════════════════

[HERENCIA]          : Candidato hereda de Persona. Reutiliza código y propiedades.

[POLIMORFISMO]      : Métodos con mismo nombre pero diferente implementación.
                      Ej: obtener_info() en Persona vs Candidato.

[COMPOSICIÓN]       : Relación fuerte "tiene un". Evaluación necesita Candidato y Búsqueda.
                      Turno necesita Evaluación.
                      Si el padre se elimina, el hijo también.

[AGREGACIÓN]        : Relación débil "contiene". Calendario contiene Turnos.
                      Si el calendario se elimina, los turnos pueden seguir existiendo.

[ENCAPSULAMIENTO]   : Atributos privados (_). Acceso controlado mediante propiedades.
                      Validación en setters.

[SEPARACIÓN RESPONS]: Lógica de negocio en servicios, no en modelos.
                      Facilita testing y mantenimiento.
"""

if __name__ == "__main__":
    print(UML_DIAGRAM)
