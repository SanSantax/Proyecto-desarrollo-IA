#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEMOSTRACIÓN VISUAL: PATRONES DE DISEÑO STRATEGY vs TEMPLATE METHOD
==================================================================

Esta aplicación demuestra visualmente la diferencia entre dos patrones de diseño fundamentales:

1. PATRÓN STRATEGY (Izquierda):
   - Permite cambiar el algoritmo/comportamiento en tiempo de ejecución
   - Ejemplos: Sistema de ordenamiento + Sistema de movimiento dinámico
   - Característica: El contexto puede intercambiar estrategias dinámicamente

2. PATRÓN TEMPLATE METHOD (Derecha):
   - Define la estructura de un algoritmo, dejando algunos pasos para las subclases
   - Ejemplos: Procesamiento de datos + Procesamiento gráfico
   - Característica: La estructura del algoritmo es fija, los pasos variables son implementados por subclases

Autor: Asistente de IA Cascade
Fecha: 2026
"""

# ========================================
# IMPORTACIONES NECESARIAS
# ========================================
import tkinter as tk
from tkinter import ttk
import math
import time
from abc import ABC, abstractmethod

# ========================================
# PATRÓN STRATEGY - SISTEMA DE ORDENAMIENTO
# ========================================

class SortStrategy(ABC):
    """
    INTERFAZ STRATEGY PARA ALGORITMOS DE ORDENAMIENTO
    ================================================
    
    Esta es la interfaz abstracta que define el contrato para todas
    las estrategias de ordenamiento. Cada estrategia concreta debe
    implementar estos métodos.
    """
    
    @abstractmethod
    def sort(self, data):
        """Ordena los datos usando un algoritmo específico"""
        pass
    
    @abstractmethod
    def get_name(self):
        """Retorna el nombre del algoritmo de ordenamiento"""
        pass

class BubbleSortStrategy(SortStrategy):
    """
    ESTRATEGIA CONCRETA: BUBBLE SORT
    ==============================
    
    Implementación del algoritmo Bubble Sort (lento, O(n²)).
    Demuestra una estrategia de ordenamiento simple.
    """
    
    def sort(self, data):
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr
    
    def get_name(self):
        return "Bubble Sort"

class QuickSortStrategy(SortStrategy):
    """
    ESTRATEGIA CONCRETA: QUICK SORT
    ==============================
    
    Implementación del algoritmo Quick Sort (rápido, O(n log n) promedio).
    Demuestra una estrategia de ordenamiento eficiente.
    """
    
    def sort(self, data):
        arr = data.copy()
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return self.sort(left) + middle + self.sort(right)
    
    def get_name(self):
        return "Quick Sort"

class MergeSortStrategy(SortStrategy):
    """
    ESTRATEGIA CONCRETA: MERGE SORT
    ===============================
    
    Implementación del algoritmo Merge Sort (estable, O(n log n)).
    Demuestra una estrategia de ordenamiento divide y vencerás.
    """
    
    def sort(self, data):
        arr = data.copy()
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self.sort(arr[:mid])
        right = self.sort(arr[mid:])
        return self.merge(left, right)
    
    def merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def get_name(self):
        return "Merge Sort"

class SortContext:
    """
    CONTEXTO DEL PATRÓN STRATEGY
    ============================
    
    Esta clase utiliza una estrategia de ordenamiento. Puede cambiar
    de estrategia dinámicamente sin modificar su estructura interna.
    """
    
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy):
        """Cambia la estrategia de ordenamiento en runtime"""
        self._strategy = strategy
    
    def execute_sort(self, data):
        """Ejecuta el ordenamiento usando la estrategia actual"""
        return self._strategy.sort(data)
    
    def get_strategy_name(self):
        """Retorna el nombre de la estrategia actual"""
        return self._strategy.get_name()

# ========================================
# PATRÓN STRATEGY - SISTEMA DE MOVIMIENTO
# ========================================

class MovimientoStrategy(ABC):
    """
    INTERFAZ STRATEGY PARA MOVIMIENTO DE OBJETOS
    ==============================================
    
    Define el contrato para diferentes estrategias de movimiento.
    Cada estrategia implementa su propia lógica de movimiento.
    """
    
    @abstractmethod
    def mover(self, x, y, canvas, objeto_id):
        """Mueve el objeto a una nueva posición"""
        pass
    
    @abstractmethod
    def get_nombre(self):
        """Retorna el nombre de la estrategia"""
        pass
    
    @abstractmethod
    def get_velocidad(self):
        """Retorna la velocidad de movimiento"""
        pass

class CaminarStrategy(MovimientoStrategy):
    """
    ESTRATEGIA CONCRETA: CAMINAR (LENTO)
    ====================================
    
    Movimiento lento y constante. Velocidad = 2 píxeles por frame.
    """
    
    def __init__(self):
        self.velocidad = 2
        
    def mover(self, x, y, canvas, objeto_id):
        coords = canvas.coords(objeto_id)
        if coords:
            current_x = (coords[0] + coords[2]) / 2
            current_y = (coords[1] + coords[3]) / 2
            
            dx = x - current_x
            dy = y - current_y
            distancia = (dx**2 + dy**2)**0.5
            
            if distancia > self.velocidad:
                dx = (dx / distancia) * self.velocidad
                dy = (dy / distancia) * self.velocidad
                canvas.move(objeto_id, dx, dy)
                return False
            else:
                canvas.coords(objeto_id, x - 15, y - 15, x + 15, y + 15)
                return True
        return True
    
    def get_nombre(self):
        return "Caminar"
    
    def get_velocidad(self):
        return self.velocidad

class CorrerStrategy(MovimientoStrategy):
    """
    ESTRATEGIA CONCRETA: CORRER (RÁPIDO)
    ====================================
    
    Movimiento rápido. Velocidad = 8 píxeles por frame.
    """
    
    def __init__(self):
        self.velocidad = 8
        
    def mover(self, x, y, canvas, objeto_id):
        coords = canvas.coords(objeto_id)
        if coords:
            current_x = (coords[0] + coords[2]) / 2
            current_y = (coords[1] + coords[3]) / 2
            
            dx = x - current_x
            dy = y - current_y
            distancia = (dx**2 + dy**2)**0.5
            
            if distancia > self.velocidad:
                dx = (dx / distancia) * self.velocidad
                dy = (dy / distancia) * self.velocidad
                canvas.move(objeto_id, dx, dy)
                return False
            else:
                canvas.coords(objeto_id, x - 15, y - 15, x + 15, y + 15)
                return True
        return True
    
    def get_nombre(self):
        return "Correr"
    
    def get_velocidad(self):
        return self.velocidad

class TeletransporteStrategy(MovimientoStrategy):
    """
    ESTRATEGIA CONCRETA: TELETRANSPORTE (INSTANTÁNEO)
    ==================================================
    
    Movimiento instantáneo al destino. Velocidad = infinito.
    """
    
    def __init__(self):
        self.velocidad = float('inf')
        
    def mover(self, x, y, canvas, objeto_id):
        canvas.coords(objeto_id, x - 15, y - 15, x + 15, y + 15)
        return True
    
    def get_nombre(self):
        return "Teletransporte"
    
    def get_velocidad(self):
        return self.velocidad

class ObjetoMovible:
    """
    CONTEXTO QUE UTILIZA ESTRATEGIAS DE MOVIMIENTO
    ==============================================
    
    Este objeto puede cambiar su estrategia de movimiento
    dinámicamente sin modificar su estructura.
    """
    
    def __init__(self, canvas, x, y, color='#FF6B6B'):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        
        # Crear objeto visual (círculo)
        self.objeto_id = canvas.create_oval(
            x - 15, y - 15, x + 15, y + 15,
            fill=color, outline='white', width=2
        )
        
        # Estrategia inicial
        self.estrategia = CaminarStrategy()
        
        # Control de animación
        self.animando = False
        self.destino_x = x
        self.destino_y = y
        
    def set_estrategia(self, estrategia: MovimientoStrategy):
        """Cambia la estrategia de movimiento"""
        self.estrategia = estrategia
        
    def mover_a(self, x, y):
        """Inicia el movimiento hacia un destino"""
        self.destino_x = x
        self.destino_y = y
        self.animando = True
        
    def actualizar(self):
        """Actualiza la posición del objeto según la estrategia actual"""
        if self.animando:
            llego = self.estrategia.mover(self.destino_x, self.destino_y, 
                                        self.canvas, self.objeto_id)
            if llego:
                self.animando = False
                
    def get_estrategia_actual(self):
        """Retorna la estrategia actual"""
        return self.estrategia.get_nombre()

# ========================================
# PATRÓN TEMPLATE METHOD - PROCESAMIENTO DE DATOS
# ========================================

class DataProcessor(ABC):
    """
    CLASE ABSTRACTA CON TEMPLATE METHOD
    ==================================
    
    Define la estructura del algoritmo de procesamiento de datos.
    Las subclases implementan los pasos variables.
    """
    
    def process_data(self, data):
        """
        TEMPLATE METHOD - Define la estructura del algoritmo
        ================================================
        
        Este método define el esqueleto del procesamiento:
        1. Validar datos (fijo)
        2. Procesar core (variable)
        3. Formatear resultado (fijo)
        4. Generar resumen (variable)
        """
        result = {
            'original': data,
            'validated': self.validate_data(data),
            'processed': self.process_core(data),
            'formatted': self.format_result(data),
            'summary': self.generate_summary(data)
        }
        return result
    
    def validate_data(self, data):
        """Paso fijo - validación básica"""
        return isinstance(data, list) and all(isinstance(x, (int, float)) for x in data)
    
    @abstractmethod
    def process_core(self, data):
        """Paso abstracto - implementación específica"""
        pass
    
    def format_result(self, data):
        """Paso fijo - formato estándar"""
        return f"Processed {len(data)} items"
    
    @abstractmethod
    def generate_summary(self, data):
        """Paso abstracto - implementación específica"""
        pass

class SumProcessor(DataProcessor):
    """
    IMPLEMENTACIÓN CONCRETA - PROCESADOR DE SUMA
    ==========================================
    
    Implementa el procesamiento calculando suma y promedio.
    """
    
    def process_core(self, data):
        return sum(data)
    
    def generate_summary(self, data):
        return f"Sum: {sum(data)}, Average: {sum(data)/len(data):.2f}"

class MaxProcessor(DataProcessor):
    """
    IMPLEMENTACIÓN CONCRETA - PROCESADOR DE MÁXIMO
    ==============================================
    
    Implementa el procesamiento calculando máximo y mínimo.
    """
    
    def process_core(self, data):
        return max(data)
    
    def generate_summary(self, data):
        return f"Max: {max(data)}, Min: {min(data)}"

class StatisticsProcessor(DataProcessor):
    """
    IMPLEMENTACIÓN CONCRETA - PROCESADOR ESTADÍSTICO
    ================================================
    
    Implementa el procesamiento calculando mediana y varianza.
    """
    
    def process_core(self, data):
        sorted_data = sorted(data)
        n = len(data)
        if n % 2 == 0:
            median = (sorted_data[n//2-1] + sorted_data[n//2]) / 2
        else:
            median = sorted_data[n//2]
        return median
    
    def generate_summary(self, data):
        sorted_data = sorted(data)
        n = len(data)
        if n % 2 == 0:
            median = (sorted_data[n//2-1] + sorted_data[n//2]) / 2
        else:
            median = sorted_data[n//2]
        variance = sum((x - sum(data)/len(data))**2 for x in data) / len(data)
        return f"Median: {median:.2f}, Variance: {variance:.2f}"

# ========================================
# PATRÓN TEMPLATE METHOD - PROCESAMIENTO GRÁFICO
# ========================================

class ProcesadorTarea(ABC):
    """
    CLASE ABSTRACTA CON TEMPLATE METHOD PARA PROCESAMIENTO GRÁFICO
    ==========================================================
    
    Define la estructura del proceso gráfico con tres pasos:
    1. inicio() - Paso fijo
    2. procesar() - Paso abstracto (implementado por subclases)
    3. fin() - Paso fijo
    """
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.paso_actual = 0
        self.animacion_activa = False
        
    def ejecutar_proceso(self):
        """
        TEMPLATE METHOD - Define la estructura del proceso
        ================================================
        
        Ejecuta los tres pasos en secuencia con temporización.
        """
        self.paso_actual = 0
        self.animacion_activa = True
        
        # Paso 1: Inicio (fijo)
        self.inicio()
        
        # Paso 2: Procesar (variable - implementado por subclases)
        self.root.after(1000, lambda: self._ejecutar_paso_procesar())
        
        # Paso 3: Fin (fijo)
        self.root.after(2000, lambda: self._ejecutar_paso_fin())
    
    def _ejecutar_paso_procesar(self):
        """Ejecuta el paso de procesamiento"""
        if self.animacion_activa:
            self.paso_actual = 1
            self.procesar()
    
    def _ejecutar_paso_fin(self):
        """Ejecuta el paso final"""
        if self.animacion_activa:
            self.paso_actual = 2
            self.fin()
            self.animacion_activa = False
    
    def inicio(self):
        """
        PASO FIJO - Inicialización común
        ==============================
        
        Todas las implementaciones comparten este paso.
        """
        self.canvas.delete("all")
        
        self.canvas.create_rectangle(
            10, 10, 540, 140,
            outline='#FFD700',
            width=3,
            fill='#1a1a1a'
        )
        
        self.canvas.create_text(
            275, 30,
            text="🚀 INICIANDO PROCESO",
            fill='#FFD700',
            font=('Arial', 14, 'bold')
        )
        
        self.canvas.create_text(
            275, 60,
            text="Paso 1: Inicio (Fijo)",
            fill='white',
            font=('Arial', 11)
        )
        
        self.canvas.create_text(
            275, 85,
            text="✓ Validando recursos",
            fill='#4CAF50',
            font=('Arial', 10)
        )
        
        self.canvas.create_text(
            275, 105,
            text="✓ Preparando entorno",
            fill='#4CAF50',
            font=('Arial', 10)
        )
        
        # Indicador de progreso
        self.canvas.create_rectangle(
            50, 125, 500, 135,
            outline='white',
            width=1
        )
        self.canvas.create_rectangle(
            50, 125, 200, 135,
            fill='#FFD700',
            outline=''
        )
    
    @abstractmethod
    def procesar(self):
        """
        PASO ABSTRACTO - Implementación específica de cada subclase
        ====================================================
        
        Cada subclase implementa su propia lógica de procesamiento.
        """
        pass
    
    def fin(self):
        """
        PASO FIJO - Finalización común
        ==============================
        
        Todas las implementaciones comparten este paso.
        """
        self.canvas.create_rectangle(
            10, 10, 540, 140,
            outline='#00FF00',
            width=3,
            fill='#1a1a1a'
        )
        
        self.canvas.create_text(
            275, 30,
            text="✅ PROCESO COMPLETADO",
            fill='#00FF00',
            font=('Arial', 14, 'bold')
        )
        
        self.canvas.create_text(
            275, 60,
            text="Paso 3: Fin (Fijo)",
            fill='white',
            font=('Arial', 11)
        )
        
        self.canvas.create_text(
            275, 85,
            text="✓ Liberando recursos",
            fill='#4CAF50',
            font=('Arial', 10)
        )
        
        self.canvas.create_text(
            275, 105,
            text="✓ Generando reporte",
            fill='#4CAF50',
            font=('Arial', 10)
        )
        
        # Indicador de progreso completo
        self.canvas.create_rectangle(
            50, 125, 500, 135,
            outline='white',
            width=1
        )
        self.canvas.create_rectangle(
            50, 125, 500, 135,
            fill='#00FF00',
            outline=''
        )

class ProcesadorGraficoRojo(ProcesadorTarea):
    """
    IMPLEMENTACIÓN CONCRETA - PROCESADOR GRÁFICO ROJO
    ==============================================
    
    Implementa el paso procesar() dibujando formas rojas.
    """
    
    def __init__(self, canvas, root):
        super().__init__(canvas)
        self.root = root
        
    def procesar(self):
        """Implementación específica - dibuja formas rojas"""
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            10, 10, 540, 140,
            outline='#FF0000',
            width=3,
            fill='#1a1a1a'
        )
        
        self.canvas.create_text(
            275, 30,
            text="🔴 PROCESANDO (MODO ROJO)",
            fill='#FF0000',
            font=('Arial', 14, 'bold')
        )
        
        self.canvas.create_text(
            275, 55,
            text="Paso 2: Procesar (Variable - Implementación Roja)",
            fill='white',
            font=('Arial', 11)
        )
        
        # Dibujar formas rojas
        self.canvas.create_oval(
            100, 75, 150, 125,
            fill='#FF0000',
            outline='white',
            width=2
        )
        
        self.canvas.create_rectangle(
            200, 80, 250, 120,
            fill='#CC0000',
            outline='white',
            width=2
        )
        
        points = [300, 120, 325, 75, 350, 120]
        self.canvas.create_polygon(
            points,
            fill='#FF4444',
            outline='white',
            width=2
        )
        
        for i in range(5):
            x = 400 + i * 20
            self.canvas.create_line(
                x, 75, x + 10, 125,
                fill='#FF6666',
                width=3
            )
        
        # Indicador de progreso medio
        self.canvas.create_rectangle(
            50, 125, 500, 135,
            outline='white',
            width=1
        )
        self.canvas.create_rectangle(
            50, 125, 350, 135,
            fill='#FF0000',
            outline=''
        )

class ProcesadorGraficoAzul(ProcesadorTarea):
    """
    IMPLEMENTACIÓN CONCRETA - PROCESADOR GRÁFICO AZUL
    ==============================================
    
    Implementa el paso procesar() dibujando formas azules.
    """
    
    def __init__(self, canvas, root):
        super().__init__(canvas)
        self.root = root
        
    def procesar(self):
        """Implementación específica - dibuja formas azules"""
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            10, 10, 540, 140,
            outline='#0000FF',
            width=3,
            fill='#1a1a1a'
        )
        
        self.canvas.create_text(
            275, 30,
            text="🔵 PROCESANDO (MODO AZUL)",
            fill='#0000FF',
            font=('Arial', 14, 'bold')
        )
        
        self.canvas.create_text(
            275, 55,
            text="Paso 2: Procesar (Variable - Implementación Azul)",
            fill='white',
            font=('Arial', 11)
        )
        
        # Dibujar formas azules
        for i in range(3):
            y = 85 + i * 15
            self.canvas.create_arc(
                100, y - 10, 200, y + 10,
                start=0,
                extent=180,
                fill='',
                outline='#0066FF',
                width=3
            )
        
        for i in range(4):
            size = 30 - i * 5
            self.canvas.create_oval(
                275 - size, 95 - size,
                275 + size, 95 + size,
                fill='',
                outline='#0088FF',
                width=2
            )
        
        self._dibujar_estrella(400, 95, 20, '#0044FF')
        
        # Indicador de progreso medio
        self.canvas.create_rectangle(
            50, 125, 500, 135,
            outline='white',
            width=1
        )
        self.canvas.create_rectangle(
            50, 125, 350, 135,
            fill='#0000FF',
            outline=''
        )
    
    def _dibujar_estrella(self, cx, cy, size, color):
        """Dibuja una estrella de 5 puntas"""
        points = []
        for i in range(10):
            angle = math.pi * i / 5 - math.pi / 2
            if i % 2 == 0:
                r = size
            else:
                r = size * 0.4
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.extend([x, y])
        
        self.canvas.create_polygon(
            points,
            fill=color,
            outline='white',
            width=2
        )

# ========================================
# INTERFAZ GRÁFICA DE USUARIO (GUI)
# ========================================

class PatternDemoApp:
    """
    APLICACIÓN PRINCIPAL - DEMOSTRACIÓN VISUAL
    ==========================================
    
    Esta clase crea y gestiona la interfaz gráfica que demuestra
    ambos patrones de diseño de forma interactiva y visual.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Demostración Visual: Strategy vs Template Method")
        self.root.geometry("1200x750")
        self.root.configure(bg='#2b2b2b')
        
        # Paleta de colores personalizada
        self.colors = {
            'bg': '#2b2b2b',
            'panel_bg': '#3c3c3c',
            'strategy': '#4CAF50',
            'template': '#2196F3',
            'text': '#ffffff',
            'button': '#555555',
            'accent': '#FF9800'
        }
        
        # Inicializar patrones
        self.setup_patterns()
        self.setup_ui()
        
    def setup_patterns(self):
        """Inicializar todas las implementaciones de los patrones"""
        
        # Estrategias para Strategy (ordenamiento)
        self.strategies = {
            "A": BubbleSortStrategy(),
            "B": QuickSortStrategy(), 
            "C": MergeSortStrategy()
        }
        self.sort_context = SortContext(self.strategies["A"])
        
        # Estrategias de movimiento
        self.movimiento_strategies = {
            "caminar": CaminarStrategy(),
            "correr": CorrerStrategy(),
            "teletransporte": TeletransporteStrategy()
        }
        
        # Procesadores para Template Method (datos)
        self.processors = {
            "A": SumProcessor(),
            "B": MaxProcessor(),
            "C": StatisticsProcessor()
        }
        
        # Procesadores gráficos para Template Method
        self.procesadores_graficos = {}
        
        # Datos de ejemplo
        self.sample_data = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50]
        
        # Control de animación
        self.animacion_activa = False
        
    def setup_ui(self):
        """Configurar la interfaz de usuario completa"""
        
        # Título principal
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = tk.Label(
            title_frame, 
            text="🎯 PATRONES DE DISEÑO: STRATEGY vs TEMPLATE METHOD",
            font=('Arial', 18, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Experimenta la diferencia entre cambiar comportamiento (Strategy) y estructura fija (Template Method)",
            font=('Arial', 11),
            fg='#888888',
            bg=self.colors['bg']
        )
        subtitle_label.pack(pady=5)
        
        # Contenedor principal con dos secciones
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Configurar ambas secciones
        self.setup_strategy_section(main_container)
        self.setup_template_section(main_container)
        
    def setup_strategy_section(self, parent):
        """Configurar la sección del patrón Strategy"""
        
        # Frame principal para Strategy
        strategy_frame = tk.Frame(parent, bg=self.colors['panel_bg'], relief=tk.RAISED, bd=2)
        strategy_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Título Strategy
        strategy_title = tk.Label(
            strategy_frame,
            text="🎲 PATRÓN STRATEGY",
            font=('Arial', 14, 'bold'),
            fg=self.colors['strategy'],
            bg=self.colors['panel_bg']
        )
        strategy_title.pack(pady=10)
        
        # Descripción
        desc_text = "✅ El algoritmo/comportamiento puede cambiar en tiempo de ejecución\n✅ Se encapsulan diferentes estrategias intercambiables"
        strategy_desc = tk.Label(
            strategy_frame,
            text=desc_text,
            font=('Arial', 10),
            fg=self.colors['text'],
            bg=self.colors['panel_bg'],
            justify=tk.CENTER
        )
        strategy_desc.pack(pady=5)
        
        # Canvas para demostración de ordenamiento
        self.strategy_canvas = tk.Canvas(
            strategy_frame,
            width=550,
            height=180,
            bg='#1e1e1e',
            highlightthickness=2,
            highlightbackground=self.colors['strategy']
        )
        self.strategy_canvas.pack(pady=5, padx=10)
        
        # Canvas para demostración de movimiento
        movimiento_frame = tk.Frame(strategy_frame, bg=self.colors['panel_bg'])
        movimiento_frame.pack(fill=tk.X, padx=10, pady=5)
        
        movimiento_label = tk.Label(
            movimiento_frame,
            text="🎮 DEMO STRATEGY - MOVIMIENTO DINÁMICO",
            font=('Arial', 11, 'bold'),
            fg=self.colors['strategy'],
            bg=self.colors['panel_bg']
        )
        movimiento_label.pack(pady=5)
        
        self.movimiento_canvas = tk.Canvas(
            movimiento_frame,
            width=550,
            height=140,
            bg='#0a0a0a',
            highlightthickness=2,
            highlightbackground=self.colors['accent']
        )
        self.movimiento_canvas.pack(pady=5)
        
        # Crear objeto movible para demostración
        self.objeto_movible = ObjetoMovible(self.movimiento_canvas, 50, 70, '#FF6B6B')
        
        # Área de clic en el canvas
        self.movimiento_canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Frame de control de movimiento
        control_frame = tk.Frame(movimiento_frame, bg=self.colors['panel_bg'])
        control_frame.pack(pady=5)
        
        # Botones de estrategia de movimiento
        self.caminar_btn = tk.Button(
            control_frame,
            text="🚶 Caminar",
            command=lambda: self.cambiar_estrategia_movimiento("caminar"),
            bg='#4CAF50',
            fg='white',
            font=('Arial', 9, 'bold'),
            width=12
        )
        self.caminar_btn.grid(row=0, column=0, padx=3)
        
        self.correr_btn = tk.Button(
            control_frame,
            text="🏃 Correr",
            command=lambda: self.cambiar_estrategia_movimiento("correr"),
            bg='#FF9800',
            fg='white',
            font=('Arial', 9, 'bold'),
            width=12
        )
        self.correr_btn.grid(row=0, column=1, padx=3)
        
        self.teletransporte_btn = tk.Button(
            control_frame,
            text="⚡ Teletransporte",
            command=lambda: self.cambiar_estrategia_movimiento("teletransporte"),
            bg='#9C27B0',
            fg='white',
            font=('Arial', 9, 'bold'),
            width=14
        )
        self.teletransporte_btn.grid(row=0, column=2, padx=3)
        
        # Estado actual
        self.estado_label = tk.Label(
            movimiento_frame,
            text=f"Estrategia actual: {self.objeto_movible.get_estrategia_actual()}",
            font=('Arial', 10),
            fg=self.colors['text'],
            bg=self.colors['panel_bg']
        )
        self.estado_label.pack(pady=3)
        
        # Frame de botones de ordenamiento
        strategy_buttons = tk.Frame(strategy_frame, bg=self.colors['panel_bg'])
        strategy_buttons.pack(pady=10)
        
        # Botones para diferentes estrategias de ordenamiento
        self.strategy_btn1 = tk.Button(
            strategy_buttons,
            text="Bubble Sort",
            command=lambda: self.execute_strategy("A"),
            bg=self.colors['button'],
            fg=self.colors['text'],
            font=('Arial', 10, 'bold'),
            width=12,
            height=2
        )
        self.strategy_btn1.grid(row=0, column=0, padx=5, pady=5)
        
        self.strategy_btn2 = tk.Button(
            strategy_buttons,
            text="Quick Sort",
            command=lambda: self.execute_strategy("B"),
            bg=self.colors['button'],
            fg=self.colors['text'],
            font=('Arial', 10, 'bold'),
            width=12,
            height=2
        )
        self.strategy_btn2.grid(row=0, column=1, padx=5, pady=5)
        
        self.strategy_btn3 = tk.Button(
            strategy_buttons,
            text="Merge Sort",
            command=lambda: self.execute_strategy("C"),
            bg=self.colors['button'],
            fg=self.colors['text'],
            font=('Arial', 10, 'bold'),
            width=12,
            height=2
        )
        self.strategy_btn3.grid(row=0, column=2, padx=5, pady=5)
        
        # Botón de demostración
        self.demo_strategy_btn = tk.Button(
            strategy_frame,
            text="🎬 INICIAR DEMOSTRACIÓN STRATEGY",
            command=self.demo_strategy_pattern,
            bg=self.colors['strategy'],
            fg=self.colors['text'],
            font=('Arial', 11, 'bold'),
            width=25,
            height=2
        )
        self.demo_strategy_btn.pack(pady=10)
        
    def setup_template_section(self, parent):
        """Configurar la sección del patrón Template Method"""
        
        # Frame principal para Template Method
        template_frame = tk.Frame(parent, bg=self.colors['panel_bg'], relief=tk.RAISED, bd=2)
        template_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Título Template Method
        template_title = tk.Label(
            template_frame,
            text="📋 PATRÓN TEMPLATE METHOD",
            font=('Arial', 14, 'bold'),
            fg=self.colors['template'],
            bg=self.colors['panel_bg']
        )
        template_title.pack(pady=10)
        
        # Descripción
        desc_text = "✅ La estructura del algoritmo es fija\n✅ Las subclases implementan pasos específicos"
        template_desc = tk.Label(
            template_frame,
            text=desc_text,
            font=('Arial', 10),
            fg=self.colors['text'],
            bg=self.colors['panel_bg'],
            justify=tk.CENTER
        )
        template_desc.pack(pady=5)
        
        # Canvas para demostración de datos
        self.template_canvas = tk.Canvas(
            template_frame,
            width=550,
            height=180,
            bg='#1e1e1e',
            highlightthickness=2,
            highlightbackground=self.colors['template']
        )
        self.template_canvas.pack(pady=5, padx=10)
        
        # Canvas para demostración gráfica
        grafico_frame = tk.Frame(template_frame, bg=self.colors['panel_bg'])
        grafico_frame.pack(fill=tk.X, padx=10, pady=5)
        
        grafico_label = tk.Label(
            grafico_frame,
            text="🎨 DEMO TEMPLATE METHOD - FLUJO GRÁFICO",
            font=('Arial', 11, 'bold'),
            fg=self.colors['template'],
            bg=self.colors['panel_bg']
        )
        grafico_label.pack(pady=5)
        
        self.grafico_canvas = tk.Canvas(
            grafico_frame,
            width=550,
            height=140,
            bg='#0a0a0a',
            highlightthickness=2,
            highlightbackground=self.colors['template']
        )
        self.grafico_canvas.pack(pady=5)
        
        # Frame de control de procesadores gráficos
        control_grafico_frame = tk.Frame(grafico_frame, bg=self.colors['panel_bg'])
        control_grafico_frame.pack(pady=5)
        
        # Botones de procesadores gráficos
        self.procesador_rojo_btn = tk.Button(
            control_grafico_frame,
            text="🔴 Procesador Rojo",
            command=lambda: self.ejecutar_procesador_grafico("rojo"),
            bg='#FF0000',
            fg='white',
            font=('Arial', 9, 'bold'),
            width=15
        )
        self.procesador_rojo_btn.grid(row=0, column=0, padx=5)
        
        self.procesador_azul_btn = tk.Button(
            control_grafico_frame,
            text="🔵 Procesador Azul",
            command=lambda: self.ejecutar_procesador_grafico("azul"),
            bg='#0000FF',
            fg='white',
            font=('Arial', 9, 'bold'),
            width=15
        )
        self.procesador_azul_btn.grid(row=0, column=1, padx=5)
        
        # Estado del procesador
        self.procesador_estado_label = tk.Label(
            grafico_frame,
            text="Esperando ejecución del Template Method...",
            font=('Arial', 10),
            fg=self.colors['text'],
            bg=self.colors['panel_bg']
        )
        self.procesador_estado_label.pack(pady=3)
        
        # Frame de botones de procesamiento de datos
        template_buttons = tk.Frame(template_frame, bg=self.colors['panel_bg'])
        template_buttons.pack(pady=10)
        
        # Botones para diferentes implementaciones
        self.template_btn1 = tk.Button(
            template_buttons,
            text="Sum Processor",
            command=lambda: self.execute_template("A"),
            bg=self.colors['button'],
            fg=self.colors['text'],
            font=('Arial', 10, 'bold'),
            width=12,
            height=2
        )
        self.template_btn1.grid(row=0, column=0, padx=5, pady=5)
        
        self.template_btn2 = tk.Button(
            template_buttons,
            text="Max Processor",
            command=lambda: self.execute_template("B"),
            bg=self.colors['button'],
            fg=self.colors['text'],
            font=('Arial', 10, 'bold'),
            width=12,
            height=2
        )
        self.template_btn2.grid(row=0, column=1, padx=5, pady=5)
        
        self.template_btn3 = tk.Button(
            template_buttons,
            text="Statistics Processor",
            command=lambda: self.execute_template("C"),
            bg=self.colors['button'],
            fg=self.colors['text'],
            font=('Arial', 10, 'bold'),
            width=12,
            height=2
        )
        self.template_btn3.grid(row=0, column=2, padx=5, pady=5)
        
        # Botón de demostración
        self.demo_template_btn = tk.Button(
            template_frame,
            text="🎬 INICIAR DEMOSTRACIÓN TEMPLATE METHOD",
            command=self.demo_template_pattern,
            bg=self.colors['template'],
            fg=self.colors['text'],
            font=('Arial', 11, 'bold'),
            width=25,
            height=2
        )
        self.demo_template_btn.pack(pady=10)
        
    # ========================================
    # MÉTODOS DE EJECUCIÓN - STRATEGY
    # ========================================
    
    def execute_strategy(self, strategy_type):
        """Ejecuta una estrategia específica del patrón Strategy"""
        strategy = self.strategies[strategy_type]
        self.sort_context.set_strategy(strategy)
        sorted_data = self.sort_context.execute_sort(self.sample_data)
        self.draw_strategy_animation(strategy_type, self.sample_data, sorted_data)
        
    def execute_template(self, template_type):
        """Ejecuta un procesador específico del patrón Template Method"""
        processor = self.processors[template_type]
        result = processor.process_data(self.sample_data)
        self.draw_template_animation(template_type, result)
        
    def demo_strategy_pattern(self):
        """Demostración animada del patrón Strategy"""
        strategies = ["A", "B", "C"]
        for strategy in strategies:
            self.execute_strategy(strategy)
            self.root.update()
            time.sleep(2)
            
    def demo_template_pattern(self):
        """Demostración animada del patrón Template Method"""
        templates = ["A", "B", "C"]
        for template in templates:
            self.execute_template(template)
            self.root.update()
            time.sleep(2)
    
    # ========================================
    # MÉTODOS DE ANIMACIÓN - STRATEGY
    # ========================================
    
    def on_canvas_click(self, event):
        """Maneja clics en el canvas de movimiento"""
        self.objeto_movible.mover_a(event.x, event.y)
        if not self.animacion_activa:
            self.animacion_activa = True
            self.actualizar_animacion()
    
    def cambiar_estrategia_movimiento(self, estrategia_nombre):
        """Cambia la estrategia de movimiento del objeto"""
        nueva_estrategia = self.movimiento_strategies[estrategia_nombre]
        self.objeto_movible.set_estrategia(nueva_estrategia)
        
        self.estado_label.config(
            text=f"Estrategia actual: {self.objeto_movible.get_estrategia_actual()}"
        )
        
        # Visual feedback
        colores = {"caminar": "#4CAF50", "correr": "#FF9800", "teletransporte": "#9C27B0"}
        self.movimiento_canvas.itemconfig(
            self.objeto_movible.objeto_id, 
            fill=colores[estrategia_nombre]
        )
        
        self.root.after(500, lambda: self.movimiento_canvas.itemconfig(
            self.objeto_movible.objeto_id, 
            fill=self.objeto_movible.color
        ))
    
    def actualizar_animacion(self):
        """Actualiza la animación del objeto movible"""
        if self.animacion_activa:
            self.objeto_movible.actualizar()
            self.root.after(30, self.actualizar_animacion)
    
    def draw_strategy_animation(self, strategy_type, original_data, sorted_data):
        """Dibuja animación para el patrón Strategy con resultados reales"""
        self.strategy_canvas.delete("all")
        
        strategy_names = {"A": "Bubble Sort", "B": "Quick Sort", "C": "Merge Sort"}
        self.strategy_canvas.create_text(
            275, 20,
            text=f"Estrategia: {strategy_names[strategy_type]}",
            fill=self.colors['strategy'],
            font=('Arial', 12, 'bold')
        )
        
        # Datos originales
        self.strategy_canvas.create_text(
            275, 45,
            text="Datos Originales:",
            fill=self.colors['text'],
            font=('Arial', 10, 'bold')
        )
        
        orig_text = str(original_data[:8]) + "..." if len(original_data) > 8 else str(original_data)
        self.strategy_canvas.create_text(
            275, 65,
            text=orig_text,
            fill=self.colors['accent'],
            font=('Arial', 9)
        )
        
        # Contexto
        context_x, context_y = 275, 110
        self.strategy_canvas.create_rectangle(
            context_x - 70, context_y - 20,
            context_x + 70, context_y + 20,
            fill=self.colors['button'],
            outline=self.colors['text'],
            width=2
        )
        self.strategy_canvas.create_text(
            context_x, context_y - 5,
            text="SortContext",
            fill=self.colors['text'],
            font=('Arial', 10, 'bold')
        )
        self.strategy_canvas.create_text(
            context_x, context_y + 8,
            text="set_strategy()",
            fill=self.colors['text'],
            font=('Arial', 8)
        )
        
        # Estrategia actual
        strategy_colors = {"A": "#4CAF50", "B": "#FF9800", "C": "#9C27B0"}
        color = strategy_colors.get(strategy_type, "#4CAF50")
        
        self.strategy_canvas.create_rectangle(
            context_x - 70, context_y + 35,
            context_x + 70, context_y + 65,
            fill=color,
            outline=self.colors['text'],
            width=2
        )
        self.strategy_canvas.create_text(
            context_x, context_y + 50,
            text=strategy_names[strategy_type],
            fill=self.colors['text'],
            font=('Arial', 9, 'bold')
        )
        
        # Flecha de conexión
        self.strategy_canvas.create_line(
            context_x, context_y + 20,
            context_x, context_y + 35,
            fill=self.colors['text'],
            width=2,
            arrow=tk.LAST
        )
        
        # Resultados
        self.strategy_canvas.create_text(
            275, 165,
            text="Datos Ordenados:",
            fill=self.colors['text'],
            font=('Arial', 10, 'bold')
        )
        
        sorted_text = str(sorted_data[:8]) + "..." if len(sorted_data) > 8 else str(sorted_data)
        self.strategy_canvas.create_text(
            275, 185,
            text=sorted_text,
            fill=self.colors['strategy'],
            font=('Arial', 9)
        )
    
    # ========================================
    # MÉTODOS DE EJECUCIÓN - TEMPLATE METHOD
    # ========================================
    
    def ejecutar_procesador_grafico(self, tipo):
        """Ejecuta un procesador gráfico usando el Template Method"""
        self.procesador_estado_label.config(
            text=f"Ejecutando Template Method con Procesador {tipo.capitalize()}..."
        )
        
        if tipo == "rojo":
            procesador = ProcesadorGraficoRojo(self.grafico_canvas, self.root)
        elif tipo == "azul":
            procesador = ProcesadorGraficoAzul(self.grafico_canvas, self.root)
        else:
            return
        
        procesador.ejecutar_proceso()
        
        self.root.after(3000, lambda: self.procesador_estado_label.config(
            text="✓ Template Method completado. Estructura fija con paso variable implementado."
        ))
    
    def draw_template_animation(self, template_type, result):
        """Dibuja animación para el patrón Template Method con resultados reales"""
        self.template_canvas.delete("all")
        
        processor_names = {"A": "SumProcessor", "B": "MaxProcessor", "C": "StatisticsProcessor"}
        self.template_canvas.create_text(
            275, 20,
            text=f"Template: {processor_names[template_type]}",
            fill=self.colors['template'],
            font=('Arial', 12, 'bold')
        )
        
        # Datos originales
        self.template_canvas.create_text(
            275, 45,
            text="Datos de entrada:",
            fill=self.colors['text'],
            font=('Arial', 10, 'bold')
        )
        
        data_text = str(result['original'][:6]) + "..." if len(result['original']) > 6 else str(result['original'])
        self.template_canvas.create_text(
            275, 65,
            text=data_text,
            fill=self.colors['accent'],
            font=('Arial', 9)
        )
        
        # Estructura del Template Method
        steps_info = [
            ("validate_data()", result['validated'], "Fijo"),
            ("process_core()", result['processed'], "Variable"),
            ("format_result()", result['formatted'], "Fijo"),
            ("generate_summary()", result['summary'], "Variable")
        ]
        
        y_positions = [90, 115, 140, 165]
        
        for i, (step_info, y_pos) in enumerate(zip(steps_info, y_positions)):
            step_name, step_result, step_type = step_info
            if step_type == "Fijo":
                color = self.colors['template']
            else:
                color = self.colors['accent']
                
            # Rectángulo del paso
            self.template_canvas.create_rectangle(
                80, y_pos - 10,
                470, y_pos + 10,
                fill=color,
                outline=self.colors['text'],
                width=2
            )
            
            # Nombre del paso
            self.template_canvas.create_text(
                120, y_pos,
                text=step_name,
                fill=self.colors['text'],
                font=('Arial', 9, 'bold'),
                anchor='w'
            )
            
            # Resultado del paso
            result_text = str(step_result)
            if len(result_text) > 35:
                result_text = result_text[:32] + "..."
            self.template_canvas.create_text(
                275, y_pos,
                text=result_text,
                fill=self.colors['text'],
                font=('Arial', 8)
            )
            
            # Flechas entre pasos
            if i < len(steps_info) - 1:
                self.template_canvas.create_line(
                    275, y_pos + 10,
                    275, y_positions[i+1] - 10,
                    fill=self.colors['text'],
                    width=2,
                    arrow=tk.LAST
                )

# ========================================
# FUNCIÓN PRINCIPAL
# ========================================

def main():
    """
    FUNCIÓN DE ENTRADA PRINCIPAL
    ============================
    
    Crea y ejecuta la aplicación de demostración.
    """
    root = tk.Tk()
    app = PatternDemoApp(root)
    root.mainloop()

# ========================================
# EJECUCIÓN DEL PROGRAMA
# ========================================

if __name__ == "__main__":
    """
    PUNTO DE ENTRADA CUANDO SE EJECUTA EL SCRIPT
    =============================================
    
    Permite ejecutar el programa directamente con:
    python demo_patrones_final.py
    """
    main()
