
  

# 💵 Sistema de Consultas de Dólar USD/ARS con AutoGen y Gemini 2.5 Flash

Un sistema cliente-servidor avanzado que utiliza un **framework de Agentes (AutoGen)** y la **IA de Google Gemini 2.5 Flash** para procesar consultas complejas sobre los diferentes tipos de dólar en Argentina con datos en tiempo real.

## 🌟 Características
-  **🤖 Arquitectura de Agentes**: Usa **AutoGen** para la orquestación de tareas y el uso de herramientas.
-  **🧠 IA Integrada**: Procesamiento de lenguaje natural y razonamiento con **Google Gemini 2.5 Flash**.
-  **🚀 Tool-Calling Avanzado**: Utiliza un **Protocolo de Comunicación de Microservicios (MCP)** para integrar herramientas.
-  **📡 Datos en Tiempo Real**: Conexión con APIs financieras a través del servidor Flask (`dollar_server.py`).
-  **💬 Consultas Naturales**: Interfaz conversacional en español.
-  **📊 Múltiples Tipos de Dólar**: Blue, Oficial, Bolsa (MEP), CCL, Turista.

## 🛠️ Tecnologías Utilizadas

- [cite_start]**Framework de Agentes**: [**AutoGen**](https://microsoft.github.io/autogen/)
-  **IA / LLM**: Google Gemini API (modelo `gemini-2.5-flash`)
-  **Backend**: Python + Flask
-  **Manejo de APIs**: Requests
-  **APIs Financieras**: [DolarAPI.com](https://dolarapi.com/), Bluelytics

## 📦 Instalación

### Prerrequisitos
- Python 3.8 o superior
- Cuenta en Google AI Studio (para API key gratuita)

### 1. Clonar el Repositorio

```bash
git  clone  https://github.com/martinchoC/mcp-dollar-ars.git
cd  mcp-dollar-ars
```

### 2. Crear Entorno Virtual (Recomendado)

```bash
# Windows
python  -m  venv  venv
venv\Scripts\activate

# Mac/Linux
python3  -m  venv  venv
source  venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip  install  -r  requirements.txt
```

### 4. Configurar API Key de Gemini
1. Ir a [Google AI Studio](https://aistudio.google.com/)
2. Iniciar sesión con una cuenta Google
3. Crear una nueva API key
4. Crear el archivo `.env`:

```bash
# env
GEMINI_API_KEY=api_key_de_gemini
```

## 🚀 Uso Rápido
El sistema completo se inicializa con un solo comando que arranca el servidor de datos y el cliente de agentes.
### Ejecutar Sistema Completo

```bash
python  __init__.py
```
El archivo init.py se encarga de:
- Iniciar el Servidor Flask (dollar_server.py) en un hilo.
- Esperar que el servidor esté listo.
- Iniciar el Cliente de Agentes AutoGen (autogen_gemini_client.py).

## 💬 Ejemplos de Consultas
  
El sistema entiende consultas en lenguaje natural:
- 🔍 Precio: "precio del dólar blue"
- 🔍 Historial: "evolución del oficial últimos 7 días" (Usa la herramienta get_dollar_history)
- 🔍 Tipos: "tipos de dólar disponibles"
- 🔍 Análisis: "qué dólar me conviene para ahorrar"

## 📡 APIs Utilizadas

### Fuentes de Datos en Tiempo Real
-  **[DolarAPI.com](https://dolarapi.com/)**: Precios oficiales y paralelos
-  **Múltiples fallbacks**: Garantía de disponibilidad

### Tipos de Dólar Disponibles

| Tipo | Descripción | Ejemplo de Consulta |
|--|--|--|
| Blue | Mercado informal | "precio blue" |
| Oficial | Bancos oficiales | "dólar oficial" |
| Bolsa | Mercado de valores (MEP) | "dólar bolsa" |
| CCL | Contado con liquidación | "dólar CCL" |
| Turista | Para viajes al exterior | "dólar turista" |

## 🏗️ Estructura del Proyecto

mcp-dollar-ars/

├── **__init__.py**                  # 🚀 Punto de inicio del sistema (Arranca Servidor y Cliente

├── **dollar_server.py**             # 📡 Servidor Flask con APIs REST (Datos reales/simulados)

├── **mcp_server.py**                # 🔧 Implementa el Servidor MCP (wrapper de herramientas)

├── **gemini_autogen_adapter.py**    # ⚙️ Adaptador para conectar Gemini con AutoGen

├── **autogen_gemini_client.py**     # 🧠 Cliente principal (Agentes AutoGen + Gemini)

├── requirements.txt                 # Dependencias

├── .env                             # Variables de entorno (GEMINI_API_KEY)

└── README.md                        # Documentación

---
## 🔧 Archivos Principales

| Archivo | Rol en el Sistema | Descripción Detallada |
| :--- | :--- | :--- |
| **`__init__.py`** | **Punto de Entrada Principal** 🚀 | Se encarga de iniciar el **Servidor Flask** (`dollar_server.py`) en un hilo y, tras verificar que esté operativo, lanza el **Modo Interactivo del Cliente AutoGen** (`autogen_gemini_client.py`). |
| **`dollar_server.py`** | **Servidor de Datos/API** 📡 | Servidor Flask que actúa como la **fuente de datos**. Gestiona la conexión a APIs financieras reales (o *fallbacks*) y expone los *endpoints* REST (ej. `/history`, `/types`) para que las herramientas puedan consultarlos. |
| **`mcp_server.py`** | **Protocolo de Comunicación (MCP)** 🛠️ | Define las **herramientas** (`get_dollar_history`, `get_dollar_price`) en un formato compatible con los LLM. Su método `execute_tool` actúa como la capa que traduce las peticiones de la IA en llamadas HTTP al `dollar_server.py`. |
| **`gemini_autogen_adapter.py`** | **Adaptador LLM** ⚙️ | Contiene la lógica para que Google Gemini 2.5 Flash pueda ser usado como el motor de razonamiento dentro del *framework* AutoGen, formateando mensajes correctamente. |
| **`autogen_gemini_client.py`** | **Cliente/Orquestador de Agentes** 🧠 | **Es el cliente interactivo y el orquestador**. Configura el entorno AutoGen, registra las funciones MCP, y contiene la lógica principal para enviar la consulta a Gemini y, basándose en la respuesta, ejecutar las herramientas y presentar el resultado. |
  

## 🔄 Flujo del Sistema

```mermaid
graph TD
A["1. Usuario: Consulta"] --> B{"autogen_gemini_client.py"};
B --> C["2. Gemini 2.5 Flash (LLM)"];
C -- "3. Decide usar Herramienta" --> B;
B -- "4. Ejecuta Wrapper (call_mcp_tool)" --> D["mcp_server.py (Capa MCP)"];
D -- "5. Petición HTTP" --> E["dollar_server.py (API Datos)"];
E -- "6. Respuesta Datos" --> D;
D -- "7. Resultado Herramienta" --> B;
B -- "8. Prompt + Datos" --> C;
C -- "9. Respuesta Final" --> B;
B --> A;

## 🎯 Casos de Uso

-  **💼 Finanzas Personales**: Seguimiento de tipos de cambio
-  **📈 Análisis de Mercado**: Comparación entre diferentes dólares
-  **🛫 Viajes**: Consulta de dólar turista
-  **💸 Inversiones**: Análisis de dólar MEP/CCL
-  **🎓 Educativo**: Estudio del mercado cambiario argentino

## 📄 Licencia

Este proyecto está bajo la Licencia Apache 2.0 - ver el archivo [LICENSE](https://license/) para detalles.

----------
<div  align="center">

**Desarrollado por Martin Castro y Carlos Almaraz para la materia Sistemas Inteligentes**

_Última actualización: Octubre 2025_

</div>








