import tkinter as tk
from tkinter import ttk
import math
import time
from abc import ABC, abstractmethod

# ========================================
# IMPLEMENTACIÓN PATRÓN STRATEGY
# ========================================

class SortStrategy(ABC):
    """Interfaz Strategy para algoritmos de ordenamiento"""
    @abstractmethod
    def sort(self, data):
        pass
    
    @abstractmethod
    def get_name(self):
        pass

# ========================================
# PATRÓN STRATEGY PARA MOVIMIENTO
# ========================================

class MovimientoStrategy(ABC):
    """Interfaz Strategy para movimiento de objetos"""
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
    """Estrategia de movimiento: Caminar (lento)"""
    def __init__(self):
        self.velocidad = 2
        
    def mover(self, x, y, canvas, objeto_id):
        """Movimiento lento y constante"""
        coords = canvas.coords(objeto_id)
        if coords:
            current_x = (coords[0] + coords[2]) / 2
            current_y = (coords[1] + coords[3]) / 2
            
            # Calcular dirección
            dx = x - current_x
            dy = y - current_y
            distancia = (dx**2 + dy**2)**0.5
            
            if distancia > self.velocidad:
                # Normalizar y aplicar velocidad
                dx = (dx / distancia) * self.velocidad
                dy = (dy / distancia) * self.velocidad
                canvas.move(objeto_id, dx, dy)
                return False  # No ha llegado al destino
            else:
                # Mover exactamente al destino
                canvas.coords(objeto_id, 
                            x - 15, y - 15, 
                            x + 15, y + 15)
                return True  # Ha llegado al destino
        return True
    
    def get_nombre(self):
        return "Caminar"
    
    def get_velocidad(self):
        return self.velocidad

class CorrerStrategy(MovimientoStrategy):
    """Estrategia de movimiento: Correr (rápido)"""
    def __init__(self):
        self.velocidad = 8
        
    def mover(self, x, y, canvas, objeto_id):
        """Movimiento rápido"""
        coords = canvas.coords(objeto_id)
        if coords:
            current_x = (coords[0] + coords[2]) / 2
            current_y = (coords[1] + coords[3]) / 2
            
            # Calcular dirección
            dx = x - current_x
            dy = y - current_y
            distancia = (dx**2 + dy**2)**0.5
            
            if distancia > self.velocidad:
                # Normalizar y aplicar velocidad
                dx = (dx / distancia) * self.velocidad
                dy = (dy / distancia) * self.velocidad
                canvas.move(objeto_id, dx, dy)
                return False  # No ha llegado al destino
            else:
                # Mover exactamente al destino
                canvas.coords(objeto_id, 
                            x - 15, y - 15, 
                            x + 15, y + 15)
                return True  # Ha llegado al destino
        return True
    
    def get_nombre(self):
        return "Correr"
    
    def get_velocidad(self):
        return self.velocidad

class TeletransporteStrategy(MovimientoStrategy):
    """Estrategia de movimiento: Teletransporte (instantáneo)"""
    def __init__(self):
        self.velocidad = float('inf')
        
    def mover(self, x, y, canvas, objeto_id):
        """Teletransporte instantáneo al destino"""
        canvas.coords(objeto_id, 
                    x - 15, y - 15, 
                    x + 15, y + 15)
        return True  # Siempre llega al destino instantáneamente
    
    def get_nombre(self):
        return "Teletransporte"
    
    def get_velocidad(self):
        return self.velocidad

class ObjetoMovible:
    """Objeto que utiliza estrategias de movimiento"""
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

class BubbleSortStrategy(SortStrategy):
    """Estrategia concreta: Bubble Sort"""
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
    """Estrategia concreta: Quick Sort"""
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
    """Estrategia concreta: Merge Sort"""
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
    """Contexto que utiliza una estrategia de ordenamiento"""
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def execute_sort(self, data):
        return self._strategy.sort(data)
    
    def get_strategy_name(self):
        return self._strategy.get_name()

# ========================================
# IMPLEMENTACIÓN PATRÓN TEMPLATE METHOD
# ========================================

class DataProcessor(ABC):
    """Clase abstracta con Template Method"""
    
    def process_data(self, data):
        """Template Method - define la estructura del algoritmo"""
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
    """Implementación concreta - procesador de suma"""
    def process_core(self, data):
        return sum(data)
    
    def generate_summary(self, data):
        return f"Sum: {sum(data)}, Average: {sum(data)/len(data):.2f}"

