# Proyecto-desarrollo-IA
En este proyecto pondremos a prueba la capacidad de la ia Windsurf para hacer un programa en el cual se implemente un ejemplo gráfico que demuestra las diferencias entre los patrones Strategy y Template Method.

Version 1.0
He completado exitosamente la creación de la aplicación Python con tkinter que demuestra visualmente la diferencia entre el patrón Strategy y el patrón Template Method.

Resumen de lo implementado:
Estructura GUI completa:

Ventana principal con dos secciones claras (Strategy a la izquierda, Template Method a la derecha)
Canvas para animaciones visuales en cada sección
Botones de interacción para cada patrón
Botones de demostración automática
Patrón Strategy implementado:

Interfaz SortStrategy con algoritmos de ordenamiento
Tres estrategias concretas: Bubble Sort, Quick Sort, Merge Sort
Clase SortContext que puede cambiar estrategias en runtime
Demostración visual de intercambio dinámico
Patrón Template Method implementado:

Clase abstracta DataProcessor con método plantilla process_data()
Tres implementaciones concretas: SumProcessor, MaxProcessor, StatisticsProcessor
Estructura fija del algoritmo con pasos variables implementados por subclases
Visualización clara de pasos fijos vs variables
Características adicionales:

Animaciones en tiempo real mostrando resultados reales
Diseño moderno con colores personalizados
Documentación completa en README.md
Código limpio y bien estructurado
La aplicación está lista para ejecutarse con python pattern_demo.py y proporciona una excelente demostración visual de las diferencias clave entre ambos patrones de diseño.
