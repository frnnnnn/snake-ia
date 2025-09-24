# 2. INSTALADOR AUTOMÁTICO COMPLETO
instalador_automatico = '''"""
🔧 INSTALADOR AUTOMATICO - SNAKE AI ULTIMATE
Instala todas las dependencias necesarias automaticamente
Maneja errores y proporciona alternativas
"""

import subprocess
import sys
import os
import time
import platform

def print_banner():
    print("🐍" + "="*60 + "🐍")
    print("   SNAKE AI ULTIMATE - INSTALADOR AUTOMATICO")
    print("   Obra Maestra Visual para Inteligencia Artificial")
    print("   Instalacion Completa de Dependencias")
    print("🐍" + "="*60 + "🐍")

def print_section(title):
    print(f"\\n{'='*50}")
    print(f"📦 {title}")
    print('='*50)

def check_python_version():
    """Verifica la version de Python"""
    print_section("VERIFICANDO PYTHON")
    
    version = sys.version_info
    print(f"🐍 Python detectado: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3:
        print("❌ ERROR: Python 2.x detectado")
        print("   Se requiere Python 3.8 o superior")
        print("   Por favor instala Python 3.8+")
        return False
    
    if version.major == 3 and version.minor < 8:
        print("⚠️  ADVERTENCIA: Python 3.{} detectado".format(version.minor))
        print("   Se recomienda Python 3.8 o superior para CustomTkinter")
        print("   El juego puede funcionar pero con limitaciones")
        
        response = input("\\n¿Continuar con la instalacion? (s/n): ").lower()
        if response not in ['s', 'si', 'y', 'yes']:
            return False
    
    print("✅ Version de Python compatible")
    return True

def get_pip_command():
    """Determina el comando pip correcto"""
    commands = ['pip', 'pip3', 'python -m pip', 'python3 -m pip']
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd.split() + ['--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Comando pip encontrado: {cmd}")
                return cmd.split()
        except:
            continue
    
    print("❌ No se pudo encontrar pip")
    return None

def install_package(pip_cmd, package, description):
    """Instala un paquete con multiples intentos"""
    print(f"\\n🔧 Instalando {description}...")
    print(f"   Paquete: {package}")
    
    # Metodos de instalacion a intentar
    methods = [
        pip_cmd + ['install', package],
        pip_cmd + ['install', package, '--user'],
        pip_cmd + ['install', package, '--upgrade'],
        pip_cmd + ['install', package, '--user', '--upgrade'],
        pip_cmd + ['install', package, '--force-reinstall'],
    ]
    
    for i, method in enumerate(methods, 1):
        try:
            print(f"   Intento {i}: {' '.join(method)}")
            result = subprocess.run(method, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"   ✅ {package} instalado correctamente")
                return True
            else:
                print(f"   ⚠️  Intento {i} fallo: {result.stderr[:100]}...")
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Intento {i} timeout")
        except Exception as e:
            print(f"   ❌ Intento {i} error: {str(e)[:50]}...")
    
    print(f"   ❌ No se pudo instalar {package}")
    return False

def install_dependencies():
    """Instala todas las dependencias necesarias"""
    print_section("INSTALANDO DEPENDENCIAS")
    
    # Obtener comando pip
    pip_cmd = get_pip_command()
    if not pip_cmd:
        print("❌ No se puede continuar sin pip")
        return False
    
    # Lista de dependencias con prioridades
    dependencies = [
        # Criticas
        ("customtkinter>=5.2.0", "Interfaz Moderna (CRITICO)", True),
        ("numpy", "Calculos Matematicos (CRITICO)", True),
        
        # Importantes
        ("pygame", "Sistema de Audio", False),
        ("pillow", "Procesamiento de Imagenes", False),
        
        # Opcionales
        ("matplotlib", "Graficos Avanzados (OPCIONAL)", False),
    ]
    
    installed = []
    failed = []
    
    for package, description, is_critical in dependencies:
        success = install_package(pip_cmd, package, description)
        
        if success:
            installed.append((package, description))
        else:
            failed.append((package, description, is_critical))
    
    # Reporte de instalacion
    print("\\n" + "="*50)
    print("📊 REPORTE DE INSTALACION")
    print("="*50)
    
    if installed:
        print("\\n✅ PAQUETES INSTALADOS:")
        for package, desc in installed:
            print(f"   ✓ {package.split('>=')[0]} - {desc}")
    
    if failed:
        print("\\n❌ PAQUETES FALLIDOS:")
        for package, desc, critical in failed:
            status = "CRITICO" if critical else "OPCIONAL"
            print(f"   ✗ {package} - {desc} ({status})")
    
    # Verificar si se pueden ejecutar las criticas
    critical_failed = [f for f in failed if f[2]]
    
    if critical_failed:
        print("\\n⚠️  ADVERTENCIA: Dependencias criticas fallaron")
        print("   El juego podria no funcionar correctamente")
        print("\\n💡 SOLUCIONES SUGERIDAS:")
        print("   1. Ejecutar como administrador")
        print("   2. Actualizar pip: python -m pip install --upgrade pip")
        print("   3. Instalar manualmente:")
        for package, _, _ in critical_failed:
            print(f"      pip install {package}")
        return False
    
    print("\\n🎉 ¡INSTALACION EXITOSA!")
    print("   Todas las dependencias criticas instaladas")
    
    if failed and not critical_failed:
        print("\\n💡 NOTA: Algunas funciones opcionales no estaran disponibles")
        print("   El juego funcionara con funcionalidad reducida")
    
    return True

def verify_installation():
    """Verifica que los paquetes se importan correctamente"""
    print_section("VERIFICANDO INSTALACION")
    
    tests = [
        ("customtkinter", "Interfaz moderna"),
        ("numpy", "Calculos matematicos"),
        ("pygame", "Sistema de audio"),
        ("PIL", "Procesamiento de imagenes"),
        ("tkinter", "GUI base")
    ]
    
    working = []
    broken = []
    
    for module, description in tests:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
            working.append((module, description))
        except ImportError as e:
            print(f"❌ {module} - {description} (Error: {str(e)[:50]})")
            broken.append((module, description))
    
    print(f"\\n📊 RESULTADOS: {len(working)}/{len(tests)} modulos funcionando")
    
    # Verificar minimos
    critical_modules = ['customtkinter', 'numpy', 'tkinter']
    critical_working = [m for m, _ in working if m in critical_modules]
    
    if len(critical_working) >= 3:
        print("\\n🎉 ¡VERIFICACION EXITOSA!")
        print("   Todos los modulos criticos funcionan")
        return True
    else:
        print("\\n❌ VERIFICACION FALLIDA")
        print("   Faltan modulos criticos")
        return False

def create_run_script():
    """Crea script de ejecucion facil"""
    print_section("CREANDO SCRIPTS DE EJECUCION")
    
    # Script para Windows
    if platform.system() == "Windows":
        batch_content = '''@echo off
