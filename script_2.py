# Corregir el instalador sin emojis en strings problemáticos

# 2. INSTALADOR AUTOMÁTICO CORREGIDO
instalador_automatico = '''"""
INSTALADOR AUTOMATICO - SNAKE AI ULTIMATE
Instala todas las dependencias necesarias automaticamente
"""

import subprocess
import sys
import os
import time
import platform

def print_banner():
    print("SNAKE AI ULTIMATE - INSTALADOR AUTOMATICO")
    print("="*60)
    print("   Obra Maestra Visual para Inteligencia Artificial")
    print("   Instalacion Completa de Dependencias")
    print("="*60)

def print_section(title):
    print(f"\\n{'='*50}")
    print(f">> {title}")
    print('='*50)

def check_python_version():
    """Verifica la version de Python"""
    print_section("VERIFICANDO PYTHON")
    
    version = sys.version_info
    print(f"Python detectado: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3:
        print("ERROR: Python 2.x detectado")
        print("   Se requiere Python 3.8 o superior")
        return False
    
    if version.major == 3 and version.minor < 8:
        print("ADVERTENCIA: Python antiguo detectado")
        print("   Se recomienda Python 3.8+")
        
        response = input("\\nContinuar instalacion? (s/n): ").lower()
        if response not in ['s', 'si', 'y', 'yes']:
            return False
    
    print("Version de Python compatible")
    return True

def get_pip_command():
    """Determina el comando pip correcto"""
    commands = ['pip', 'pip3', 'python -m pip', 'python3 -m pip']
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd.split() + ['--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"Comando pip encontrado: {cmd}")
                return cmd.split()
        except:
            continue
    
    print("No se pudo encontrar pip")
    return None

def install_package(pip_cmd, package, description):
    """Instala un paquete con multiples intentos"""
    print(f"\\nInstalando {description}...")
    print(f"   Paquete: {package}")
    
    methods = [
        pip_cmd + ['install', package],
        pip_cmd + ['install', package, '--user'],
        pip_cmd + ['install', package, '--upgrade'],
        pip_cmd + ['install', package, '--user', '--upgrade'],
    ]
    
    for i, method in enumerate(methods, 1):
        try:
            print(f"   Intento {i}: {' '.join(method)}")
            result = subprocess.run(method, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"   EXITO: {package} instalado")
                return True
            else:
                print(f"   Intento {i} fallo")
                
        except subprocess.TimeoutExpired:
            print(f"   Intento {i} timeout")
        except Exception as e:
            print(f"   Intento {i} error: {str(e)[:50]}")
    
    print(f"   ERROR: No se pudo instalar {package}")
    return False

def install_dependencies():
    """Instala todas las dependencias"""
    print_section("INSTALANDO DEPENDENCIAS")
    
    pip_cmd = get_pip_command()
    if not pip_cmd:
        return False
    
    dependencies = [
        ("customtkinter>=5.2.0", "Interfaz Moderna", True),
        ("numpy", "Calculos Matematicos", True),
        ("pygame", "Sistema de Audio", False),
        ("pillow", "Procesamiento de Imagenes", False),
    ]
    
    installed = []
    failed = []
    
    for package, description, is_critical in dependencies:
        success = install_package(pip_cmd, package, description)
        
        if success:
            installed.append((package, description))
        else:
            failed.append((package, description, is_critical))
    
    print("\\n" + "="*50)
    print("REPORTE DE INSTALACION")
    print("="*50)
    
    if installed:
        print("\\nPAQUETES INSTALADOS:")
        for package, desc in installed:
            print(f"   * {package.split('>=')[0]} - {desc}")
    
    if failed:
        print("\\nPAQUETES FALLIDOS:")
        for package, desc, critical in failed:
            status = "CRITICO" if critical else "OPCIONAL"
            print(f"   * {package} - {desc} ({status})")
    
    critical_failed = [f for f in failed if f[2]]
    
    if critical_failed:
        print("\\nADVERTENCIA: Dependencias criticas fallaron")
        print("SOLUCIONES:")
        print("   1. Ejecutar como administrador")
        print("   2. Actualizar pip")
        print("   3. Instalar manualmente")
        return False
    
    print("\\nINSTALACION EXITOSA!")
    return True

def verify_installation():
    """Verifica los paquetes instalados"""
    print_section("VERIFICANDO INSTALACION")
    
    tests = [
        ("customtkinter", "Interfaz moderna"),
        ("numpy", "Calculos matematicos"),
        ("pygame", "Sistema de audio"),
        ("PIL", "Procesamiento de imagenes"),
        ("tkinter", "GUI base")
    ]
    
    working = 0
    
    for module, description in tests:
        try:
            __import__(module)
            print(f"OK: {module} - {description}")
            working += 1
        except ImportError:
            print(f"ERROR: {module} - {description}")
    
    print(f"\\nRESULTADOS: {working}/{len(tests)} modulos funcionando")
    
    return working >= 3

def create_run_script():
    """Crea scripts de ejecucion"""
    print_section("CREANDO SCRIPTS")
    
    if platform.system() == "Windows":
        batch_content = '''@echo off
