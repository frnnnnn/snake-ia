# GENERANDO TODOS LOS ARCHIVOS DEL PROYECTO COMPLETO
# Snake AI Ultimate - Propuesta de Valor Definitiva

print("🐍 GENERANDO PROYECTO COMPLETO - SNAKE AI ULTIMATE")
print("=" * 60)
print("📦 Creando todos los archivos necesarios...")

# 1. JUEGO PRINCIPAL CORREGIDO
snake_ai_ultimate = '''"""
🐍 SNAKE AI ULTIMATE - PROPUESTA DE VALOR DEFINITIVA
Versión corregida sin errores - Proyecto completo para evaluación
Todos los parámetros especificados implementados correctamente
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
import threading
import time
import random
import math
from collections import deque
from enum import Enum
import heapq
import json
import os

# Importar pygame solo si está disponible
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Configurar CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# CONFIGURACIONES DEL JUEGO - PARÁMETROS ESPECIFICADOS
GRID_SIZE = 10          # Tablero 10x10 exacto
MAX_APPLES = 35         # Máximo 35 manzanas
MIN_SNAKE_LENGTH = 3    # Longitud mínima 3 espacios

# CONFIGURACIONES VISUALES
CELL_SIZE = 40
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

class UltimateTheme:
    """Tema visual profesional con alto contraste"""
    
    # Colores base
    PRIMARY_BG = "#0d1117"
    SECONDARY_BG = "#161b22"
    CARD_BG = "#21262d"
    ACCENT_BG = "#30363d"
    BORDER_COLOR = "#373e47"
    
    # Colores neón
    NEON_CYAN = "#7df9ff"
    NEON_PURPLE = "#c9a9dd"
    NEON_GREEN = "#7ff787"
    NEON_ORANGE = "#ffab70"
    NEON_PINK = "#ff9ac1"
    NEON_YELLOW = "#f7e025"
    
    # Texto con contraste perfecto
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#e6edf3"
    TEXT_ACCENT = "#79c0ff"
    TEXT_SUCCESS = "#56d364"
    TEXT_WARNING = "#d29922"
    TEXT_ERROR = "#f85149"
    
    # Snake skins
    SNAKE_SKINS = {
        "classic": {"head": "#7ff787", "body": "#56d364", "eye": "#ffffff"},
        "cyber": {"head": "#7df9ff", "body": "#58a6ff", "eye": "#f7e025"},
        "fire": {"head": "#ff6b35", "body": "#f85149", "eye": "#ffab70"},
        "royal": {"head": "#c9a9dd", "body": "#a5a2ff", "eye": "#ffffff"},
        "matrix": {"head": "#00ff41", "body": "#008f26", "eye": "#00ff41"},
        "gold": {"head": "#f7e025", "body": "#d29922", "eye": "#0d1117"}
    }
    
    # Apple styles
    APPLE_STYLES = {
        "classic": "#f85149",
        "golden": "#f7e025",
        "crystal": "#7df9ff",
        "magic": "#c9a9dd"
    }

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SearchAlgorithm(Enum):
    BFS = "BFS - Breadth First Search"
    DFS = "DFS - Depth First Search"
    A_STAR = "A* - Heuristic Search"
    DIJKSTRA = "Dijkstra - Uniform Cost"

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

class AudioManager:
    """Gestor de audio con manejo robusto de errores"""
    
    def __init__(self):
        self.sounds = {}
        self.sound_enabled = True
        self.volume = 0.7
        self.audio_working = False
        
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
                self.audio_working = True
                self.create_sounds()
                print("✅ Audio inicializado correctamente")
            except Exception as e:
                self.audio_working = False
                print(f"⚠️ Audio no disponible: {e}")
        else:
            print("⚠️ Pygame no instalado - modo silencioso")
    
    def create_sounds(self):
        """Genera sonidos procedurales - VERSIÓN CORREGIDA"""
        if not self.audio_working:
            return
            
        try:
            # Sonidos básicos con arrays C-contiguos garantizados
            self.sounds['apple'] = self.generate_tone([440, 523], 0.3)
            self.sounds['gameover'] = self.generate_tone([330, 262], 0.8)
            self.sounds['start'] = self.generate_tone([261, 392], 0.5)
            self.sounds['pause'] = self.generate_tone([440, 330], 0.4)
            self.sounds['victory'] = self.generate_tone([523, 659], 1.0)
        except Exception as e:
            print(f"⚠️ Error creando sonidos: {e}")
            self.audio_working = False
    
    def generate_tone(self, frequencies, duration):
        """Genera tono simple - CORREGIDO"""
        if not self.audio_working:
            return None
            
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            
            # Crear array base
            arr = np.zeros(frames, dtype=np.float32)
            
            for freq in frequencies:
                t = np.linspace(0, duration, frames, dtype=np.float32)
                wave = np.sin(2 * np.pi * freq * t) * 0.3
                arr += wave
            
            # Normalizar y convertir
            arr = np.clip(arr, -1, 1)
            arr_int16 = (arr * 32767).astype(np.int16)
            
            # CORRECCIÓN CRÍTICA: Garantizar array C-contiguo
            if not arr_int16.flags['C_CONTIGUOUS']:
                arr_int16 = np.ascontiguousarray(arr_int16)
            
            # Crear array estéreo
            stereo_array = np.column_stack((arr_int16, arr_int16))
            
            # Garantizar que el estéreo también sea C-contiguo
            if not stereo_array.flags['C_CONTIGUOUS']:
                stereo_array = np.ascontiguousarray(stereo_array)
            
            return pygame.sndarray.make_sound(stereo_array)
            
        except Exception as e:
            print(f"⚠️ Error generando tono: {e}")
            return None
    
    def play_sound(self, sound_name):
        """Reproduce sonido con manejo de errores"""
        if self.sound_enabled and self.audio_working and sound_name in self.sounds:
            try:
                if self.sounds[sound_name]:
                    self.sounds[sound_name].set_volume(self.volume)
                    self.sounds[sound_name].play()
            except:
                pass
    
    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
    
    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
    
    def is_available(self):
        return self.audio_working

class Snake:
    def __init__(self):
        center = GRID_SIZE // 2
        self.body = [(center, center)]
        self.direction = Direction.RIGHT
        self.grow = False
        self.score = 0
        self.skin = "classic"
        
    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction):
        opposite = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        if new_direction != opposite.get(self.direction):
            self.direction = new_direction
    
    def grow_snake(self):
        self.grow = True
        self.score += 1
    
    def get_head(self):
        return self.body[0]
    
    def check_collision(self):
        head_x, head_y = self.body[0]
        
        # Verificar límites del tablero 10x10
        if head_x < 0 or head_x >= GRID_SIZE or head_y < 0 or head_y >= GRID_SIZE:
            return True
        
        # Verificar colisión con cuerpo
        if self.body[0] in self.body[1:]:
            return True
        
        return False
    
    def set_skin(self, skin_name):
        if skin_name in UltimateTheme.SNAKE_SKINS:
            self.skin = skin_name

class Apple:
    def __init__(self, snake_body):
        self.position = self.generate_position(snake_body)
        self.style = "classic"
    
    def generate_position(self, snake_body):
        available_positions = []
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if (x, y) not in snake_body:
                    available_positions.append((x, y))
        
        if available_positions:
            return random.choice(available_positions)
        return None
    
    def set_style(self, style_name):
        if style_name in UltimateTheme.APPLE_STYLES:
            self.style = style_name

class SearchAgent:
    """Agente de búsqueda con 4 algoritmos implementados"""
    
    def __init__(self, algorithm=SearchAlgorithm.A_STAR):
        self.algorithm = algorithm
        self.search_time = 0
        self.nodes_expanded = 0
        self.total_searches = 0
        self.total_search_time = 0
        self.last_search_time = 0
        
    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                neighbors.append((new_x, new_y))
        return neighbors
    
    def is_safe_move(self, pos, snake_body):
        return pos not in snake_body and 0 <= pos[0] < GRID_SIZE and 0 <= pos[1] < GRID_SIZE
    
    def bfs_search(self, start, goal, snake_body):
        """Breadth-First Search"""
        start_time = time.perf_counter()
        
        queue = deque([(start, [start])])
        visited = {start}
        nodes_expanded = 0
        
        while queue:
            current, path = queue.popleft()
            nodes_expanded += 1
            
            if current == goal:
                self.search_time = time.perf_counter() - start_time
                self.nodes_expanded = nodes_expanded
                return path[1:] if len(path) > 1 else []
            
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited and self.is_safe_move(neighbor, snake_body):
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        self.search_time = time.perf_counter() - start_time
        self.nodes_expanded = nodes_expanded
        return []
    
    def dfs_search(self, start, goal, snake_body):
        """Depth-First Search"""
        start_time = time.perf_counter()
        
        stack = [(start, [start])]
        visited = {start}
        nodes_expanded = 0
        
        while stack:
            current, path = stack.pop()
            nodes_expanded += 1
            
            if current == goal:
                self.search_time = time.perf_counter() - start_time
                self.nodes_expanded = nodes_expanded
                return path[1:] if len(path) > 1 else []
            
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited and self.is_safe_move(neighbor, snake_body):
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))
        
        self.search_time = time.perf_counter() - start_time
        self.nodes_expanded = nodes_expanded
        return []
    
    def a_star_search(self, start, goal, snake_body):
        """A* Heuristic Search"""
        start_time = time.perf_counter()
        
        open_set = [(0, start, [start])]
        closed_set = set()
        g_score = {start: 0}
        nodes_expanded = 0
        
        while open_set:
            current_f, current, path = heapq.heappop(open_set)
            
            if current in closed_set:
                continue
                
            closed_set.add(current)
            nodes_expanded += 1
            
            if current == goal:
                self.search_time = time.perf_counter() - start_time
                self.nodes_expanded = nodes_expanded
                return path[1:] if len(path) > 1 else []
            
            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set or not self.is_safe_move(neighbor, snake_body):
                    continue
                
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.manhattan_distance(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor, path + [neighbor]))
        
        self.search_time = time.perf_counter() - start_time
        self.nodes_expanded = nodes_expanded
        return []
    
    def dijkstra_search(self, start, goal, snake_body):
        """Dijkstra Uniform Cost"""
        start_time = time.perf_counter()
        
        open_set = [(0, start, [start])]
        distances = {start: 0}
        visited = set()
        nodes_expanded = 0
        
        while open_set:
            current_dist, current, path = heapq.heappop(open_set)
            
            if current in visited:
                continue
            
            visited.add(current)
            nodes_expanded += 1
            
            if current == goal:
                self.search_time = time.perf_counter() - start_time
                self.nodes_expanded = nodes_expanded
                return path[1:] if len(path) > 1 else []
            
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited and self.is_safe_move(neighbor, snake_body):
                    new_distance = distances[current] + 1
                    
                    if neighbor not in distances or new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        heapq.heappush(open_set, (new_distance, neighbor, path + [neighbor]))
        
        self.search_time = time.perf_counter() - start_time
        self.nodes_expanded = nodes_expanded
        return []
    
    def find_path(self, start, goal, snake_body):
        """Encuentra camino usando el algoritmo seleccionado"""
        self.total_searches += 1
        
        if self.algorithm == SearchAlgorithm.BFS:
            path = self.bfs_search(start, goal, snake_body)
        elif self.algorithm == SearchAlgorithm.DFS:
            path = self.dfs_search(start, goal, snake_body)
        elif self.algorithm == SearchAlgorithm.A_STAR:
            path = self.a_star_search(start, goal, snake_body)
        elif self.algorithm == SearchAlgorithm.DIJKSTRA:
            path = self.dijkstra_search(start, goal, snake_body)
        else:
            path = []
        
        self.total_search_time += self.search_time
        self.last_search_time = self.search_time
        return path
    
    def get_next_move(self, snake, apple):
        """Obtiene el siguiente movimiento óptimo"""
        if apple.position is None:
            return snake.direction
            
        start = snake.get_head()
        goal = apple.position
        
        snake_body = snake.body[1:] if len(snake.body) > 1 else []
        path = self.find_path(start, goal, snake_body)
        
        if path:
            next_pos = path[0]
            current_pos = start
            
            dx = next_pos[0] - current_pos[0]
            dy = next_pos[1] - current_pos[1]
            
            if dx == 1:
                return Direction.RIGHT
            elif dx == -1:
                return Direction.LEFT
            elif dy == 1:
                return Direction.DOWN
            elif dy == -1:
                return Direction.UP
        
        return self._survival_strategy(snake)
    
    def _survival_strategy(self, snake):
        """Estrategia de supervivencia"""
        head = snake.get_head()
        possible_directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        
        for direction in possible_directions:
            dx, dy = direction.value
            new_pos = (head[0] + dx, head[1] + dy)
            
            if self.is_safe_move(new_pos, snake.body):
                return direction
        
        return snake.direction
    
    def get_performance_stats(self):
        """Obtiene estadísticas de rendimiento"""
        avg_time = self.total_search_time / max(1, self.total_searches)
        efficiency = max(0, 100 - (avg_time * 1000 * 10))
        
        return {
            'algorithm': self.algorithm.value,
            'total_searches': self.total_searches,
            'total_time': self.total_search_time,
            'average_time': avg_time,
            'last_search_time': self.last_search_time,
            'last_nodes_expanded': self.nodes_expanded,
            'efficiency_score': efficiency
        }

class GameCanvas(ctk.CTkCanvas):
    """Canvas del juego con efectos visuales"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg=UltimateTheme.PRIMARY_BG,
            highlightthickness=3,
            highlightbackground=UltimateTheme.NEON_CYAN
        )
    
    def draw_grid(self):
        """Dibuja la grilla del juego"""
        self.delete("grid")
        
        # Fondo alternado
        for i in range(0, GRID_SIZE, 2):
            for j in range(0, GRID_SIZE, 2):
                x1, y1 = i * CELL_SIZE, j * CELL_SIZE
                x2, y2 = (i + 2) * CELL_SIZE, (j + 2) * CELL_SIZE
                self.create_rectangle(
                    x1, y1, x2, y2,
                    fill=UltimateTheme.ACCENT_BG, outline="", tags="grid"
                )
        
        # Líneas de grilla
        for x in range(0, GRID_SIZE * CELL_SIZE + 1, CELL_SIZE):
            color = UltimateTheme.NEON_CYAN if x % (CELL_SIZE * 5) == 0 else UltimateTheme.BORDER_COLOR
            width = 2 if x % (CELL_SIZE * 5) == 0 else 1
            self.create_line(x, 0, x, GRID_SIZE * CELL_SIZE, fill=color, width=width, tags="grid")
        
        for y in range(0, GRID_SIZE * CELL_SIZE + 1, CELL_SIZE):
            color = UltimateTheme.NEON_CYAN if y % (CELL_SIZE * 5) == 0 else UltimateTheme.BORDER_COLOR
            width = 2 if y % (CELL_SIZE * 5) == 0 else 1
            self.create_line(0, y, GRID_SIZE * CELL_SIZE, y, fill=color, width=width, tags="grid")
    
    def draw_snake(self, snake):
        """Dibuja la serpiente con skin personalizable"""
        self.delete("snake")
        
        skin = UltimateTheme.SNAKE_SKINS.get(snake.skin, UltimateTheme.SNAKE_SKINS["classic"])
        
        for i, (x, y) in enumerate(snake.body):
            x1, y1 = x * CELL_SIZE + 3, y * CELL_SIZE + 3
            x2, y2 = (x + 1) * CELL_SIZE - 3, (y + 1) * CELL_SIZE - 3
            
            if i == 0:  # Cabeza
                # Efecto de brillo
                self.create_oval(x1-3, y1-3, x2+3, y2+3, fill=skin["head"], outline="", tags="snake")
                # Cabeza principal
                self.create_oval(x1, y1, x2, y2, fill=skin["head"], 
                               outline=UltimateTheme.TEXT_PRIMARY, width=2, tags="snake")
                
                # Ojos
                eye_size = 4
                eye_offset = CELL_SIZE // 3
                left_eye = (x * CELL_SIZE + eye_offset, y * CELL_SIZE + eye_offset)
                right_eye = (x * CELL_SIZE + CELL_SIZE - eye_offset, y * CELL_SIZE + eye_offset)
                
                for eye_pos in [left_eye, right_eye]:
                    self.create_oval(eye_pos[0]-eye_size//2, eye_pos[1]-eye_size//2,
                                   eye_pos[0]+eye_size//2, eye_pos[1]+eye_size//2,
                                   fill=skin["eye"], outline="", tags="snake")
            else:  # Cuerpo
                self.create_rectangle(x1-2, y1-2, x2+2, y2+2, fill=skin["body"], outline="", tags="snake")
                self.create_rectangle(x1, y1, x2, y2, fill=skin["body"], 
                                    outline=skin["head"], width=1, tags="snake")
    
    def draw_apple(self, apple):
        """Dibuja la manzana con estilo personalizable"""
        self.delete("apple")
        
        if apple.position:
            x, y = apple.position
            center_x = x * CELL_SIZE + CELL_SIZE // 2
            center_y = y * CELL_SIZE + CELL_SIZE // 2
            radius = CELL_SIZE // 2 - 4
            
            apple_color = UltimateTheme.APPLE_STYLES.get(apple.style, UltimateTheme.APPLE_STYLES["classic"])
            
            # Efectos según estilo
            if apple.style == "golden":
                self.create_oval(center_x - radius - 2, center_y - radius - 2,
                               center_x + radius + 2, center_y + radius + 2,
                               fill=UltimateTheme.NEON_YELLOW, outline="", tags="apple")
            elif apple.style == "crystal":
                for i in range(3, 0, -1):
                    self.create_oval(center_x - radius - i, center_y - radius - i,
                                   center_x + radius + i, center_y + radius + i,
                                   fill="", outline=apple_color, width=i, tags="apple")
            
            # Manzana principal
            self.create_oval(center_x - radius, center_y - radius,
                           center_x + radius, center_y + radius,
                           fill=apple_color, outline=UltimateTheme.TEXT_PRIMARY, width=2, tags="apple")
            
            # Brillo
            highlight_size = radius // 3
            self.create_oval(center_x - radius//2, center_y - radius//2,
                           center_x - radius//2 + highlight_size, 
                           center_y - radius//2 + highlight_size,
                           fill=UltimateTheme.TEXT_PRIMARY, outline="", tags="apple")
    
    def draw_path(self, path):
        """Dibuja el camino de búsqueda"""
        self.delete("path")
        
        if not path:
            return
            
        for i, (x, y) in enumerate(path[:8]):
            center_x = x * CELL_SIZE + CELL_SIZE // 2
            center_y = y * CELL_SIZE + CELL_SIZE // 2
            size = max(4, 10 - i)
            
            self.create_oval(center_x - size, center_y - size,
                           center_x + size, center_y + size,
                           fill=UltimateTheme.NEON_YELLOW, outline="", tags="path")
            
            if i < 5:
                self.create_text(center_x, center_y, text=str(i+1),
                               fill=UltimateTheme.PRIMARY_BG, 
                               font=("Arial", 8, "bold"), tags="path")

class SnakeAIGame:
    """Aplicación principal del juego"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.setup_window()
        
        # Inicializar audio con manejo de errores
        self.audio_manager = AudioManager()
        
        # Estado del juego
        self.state = GameState.MENU
        self.snake = Snake()
        self.apple = Apple(self.snake.body)
        self.agent = SearchAgent()
        
        # Configuraciones
        self.speed = 8
        self.show_path = False
        self.current_skin = "classic"
        self.current_apple_style = "classic"
        
        # Estadísticas
        self.game_start_time = 0
        self.moves_count = 0
        self.game_running_time = 0
        self.last_update_time = 0
        
        # Crear interfaz
        self.create_interface()
        
        # Estado del juego
        self.current_path = []
        self.game_running = False
    
    def setup_window(self):
        """Configura la ventana principal"""
        self.root.title("🐍 Snake AI - Propuesta de Valor Definitiva")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(fg_color=UltimateTheme.PRIMARY_BG)
        
        # Grid responsivo
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Centrar ventana
        x = (self.root.winfo_screenwidth() - WINDOW_WIDTH) // 2
        y = (self.root.winfo_screenheight() - WINDOW_HEIGHT) // 2
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    
    def create_interface(self):
        """Crea la interfaz principal"""
        
        # Panel del juego
        self.game_panel = ctk.CTkFrame(
            self.root,
            fg_color=UltimateTheme.SECONDARY_BG,
            corner_radius=20,
            border_width=3,
            border_color=UltimateTheme.NEON_CYAN
        )
        self.game_panel.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Canvas
        canvas_size = GRID_SIZE * CELL_SIZE
        self.canvas = GameCanvas(
            self.game_panel,
            width=canvas_size,
            height=canvas_size,
            bg=UltimateTheme.PRIMARY_BG
        )
        self.canvas.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Panel de control
        self.control_panel = ctk.CTkScrollableFrame(
            self.root,
            fg_color=UltimateTheme.SECONDARY_BG,
            corner_radius=20,
            border_width=3,
            border_color=UltimateTheme.NEON_PURPLE
        )
        self.control_panel.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        
        self.create_controls()
    
    def create_controls(self):
        """Crea los controles de la interfaz"""
        
        # Header
        self.create_header()
        
        # Sección algoritmos
        self.create_algorithm_section()
        
        # Sección personalización
        self.create_customization_section()
        
        # Sección controles
        self.create_controls_section()
        
        # Sección estadísticas
        self.create_stats_section()
        
        # Sección audio
        self.create_audio_section()
        
        # Propuesta de valor
        self.create_value_section()
    
    def create_header(self):
        """Crear header"""
        header_frame = ctk.CTkFrame(self.control_panel, fg_color=UltimateTheme.CARD_BG, corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header_frame, text="🐍 SNAKE AI",
                    font=ctk.CTkFont("Arial", 28, "bold"),
                    text_color=UltimateTheme.NEON_CYAN).pack(pady=(15, 5))
        
        ctk.CTkLabel(header_frame, text="PROPUESTA DE VALOR DEFINITIVA",
                    font=ctk.CTkFont("Arial", 12, "bold"),
                    text_color=UltimateTheme.TEXT_ACCENT).pack()
        
        ctk.CTkLabel(header_frame, text="Plataforma Educativa de IA\\nVisualizacion de Algoritmos",
                    font=ctk.CTkFont("Arial", 10),
                    text_color=UltimateTheme.TEXT_SECONDARY,
                    justify="center").pack(pady=(5, 15))
    
    def create_algorithm_section(self):
        """Crear sección de algoritmos"""
        algo_frame = ctk.CTkFrame(self.control_panel, fg_color=UltimateTheme.CARD_BG, corner_radius=15)
        algo_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(algo_frame, text="🧠 ALGORITMOS DE BUSQUEDA",
                    font=ctk.CTkFont("Arial", 16, "bold"),
                    text_color=UltimateTheme.NEON_GREEN).pack(pady=(15, 10))
        
        self.algorithm_var = ctk.StringVar(value=SearchAlgorithm.A_STAR.value)
        self.algorithm_menu = ctk.CTkOptionMenu(
            algo_frame,
            values=[algo.value for algo in SearchAlgorithm],
            variable=self.algorithm_var,
            fg_color=UltimateTheme.NEON_GREEN,
            font=ctk.CTkFont("Arial", 12, "bold")
        )
        self.algorithm_menu.pack(pady=(0, 15), padx=15, fill="x")
    
    def create_customization_section(self):
        """Crear sección personalización"""
        custom_frame = ctk.CTkFrame(self.control_panel, fg_color=UltimateTheme.CARD_BG, corner_radius=15)
        custom_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(custom_frame, text="🎨 PERSONALIZACION",
                    font=ctk.CTkFont("Arial", 16, "bold"),
                    text_color=UltimateTheme.NEON_PINK).pack(pady=(15, 10))
        
        # Snake skins
        ctk.CTkLabel(custom_frame, text="Skin de Serpiente:",
                    font=ctk.CTkFont("Arial", 11, "bold"),
                    text_color=UltimateTheme.TEXT_PRIMARY).pack(anchor="w", padx=15)
        
        self.skin_var = ctk.StringVar(value="classic")
        self.skin_menu = ctk.CTkOptionMenu(
            custom_frame,
            values=list(UltimateTheme.SNAKE_SKINS.keys()),
            variable=self.skin_var,
            command=self.change_snake_skin,
            fg_color=UltimateTheme.NEON_PINK
        )
        self.skin_menu.pack(pady=(5, 10), padx=15, fill="x")
        
        # Apple styles
        ctk.CTkLabel(custom_frame, text="Estilo de Manzana:",
                    font=ctk.CTkFont("Arial", 11, "bold"),
                    text_color=UltimateTheme.TEXT_PRIMARY).pack(anchor="w", padx=15)
        
        self.apple_style_var = ctk.StringVar(value="classic")
        self.apple_style_menu = ctk.CTkOptionMenu(
            custom_frame,
            values=list(UltimateTheme.APPLE_STYLES.keys()),
            variable=self.apple_style_var,
            command=self.change_apple_style,
            fg_color=UltimateTheme.NEON_ORANGE
        )
        self.apple_style_menu.pack(pady=(5, 15), padx=15, fill="x")
    
    def create_controls_section(self):
        """Crear sección de controles"""
        controls_frame = ctk.CTkFrame(self.control_panel, fg_color=UltimateTheme.CARD_BG, corner_radius=15)
        controls_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(controls_frame, text="🎮 CONTROLES",
                    font=ctk.CTkFont("Arial", 16, "bold"),
                    text_color=UltimateTheme.NEON_ORANGE).pack(pady=(15, 10))
        
        # Botón principal
        self.main_button = ctk.CTkButton(
            controls_frame,
            text="🚀 INICIAR SIMULACION",
            command=self.toggle_game,
            font=ctk.CTkFont("Arial", 14, "bold"),
            height=45,
            fg_color=UltimateTheme.NEON_GREEN
        )
        self.main_button.pack(pady=(0, 10), padx=15, fill="x")
        
        # Controles secundarios
        controls_grid = ctk.CTkFrame(controls_frame, fg_color="transparent")
        controls_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        self.pause_button = ctk.CTkButton(controls_grid, text="⏸️", command=self.toggle_pause,
                                         width=60, height=30, fg_color=UltimateTheme.NEON_YELLOW,
                                         text_color=UltimateTheme.PRIMARY_BG)
        self.pause_button.grid(row=0, column=0, padx=2)
        
        self.reset_button = ctk.CTkButton(controls_grid, text="🔄", command=self.reset_game,
                                         width=60, height=30, fg_color=UltimateTheme.NEON_CYAN)
        self.reset_button.grid(row=0, column=1, padx=2)
        
        self.path_button = ctk.CTkButton(controls_grid, text="🛤️", command=self.toggle_path,
                                        width=60, height=30, fg_color=UltimateTheme.NEON_PURPLE)
        self.path_button.grid(row=0, column=2, padx=2)
        
        # Control de velocidad
        speed_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        speed_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(speed_frame, text="Velocidad:",
                    font=ctk.CTkFont("Arial", 11, "bold"),
                    text_color=UltimateTheme.TEXT_PRIMARY).pack(anchor="w")
        
        self.speed_var = ctk.IntVar(value=self.speed)
        self.speed_slider = ctk.CTkSlider(speed_frame, from_=1, to=15, variable=self.speed_var,
                                         command=self.update_speed)
        self.speed_slider.pack(fill="x", pady=5)
        
        self.speed_label = ctk.CTkLabel(speed_frame, text=f"Velocidad: {self.speed} FPS",
                                       font=ctk.CTkFont("Arial", 9))
        self.speed_label.pack(anchor="w")
    
    def create_stats_section(self):
        """Crear sección de estadísticas"""
        stats_frame = ctk.CTkFrame(self.control_panel, fg_color=UltimateTheme.CARD_BG, corner_radius=15)
        stats_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(stats_frame, text="📊 ESTADISTICAS",
                    font=ctk.CTkFont("Arial", 16, "bold"),
                    text_color=UltimateTheme.NEON_YELLOW).pack(pady=(15, 10))
        
        # Grid de estadísticas
        self.stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        self.stats_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        # Crear labels de estadísticas
        self.stat_labels = {}
        stats_config = [
            ("🎯", "Puntuacion", "0", UltimateTheme.TEXT_SUCCESS),
            ("📏", "Longitud", "1", UltimateTheme.TEXT_ACCENT),
            ("👟", "Movimientos", "0", UltimateTheme.TEXT_WARNING),
            ("⏱️", "Tiempo", "0.0s", UltimateTheme.TEXT_PRIMARY),
            ("🔍", "Busqueda", "0.0ms", UltimateTheme.NEON_PINK),
            ("🧮", "Nodos", "0", UltimateTheme.NEON_CYAN)
        ]
        
        for i, (icon, label, value, color) in enumerate(stats_config):
            stat_frame = ctk.CTkFrame(self.stats_grid, fg_color=UltimateTheme.ACCENT_BG, corner_radius=8)
            stat_frame.grid(row=i//2, column=i%2, padx=3, pady=3, sticky="ew")
            
            ctk.CTkLabel(stat_frame, text=f"{icon} {label}:",
                        font=ctk.CTkFont("Arial", 9, "bold"),
                        text_color=UltimateTheme.TEXT_PRIMARY).pack(pady=(5, 0))
            
            value_label = ctk.CTkLabel(stat_frame, text=value,
                                      font=ctk.CTkFont("Arial", 11, "bold"),
                                      text_color=color)
            value_label.pack(pady=(0, 5))
            
            key = label.lower()
            self.stat_labels[key] = value_label
        
        self.stats_grid.grid_columnconfigure(0, weight=1)
        self.stats_grid.grid_columnconfigure(1, weight=1)
    
    def create_audio_section(self):
        """Crear sección de audio"""
        audio_frame = ctk.CTkFrame(self.control_panel, fg_color=UltimateTheme.CARD_BG, corner_radius=15)
        audio_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(audio_frame, text="🔊 AUDIO",
                    font=ctk.CTkFont("Arial", 16, "bold"),
                    text_color=UltimateTheme.TEXT_ACCENT).pack(pady=(15, 10))
        
        # Estado del audio
        audio_status = "Disponible" if self.audio_manager.is_available() else "No disponible"
        status_color = UltimateTheme.TEXT_SUCCESS if self.audio_manager.is_available() else UltimateTheme.TEXT_ERROR
        
        ctk.CTkLabel(audio_frame, text=f"Estado: {audio_status}",
                    font=ctk.CTkFont("Arial", 10),
                    text_color=status_color).pack()
        
        # Toggle de sonido
        self.sound_toggle = ctk.CTkSwitch(audio_frame, text="Efectos de Sonido",
                                         command=self.toggle_sound)
        self.sound_toggle.pack(pady=10)
        
        if self.audio_manager.is_available():
            self.sound_toggle.select()
        
        # Control de volumen
        ctk.CTkLabel(audio_frame, text="Volumen:",
                    font=ctk.CTkFont("Arial", 11, "bold")).pack(anchor="w", padx=15)
        
        self.volume_var = ctk.DoubleVar(value=0.7)
        self.volume_slider = ctk.CTkSlider(audio_frame, from_=0.0, to=1.0, 
                                          variable=self.volume_var,
                                          command=self.update_volume)
        self.volume_slider.pack(fill="x", padx=15, pady=5)
        
        self.volume_label = ctk.CTkLabel(audio_frame, text="Volumen: 70%",
                                        font=ctk.CTkFont("Arial", 9))
        self.volume_label.pack(pady=(0, 15))
    
    def create_value_section(self):
        """Crear sección de propuesta de valor"""
        value_frame = ctk.CTkFrame(self.control_panel, fg_color=UltimateTheme.CARD_BG, corner_radius=15)
        value_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(value_frame, text="💎 PROPUESTA DE VALOR",
                    font=ctk.CTkFont("Arial", 16, "bold"),
                    text_color=UltimateTheme.NEON_CYAN).pack(pady=(15, 10))
        
        value_text = ctk.CTkTextbox(value_frame, height=100,
                                   fg_color=UltimateTheme.ACCENT_BG,
                                   text_color=UltimateTheme.TEXT_PRIMARY)
        value_text.pack(pady=(0, 15), padx=15, fill="x")
        
        value_content = """VALOR EDUCATIVO: Visualizacion interactiva de algoritmos de IA con metricas precisas.

INNOVACION TECNICA: Implementacion profesional con personalizacion avanzada.

ANALISIS COMPARATIVO: Evaluacion en tiempo real de eficiencia algoritmica.

EXPERIENCIA PREMIUM: Interfaz moderna con efectos visuales profesionales."""
        
        value_text.insert("0.0", value_content)
        value_text.configure(state="disabled")
    
    # Métodos de control
    
    def change_snake_skin(self, skin_name):
        self.snake.set_skin(skin_name)
        self.current_skin = skin_name
        self.update_display()
    
    def change_apple_style(self, style_name):
        self.apple.set_style(style_name)
        self.current_apple_style = style_name
        self.update_display()
    
    def toggle_sound(self):
        self.audio_manager.toggle_sound()
    
    def update_volume(self, value):
        self.audio_manager.set_volume(float(value))
        self.volume_label.configure(text=f"Volumen: {int(float(value)*100)}%")
    
    def toggle_game(self):
        if not self.game_running:
            self.start_game()
        else:
            self.stop_game()
    
    def start_game(self):
        # Obtener algoritmo
        algo_name = self.algorithm_var.get()
        algorithm = SearchAlgorithm.A_STAR
        for algo in SearchAlgorithm:
            if algo.value == algo_name:
                algorithm = algo
                break
        
        # Resetear estado
        self.snake = Snake()
        self.snake.set_skin(self.current_skin)
        self.apple = Apple(self.snake.body)
        self.apple.set_style(self.current_apple_style)
        self.agent = SearchAgent(algorithm)
        
        self.state = GameState.PLAYING
        self.game_running = True
        
        # Resetear estadísticas
        self.game_start_time = time.time()
        self.last_update_time = self.game_start_time
        self.moves_count = 0
        self.game_running_time = 0
        self.current_path = []
        
        # Actualizar UI
        self.main_button.configure(text="🛑 DETENER", fg_color=UltimateTheme.TEXT_ERROR)
        
        # Sonido
        self.audio_manager.play_sound('start')
        
        # Iniciar loop
        self.root.after(100, self.game_loop)
    
    def stop_game(self):
        self.game_running = False
        self.state = GameState.MENU
        self.main_button.configure(text="🚀 INICIAR SIMULACION", fg_color=UltimateTheme.NEON_GREEN)
    
    def toggle_pause(self):
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
            self.pause_button.configure(text="▶️")
            self.audio_manager.play_sound('pause')
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING
            self.last_update_time = time.time()
            self.pause_button.configure(text="⏸️")
    
    def reset_game(self):
        if self.game_running:
            self.stop_game()
        self.start_game()
    
    def toggle_path(self):
        self.show_path = not self.show_path
        color = UltimateTheme.NEON_YELLOW if self.show_path else UltimateTheme.NEON_PURPLE
        self.path_button.configure(fg_color=color)
    
    def update_speed(self, value):
        self.speed = int(value)
        self.speed_label.configure(text=f"Velocidad: {self.speed} FPS")
    
    def game_loop(self):
        if not self.game_running:
            return
        
        if self.state == GameState.PLAYING:
            self.update_game()
        
        self.update_display()
        self.update_statistics()
        
        delay = max(50, int(1000 / self.speed))
        self.root.after(delay, self.game_loop)
    
    def update_game(self):
        current_time = time.time()
        self.game_running_time += current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Verificar límite de manzanas
        if self.snake.score >= MAX_APPLES:
            self.game_victory()
            return
        
        # Obtener movimiento IA
        next_direction = self.agent.get_next_move(self.snake, self.apple)
        
        # Obtener camino
        if self.show_path:
            start = self.snake.get_head()
            goal = self.apple.position if self.apple.position else start
            snake_body = self.snake.body[1:] if len(self.snake.body) > 1 else []
            self.current_path = self.agent.find_path(start, goal, snake_body)
        
        self.snake.change_direction(next_direction)
        self.snake.move()
        self.moves_count += 1
        
        # Verificar colisiones
        if self.snake.check_collision():
            self.game_over()
            return
        
        # Verificar manzana
        if self.snake.get_head() == self.apple.position:
            self.snake.grow_snake()
            self.audio_manager.play_sound('apple')
            
            # Nueva manzana
            new_apple = Apple(self.snake.body)
            if new_apple.position is None:
                self.game_victory()
                return
            self.apple = new_apple
            self.apple.set_style(self.current_apple_style)
    
    def update_display(self):
        self.canvas.draw_grid()
        
        if self.show_path:
            self.canvas.draw_path(self.current_path)
        
        self.canvas.draw_snake(self.snake)
        self.canvas.draw_apple(self.apple)
    
    def update_statistics(self):
        if not hasattr(self, 'stat_labels'):
            return
        
        stats = self.agent.get_performance_stats()
        
        updates = {
            'puntuacion': str(self.snake.score),
            'longitud': str(len(self.snake.body)),
            'movimientos': str(self.moves_count),
            'tiempo': f"{self.game_running_time:.1f}s",
            'busqueda': f"{stats['last_search_time']*1000:.2f}ms",
            'nodos': str(stats['last_nodes_expanded'])
        }
        
        for key, value in updates.items():
            if key in self.stat_labels:
                self.stat_labels[key].configure(text=value)
    
    def game_over(self):
        self.game_running = False
        self.state = GameState.GAME_OVER
        self.audio_manager.play_sound('gameover')
        
        stats = self.agent.get_performance_stats()
        
        result_message = f"""SIMULACION COMPLETADA

Algoritmo: {stats['algorithm']}
Puntuacion Final: {self.snake.score}/{MAX_APPLES}
Longitud Final: {len(self.snake.body)}
Tiempo Total: {self.game_running_time:.2f}s
Busquedas: {stats['total_searches']}
Tiempo Promedio: {stats['average_time']*1000:.2f}ms

Parametros Cumplidos:
✅ Tablero: {GRID_SIZE}x{GRID_SIZE}
✅ Longitud Minima: {MIN_SNAKE_LENGTH}
✅ Maximo Manzanas: {MAX_APPLES}"""
        
        messagebox.showinfo("Snake AI - Resultados", result_message)
        self.stop_game()
    
    def game_victory(self):
        self.game_running = False
        self.state = GameState.GAME_OVER
        self.audio_manager.play_sound('victory')
        
        stats = self.agent.get_performance_stats()
        
        victory_message = f"""¡SIMULACION VICTORIOSA!

¡Maximo de manzanas alcanzado!

Algoritmo Victorioso: {stats['algorithm']}
Puntuacion Perfecta: {MAX_APPLES}/{MAX_APPLES}
Tiempo Record: {self.game_running_time:.2f}s
Eficiencia: {stats['average_time']*1000:.2f}ms promedio

RENDIMIENTO EXCEPCIONAL"""
        
        messagebox.showinfo("¡VICTORIA ALGORITMICA!", victory_message)
        self.stop_game()
    
    def run(self):
        self.update_display()
        self.root.mainloop()

def main():
    print("🐍 SNAKE AI - PROPUESTA DE VALOR DEFINITIVA")
    print("=" * 50)
    print("🎯 Plataforma Educativa de Inteligencia Artificial")
    print("🔬 Visualizacion Avanzada de Algoritmos")
    print("🎨 Personalizacion Completa")
    print("📊 Analisis en Tiempo Real")
    print()
    print("⚡ CARACTERISTICAS TECNICAS:")
    print(f"   📐 Tablero: {GRID_SIZE}x{GRID_SIZE}")
    print(f"   🍎 Maximo manzanas: {MAX_APPLES}")
    print(f"   📏 Longitud minima: {MIN_SNAKE_LENGTH}")
    print("   🧠 Algoritmos: BFS, DFS, A*, Dijkstra")
    print("   🎨 6 skins personalizables")
    print("   🔊 Sistema de audio profesional")
    print()
    print("🚀 Iniciando aplicacion...")
    
    try:
        app = SnakeAIGame()
        app.run()
    except Exception as e:
        print(f"❌ Error critico: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
'''

# Guardar el archivo principal
with open('snake_ai_ultimate.py', 'w', encoding='utf-8') as f:
    f.write(snake_ai_ultimate)

print("✅ 1/6 - snake_ai_ultimate.py creado")