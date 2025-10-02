import threading
import time
import requests
import dollar_server
from autogen_gemini_client import interactive_mode

def run_dollar_server():
    """Ejecuta el servidor de dólar en segundo plano"""
    print("🚀 Iniciando servidor dólar...")
    dollar_server.app.run(port=5000, debug=False, use_reloader=False)

def wait_for_server():
    """Espera a que el servidor esté listo"""
    print("⏳ Esperando servidor...")
    for i in range(30):
        try:
            response = requests.get('http://localhost:5000/types', timeout=2)
            if response.status_code == 200:
                print("✅ Servidor dólar listo!")
                return True
        except:
            if i % 5 == 0:
                print(f"   Intentando conectar... ({i+1}/30)")
            time.sleep(1)
    print("❌ Servidor no respondió")
    return False

def main():
    """Sistema final con Gemini 2.5 Flash funcionando"""
    print("💵 SISTEMA FINAL: Gemini 2.5 Flash + APIs Reales")
    print("="*50)
    
    # Iniciar servidor en hilo separado
    server_thread = threading.Thread(target=run_dollar_server, daemon=True)
    server_thread.start()
    
    # Esperar servidor
    if wait_for_server():
        # Iniciar cliente interactivo
        interactive_mode()
    else:
        print("No se pudo iniciar el sistema")

if __name__ == "__main__":
    main()