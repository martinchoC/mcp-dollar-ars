import asyncio
import requests
from typing import Dict, Any

class DollarMCPServer:
    def __init__(self):
        self.tools = {
            "get_dollar_price": {
                "name": "get_dollar_price",
                "description": "Obtiene el precio actual del dólar según el tipo",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dollar_type": {
                            "type": "string",
                            "description": "Tipo de dólar: blue, oficial, bolsa, liqui, turista",
                            "default": "blue"
                        }
                    },
                    "required": ["dollar_type"]
                }
            },
            "get_dollar_history": {
                "name": "get_dollar_history", 
                "description": "Obtiene el historial del dólar de los últimos días",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dollar_type": {
                            "type": "string",
                            "description": "Tipo de dólar",
                            "default": "blue"
                        },
                        "days": {
                            "type": "integer", 
                            "description": "Número de días",
                            "default": 7
                        }
                    },
                    "required": ["dollar_type", "days"]
                }
            },
            "get_dollar_types": {
                "name": "get_dollar_types",
                "description": "Obtiene los tipos de dólar disponibles", 
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Ejecuta una herramienta MCP"""
        try:
            if tool_name == "get_dollar_price":
                dollar_type = arguments.get("dollar_type", "blue")
                response = requests.get(f'http://localhost:5000/dollar/{dollar_type}')
                return response.json()["result"]
            
            elif tool_name == "get_dollar_history":
                dollar_type = arguments.get("dollar_type", "blue")
                days = arguments.get("days", 7)
                response = requests.get(f'http://localhost:5000/history/{dollar_type}/{days}')
                return response.json()["result"]
            
            elif tool_name == "get_dollar_types":
                response = requests.get('http://localhost:5000/types')
                return response.json()["result"]
            
            else:
                return f"❌ Herramienta {tool_name} no encontrada"
                
        except Exception as e:
            return f"❌ Error ejecutando {tool_name}: {str(e)}"
    
    def get_tools(self):
        """Retorna la lista de herramientas disponibles"""
        return list(self.tools.values())

# Instancia global del servidor MCP
mcp_server = DollarMCPServer()