import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
import json

load_dotenv()

class GeminiAutogenAdapter:
    """Adaptador para usar Gemini con AutoGen"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY no encontrada en .env")
        
        genai.configure(api_key=api_key)
        
        # Usar el modelo que sabemos que funciona
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ Adaptador Gemini 2.5 Flash configurado correctamente")
    
    def create_chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        
        # Convertir mensajes de AutoGen a prompt de Gemini
        prompt = self._format_messages_for_gemini(messages)
        
        try:
            response = self.model.generate_content(prompt)
            
            # Formatear respuesta para AutoGen
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": response.text
                        },
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                }
            }
        except Exception as e:
            print(f"❌ Error en Gemini: {e}")
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant", 
                            "content": f"❌ Error procesando la consulta: {str(e)}"
                        },
                        "finish_reason": "stop"
                    }
                ]
            }
    
    def _format_messages_for_gemini(self, messages: List[Dict[str, str]]) -> str:
        """Formatea los mensajes de AutoGen para Gemini"""
        
        formatted_text = "Sos un analista financiero especializado en el dólar argentino. Respondé en español.\n\n"
        
        for message in messages:
            role = message.get("role", "")
            content = message.get("content", "")
            
            if role == "system":
                formatted_text += f"INSTRUCCIONES: {content}\n\n"
            elif role == "user":
                formatted_text += f"USUARIO: {content}\n\n"
            elif role == "assistant":
                formatted_text += f"ASISTENTE: {content}\n\n"
        
        formatted_text += "ASISTENTE:"
        return formatted_text

# Instancia global del adaptador
gemini_adapter = GeminiAutogenAdapter()