class MaxProcessor(DataProcessor):
    """Implementación concreta - procesador de máximo"""
    def process_core(self, data):
        return max(data)
    
    def generate_summary(self, data):
        return f"Max: {max(data)}, Min: {min(data)}"

class StatisticsProcessor(DataProcessor):
    """Implementación concreta - procesador estadístico"""
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

class PatternDemoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Demostración Visual: Strategy vs Template Method")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2b2b2b')
        
        # Colores personalizados
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
        """Inicializar las implementaciones de los patrones"""
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
        
        # Procesadores para Template Method
        self.processors = {
            "A": SumProcessor(),
            "B": MaxProcessor(),
            "C": StatisticsProcessor()
        }
        
        # Datos de ejemplo
        self.sample_data = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50]
        
        # Control de animación
        self.animacion_activa = False
        
    def setup_ui(self):
        # Título principal
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = tk.Label(
            title_frame, 
            text="Patrones de Diseño: Strategy vs Template Method",
            font=('Arial', 18, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        title_label.pack()
        
        # Contenedor principal con dos secciones
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Sección Strategy (izquierda)
        self.setup_strategy_section(main_container)
        
        # Sección Template Method (derecha)
        self.setup_template_section(main_container)
        
    def setup_strategy_section(self, parent):
        # Frame para Strategy
        strategy_frame = tk.Frame(parent, bg=self.colors['panel_bg'], relief=tk.RAISED, bd=2)
        strategy_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Título Strategy
        strategy_title = tk.Label(
            strategy_frame,
            text="PATRÓN STRATEGY",
            font=('Arial', 14, 'bold'),
            fg=self.colors['strategy'],
            bg=self.colors['panel_bg']
        )
        strategy_title.pack(pady=10)
        
        # Descripción
        desc_text = "El algoritmo puede cambiar en tiempo de ejecución.\nSe encapsulan diferentes estrategias intercambiables."
        strategy_desc = tk.Label(
            strategy_frame,
            text=desc_text,
            font=('Arial', 10),
            fg=self.colors['text'],
            bg=self.colors['panel_bg'],
            justify=tk.CENTER
        )
        strategy_desc.pack(pady=5)
        
        # Canvas para animación Strategy (ordenamiento)
        self.strategy_canvas = tk.Canvas(
            strategy_frame,
            width=550,
            height=200,
            bg='#1e1e1e',
            highlightthickness=2,
            highlightbackground=self.colors['strategy']
        )
        self.strategy_canvas.pack(pady=5, padx=10)
        
        # Canvas para demostración de movimiento Strategy
        movimiento_frame = tk.Frame(strategy_frame, bg=self.colors['panel_bg'])
        movimiento_frame.pack(fill=tk.X, padx=10, pady=5)
        
        movimiento_label = tk.Label(
            movimiento_frame,
            text="DEMO STRATEGY - MOVIMIENTO DINÁMICO",
            font=('Arial', 11, 'bold'),
            fg=self.colors['strategy'],
            bg=self.colors['panel_bg']
        )
        movimiento_label.pack(pady=5)
        
        self.movimiento_canvas = tk.Canvas(
            movimiento_frame,
            width=550,
            height=150,
            bg='#0a0a0a',
            highlightthickness=2,
            highlightbackground=self.colors['accent']
        )
        self.movimiento_canvas.pack(pady=5)
        
        # Crear objeto movible para demostración
        self.objeto_movible = ObjetoMovible(self.movimiento_canvas, 50, 75, '#FF6B6B')
        
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
        
        # Frame de botones Strategy
        strategy_buttons = tk.Frame(strategy_frame, bg=self.colors['panel_bg'])
        strategy_buttons.pack(pady=10)
        
        # Botones para diferentes estrategias
        self.strategy_btn1 = tk.Button(
            strategy_buttons,
            text="Estrategia A",
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
            text="Estrategia B",
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
            text="Estrategia C",
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
            text="INICIAR DEMOSTRACIÓN",
            command=self.demo_strategy_pattern,
            bg=self.colors['strategy'],
            fg=self.colors['text'],
            font=('Arial', 11, 'bold'),
            width=20,
            height=2
        )
        self.demo_strategy_btn.pack(pady=10)
        
    def setup_template_section(self, parent):
        # Frame para Template Method
        template_frame = tk.Frame(parent, bg=self.colors['panel_bg'], relief=tk.RAISED, bd=2)
        template_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Título Template Method
        template_title = tk.Label(
            template_frame,
            text="PATRÓN TEMPLATE METHOD",
            font=('Arial', 14, 'bold'),
            fg=self.colors['template'],
            bg=self.colors['panel_bg']
        )
        template_title.pack(pady=10)
        
        # Descripción
        desc_text = "La estructura del algoritmo es fija.\nLas subclases implementan pasos específicos."
        template_desc = tk.Label(
            template_frame,
            text=desc_text,
            font=('Arial', 10),
            fg=self.colors['text'],
            bg=self.colors['panel_bg'],
            justify=tk.CENTER
        )
        template_desc.pack(pady=5)
        
        # Canvas para animación Template Method
        self.template_canvas = tk.Canvas(
            template_frame,
            width=550,
            height=300,
            bg='#1e1e1e',
            highlightthickness=2,
            highlightbackground=self.colors['template']
        )
        self.template_canvas.pack(pady=10, padx=10)
        
        # Frame de botones Template Method
        template_buttons = tk.Frame(template_frame, bg=self.colors['panel_bg'])
        template_buttons.pack(pady=10)
        
        # Botones para diferentes implementaciones
        self.template_btn1 = tk.Button(
            template_buttons,
            text="Implementación A",
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
            text="Implementación B",
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
            text="Implementación C",
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
            text="INICIAR DEMOSTRACIÓN",
            command=self.demo_template_pattern,
            bg=self.colors['template'],
            fg=self.colors['text'],
            font=('Arial', 11, 'bold'),
            width=20,
            height=2
        )
        self.demo_template_btn.pack(pady=10)
        
    def execute_strategy(self, strategy_type):
        """Ejecuta una estrategia específica del patrón Strategy"""
        # Cambiar la estrategia en tiempo de ejecución
        strategy = self.strategies[strategy_type]
        self.sort_context.set_strategy(strategy)
        
        # Ejecutar el ordenamiento
        sorted_data = self.sort_context.execute_sort(self.sample_data)
        
        # Mostrar animación con resultados
        self.draw_strategy_animation(strategy_type, self.sample_data, sorted_data)
        
    def execute_template(self, template_type):
        """Ejecuta un procesador específico del patrón Template Method"""
        # Usar el procesador específico
        processor = self.processors[template_type]
        
        # Ejecutar el template method
        result = processor.process_data(self.sample_data)
        
        # Mostrar animación con resultados
        self.draw_template_animation(template_type, result)
        
    def demo_strategy_pattern(self):
        """Demostración animada del patrón Strategy"""
        self.animate_strategy_demo()
        
    def demo_template_pattern(self):
        """Demostración animada del patrón Template Method"""
        self.animate_template_demo()
        
    def draw_strategy_animation(self, strategy_type, original_data, sorted_data):
        """Dibuja animación para el patrón Strategy con resultados reales"""
        self.strategy_canvas.delete("all")
        
        # Título
        strategy_names = {"A": "Bubble Sort", "B": "Quick Sort", "C": "Merge Sort"}
        self.strategy_canvas.create_text(
            275, 20,
            text=f"Estrategia: {strategy_names[strategy_type]}",
            fill=self.colors['strategy'],
            font=('Arial', 12, 'bold')
        )
        
        # Datos originales
        self.strategy_canvas.create_text(
            275, 50,
            text="Datos Originales:",
            fill=self.colors['text'],
            font=('Arial', 10, 'bold')
        )
        
        orig_text = str(original_data[:8]) + "..." if len(original_data) > 8 else str(original_data)
        self.strategy_canvas.create_text(
            275, 70,
            text=orig_text,
            fill=self.colors['accent'],
            font=('Arial', 9)
        )
        
        # Contexto
        context_x, context_y = 275, 120
        self.strategy_canvas.create_rectangle(
            context_x - 70, context_y - 25,
            context_x + 70, context_y + 25,
            fill=self.colors['button'],
            outline=self.colors['text'],
            width=2
        )
        self.strategy_canvas.create_text(
            context_x, context_y - 8,
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
            context_x - 70, context_y + 45,
            context_x + 70, context_y + 85,
            fill=color,
            outline=self.colors['text'],
            width=2
        )
        self.strategy_canvas.create_text(
            context_x, context_y + 65,
            text=strategy_names[strategy_type],
            fill=self.colors['text'],
            font=('Arial', 9, 'bold')
        )
        
        # Flecha de conexión
        self.strategy_canvas.create_line(
            context_x, context_y + 25,
            context_x, context_y + 45,
            fill=self.colors['text'],
            width=2,
            arrow=tk.LAST
        )
        
        # Resultados
        self.strategy_canvas.create_text(
            275, 230,
            text="Datos Ordenados:",
            fill=self.colors['text'],
            font=('Arial', 10, 'bold')
        )
        
        sorted_text = str(sorted_data[:8]) + "..." if len(sorted_data) > 8 else str(sorted_data)
        self.strategy_canvas.create_text(
            275, 250,
            text=sorted_text,
            fill=self.colors['strategy'],
            font=('Arial', 9)
        )
        
        # Indicador de tiempo de ejecución
        self.strategy_canvas.create_text(
            275, 280,
            text="✓ Estrategia intercambiable en runtime",
            fill=self.colors['strategy'],
            font=('Arial', 9, 'italic')
        )
        
    def draw_template_animation(self, template_type, result):
        """Dibuja animación para el patrón Template Method con resultados reales"""
        self.template_canvas.delete("all")
        
        # Título
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
        
        y_positions = [100, 140, 180, 220]
        
        for i, (step_info, y_pos) in enumerate(zip(steps_info, y_positions)):
            step_name, step_result, step_type = step_info
            if step_type == "Fijo":
                color = self.colors['template']
            else:
                color = self.colors['accent']
                
            # Rectángulo del paso
            self.template_canvas.create_rectangle(
                80, y_pos - 12,
                470, y_pos + 12,
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
            if len(result_text) > 40:
                result_text = result_text[:37] + "..."
            self.template_canvas.create_text(
                275, y_pos,
                text=result_text,
                fill=self.colors['text'],
                font=('Arial', 8)
            )
            
            # Flechas entre pasos
            if i < len(steps_info) - 1:
                self.template_canvas.create_line(
                    275, y_pos + 12,
                    275, y_positions[i+1] - 12,
                    fill=self.colors['text'],
                    width=2,
                    arrow=tk.LAST
                )
        
        # Clase concreta que implementa los pasos variables
        self.template_canvas.create_rectangle(
            150, 245,
            400, 275,
            fill=self.colors['button'],
            outline=self.colors['text'],
            width=2
        )
        self.template_canvas.create_text(
            275, 260,
            text=processor_names[template_type],
            fill=self.colors['text'],
            font=('Arial', 9, 'bold')
        )
        
        # Indicador de estructura fija
        self.template_canvas.create_text(
            275, 290,
            text="✓ Estructura del algoritmo fija, pasos variables implementados",
            fill=self.colors['template'],
            font=('Arial', 9, 'italic')
        )
        
    def animate_strategy_demo(self):
        """Animación de demostración del patrón Strategy"""
        strategies = ["A", "B", "C"]
        for strategy in strategies:
            self.execute_strategy(strategy)
            self.root.update()
            time.sleep(2)
            
    def animate_template_demo(self):
        """Animación de demostración del patrón Template Method"""
        templates = ["A", "B", "C"]
        for template in templates:
            self.execute_template(template)
            self.root.update()
            time.sleep(2)
    
    def on_canvas_click(self, event):
        """Maneja clics en el canvas de movimiento"""
        # Mover el objeto a la posición del clic
        self.objeto_movible.mover_a(event.x, event.y)
        
        # Iniciar animación si no está activa
        if not self.animacion_activa:
            self.animacion_activa = True
            self.actualizar_animacion()
    
    def cambiar_estrategia_movimiento(self, estrategia_nombre):
        """Cambia la estrategia de movimiento del objeto"""
        nueva_estrategia = self.movimiento_strategies[estrategia_nombre]
        self.objeto_movible.set_estrategia(nueva_estrategia)
        
        # Actualizar etiqueta de estado
        self.estado_label.config(
            text=f"Estrategia actual: {self.objeto_movible.get_estrategia_actual()}"
        )
        
        # Visual feedback - cambiar color del objeto temporalmente
        colores = {"caminar": "#4CAF50", "correr": "#FF9800", "teletransporte": "#9C27B0"}
        self.movimiento_canvas.itemconfig(
            self.objeto_movible.objeto_id, 
            fill=colores[estrategia_nombre]
        )
        
        # Restaurar color original después de 500ms
        self.root.after(500, lambda: self.movimiento_canvas.itemconfig(
            self.objeto_movible.objeto_id, 
            fill=self.objeto_movible.color
        ))
    
    def actualizar_animacion(self):
        """Actualiza la animación del objeto movible"""
        if self.animacion_activa:
            # Actualizar posición del objeto
            self.objeto_movible.actualizar()
            
            # Continuar animación
            self.root.after(30, self.actualizar_animacion)  # ~33 FPS

def main():
    root = tk.Tk()
    app = PatternDemoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
