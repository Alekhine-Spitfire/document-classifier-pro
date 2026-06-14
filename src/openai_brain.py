import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Inicializamos el cliente nativo de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_commercial_schema():
    """
    Define el esquema estricto de negocio que GPT-4o debe seguir.
    Esto garantiza un JSON predecible para el cliente o su ERP.
    """
    return {
        "name": "document_extraction",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "tipo_documento": {
                    "type": "string",
                    "enum": ["Factura", "Recibo", "Contrato", "Orden de Compra", "Desconocido"]
                },
                "proveedor": {"type": "string"},
                "nit_rutf_id": {"type": "string"},
                "fecha_emision": {"type": "string"},
                "moneda": {"type": "string"},
                "total_neto": {"type": "number"},
                "impuestos": {"type": "number"},
                "total_pagar": {"type": "number"},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "descripcion": {"type": "string"},
                            "cantidad": {"type": "number"},
                            "precio_unitario": {"type": "number"},
                            "total_item": {"type": "number"}
                        },
                        "required": ["descripcion", "cantidad", "precio_unitario", "total_item"],
                        "additionalProperties": False
                    }
                }
            },
            "required": [
                "tipo_documento", "proveedor", "nit_rutf_id", "fecha_emision", 
                "moneda", "total_neto", "impuestos", "total_pagar", "items"
            ],
            "additionalProperties": False
        }
    }

def process_document_with_gpt4o(markdown_content: str) -> dict:
    """
    Toma el texto estructurado por Azure OCR, lo analiza semánticamente con
    GPT-4o y devuelve un diccionario/JSON limpio bajo estándar corporativo.
    """
    
    system_prompt = (
        "Eres un auditor de sistemas financieros automatizados de alta precisión. "
        "Tu tarea es analizar el texto en formato Markdown extraído de un documento legal/contable "
        "y estructurar la información clave de forma exacta. "
        "Si un valor numérico no está explícito, calcula de forma lógica o pon 0. No inventes datos."
    )
    
    try:
        # Invocamos la API nativa usando el formato estructurado
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Por favor procesa el siguiente contenido:\n\n{markdown_content}"}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": get_commercial_schema()
            },
            temperature=0.0  # Determinismo puro: evita respuestas creativas
        )
        
        # Como usamos Structured Outputs, la respuesta viene garantizada en formato JSON string válido
        raw_json_output = response.choices[0].message.content
        return json.loads(raw_json_output)
        
    except Exception as e:
        print(f"[ERROR CEREBRO]: Fallo en la comunicación con OpenAI: {str(e)}")
        return {"error": "No se pudo procesar el documento con el modelo de lenguaje."}