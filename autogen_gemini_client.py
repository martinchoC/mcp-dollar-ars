import autogen
import requests
import os
from dotenv import load_dotenv
from mcp_server import mcp_server
from gemini_autogen_adapter import gemini_adapter

load_dotenv()

class AutoGenGeminiClient:
    def __init__(self):
        # Configurar AutoGen con Gemini
        self.setup_autogen_with_gemini()
    
    def setup_autogen_with_gemini(self):
        """Configura AutoGen para usar Gemini como backend"""
        
        # Configuración MÍNIMA para Gemini
        self.llm_config = {
            "config_list": [
                {
                    "model": "gemini-2.5-flash",
                    "api_key": "dummy-key",  
                }
            ],
            "functions": mcp_server.get_tools(),
            "temperature": 0.1,
        }
        
        # Agente Usuario
        self.user_proxy = autogen.UserProxyAgent(
            name="Usuario",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            code_execution_config=False,
            system_message="Eres un usuario consultando sobre el dólar argentino.",
            default_auto_reply="CONTINUAR"
        )
        
        # Agente Asistente Especializado
        self.assistant = autogen.AssistantAgent(
            name="AnalistaDolar",
            system_message="""
            Eres un analista financiero especializado en el dólar USD/ARS.
            
            HERRAMIENTAS DISPONIBLES:
            - get_dollar_price(tipo): Precio actual
            - get_dollar_history(tipo, dias): Historial  
            - get_dollar_types(): Tipos disponibles
            
            Responde en español de forma clara y profesional.
            Usa las herramientas para obtener datos actualizados.
            """,
            llm_config=self.llm_config
        )
        
        # Registrar funciones MCP usando el adaptador personalizado
        self.register_mcp_functions_with_adapter()
        print("✅ AutoGen configurado con Gemini 2.5 Flash")
    
    def register_mcp_functions_with_adapter(self):
        """Registra las funciones MCP usando el adaptador personalizado"""
        
        def call_mcp_tool(function_name, **kwargs):
            """Wrapper para llamar herramientas MCP (Síncrono)"""
            import asyncio
            try:
                # Ejecutar de manera síncrona
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(mcp_server.execute_tool(function_name, kwargs))
                loop.close()
                return result
            except Exception as e:
                return f"❌ Error ejecutando {function_name}: {str(e)}"
        
        # Registrar herramientas
        self.call_mcp_tool = call_mcp_tool 
        
        function_map = {}
        for tool in mcp_server.get_tools():
            function_map[tool["name"]] = call_mcp_tool
        
        self.user_proxy.register_function(function_map=function_map)
    
    def query_dollar(self, question: str) -> str:
        """Consulta usando el adaptador Gemini directamente"""
        try:
            print(f"🔍 Consulta: {question}")
            
            # --- 1. PREPARACIÓN DEL PROMPT ---
            prompt = f"""
            Sos un analista financiero especializado en el dólar argentino.
            
            Consulta del usuario: {question}
            
            Para responder, puedes usar estas herramientas:
            - get_dollar_price(tipo): Obtener precio actual
            - get_dollar_history(tipo, dias): Obtener historial
            - get_dollar_types(): Ver tipos disponibles
            
            Responde en español de forma clara y profesional.
            """
            
            # --- 2. DETECCIÓN DE HERRAMIENTAS Y EJECUCIÓN MANUAL ---
            
            # Detectar si se pide historial (Ejecución de get_dollar_history)
            if any(keyword in question.lower() for keyword in ['evolución', 'historial', 'últimos', 'días']):
                print("🛠️ Detectada solicitud de historial. Ejecutando herramienta...")
                
                # Simple heurística: Extraer tipo (o usar 'blue') y días (o usar 7)
                dollar_type = 'blue' 
                days = 7 
                
                # Ejecutar la herramienta usando el wrapper MCP
                history_data = self.call_mcp_tool('get_dollar_history', dollar_type=dollar_type, days=days)
                
                # Añadir los datos del historial al prompt para que Gemini los use
                prompt_with_data = f"""
                {prompt}
                
                DATOS OBTENIDOS DEL HISTORIAL:
                {history_data}
                
                Proporciona una respuesta útil con esta información.
                """
                
                final_response = gemini_adapter.model.generate_content(prompt_with_data)
                return final_response.text

            # Detectar si se pide precio o tipos (Ejecución de get_dollar_types/get_dollar_price)
            elif any(keyword in question.lower() for keyword in ['precio', 'tipos', 'cuánto está', 'dólar']):
                print("🛠️ Detectada solicitud de precios/tipos. Ejecutando herramientas de contexto...")
                
                # Obtener datos básicos del servidor
                try:
                    types_data = self.call_mcp_tool('get_dollar_types') # Usar el wrapper
                    blue_data = self.call_mcp_tool('get_dollar_price', dollar_type='blue') # Usar el wrapper
                    
                    prompt_with_data = f"""
                    {prompt}
                    
                    DATOS ACTUALES:
                    {types_data}
                    
                    EJEMPLO DÓLAR BLUE:
                    {blue_data}
                    
                    Proporciona una respuesta útil con esta información.
                    """
                    
                    final_response = gemini_adapter.model.generate_content(prompt_with_data)
                    return final_response.text
                    
                except Exception as e:
                    # Fallback si las herramientas fallan
                    return f"{gemini_adapter.model.generate_content(prompt).text}\n\n❌ Error obteniendo datos: {str(e)}"
            
            # --- 3. CONSULTA SIN HERRAMIENTAS (Pregunta conceptual/general) ---
            print("🧠 Consulta conceptual. Llamando a Gemini sin herramientas.")
            return gemini_adapter.model.generate_content(prompt).text
                
        except Exception as e:
            return f"❌ Error en la consulta: {str(e)}"

def interactive_mode():
    """Modo interactivo del sistema completo"""
    client = AutoGenGeminiClient()
    
    print("\n" + "="*70)
    print("💵 SISTEMA AUTOGen + GEMINI 2.5 FLASH + APIs Reales")
    print("="*70)
    print("🧠 Backend: Google Gemini 2.5 Flash (Funcionando ✅)")
    print("📡 Datos: APIs financieras en tiempo real")
    print("="*70)
    print("\n💡 Ejemplos de consultas:")
    print("• 'precio del dólar blue'")
    print("• 'evolución del oficial últimos 7 días'") 
    print("• 'tipos de dólar disponibles'")
    print("• 'qué dólar me conviene para ahorrar'")
    print("="*70)
    
    while True:
        try:
            user_query = input("\n🔍 Tu consulta: ").strip()
            
            if user_query.lower() in ['salir', 'exit', 'quit']:
                print("👋 ¡Hasta luego!")
                break
                
            if user_query:
                print("🔄 Procesando con Gemini 2.5 Flash...")
                response = client.query_dollar(user_query)
                print(f"\n📊 RESPUESTA:\n{response}")
                print("-" * 70)
                
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    interactive_mode()