echo SNAKE AI ULTIMATE - EJECUTOR
echo ================================
echo.
echo Ejecutando Snake AI Ultimate...
echo.
python snake_ai_ultimate.py
echo.
echo Juego finalizado
pause
'''
        try:
            with open('ejecutar_snake_ai.bat', 'w') as f:
                f.write(batch_content)
            print("ejecutar_snake_ai.bat creado")
        except:
            print("No se pudo crear .bat")
    
    universal_content = '''#!/usr/bin/env python3
"""
EJECUTOR UNIVERSAL - SNAKE AI ULTIMATE
"""

import sys
import os

def main():
    print("SNAKE AI ULTIMATE - EJECUTOR")
    print("="*40)
    
    if not os.path.exists('snake_ai_ultimate.py'):
        print("ERROR: snake_ai_ultimate.py no encontrado")
        input("Presiona Enter para salir...")
        return
    
    try:
        import customtkinter
        import numpy
        print("Dependencias verificadas")
    except ImportError as e:
        print(f"ERROR: {e}")
        print("Ejecuta: python instalar_dependencias.py")
        input("Presiona Enter para salir...")
        return
    
    print("Ejecutando Snake AI Ultimate...")
    
    try:
        import snake_ai_ultimate
        snake_ai_ultimate.main()
    except Exception as e:
        print(f"ERROR: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
'''
    
    try:
        with open('ejecutar_juego.py', 'w', encoding='utf-8') as f:
            f.write(universal_content)
        print("ejecutar_juego.py creado")
    except:
        print("No se pudo crear ejecutor")

def main():
    """Funcion principal"""
    print_banner()
    
    if not check_python_version():
        input("\\nPresiona Enter para salir...")
        return
    
    if not install_dependencies():
        print("\\nINSTALACION INCOMPLETA")
        input("\\nPresiona Enter para salir...")
        return
    
    if not verify_installation():
        print("\\nVERIFICACION FALLIDA")
        input("\\nPresiona Enter para salir...")
        return
    
    create_run_script()
    
    print("\\n" + "="*50)
    print("INSTALACION COMPLETADA")
    print("="*50)
    
    print("\\nCOMO EJECUTAR:")
    print("   python snake_ai_ultimate.py")
    print("   python ejecutar_juego.py")
    
    print("\\nCARACTERISTICAS:")
    print("   * Tablero 10x10")
    print("   * 4 algoritmos de IA")
    print("   * 6 skins personalizables")
    print("   * Sistema de audio")
    print("   * Metricas en tiempo real")
    
    print("\\nEjecutar ahora? (s/n): ", end="")
    try:
        response = input().lower().strip()
        if response in ['s', 'si', 'y', 'yes']:
            print("\\nEjecutando...")
            import snake_ai_ultimate
            snake_ai_ultimate.main()
    except:
        pass
    
    input("\\nPresiona Enter para finalizar...")

if __name__ == "__main__":
    main()
'''

# 3. VERIFICADOR CORREGIDO
verificador_sistema = '''"""
VERIFICADOR DE SISTEMA - SNAKE AI ULTIMATE
Diagnostico completo del sistema
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
    
    def log(self, level, test, message):
        """Registra resultado"""
        self.results.append({'level': level, 'test': test, 'message': message})
        
        if level == 'ERROR':
            self.errors += 1
            print(f"ERROR - {test}: {message}")
        elif level == 'WARNING':
            self.warnings += 1
            print(f"WARN - {test}: {message}")
        else:
            print(f"OK - {test}: {message}")
    
    def check_python(self):
        """Verificacion de Python"""
        print("\\nVERIFICANDO PYTHON")
        print("="*30)
        
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        
        self.log('INFO', 'Python Version', version_str)
        
        if version.major < 3:
            self.log('ERROR', 'Python', "Se requiere Python 3.8+")
        elif version.major == 3 and version.minor < 8:
            self.log('WARNING', 'Python', "Version antigua, se recomienda 3.8+")
        else:
            self.log('SUCCESS', 'Python', "Version compatible")
    
    def check_dependencies(self):
        """Verificacion de dependencias"""
        print("\\nVERIFICANDO DEPENDENCIAS")
        print("="*30)
        
        deps = [
            ('customtkinter', 'Interfaz moderna', True),
            ('numpy', 'Calculos matematicos', True),
            ('tkinter', 'GUI base', True),
            ('pygame', 'Audio', False),
            ('PIL', 'Imagenes', False),
        ]
        
        working = 0
        critical_missing = 0
        
        for module, desc, critical in deps:
            try:
                imported = __import__(module)
                version = getattr(imported, '__version__', 'N/A')
                self.log('SUCCESS', module, f"{desc} v{version}")
                working += 1
            except ImportError:
                level = 'ERROR' if critical else 'WARNING'
                self.log(level, module, f"{desc} no disponible")
                if critical:
                    critical_missing += 1
        
        if critical_missing > 0:
            self.log('ERROR', 'Dependencias', f"{critical_missing} criticas faltantes")
        else:
            self.log('SUCCESS', 'Dependencias', "Todas las criticas disponibles")
    
    def check_files(self):
        """Verificacion de archivos"""
        print("\\nVERIFICANDO ARCHIVOS")
        print("="*30)
        
        files = [
            ('snake_ai_ultimate.py', 'Juego principal', True),
            ('instalar_dependencias.py', 'Instalador', False),
            ('verificar_sistema.py', 'Verificador', False),
        ]
        
        for filename, desc, critical in files:
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                self.log('SUCCESS', filename, f"{desc} ({size} bytes)")
            else:
                level = 'ERROR' if critical else 'WARNING'
                self.log(level, filename, f"{desc} no encontrado")
    
    def check_performance(self):
        """Pruebas de rendimiento"""
        print("\\nPRUEBAS DE RENDIMIENTO")
        print("="*30)
        
        try:
            start = time.time()
            import numpy as np
            arr = np.random.rand(5000)
            result = np.sin(arr).mean()
            numpy_time = (time.time() - start) * 1000
            
            if numpy_time < 100:
                self.log('SUCCESS', 'NumPy', f"Excelente ({numpy_time:.1f}ms)")
            elif numpy_time < 500:
                self.log('SUCCESS', 'NumPy', f"Bueno ({numpy_time:.1f}ms)")
            else:
                self.log('WARNING', 'NumPy', f"Lento ({numpy_time:.1f}ms)")
        except Exception as e:
            self.log('ERROR', 'NumPy', f"Fallo: {e}")
        
        try:
            start = time.time()
            import customtkinter as ctk
            root = ctk.CTk()
            root.withdraw()
            root.destroy()
            ui_time = (time.time() - start) * 1000
            
            if ui_time < 200:
                self.log('SUCCESS', 'UI', f"Excelente ({ui_time:.1f}ms)")
            else:
                self.log('WARNING', 'UI', f"Lento ({ui_time:.1f}ms)")
        except Exception as e:
            self.log('ERROR', 'UI', f"Fallo: {e}")
    
    def generate_report(self):
        """Genera reporte final"""
        print("\\n" + "="*50)
        print("REPORTE FINAL")
        print("="*50)
        
        total = len(self.results)
        success = total - self.errors - self.warnings
        
        print(f"\\nRESUMEN:")
        print(f"   Total: {total}")
        print(f"   Exitosas: {success}")
        print(f"   Advertencias: {self.warnings}")
        print(f"   Errores: {self.errors}")
        
        if self.errors == 0:
            if self.warnings == 0:
                status = "PERFECTO"
            else:
                status = "BUENO"
        else:
            status = "PROBLEMATICO"
        
        print(f"\\nESTADO: {status}")
        
        if self.errors > 0:
            print("\\nSOLUCIONES:")
            print("   1. python instalar_dependencias.py")
            print("   2. Verificar Python 3.8+")
            print("   3. Instalar dependencias manualmente")
        
        print("\\nPARA EJECUTAR:")
        print("   python snake_ai_ultimate.py")
        
        return self.errors == 0

def main():
    """Funcion principal"""
    print("VERIFICADOR DE SISTEMA - SNAKE AI ULTIMATE")
    print("="*50)
    
    checker = SystemChecker()
    
    checker.check_python()
    checker.check_dependencies()
    checker.check_files()
    checker.check_performance()
    
    system_ok = checker.generate_report()
    
    if system_ok:
        print("\\nEjecutar juego? (s/n): ", end="")
        try:
            response = input().lower().strip()
            if response in ['s', 'si', 'y', 'yes']:
                import snake_ai_ultimate
                snake_ai_ultimate.main()
        except:
            pass
    
    input("\\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()
'''

# Guardar archivos corregidos
with open('instalar_dependencias.py', 'w', encoding='utf-8') as f:
    f.write(instalador_automatico)

with open('verificar_sistema.py', 'w', encoding='utf-8') as f:
    f.write(verificador_sistema)

print("✅ 2/6 - instalar_dependencias.py creado")
print("✅ 3/6 - verificar_sistema.py creado")