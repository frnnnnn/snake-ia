# INSTALADOR AUTOMATICO - SNAKE AI ULTIMATE
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

    print("\nInstalando dependencias...")
    installed = 0

    for package, desc in deps:
        if install_package(package, desc):
            installed += 1

    print(f"\nInstaladas: {installed}/{len(deps)}")

    if installed >= 2:
        print("INSTALACION EXITOSA!")
        print("Ejecutar: python snake_ai_ultimate.py")
    else:
        print("INSTALACION INCOMPLETA")
        print("Instalar manualmente las dependencias")

    input("\nPresiona Enter...")

if __name__ == "__main__":
    main()
