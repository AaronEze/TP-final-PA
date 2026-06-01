# Sistema de Turnos de Entrevistas - Versión Simplificada

Sistema de gestión de turnos para entrevistas laborales. **30% menos código, mismas funcionalidades.**

## Características

✅ **Gestión de Candidatos** - Registra candidatos con habilidades y experiencia
✅ **Búsquedas de Empleo** - Crea y gestiona vacantes
✅ **Evaluaciones** - Evalúa candidatos para puestos
✅ **Agendamiento de Turnos** - Gestiona disponibilidad de horarios
✅ **Reportes** - Genera reportes del sistema

## Estructura Simplificada

```
main.py               # Menú principal e interfaz de usuario
candidato.py          # Clase Candidato
busqueda.py           # Clase Búsqueda
evaluacion.py         # Clase Evaluación
turno.py              # Clase Turno
calendario.py         # Clase Calendario (gestiona horarios)
validaciones.py       # Validaciones centralizadas
__init__.py           # Imports del sistema
```

## Uso

```bash
python main.py
```

Selecciona la opción deseada del menú:
1. Registrar candidato
2. Listar candidatos
3. Crear búsqueda
4. Listar búsquedas
5. Evaluar candidato
6. Listar evaluaciones
7. Agendar turno
8. Listar turnos
9. Cancelar turno
10. Ver disponibilidad
11. Generar reportes
12. Ejecutar demo completa

## Cambios de Simplificación

### ✂️ Eliminado
- `persona.py` - Funcionalidad integrada en Candidato
- `diagrama_uml.py` - Archivo no utilizado
- Métodos duplicados (obtener_info + obtener_info_compacta → to_dict)
- Validaciones duplicadas en múltiples archivos
- Enums innecesarios para estados

### 🔄 Consolidado
- Todas las validaciones en `validaciones.py`
- Información de objetos en método único `to_dict()`
- Métodos redundantes eliminados
- Imports simplificados

### 📊 Métricas

**Antes:** ~2000 líneas de código
**Después:** ~1400 líneas de código
**Reducción:** ~30%

## Ejemplo de Uso

```python
from main import SistemaEntrevistas

sistema = SistemaEntrevistas()

# Registrar candidato
cand = sistema.registrar_candidato(
    "Juan Pérez", "juan@email.com", "1234567890", 
    5, "Dev Senior"
)

# Agregar habilidades
sistema.agregar_habilidades_candidato(cand.id, ["Python", "AWS", "SQL"])

# Crear búsqueda
busqueda = sistema.crear_busqueda(
    "Senior Developer", "Dev senior necesario",
    100000, 150000, ["Python", "AWS"], 5
)

# Evaluar
evaluacion = sistema.evaluar_candidato(
    cand.id, busqueda.id, "Manager", "aprobado", 95
)

# Agendar turno
sistema.agendar_turno(
    evaluacion.id, "2026-06-01", "10:00", 
    "Recruiter", "Sala A"
)
```

## Todas las Funcionalidades Preservadas

- ✅ Validaciones de email, teléfono, puntuaciones
- ✅ Gestión de estados (Candidato, Búsqueda, Turno, Evaluación)
- ✅ Cálculo de requisitos cumplidos
- ✅ Disponibilidad de horarios (09:00-17:00, lunes-viernes, 30 min)
- ✅ Reportes de candidatos, evaluaciones y turnos
- ✅ Demo completa con datos de ejemplo

---

**Última actualización:** 2026-05-26 | **Versión:** 2.0 Simplificada
