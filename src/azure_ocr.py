import os
import logging
from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError

# ==========================================
# Configuración del Sistema de Logging Enterprise
# ==========================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

def get_document_intelligence_client() -> DocumentIntelligenceClient:
    """
    Inicializa y retorna el cliente oficial de Azure Document Intelligence.
    Valida la existencia de credenciales para evitar caídas en producción.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    
    if not endpoint or not key:
        logger.error("🚨 CRÍTICO: Faltan las credenciales de Azure Document Intelligence en el .env")
        raise ValueError("Variables de entorno de Azure no configuradas.")
        
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def extract_layout_to_markdown(file_path: str) -> str:
    """
    Envía un archivo a Azure Document Intelligence usando el modelo Layout
    y retorna el contenido formateado explícitamente en Markdown.
    Includes robust error handling for corporate stability.
    """
    if not os.path.exists(file_path):
        logger.error(f"❌ El archivo no existe en la ruta especificada: {file_path}")
        return ""

    try:
        client = get_document_intelligence_client()
        logger.info(f"🚀 Iniciando análisis OCR del documento: {os.path.basename(file_path)}")
        
        with open(file_path, "rb") as f:
            # En la versión estable (GA), podemos forzar explícitamente la salida a Markdown
            poller = client.begin_analyze_document(
                model_id="prebuilt-layout",
                body=f,
                content_type="application/octet-stream",
                output_content_format="markdown"  # <-- Especificación explícita para GPT-4o
            )
            result = poller.result()
        
        # Extracción segura del contenido estructurado
        markdown_content = getattr(result, "content", "")
        
        if not markdown_content:
            logger.warning(f"⚠️ El documento {os.path.basename(file_path)} se procesó pero no devolvió texto.")
            return ""
            
        logger.info("✅ Extracción de Layout y conversión a Markdown exitosa.")
        return markdown_content

    except AzureError as ae:
        # Captura errores específicos de la nube de Azure (ej. Llave vencida, cuota superada)
        logger.error(f"🚨 Error de Azure Document Intelligence: {str(ae)}")
        return ""
    except Exception as e:
        # Captura cualquier otro fallo inesperado del sistema o de lectura de archivo
        logger.error(f"💥 Error inesperado en el motor OCR: {str(e)}")
        return ""