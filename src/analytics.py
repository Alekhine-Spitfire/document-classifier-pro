import os
import logging
import pandas as pd
from datetime import datetime

# Configuración del Sistema de Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ==========================================
# Constantes FinOps y Métricas de Negocio (Modificables por el Cliente)
# ==========================================
COSTO_HORA_MANUAL_USD = 15.00  # Salario promedio estimado de un digitador contable
TIEMPO_MANUAL_DOC_MINUTOS = 5.0  # Minutos promedio que toma registrar un doc a mano
TIEMPO_IA_DOC_MINUTOS = 0.02    # Segundos que toma la automatización (aprox 1.2 seg)
COSTO_PROCESAMIENTO_IA_USD = 0.005 # Costo estimado de tokens de GPT-4o por documento

def calculate_roi_metrics(total_documents: int) -> dict:
    """
    Calcula el Retorno de Inversión (ROI) financiero y de eficiencia operativa.
    Herramienta clave para 'vender' el impacto del software a gerentes.
    """
    if total_documents <= 0:
        return {
            "tiempo_manual_horas": 0.0,
            "tiempo_ia_horas": 0.0,
            "horas_ahorradas": 0.0,
            "costo_manual_usd": 0.0,
            "costo_ia_usd": 0.0,
            "dinero_ahorrado_usd": 0.0,
            "eficiencia_porcentaje": 0.0
        }

    # Cálculos de Tiempo
    tiempo_manual_horas = (total_documents * TIEMPO_MANUAL_DOC_MINUTOS) / 60.0
    tiempo_ia_horas = (total_documents * TIEMPO_IA_DOC_MINUTOS) / 60.0
    horas_ahorradas = tiempo_manual_horas - tiempo_ia_horas

    # Cálculos de Costo Financiero
    costo_manual_usd = tiempo_manual_horas * COSTO_HORA_MANUAL_USD
    costo_ia_usd = total_documents * COSTO_PROCESAMIENTO_IA_USD
    dinero_ahorrado_usd = costo_manual_usd - costo_ia_usd

    # Porcentaje de Eficiencia (Gana velocidad)
    eficiencia_porcentaje = ((tiempo_manual_horas - tiempo_ia_horas) / tiempo_manual_horas) * 100.0

    return {
        "tiempo_manual_horas": round(tiempo_manual_horas, 2),
        "tiempo_ia_horas": round(tiempo_ia_horas, 4),
        "horas_ahorradas": round(horas_ahorradas, 2),
        "costo_manual_usd": round(costo_manual_usd, 2),
        "costo_ia_usd": round(costo_ia_usd, 4),
        "dinero_ahorrado_usd": round(dinero_ahorrado_usd, 2),
        "eficiencia_porcentaje": round(eficiencia_porcentaje, 1)
    }

def generate_enterprise_excel(extracted_documents: list, output_path: str = "reporte_clasificador.xlsx") -> str:
    """
    Toma una lista de JSONs estrictos estructurados por GPT-4o y genera
    un archivo Excel corporativo multi-pestaña listo para auditoría o ERP.
    """
    if not extracted_documents:
        logger.warning("⚠️ No hay datos extraídos para exportar a Excel.")
        return ""

    try:
        logger.info(f"📁 Iniciando canalización de datos hacia Excel: {output_path}")
        
        # 1. Construir Estructura para Tab 1: Resumen de Documentos (Cabeceras)
        summary_data = []
        # 2. Construir Estructura para Tab 2: Detalle de Items (Líneas de factura)
        items_data = []

        for idx, doc in enumerate(extracted_documents):
            # Identificador único para relacionar ambas tablas (Llave Foránea conceptual)
            doc_id = f"DOC-{datetime.now().strftime('%Y%m%d%H%M')}-{idx+1}"
            
            # Extraer campos de la cabecera
            summary_data.append({
                "ID_Documento": doc_id,
                "Tipo_Documento": doc.get("tipo_documento", "Desconocido"),
                "Proveedor": doc.get("proveedor", "N/A"),
                "NIT_RUTF_ID": doc.get("nit_rutf_id", "N/A"),
                "Fecha_Emision": doc.get("fecha_emision", "N/A"),
                "Moneda": doc.get("moneda", "N/A"),
                "Total_Neto": doc.get("total_neto", 0.0),
                "Impuestos": doc.get("impuestos", 0.0),
                "Total_Pagar": doc.get("total_pagar", 0.0),
                "Fecha_Procesado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # Extraer las líneas de ítem detalladas de este documento
            for item in doc.get("items", []):
                items_data.append({
                    "ID_Documento": doc_id,  # Vinculación con el documento padre
                    "Proveedor": doc.get("proveedor", "N/A"),
                    "Descripcion_Articulo": item.get("descripcion", "N/A"),
                    "Cantidad": item.get("cantidad", 0.0),
                    "Precio_Unitario": item.get("precio_unitario", 0.0),
                    "Total_Linea": item.get("total_item", 0.0)
                })

        # Convertir a DataFrames de Pandas
        df_summary = pd.DataFrame(summary_data)
        df_items = pd.DataFrame(items_data)

        # Escritura Multi-pestaña usando openpyxl (Fijado en requirements.txt)
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df_summary.to_excel(writer, sheet_name="Resumen_Ejecutivo", index=False)
            df_items.to_excel(writer, sheet_name="Detalle_Lineas", index=False)

        logger.info("✅ Archivo Excel corporativo generado con éxito.")
        return output_path

    except Exception as e:
        logger.error(f"🚨 Error crítico al generar el reporte Excel: {str(e)}")
        return ""