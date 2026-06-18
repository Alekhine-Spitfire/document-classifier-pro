import os
import logging
from openai import AzureOpenAI  # 🚀 Cambiamos a la clase nativa de Azure
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Configuración del Logger Corporativo
logger = logging.getLogger(__name__)

# ==========================================
# Esquemas Pydantic Estrictos (Gobernanza de Datos)
# ==========================================
class ItemDetalle(BaseModel):
    descripcion: str
    cantidad: float
    precio_unitario: float
    total_item: float

class DocumentoEstructurado(BaseModel):
    tipo_documento: str
    proveedor: str
    nit_rutf_id: str
    fecha_emision: str
    moneda: str
    total_neto: float
    impuestos: float
    total_pagar: float
    items: List[ItemDetalle]

# ==========================================
# Conector y Orquestador de Azure OpenAI
# ==========================================
def get_azure_openai_client():
    """Inicializa el cliente perimetral seguro de Azure OpenAI."""
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2024-08-01-preview",  # Versión de API estable compatible con Structured Outputs
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

def process_document_with_gpt4o(markdown_text: str) -> dict:
    """
    Consume el Markdown del OCR y aplica razonamiento semántico mediante GPT-4o 
    en Azure, forzando una respuesta JSON estricta basada en el esquema Pydantic.
    """
    try:
        logger.info("🧠 Invocando razonamiento semántico en Azure OpenAI (GPT-4o)...")
        client = get_azure_openai_client()
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

        # El SDK de OpenAI parsea nativamente los esquemas en Azure OpenAI
        response = client.beta.chat.completions.parse(
            model=deployment_name,
            messages = [
            {
                "role": "system", 
                "content": """# ROL: AUDITOR CONTABLE SENIOR
                Tu tarea es extraer de forma estricta la información del documento en Markdown provisto.

                ## ⚠️ REGLA DE CLASIFICACIÓN ESTRICTA (EVITAR AMBIGÜEDAD)
                * Si el documento contiene un título explícito en mayúsculas como **'FACTURA'** o **'INVOICE'**, o posee un campo estructurado **'Número de factura'**, clasifícalo **SIEMPRE** como `'Factura'`.
                * **Ignora frases contextuales ambiguas** como *"conserve esta factura como recibo"*. El título principal y el ID de facturación tienen peso y prioridad absoluta para determinar que es una `'Factura'`.
                * Si el documento es un ticket de compra simple o carece de datos fiscales corporativos, clasifícalo como `'Boleta'` o `'Recibo'` según corresponda.
                * Si no puedes determinar un dato, clasifícalo como `'Desconocido'` o coloca `0.0` en los montos numéricos.

                ## ⚠️ REGLA DE NORMALIZACIÓN DE PROVEEDORES CRÍTICA
                Para el campo 'proveedor', debes extraer la razón social o nombre comercial más limpio y asegurar consistencia absoluta entre documentos del mismo emisor. Elimina espacios dobles, espacios al inicio o final, y puntos finales de abreviaturas si generan duplicados.
                * Si detectas variaciones como `'NCS Pearson, Inc.'`, `'NCS Pearson, Inc'` o `'NCS Pearson Inc'` -> Guarda **SIEMPRE** exactamente: `'NCS Pearson, Inc'`
                * Si detectas `'Delivery Hero Peru S.A.C.'` o `'Delivery Hero Perú S.A.C'` -> Guarda **SIEMPRE** exactamente: `'Delivery Hero Peru S.A.C.'`

                ## ⚠️ REGLA DE NORMALIZACIÓN MONETARIA CRÍTICA
                Para el campo 'moneda', debes homologar y estandarizar **CUALQUIER** divisa detectada a su símbolo limpio abreviado o código ISO estándar. No permitas variaciones de texto en el output final.
                * Si detectas Soles, PEN, S/., SOL o Nuevos Soles -> Guarda estrictamente: `'S/'`
                * Si detectas Dólares, USD, US$, Dollar o $, -> Guarda estrictamente: `'USD'`
                * Si detectas Euros, EUR, EUR$, €, -> Guarda estrictamente: `'EUR'`
                * Para cualquier otra moneda, usa siempre su código ISO de 3 letras (ej. MXN, CLP, COP)."""
            },
            {
                "role": "user", 
                "content": f"Analiza la siguiente subestructura de datos:\n\n{markdown_text}"
            }
        ],
            response_format=DocumentoEstructurado,
        )
        
        logger.info("✅ Extracción y estructuración JSON completada por Azure con éxito.")
        return response.choices[0].message.parsed.model_dump()

    except Exception as e:
        logger.error(f"💥 Fallo crítico en el procesamiento semántico de Azure OpenAI: {str(e)}")
        # Esquema seguro de contingencia (Fallback) para no romper las gráficas de la App
        return {
            "tipo_documento": "Desconocido",
            "proveedor": "Fallo en Pipeline",
            "nit_rutf_id": "N/A",
            "fecha_emision": "N/A",
            "moneda": "N/A",
            "total_neto": 0.0,
            "impuestos": 0.0,
            "total_pagar": 0.0,
            "items": []
        }