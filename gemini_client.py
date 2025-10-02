import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class DollarClientGemini:
    def __init__(self):
        # Configurar Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY no encontrada en .env")
            print("💡 Obtén una API key gratis en: https://aistudio.google.com/")
            exit(1)
        
        genai.configure(api_key=api_key)
        
        # Listar modelos disponibles y usar uno compatible
        try:
            models = list(genai.list_models())
            print("🤖 Modelos disponibles:")
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    print(f"  ✅ {model.name}")
            
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            print("✅ Gemini configurado correctamente con gemini-2.5-flash")
            
        except Exception as e:
            print(f"❌ Error configurando Gemini: {e}")
            exit(1)
    
    def get_server_data(self, endpoint: str) -> str:
        """Obtiene datos del servidor"""
        try:
            response = requests.get(f'http://localhost:5000{endpoint}', timeout=10)
            return response.json()["result"]
        except Exception as e:
            return f"❌ Error conectando al servidor: {str(e)}"
    
    def query_dollar(self, question: str) -> str:
        """Consulta información sobre el dólar usando Gemini"""
        try:
            # Obtener información disponible del servidor
            available_types = self.get_server_data('/types')
            
            # Obtener datos actuales para contexto
            blue_price = self.get_server_data('/dollar/blue')
            oficial_price = self.get_server_data('/dollar/oficial')
            
            prompt = f"""
            Sos un experto analista financiero especializado en el dólar estadounidense vs peso argentino.

            DATOS ACTUALES DISPONIBLES:
            {available_types}

            EJEMPLOS DE PRECIOS ACTUALES:
            {blue_price}
            {oficial_price}

            INSTRUCCIONES:
            - Responde ÚNICAMENTE en español
            - Sé claro y conciso
            - Si preguntás por precios actuales, mencioná los tipos disponibles
            - Si preguntás por evolución, sugerí consultar el historial
            - Explicá las diferencias entre los tipos de dólar cuando sea relevante

            PREGUNTA DEL USUARIO: {question}

            Proporciona una respuesta útil basada en los datos disponibles.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"❌ Error en la consulta: {str(e)}"

def interactive_mode():
    """Modo interactivo para consultas"""
    client = DollarClientGemini()
    
    print("\n💵 CONSULTAS DE DÓLAR USD/ARS (Google Gemini)")
    print("=" * 50)
    print("Tipos disponibles: blue, oficial, bolsa, liqui, turista")
    print("Ejemplos:")
    print("• 'precio del dólar blue'")
    print("• 'tipos de dólar disponibles'") 
    print("• 'diferencia entre blue y oficial'")
    print("• 'salir' para terminar")
    print("=" * 50)
    
    while True:
        try:
            user_query = input("\n🔍 Tu consulta: ").strip()
            
            if user_query.lower() in ['salir', 'exit', 'quit']:
                print("👋 ¡Hasta luego!")
                break
                
            if user_query:
                print("⏳ Consultando datos...")
                response = client.query_dollar(user_query)
                print(f"\n📊 Respuesta:\n{response}")
                print("-" * 60)
                
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    interactive_mode()