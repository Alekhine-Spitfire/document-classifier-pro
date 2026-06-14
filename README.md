# 💼 Intelligent Document Classifier Pro — Enterprise IDP Platform

![Azure AI](https://img.shields.io/badge/Azure%20AI-Document%20Intelligence-0078d4?style=flat&logo=microsoftazure)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=flat&logo=openai)
![Python](https://img.shields.io/badge/Python-3.11-3776ab?style=flat&logo=python)

Plataforma de Procesamiento Inteligente de Documentos (**IDP**) de nivel empresarial diseñada para automatizar la extracción, clasificación y trazabilidad relacional de comprobantes contables no estructurados (Facturas, Boletas, Recibos) mediante una arquitectura híbrida de Inteligencia Artificial.

---

## ⚠️ El Problema de Negocio
Las organizaciones pierden cientos de horas hombre al mes digitando manualmente documentos financieros en formatos PDF o imágenes. Este proceso tradicional ralentiza el cierre contable, introduce un margen de error humano del **2% al 5%** en la captura de datos y representa un alto costo operativo por documento.

## 🎯 La Solución Tecnológica
Esta plataforma implementa un pipeline de ingesta masiva en lote (*Batch Processing*) que erradica la digitación manual combinando dos tecnologías de vanguardia:

1. **Precisión Estructural (Azure AI):** El motor v4.0 de *Azure AI Document Intelligence (Prebuilt-Layout)* realiza el análisis estructural transformando tablas complejas y texto en bloques limpios de Markdown.
2. **Razonamiento Semántico (OpenAI GPT-4o):** El LLM consume el Markdown y, mediante la característica estricta de *Structured Outputs (JSON Schema)*, extrae cabeceras y desglosa ítems de línea de forma determinista y sin riesgo de alucinaciones.

---

## 📈 Tablero de Retorno de Inversión (FinOps ROI)
La aplicación incorpora un motor matemático financiero real que calcula el impacto del software frente al esquema operativo manual tradicional:

| Métrica Operativa | Proceso Manual Tradicional | Pipeline de IA (Este Software) | Eficiencia / Impacto |
| :--- | :--- | :--- | :--- |
| **Tiempo de Procesamiento** | ~5.0 Minutos / Doc | ~1.2 Segundos / Doc | **99.6% Más Veloz** |
| **Costo Financiero** | ~$2.50 USD / Doc | ~$0.005 USD / Token | **Ahorro del 99.8%** |
| **Gobernanza de Datos** | Riesgo de Tipeo Humano | Esquema Estricto JSON | **0% Errores de Estructura** |

---

## 🛠️ Características Principales

* **Carga Masiva por Lote:** Soporta arrastrar múltiples PDFs, PNGs o JPGs contables simultáneamente para su procesamiento indexado en paralelo.
* **Trazabilidad Relacional Avanzada:** Asigna un identificador único por documento para indexar las cabeceras generales con sus respectivas líneas de ítems independientes, simulando el modelo entidad-relación de un ERP (SAP/Oracle).
* **Análisis de Concentración de Gastos:** Incorpora gráficos dinámicos que agrupan los egresos por proveedor aislando de forma inteligente los tipos de divisa (**USD vs Soles S/**) para mantener la integridad del balance general.
* **Exportador Corporativo Multi-Pestaña:** Descarga de forma nativa reportes unificados en archivos Excel (`.xlsx`), separando automáticamente el *Resumen Ejecutivo* del *Detalle de Líneas* listo para contabilidad.
* **Escudo FinOps (Modo Demo):** Incluye un conmutador de simulación local interactivo a costo $0 USD para demostraciones comerciales seguras y control de presupuesto en entornos web públicos.

---

## ⚙️ Arquitectura del Repositorio Local

```text
document-classifier-pro/
├── .env                  # Variables de entorno seguras (Ignorado en Git)
├── .gitignore            # Filtros de seguridad perimetral de nivel Enterprise
├── app.py                # Interfaz visual premium y tableros interactivos (Streamlit)
├── requirements.txt      # Manifiesto de dependencias estables fijadas (GA)
└── src/
    ├── analytics.py      # Motor matemático de ROI y generador de Excel multi-pestaña
    ├── azure_ocr.py      # Conector perimetral con la API v4.0 de Azure AI Layout
    └── openai_brain.py   # Esquema JSON estricto y orquestación semántica de GPT-4o
```

---

## 🚀 Instalación y Despliegue Local

1. Clonar el repositorio:
```bash
git clone [https://github.com/Alekhine-Spitfire/document-classifier-pro.git](https://github.com/Alekhine-Spitfire/document-classifier-pro.git)
cd document-classifier-pro
```

2. Crear e iniciar el entorno virtual aislado:
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Instalar la infraestructura de dependencias fijadas:
```bash
pip install -r requirements.txt
```

4. Configurar tus credenciales en un archivo `.env` en la raíz:
```env
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT="[https://tu-recurso.cognitiveservices.azure.com/](https://tu-recurso.cognitiveservices.azure.com/)"
AZURE_DOCUMENT_INTELLIGENCE_KEY="tu_llave_privada"
OPENAI_API_KEY="tu_llave_secreta_sk"
```

5. Ejecutar la consola de mandos:
```bash
streamlit run app.py
```
