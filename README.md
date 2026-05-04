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
- **Ejemplos**:
  - **Procesamiento de datos** con estructura fija:
    - SumProcessor (Implementación A)
    - MaxProcessor (Implementación B)
    - StatisticsProcessor (Implementación C)
  - **Procesamiento gráfico** con flujo visual:
    - 🔴 **Procesador Rojo**: Dibuja formas geométricas rojas (círculos, rectángulos, triángulos)
    - 🔵 **Procesador Azul**: Dibuja formas azules (ondas, círculos concéntricos, estrellas)
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
4. **Template Method gráfico**:
   - Click en "Procesador Rojo" o "Procesador Azul" para ejecutar el flujo completo
   - Observa cómo los pasos fijos (Inicio y Fin) son idénticos
   - El paso variable (Procesar) cambia según la implementación concreta
   - La animación muestra: Inicio (amarillo) → Procesar (rojo/azul) → Fin (verde)
5. **Comparación visual**: Observa las diferencias en cómo cada patrón maneja la variabilidad

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
│   ├── DataProcessor (ABC) - Procesamiento de datos
│   ├── SumProcessor
│   ├── MaxProcessor
│   ├── StatisticsProcessor
│   ├── ProcesadorTarea (ABC) - Procesamiento gráfico
│   ├── ProcesadorGraficoRojo
│   └── ProcesadorGraficoAzul
└── GUI (PatternDemoApp)
    ├── Sección Strategy (con demo de movimiento)
    └── Sección Template Method (con demo gráfica)
```

## Requisitos

- Python 3.x
- tkinter (incluido en la instalación estándar de Python)

## Arquitectura

La aplicación sigue principios de diseño limpio:
- **Separación de responsabilidades**: Lógica de patrones separada de la GUI
- **Principio abierto/cerrado**: Fácil extensión con nuevas estrategias/implementaciones
- **Programación a interfaces**: Dependencia de abstracciones, no de implementaciones concretas

SEGUNDA VERSION:

Resumen de lo implementado:
Nuevas clases de Strategy de movimiento:

MovimientoStrategy (interfaz abstracta)
CaminarStrategy (movimiento lento, velocidad 2)
CorrerStrategy (movimiento rápido, velocidad 8)
TeletransporteStrategy (salto instantáneo)
ObjetoMovible (contexto que utiliza estrategias)
Funcionalidades interactivas:

Canvas de movimiento donde el usuario puede hacer clic para mover el objeto
Botones para cambiar estrategias dinámicamente mientras el objeto se mueve
Animación continua a ~33 FPS
Feedback visual con cambios de color al cambiar estrategia
Indicador en tiempo real de la estrategia actual
Características clave demostradas:

Cambio en runtime: El objeto puede cambiar de estrategia mientras está en movimiento
Desacoplamiento: El objeto no conoce los detalles de implementación del movimiento
Intercambiabilidad: Las tres estrategias son completamente intercambiables sin modificar el objeto principal
La aplicación ahora proporciona una demostración completa y funcional del patrón Strategy tanto para ordenamiento como para movimiento, permitiendo al usuario experimentar directamente cómo el comportamiento puede cambiar dinámicamente sin alterar la estructura del objeto principal.