# 💼 Intelligent Document Classifier Pro — Enterprise IDP Platform

![Azure AI](https://img.shields.io/badge/Azure%20AI-Document%20Intelligence-0078d4?style=flat&logo=microsoftazure)
![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4o-0078d4?style=flat&logo=microsoftazure)
![Python](https://img.shields.io/badge/Python-3.11-3776ab?style=flat&logo=python)

Plataforma de Procesamiento Inteligente de Documentos (**IDP**) de nivel empresarial diseñada para automatizar la extracción, clasificación y trazabilidad relacional de comprobantes contables no estructurados (Facturas, Boletas, Recibos) mediante una arquitectura híbrida construida íntegramente sobre el ecosistema de **Microsoft Azure AI**.

---

## ⚠️ El Problema de Negocio
Las organizaciones pierden cientos de horas hombre al mes digitando manualmente documentos financieros en formatos PDF o imágenes. Este proceso tradicional ralentiza el cierre contable, introduce un margen de error humano del **2% al 5%** en la captura de datos y representa un alto costo operativo por documento.

## 🎯 La Solución Tecnológica
Esta plataforma implementa un pipeline de ingesta masiva en lote (*Batch Processing*) que erradica la digitación manual combinando dos tecnologías cloud de vanguardia:

1. **Precisión Estructural (Azure AI Document Intelligence):** El motor moderno v4.0 de *Azure AI* realiza el análisis de Layout transformando tablas complejas y texto no estructurado en bloques limpios de Markdown.
2. **Razonamiento Semántico (Azure OpenAI Service):** Una instancia privada y segura de **GPT-4o** consume el Markdown y, mediante la característica de *Structured Outputs (JSON Schema)* de Azure, extrae cabeceras generales y desglosa ítems de línea de forma determinista y sin riesgo de alucinaciones.

---

## 📈 Tablero de Retorno de Inversión (FinOps ROI)
La aplicación incorpora un motor matemático financiero real que calcula el impacto del software frente al esquema operativo manual tradicional:

| Métrica Operativa | Proceso Manual Tradicional | Pipeline de IA (Este Software) | Eficiencia / Impacto |
| :--- | :--- | :--- | :--- |
| **Tiempo de Procesamiento** | ~5.0 Minutos / Doc | ~1.2 Segundos / Doc | **99.6% Más Veloz** |
| **Costo Financiero** | ~$2.50 USD / Doc | Costo por Token Azure | **Ahorro del 99.8%** |
| **Gobernanza de Datos** | Riesgo de Tipeo Humano | Esquema Estricto JSON | **0% Errores de Estructura** |

---

## 🛠️ Características Principales

* **Carga Masiva por Lote:** Soporta arrastrar múltiples PDFs, PNGs o JPGs contables simultáneamente para su procesamiento indexado en paralelo.
* **Gobernanza Semántica de Datos:** El modelo de IA cuenta con un prompt avanzado de auditoría que normaliza e integra automáticamente nombres de proveedores (ej. unificando variantes con puntos o comas de *NCS Pearson*) y códigos de divisas internacionales (**USD**, **S/**, **EUR**) de forma nativa desde el origen.
* **Trazabilidad Relacional Avanzada:** Indexa las cabeceras generales con sus respectivas líneas de ítems independientes, simulando el modelo entidad-relación de un ERP (SAP/Oracle).
* **Análisis de Concentración de Gastos:** Incorpora gráficos interactivos paralelos mediante *Altair* que muestran el volumen operativo y la carga financiera agrupada de forma limpia, proporcional y en paralelo.
* **Exportador Corporativo Multi-Pestaña:** Descarga de forma nativa reportes unificados en archivos Excel (`.xlsx`), separando automáticamente el *Resumen Ejecutivo* del *Detalle de Líneas* listo para contabilidad.
* **Escudo FinOps (Modo Demo):** Incluye un conmutador de simulación local interactivo a costo $0 USD basado en un pool de datos reales precargados (*Mock Data*) para demostraciones comerciales seguras y control de presupuesto.

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
    └── openai_brain.py   # Esquema JSON estricto y orquestación semántica de Azure OpenAI
```

---

## 🚀 Instalación y Despliegue Local

1. Clonar el repositorio:
```bash
git clone [https://github.com/Alekhine-Spitfire/document-classifier-pro.git](https://github.com/Alekhine-Spitfire/document-classifier-pro.git)
cd document-classifier-pro
```

2. Crea el entorno virtual de Python e inicialízalo según tu sistema operativo:

En Windows (PowerShell):
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

En Linux / macOS:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar tus credenciales en un archivo `.env` en la raíz:
```env
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT="[https://tu-recurso-ocr.cognitiveservices.azure.com/](https://tu-recurso-ocr.cognitiveservices.azure.com/)"
AZURE_DOCUMENT_INTELLIGENCE_KEY="tu_llave_de_document_intelligence"

AZURE_OPENAI_ENDPOINT="[https://tu-recurso-openai.openai.azure.com/](https://tu-recurso-openai.openai.azure.com/)"
AZURE_OPENAI_KEY="tu_llave_de_azure_openai"
AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o"
```

5. Ejecutar la consola de mandos:
```bash
streamlit run app.py
```