echo 🐍 SNAKE AI ULTIMATE - EJECUTOR
echo ================================
echo.
echo 🚀 Ejecutando Snake AI Ultimate...
echo.
python snake_ai_ultimate.py
echo.
echo ✅ Juego finalizado
pause
'''
        try:
            with open('ejecutar_snake_ai.bat', 'w', encoding='utf-8') as f:
                f.write(batch_content)
            print("✅ ejecutar_snake_ai.bat creado")
        except:
            print("⚠️  No se pudo crear .bat")
    
    # Script universal
    universal_content = '''#!/usr/bin/env python3
"""
🚀 EJECUTOR UNIVERSAL - SNAKE AI ULTIMATE
Script de ejecucion con verificacion automatica
"""

import sys
import os

def main():
    print("🐍 SNAKE AI ULTIMATE - EJECUTOR")
    print("="*40)
    
    # Verificar archivo principal
    if not os.path.exists('snake_ai_ultimate.py'):
        print("❌ Error: snake_ai_ultimate.py no encontrado")
        print("   Asegurate de estar en la carpeta correcta")
        input("Presiona Enter para salir...")
        return
    
    # Verificar dependencias basicas
    try:
        import customtkinter
        import numpy
        print("✅ Dependencias basicas verificadas")
    except ImportError as e:
        print(f"❌ Error de dependencias: {e}")
        print("   Ejecuta: python instalar_dependencias.py")
        input("Presiona Enter para salir...")
        return
    
    print("🚀 Ejecutando Snake AI Ultimate...")
    print()
    
    # Ejecutar juego
    try:
        import snake_ai_ultimate
        snake_ai_ultimate.main()
    except Exception as e:
        print(f"❌ Error ejecutando el juego: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
'''
    
    try:
        with open('ejecutar_juego.py', 'w', encoding='utf-8') as f:
            f.write(universal_content)
        print("✅ ejecutar_juego.py creado")
    except:
        print("⚠️  No se pudo crear ejecutor universal")

def show_final_instructions():
    """Muestra instrucciones finales"""
    print("\\n" + "🎉" + "="*48 + "🎉")
    print("   ¡INSTALACION COMPLETADA EXITOSAMENTE!")
    print("🎉" + "="*48 + "🎉")
    
    print("\\n📋 ARCHIVOS DEL PROYECTO:")
    files_to_check = [
        "snake_ai_ultimate.py",
        "instalar_dependencias.py", 
        "verificar_sistema.py",
        "manual_usuario.md",
        "ejecutar_juego.py"
    ]
    
    for filename in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"   ✅ {filename} ({size} bytes)")
        else:
            print(f"   ⚠️  {filename} (no encontrado)")
    
    print("\\n🚀 COMO EJECUTAR EL JUEGO:")
    print("   Opcion 1: python snake_ai_ultimate.py")
    print("   Opcion 2: python ejecutar_juego.py")
    
    if platform.system() == "Windows":
        print("   Opcion 3: Doble click en ejecutar_snake_ai.bat")
    
    print("\\n🔧 SI HAY PROBLEMAS:")
    print("   1. Ejecutar: python verificar_sistema.py")
    print("   2. Reinstalar: python instalar_dependencias.py")
    print("   3. Consultar: manual_usuario.md")
    
    print("\\n💎 CARACTERISTICAS DEL JUEGO:")
    print("   🎯 Tablero 10x10 con 35 manzanas maximo")
    print("   🧠 4 algoritmos de IA (BFS, DFS, A*, Dijkstra)")
    print("   🎨 6 skins personalizables para serpiente")
    print("   🔊 Sistema de audio profesional")
    print("   📊 Metricas de rendimiento en tiempo real")
    
    print("\\n🏆 ¡DISFRUTA TU OBRA MAESTRA DE IA!")

def main():
    """Funcion principal del instalador"""
    print_banner()
    
    # Verificar Python
    if not check_python_version():
        input("\\nPresiona Enter para salir...")
        return
    
    # Instalar dependencias
    if not install_dependencies():
        print("\\n❌ INSTALACION INCOMPLETA")
        print("💡 Revisa los errores arriba e intenta las soluciones sugeridas")
        input("\\nPresiona Enter para salir...")
        return
    
    # Verificar instalacion
    if not verify_installation():
        print("\\n❌ VERIFICACION FALLIDA")
        print("💡 Algunas dependencias no se importan correctamente")
        input("\\nPresiona Enter para salir...")
        return
    
    # Crear scripts
    create_run_script()
    
    # Instrucciones finales
    show_final_instructions()
    
    # Opcion de ejecutar inmediatamente
    print("\\n🎮 ¿Ejecutar Snake AI Ultimate ahora? (s/n): ", end="")
    try:
        response = input().lower().strip()
        if response in ['s', 'si', 'y', 'yes']:
            print("\\n🚀 Ejecutando Snake AI Ultimate...")
            import snake_ai_ultimate
            snake_ai_ultimate.main()
    except KeyboardInterrupt:
        print("\\n👋 Instalacion completada")
    except Exception as e:
        print(f"\\n❌ Error ejecutando: {e}")
    
    input("\\nPresiona Enter para finalizar...")

if __name__ == "__main__":
    main()
'''

# 3. VERIFICADOR DE SISTEMA COMPLETO
verificador_sistema = '''"""
🧪 VERIFICADOR DE SISTEMA - SNAKE AI ULTIMATE
Diagnostico completo del sistema y dependencias
Solucion de problemas automatizada
"""

import sys
import os
import platform
import time
import subprocess

class SystemChecker:
    def __init__(self):
        self.results = []
        self.errors = 0
        self.warnings = 0
        self.info = 0
    
    def log(self, level, test, message, details=""):
        """Registra resultado de prueba"""
        self.results.append({
            'level': level,
            'test': test,
            'message': message,
            'details': details,
            'timestamp': time.time()
        })
        
        icons = {'ERROR': '❌', 'WARNING': '⚠️', 'SUCCESS': '✅', 'INFO': 'ℹ️'}
        icon = icons.get(level, '?')
        
        if level == 'ERROR':
            self.errors += 1
        elif level == 'WARNING':
            self.warnings += 1
        elif level == 'INFO':
            self.info += 1
        
        print(f"{icon} {test}: {message}")
        if details:
            print(f"   {details}")
    
    def check_system_info(self):
        """Informacion del sistema"""
        print("\\n🖥️  INFORMACION DEL SISTEMA")
        print("="*40)
        
        try:
            system = platform.system()
            version = platform.version()
            machine = platform.machine()
            processor = platform.processor()
            
            self.log('INFO', 'Sistema Operativo', f"{system} {version}")
            self.log('INFO', 'Arquitectura', f"{machine}")
            if processor:
                self.log('INFO', 'Procesador', f"{processor[:50]}...")
                
        except Exception as e:
            self.log('WARNING', 'Info Sistema', f"No se pudo obtener: {e}")
    
    def check_python(self):
        """Verificacion de Python"""
        print("\\n🐍 VERIFICACION DE PYTHON")
        print("="*40)
        
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        
        self.log('INFO', 'Version Python', version_str)
        
        if version.major < 3:
            self.log('ERROR', 'Python Version', 
                    "Python 2.x detectado", 
                    "Se requiere Python 3.8+")
        elif version.major == 3 and version.minor < 8:
            self.log('WARNING', 'Python Version', 
                    f"Python 3.{version.minor} puede tener limitaciones",
                    "Se recomienda Python 3.8+")
        else:
            self.log('SUCCESS', 'Python Version', "Version compatible")
        
        # Verificar pip
        try:
            import pip
            self.log('SUCCESS', 'Pip', "Disponible")
        except ImportError:
            self.log('WARNING', 'Pip', "No encontrado como modulo")
            
            # Verificar pip desde comando
            try:
                result = subprocess.run(['pip', '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.log('SUCCESS', 'Pip Comando', "Disponible desde terminal")
                else:
                    self.log('ERROR', 'Pip', "No disponible")
            except:
                self.log('ERROR', 'Pip', "No disponible")
    
    def check_dependencies(self):
        """Verificacion de dependencias"""
        print("\\n📦 VERIFICACION DE DEPENDENCIAS")
        print("="*40)
        
        dependencies = [
            # (modulo, nombre, descripcion, critico)
            ('customtkinter', 'CustomTkinter', 'Interfaz moderna', True),
            ('numpy', 'NumPy', 'Calculos matematicos', True),
            ('tkinter', 'Tkinter', 'GUI base de Python', True),
            ('pygame', 'Pygame', 'Sistema de audio', False),
            ('PIL', 'Pillow', 'Procesamiento imagenes', False),
            ('json', 'JSON', 'Manejo de configuracion', True),
            ('time', 'Time', 'Funciones de tiempo', True),
            ('threading', 'Threading', 'Multiproceso', True),
            ('heapq', 'Heapq', 'Algoritmos de heap', True),
            ('math', 'Math', 'Funciones matematicas', True),
            ('random', 'Random', 'Numeros aleatorios', True),
            ('collections', 'Collections', 'Estructuras de datos', True),
            ('enum', 'Enum', 'Enumeraciones', True)
        ]
        
        working = 0
        critical_missing = 0
        
        for module, name, description, critical in dependencies:
            try:
                imported = __import__(module)
                version = getattr(imported, '__version__', 'Desconocida')
                self.log('SUCCESS', name, f"{description} v{version}")
                working += 1
                
                # Verificaciones especiales
                if module == 'customtkinter':
                    try:
                        # Verificar version minima
                        import customtkinter as ctk
                        test_root = ctk.CTk()
                        test_root.withdraw()
                        test_root.destroy()
                        self.log('SUCCESS', 'CustomTkinter Test', "Interfaz funcional")
                    except Exception as e:
                        self.log('WARNING', 'CustomTkinter Test', f"Problema: {e}")
                
                elif module == 'pygame':
                    try:
                        import pygame
                        pygame.mixer.init()
                        pygame.mixer.quit()
                        self.log('SUCCESS', 'Pygame Audio', "Sistema de audio funcional")
                    except Exception as e:
                        self.log('WARNING', 'Pygame Audio', f"Audio no disponible: {e}")
                
            except ImportError as e:
                level = 'ERROR' if critical else 'WARNING'
                self.log(level, name, f"{description} no disponible", str(e))
                if critical:
                    critical_missing += 1
        
        # Resumen
        total = len(dependencies)
        self.log('INFO', 'Resumen Dependencias', 
                f"{working}/{total} modulos disponibles")
        
        if critical_missing > 0:
            self.log('ERROR', 'Dependencias Criticas', 
                    f"{critical_missing} modulos criticos faltantes")
        else:
            self.log('SUCCESS', 'Dependencias Criticas', "Todas disponibles")
    
    def check_files(self):
        """Verificacion de archivos del proyecto"""
        print("\\n📁 VERIFICACION DE ARCHIVOS")
        print("="*40)
        
        required_files = [
            ('snake_ai_ultimate.py', 'Juego principal', True),
            ('instalar_dependencias.py', 'Instalador', False),
            ('verificar_sistema.py', 'Este verificador', False),
            ('manual_usuario.md', 'Manual de usuario', False),
            ('ejecutar_juego.py', 'Ejecutor', False)
        ]
        
        found_files = 0
        missing_critical = 0
        
        for filename, description, critical in required_files:
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                self.log('SUCCESS', filename, f"{description} ({size} bytes)")
                found_files += 1
            else:
                level = 'ERROR' if critical else 'WARNING'
                self.log(level, filename, f"{description} no encontrado")
                if critical:
                    missing_critical += 1
        
        if missing_critical > 0:
            self.log('ERROR', 'Archivos Criticos', 
                    f"{missing_critical} archivos criticos faltantes")
        else:
            self.log('SUCCESS', 'Archivos Criticos', "Todos presentes")
    
    def check_performance(self):
        """Pruebas de rendimiento basicas"""
        print("\\n⚡ PRUEBAS DE RENDIMIENTO")
        print("="*40)
        
        try:
            # Prueba de importacion de numpy
            start_time = time.time()
            import numpy as np
            arr = np.random.rand(10000)
            result = np.sin(arr).mean()
            numpy_time = (time.time() - start_time) * 1000
            
            if numpy_time < 100:
                self.log('SUCCESS', 'NumPy Performance', f"Excelente ({numpy_time:.1f}ms)")
            elif numpy_time < 500:
                self.log('SUCCESS', 'NumPy Performance', f"Bueno ({numpy_time:.1f}ms)")
            else:
                self.log('WARNING', 'NumPy Performance', f"Lento ({numpy_time:.1f}ms)")
            
        except Exception as e:
            self.log('ERROR', 'NumPy Performance', f"Fallo: {e}")
        
        try:
            # Prueba de CustomTkinter
            start_time = time.time()
            import customtkinter as ctk
            root = ctk.CTk()
            root.withdraw()
            
            # Crear algunos widgets
            frame = ctk.CTkFrame(root)
            for i in range(10):
                button = ctk.CTkButton(frame, text=f"Button {i}")
                label = ctk.CTkLabel(frame, text=f"Label {i}")
            
            ui_time = (time.time() - start_time) * 1000
            root.destroy()
            
            if ui_time < 200:
                self.log('SUCCESS', 'UI Performance', f"Excelente ({ui_time:.1f}ms)")
            elif ui_time < 1000:
                self.log('SUCCESS', 'UI Performance', f"Bueno ({ui_time:.1f}ms)")
            else:
                self.log('WARNING', 'UI Performance', f"Lento ({ui_time:.1f}ms)")
                
        except Exception as e:
            self.log('ERROR', 'UI Performance', f"Fallo: {e}")
    
    def check_game_components(self):
        """Verificacion de componentes del juego"""
        print("\\n🎮 VERIFICACION DE COMPONENTES DEL JUEGO")
        print("="*40)
        
        if not os.path.exists('snake_ai_ultimate.py'):
            self.log('ERROR', 'Archivo Principal', "snake_ai_ultimate.py no encontrado")
            return
        
        try:
            # Importar modulos del juego
            sys.path.insert(0, '.')
            import snake_ai_ultimate
            
            # Verificar clases principales
            components = [
                ('Snake', 'Clase serpiente'),
                ('Apple', 'Clase manzana'),
                ('SearchAgent', 'Agente de IA'),
                ('GameCanvas', 'Canvas del juego'),
                ('SnakeAIGame', 'Aplicacion principal'),
                ('AudioManager', 'Gestor de audio')
            ]
            
            for component, description in components:
                if hasattr(snake_ai_ultimate, component):
                    self.log('SUCCESS', component, f"{description} disponible")
                else:
                    self.log('ERROR', component, f"{description} no encontrado")
            
            # Verificar constantes
            constants = [
                ('GRID_SIZE', 'Tamaño de grilla'),
                ('MAX_APPLES', 'Maximo de manzanas'),
                ('MIN_SNAKE_LENGTH', 'Longitud minima')
            ]
            
            for constant, description in constants:
                if hasattr(snake_ai_ultimate, constant):
                    value = getattr(snake_ai_ultimate, constant)
                    self.log('SUCCESS', constant, f"{description} = {value}")
                else:
                    self.log('WARNING', constant, f"{description} no definido")
            
        except Exception as e:
            self.log('ERROR', 'Importacion Juego', f"Error importando: {e}")
    
    def generate_report(self):
        """Genera reporte final"""
        print("\\n" + "="*60)
        print("📋 REPORTE FINAL DEL SISTEMA")
        print("="*60)
        
        total_tests = len(self.results)
        
        print(f"\\n📊 RESUMEN EJECUTIVO:")
        print(f"   Total de pruebas: {total_tests}")
        print(f"   ✅ Exitosas: {total_tests - self.errors - self.warnings}")
        print(f"   ⚠️  Advertencias: {self.warnings}")
        print(f"   ❌ Errores: {self.errors}")
        
        # Estado general
        if self.errors == 0:
            if self.warnings == 0:
                status = "🎉 PERFECTO"
                description = "Sistema completamente funcional"
            else:
                status = "✅ BUENO" 
                description = "Sistema funcional con advertencias menores"
        elif self.errors <= 2:
            status = "⚠️  FUNCIONAL"
            description = "Sistema funcional con limitaciones"
        else:
            status = "❌ PROBLEMATICO"
            description = "Sistema requiere atencion"
        
        print(f"\\n🏆 ESTADO GENERAL: {status}")
        print(f"   {description}")
        
        # Recomendaciones
        print("\\n💡 RECOMENDACIONES:")
        
        if self.errors > 0:
            print("   🔧 Errores encontrados:")
            error_results = [r for r in self.results if r['level'] == 'ERROR']
            for result in error_results[:5]:  # Top 5 errores
                print(f"      • {result['test']}: {result['message']}")
            
            print("\\n   🛠️  Soluciones sugeridas:")
            print("      1. Ejecutar: python instalar_dependencias.py")
            print("      2. Verificar version de Python (3.8+)")
            print("      3. Instalar dependencias manualmente")
        
        if self.warnings > 0:
            print("\\n   ⚠️  Advertencias:")
            warning_results = [r for r in self.results if r['level'] == 'WARNING']
            for result in warning_results[:3]:  # Top 3 advertencias
                print(f"      • {result['test']}: {result['message']}")
        
        print("\\n🚀 PASOS SIGUIENTES:")
        if self.errors == 0:
            print("   1. Ejecutar: python snake_ai_ultimate.py")
            print("   2. Disfrutar del juego con IA")
            print("   3. Experimentar con diferentes algoritmos")
        else:
            print("   1. Resolver errores criticos")
            print("   2. Reinstalar dependencias si es necesario")
            print("   3. Consultar manual de usuario")
        
        return self.errors == 0

def main():
    """Funcion principal del verificador"""
    print("🧪 VERIFICADOR DE SISTEMA - SNAKE AI ULTIMATE")
    print("="*60)
    print("Ejecutando diagnostico completo del sistema...")
    print("Esto puede tomar unos minutos...")
    
    checker = SystemChecker()
    
    # Ejecutar todas las verificaciones
    checker.check_system_info()
    checker.check_python()
    checker.check_dependencies()
    checker.check_files()
    checker.check_performance()
    checker.check_game_components()
    
    # Generar reporte
    system_ok = checker.generate_report()
    
    # Opcion de ejecutar el juego si todo esta bien
    if system_ok:
        print("\\n🎮 ¿Ejecutar Snake AI Ultimate ahora? (s/n): ", end="")
        try:
            response = input().lower().strip()
            if response in ['s', 'si', 'y', 'yes']:
                print("\\n🚀 Ejecutando Snake AI Ultimate...")
                import snake_ai_ultimate
                snake_ai_ultimate.main()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"\\n❌ Error ejecutando: {e}")
    
    print("\\n👋 Verificacion completada")
    input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
'''

# Guardar archivos 2 y 3
with open('instalar_dependencias.py', 'w', encoding='utf-8') as f:
    f.write(instalador_automatico)

with open('verificar_sistema.py', 'w', encoding='utf-8') as f:
    f.write(verificador_sistema)

print("✅ 2/6 - instalar_dependencias.py creado")
print("✅ 3/6 - verificar_sistema.py creado")