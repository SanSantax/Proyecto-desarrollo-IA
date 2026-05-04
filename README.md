PRIMERA VERSION:

# Demostración Visual: Strategy vs Template Method

Aplicación en Python con tkinter que demuestra visualmente la diferencia entre el patrón Strategy y el patrón Template Method.

## Características

- **Interfaz gráfica intuitiva** con dos secciones claras para comparar ambos patrones
- **Animaciones visuales** que muestran el flujo de ejecución de cada patrón
- **Implementaciones funcionales** de ambos patrones con ejemplos reales
- **Interacción en tiempo real** para cambiar estrategias y ver resultados inmediatos

## Patrones Implementados

### Patrón Strategy (Izquierda)
- **Propósito**: Permite cambiar el algoritmo en tiempo de ejecución
- **Ejemplos**:
  - **Sistema de ordenamiento** con diferentes algoritmos:
    - Bubble Sort (Estrategia A)
    - Quick Sort (Estrategia B) 
    - Merge Sort (Estrategia C)
  - **Sistema de movimiento dinámico** con estrategias intercambiables:
    - 🚶 **Caminar**: Movimiento lento y constante (velocidad 2)
    - 🏃 **Correr**: Movimiento rápido (velocidad 8)
    - ⚡ **Teletransporte**: Salto instantáneo al destino
- **Característica clave**: El contexto puede intercambiar estrategias dinámicamente

### Patrón Template Method (Derecha)
- **Propósito**: Define la estructura de un algoritmo, dejando algunos pasos para las subclases
- **Ejemplo**: Procesamiento de datos con estructura fija
  - SumProcessor (Implementación A)
  - MaxProcessor (Implementación B)
  - StatisticsProcessor (Implementación C)
- **Característica clave**: La estructura del algoritmo es fija, los pasos variables son implementados por subclases

## Uso

### Ejecutar la aplicación
```bash
python pattern_demo.py
```

### Interacción con la aplicación

1. **Botones individuales**: Click en cualquier botón de estrategia/implementación para ver resultados específicos
2. **Demostración automática**: Click en "INICIAR DEMOSTRACIÓN" para ver una animación secuencial de todas las opciones
3. **Movimiento Strategy dinámico**: 
   - Click en cualquier punto del canvas de movimiento para mover el objeto
   - Cambia la estrategia de movimiento mientras el objeto se mueve para ver el cambio en tiempo real
   - Prueba las tres estrategias: Caminar (lento), Correr (rápido), Teletransporte (instantáneo)
4. **Comparación visual**: Observa las diferencias en cómo cada patrón maneja la variabilidad

## Diferencias Clave Demostradas

### Strategy Pattern
- ✅ **Flexibilidad en runtime**: El contexto puede cambiar de estrategia dinámicamente
- ✅ **Desacoplamiento**: El contexto no conoce los detalles de implementación
- ✅ **Intercambiabilidad**: Las estrategias son completamente intercambiables

### Template Method Pattern
- ✅ **Estructura fija**: El esqueleto del algoritmo no cambia
- ✅ **Control inverso**: La superclase controla el flujo, las subclases implementan detalles
- ✅ **Reutilización de código**: Pasos comunes se comparten entre implementaciones

## Estructura del Código

```
pattern_demo.py
├── Clases Strategy
│   ├── SortStrategy (ABC) - Ordenamiento
│   ├── BubbleSortStrategy
│   ├── QuickSortStrategy
│   ├── MergeSortStrategy
│   ├── SortContext
│   ├── MovimientoStrategy (ABC) - Movimiento
│   ├── CaminarStrategy
│   ├── CorrerStrategy
│   ├── TeletransporteStrategy
│   └── ObjetoMovible
├── Clases Template Method
│   ├── DataProcessor (ABC)
│   ├── SumProcessor
│   ├── MaxProcessor
│   └── StatisticsProcessor
└── GUI (PatternDemoApp)
    ├── Sección Strategy (con demo de movimiento)
    └── Sección Template Method
```

## Requisitos

- Python 3.x
- tkinter (incluido en la instalación estándar de Python)

## Arquitectura

La aplicación sigue principios de diseño limpio:
- **Separación de responsabilidades**: Lógica de patrones separada de la GUI
- **Principio abierto/cerrado**: Fácil extensión con nuevas estrategias/implementaciones
- **Programación a interfaces**: Dependencia de abstracciones, no de implementaciones concretas
