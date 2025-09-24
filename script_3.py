# Crear archivos 2 y 3 corregidos completamente

# 2. INSTALADOR AUTOMÁTICO
instalador_code = """# INSTALADOR AUTOMATICO - SNAKE AI ULTIMATE
import subprocess
import sys
import os
import platform

def check_python():
    version = sys.version_info
    print(f"Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("ERROR: Se requiere Python 3.8+")
        return False
    print("Python compatible")
    return True

def install_package(package, description):
    print(f"Instalando {description}...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print(f"  EXITO: {package}")
        return True
    except:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '--user'])
            print(f"  EXITO: {package} (usuario)")
            return True
        except:
            print(f"  ERROR: {package}")
            return False

def main():
    print("SNAKE AI - INSTALADOR AUTOMATICO")
    print("="*40)
    
    if not check_python():
        input("Presiona Enter...")
        return
    
    deps = [
        ("customtkinter>=5.2.0", "Interfaz Moderna"),
        ("numpy", "Calculos Matematicos"),
        ("pygame", "Sistema Audio"),
        ("pillow", "Procesamiento Imagenes")
    ]
    
    print("\\nInstalando dependencias...")
    installed = 0
    
    for package, desc in deps:
        if install_package(package, desc):
            installed += 1
    
    print(f"\\nInstaladas: {installed}/{len(deps)}")
    
    if installed >= 2:
        print("INSTALACION EXITOSA!")
        print("Ejecutar: python snake_ai_ultimate.py")
    else:
        print("INSTALACION INCOMPLETA")
        print("Instalar manualmente las dependencias")
    
    input("\\nPresiona Enter...")

if __name__ == "__main__":
    main()
"""

# 3. VERIFICADOR DE SISTEMA
verificador_code = """# VERIFICADOR DE SISTEMA - SNAKE AI ULTIMATE
import sys
import os

def check_python():
    version = sys.version_info
    print(f"Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("  OK: Version compatible")
        return True
    else:
        print("  ERROR: Se requiere Python 3.8+")
        return False

def check_dependencies():
    deps = [
        ("customtkinter", "Interfaz moderna", True),
        ("numpy", "Calculos matematicos", True),
        ("pygame", "Sistema audio", False),
        ("PIL", "Procesamiento imagenes", False),
        ("tkinter", "GUI base", True)
    ]
    
    working = 0
    critical_missing = 0
    
    print("\\nDependencias:")
    for module, desc, critical in deps:
        try:
            __import__(module)
            print(f"  OK: {module} - {desc}")
            working += 1
        except ImportError:
            status = "CRITICO" if critical else "OPCIONAL"
            print(f"  ERROR: {module} - {desc} ({status})")
            if critical:
                critical_missing += 1
    
    print(f"\\nDisponibles: {working}/{len(deps)}")
    return critical_missing == 0

def check_files():
    files = [
        ("snake_ai_ultimate.py", "Juego principal", True),
        ("instalar_dependencias.py", "Instalador", False)
    ]
    
    print("\\nArchivos:")
    missing_critical = 0
    
    for filename, desc, critical in files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  OK: {filename} ({size} bytes)")
        else:
            status = "CRITICO" if critical else "OPCIONAL"
            print(f"  ERROR: {filename} - {desc} ({status})")
            if critical:
                missing_critical += 1
    
    return missing_critical == 0

def main():
    print("VERIFICADOR DE SISTEMA")
    print("="*30)
    
    python_ok = check_python()
    deps_ok = check_dependencies()
    files_ok = check_files()
    
    print("\\n" + "="*30)
    print("RESULTADO FINAL")
    print("="*30)
    
    if python_ok and deps_ok and files_ok:
        print("ESTADO: PERFECTO")
        print("Sistema listo para ejecutar")
        
        response = input("\\nEjecutar juego? (s/n): ")
        if response.lower() in ['s', 'si', 'y', 'yes']:
            try:
                import snake_ai_ultimate
                snake_ai_ultimate.main()
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("ESTADO: PROBLEMATICO")
        if not python_ok:
            print("  - Actualizar Python a 3.8+")
        if not deps_ok:
            print("  - Ejecutar: python instalar_dependencias.py")
        if not files_ok:
            print("  - Verificar archivos del proyecto")
    
    input("\\nPresiona Enter...")

if __name__ == "__main__":
    main()
"""

# Guardar archivos
with open('instalar_dependencias.py', 'w', encoding='utf-8') as f:
    f.write(instalador_code)

with open('verificar_sistema.py', 'w', encoding='utf-8') as f:
    f.write(verificador_code)

print("✅ 2/6 - instalar_dependencias.py creado")
print("✅ 3/6 - verificar_sistema.py creado")