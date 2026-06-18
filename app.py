import streamlit as st
import os
import json
import pandas as pd
import altair as alt  # Motor gráfico de alta precisión enterprise
from datetime import datetime
from src.azure_ocr import extract_layout_to_markdown
from src.openai_brain import process_document_with_gpt4o
from src.analytics import calculate_roi_metrics, generate_enterprise_excel

# Configuración de cabecera de nivel corporativo
st.set_page_config(
    page_title="Document Intelligence Pro - Enterprise Classifier",
    page_icon="📊",
    layout="wide"
)

# Inyección de CSS de Nivel Premium con fuentes Sans-Serif Modernas (Inter)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Forzar la tipografía limpia en toda la aplicación */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3 {
        font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif !important;
    }
    
    /* Tarjetas Métricas con diseño horizontal amplio */
    .metric-card-horizontal {
        background-color: #ffffff;
        padding: 18px 22px;
        border-radius: 8px;
        border-left: 5px solid #007bff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 12px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-label {
        font-size: 12px;
        font-weight: 600;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 4px;
    }
    .metric-val {
        font-size: 26px;
        font-weight: 700;
        color: #1e293b;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado Comercial
st.title("💼 Intelligent Document Classifier Pro")
st.subheader("Procesamiento Inteligente de Documentos No Estructurados con Azure AI & GPT-4o")

# ==========================================
# Barra Lateral (Sidebar): Configuración de Negocio y FinOps
# ==========================================
with st.sidebar:
    st.header("⚙️ Panel de Control FinOps")
    st.write("Optimiza costos y flujos de datos en tiempo real.")
    
    modo_demo = st.toggle("🚀 Activar Modo Demo (Costo $0 USD)", value=True, 
                          help="Simula la extracción masiva instantáneamente usando datos corporativos precargados.")
    
    st.divider()
    st.markdown("### 🔒 Estado de Infraestructura")
    
    has_azure_ocr = bool(os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"))
    has_azure_llm = bool(os.getenv("AZURE_OPENAI_KEY"))
    
    if has_azure_ocr and has_azure_llm:
        st.success("Conectores Cloud: ONLINE")
    else:
        st.warning("Conectores Cloud: MODO LOCAL")

# ==========================================
# Lógica de Simulación (Pool de Datos unificado de tus 4 PDF reales)
# ==========================================
MOCK_BATCH_DATA = [
    {
        "tipo_documento": "Factura", "proveedor": "NCS Pearson, Inc", "nit_rutf_id": "41-0850527",
        "fecha_emision": "2026-03-13", "moneda": "USD", "total_neto": 59.00, "impuestos": 0.0, "total_pagar": 59.00,
        "items": [{"descripcion": "Examen de Certificación IA-900", "cantidad": 1, "precio_unitario": 59.00, "total_item": 59.00}]
    },
    {
        "tipo_documento": "Boleta", "proveedor": "Delivery Hero Peru S.A.C.", "nit_rutf_id": "20551348041",
        "fecha_emision": "2026-03-29", "moneda": "S/", "total_neto": 2.20, "impuestos": 0.40, "total_pagar": 2.60,
        "items": [
            {"descripcion": "Servicio logístico PedidosYa", "cantidad": 1, "precio_unitario": 1.61, "total_item": 1.61},
            {"descripcion": "Tarifa de servicio", "cantidad": 1, "precio_unitario": 0.59, "total_item": 0.59}
        ]
    }
]

if "processed_docs" not in st.session_state:
    st.session_state.processed_docs = []

# ==========================================
# Zona de Carga Masiva (Batch Processing Area)
# ==========================================
st.write("---")
uploaded_files = st.file_uploader(
    "📥 Arrastra aquí los documentos contables de la empresa (PDF, PNG, JPG)", 
    type=["pdf", "png", "jpg"], 
    accept_multiple_files=True,
    help="Soporta procesamiento masivo en lote."
)

if uploaded_files:
    if st.button("🚀 Iniciar Procesamiento Inteligente Masivo", type="primary"):
        results = []
        progress_bar = st.progress(0)
        
        for index, file in enumerate(uploaded_files):
            st.write(f"⚙️ Analizando subestructura: **{file.name}**...")
            
            if modo_demo:
                import time
                time.sleep(0.4)
                doc_res = MOCK_BATCH_DATA[index % len(MOCK_BATCH_DATA)]
            else:
                temp_path = f"temp_{file.name}"
                with open(temp_path, "wb") as f:
                    f.write(file.getbuffer())
                
                markdown_text = extract_layout_to_markdown(temp_path)
                doc_res = process_document_with_gpt4o(markdown_text)
                
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            
            results.append(doc_res)
            progress_bar.progress((index + 1) / len(uploaded_files))
            
        st.session_state.processed_docs = results
        st.success(f"🎯 ¡Procesamiento por lote completado con éxito! {len(results)} documentos indexados.")

# ==========================================
# El Tablero de ROI e Impacto de Negocio
# ==========================================
if st.session_state.processed_docs:
    st.write("---")
    st.header("📊 Tablero Corporativo de Retorno de Inversión (ROI)")
    
    roi = calculate_roi_metrics(len(st.session_state.processed_docs))
    
    # 🎯 ALGORITMO PREMIUM: Conversión de decimales a formato Reloj real (h y min)
    horas_raw = roi['horas_ahorradas']
    total_minutos = int(round(horas_raw * 60))
    entero_horas = total_minutos // 60
    minutos = total_minutos % 60

    if entero_horas == 0:
        tiempo_display = f"{minutos} Min"
    else:
        if minutos == 0:
            tiempo_display = f"{entero_horas}h"
        else:
            tiempo_display = f"{entero_horas}h {minutos}min"
    
    # Renderizado de métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card-horizontal'><div class='metric-label'>🏢 Docs Procesados</div><div class='metric-val'>{len(st.session_state.processed_docs)}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card-horizontal'><div class='metric-label'>⏳ Tiempo Ahorrado</div><div class='metric-val'>{tiempo_display}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card-horizontal'><div class='metric-label'>💸 Dinero Ahorrado</div><div class='metric-val'>${roi['dinero_ahorrado_usd']} USD</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card-horizontal'><div class='metric-label'>⚡ Eficiencia</div><div class='metric-val'>{roi['eficiencia_porcentaje']}%</div></div>", unsafe_allow_html=True)

    st.caption(f"📊 Costo Operativo Estimado del Pipeline de IA: **${roi['costo_ia_usd']} USD** frente a los **${roi['costo_manual_usd']} USD** del proceso tradicional manual.")

    # ==========================================
    # BI DASHBOARD REPOTENCIADO (COMPACTADO LADO A LADO)
    # ==========================================
    st.write("")
    st.write("### 📈 Visualización Avanzada de Carga Financiera")
    
    headers_list = [{k: v for k, v in doc.items() if k != 'items'} for doc in st.session_state.processed_docs]
    df_hd = pd.DataFrame(headers_list)
    
    df_hd['total_pagar'] = pd.to_numeric(df_hd['total_pagar'], errors='coerce').fillna(0.0)
    df_hd['proveedor'] = df_hd['proveedor'].fillna('Desconocido')
    df_hd['tipo_documento'] = df_hd['tipo_documento'].fillna('Desconocido')
    df_hd['moneda'] = df_hd['moneda'].fillna('N/A')

    # 🎯 CONTROL PERIMETRAL: El doble candado para quitar espacios fantasmas en strings
    if not df_hd.empty:
        df_hd['moneda'] = df_hd['moneda'].astype(str).str.strip()
        df_hd['proveedor'] = df_hd['proveedor'].astype(str).str.strip()

    # Dividimos el espacio horizontal en 2 columnas paralelas para contener perfectamente las barras
    col_grafico1, col_grafico2 = st.columns(2)

    with col_grafico1:
        st.markdown("**💰 Concentración de Gastos por Proveedor y Divisa**")
        if not df_hd.empty:
            # 🎯 ALTAIR OPTIMIZADO: Consume df_hd (100% plano, serializable y libre de crashes)
            chart_spend = alt.Chart(df_hd).mark_bar(size=35).encode(
                x=alt.X('proveedor:N', title='Proveedor', axis=alt.Axis(labelAngle=0, labelAlign='center', labelPadding=8)),
                y=alt.Y('total_pagar:Q', title='Monto Total Acumulado'),
                color=alt.Color('moneda:N', title='Divisa', scale=alt.Scale(scheme='tableau10')),
                tooltip=['proveedor', 'moneda', 'total_pagar']
            ).properties(height=320).interactive()
        
            st.altair_chart(chart_spend, use_container_width=True)
            st.caption("Análisis por divisa unificada.")

    with col_grafico2:
        st.markdown("**🗂️ Volumen Operativo por Categoría de Documento**")
        if not df_hd.empty:
            df_counts = df_hd['tipo_documento'].value_counts().reset_index()
            df_counts.columns = ['tipo_documento', 'count']
            
            chart_counts = alt.Chart(df_counts).mark_bar(size=35).encode(
                x=alt.X('tipo_documento:N', title='Categoría de Documento', axis=alt.Axis(labelAngle=0, labelAlign='center', labelPadding=8)),
                y=alt.Y('count:Q', title='Cantidad de Comprobantes'),
                color=alt.Color('tipo_documento:N', title='Tipo', scale=alt.Scale(scheme='tableau10')),
                tooltip=['tipo_documento', 'count']
            ).properties(height=320).interactive()
        
            st.altair_chart(chart_counts, use_container_width=True)
            st.caption("Clasificación semántica automatizada por lote.")

    # ==========================================
    # El Botón de Oro: Exportación Directa a Excel ERP
    # ==========================================
    st.write("")
    excel_filename = "reporte_automatizacion_documentos.xlsx"
    generate_enterprise_excel(st.session_state.processed_docs, excel_filename)
    
    with open(excel_filename, "rb") as file_excel:
        st.download_button(
            label="📥 Descargar Reporte Unificado para Contabilidad (Excel)",
            data=file_excel,
            file_name=excel_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="secondary"
        )

    # ==========================================
    # Visualización de Estructuras Relacionales (Tabs)
    # ==========================================
    st.write("")
    tab1, tab2, tab3 = st.tabs(["📋 Tabla Consolidada (Cabeceras)", "🔍 Detalle de Líneas de Ítems", "🤖 JSON de Auditoría"])
    
    with tab1:
        st.write("### Datos Generales Extraídos por Documento")
        st.dataframe(df_hd, use_container_width=True)
        
    with tab2:
        st.write("### Desglose Detallado de Artículos (Trazabilidad Relacional)")
        all_items = []
        for doc in st.session_state.processed_docs:
            for item in doc.get("items", []):
                item_row = {"Proveedor": doc.get("proveedor"), **item}
                all_items.append(item_row)
        st.dataframe(pd.DataFrame(all_items), use_container_width=True)
        
    with tab3:
        st.write("### Esquema Estricto de Datos Estructurados")
        st.json(st.session_state.processed_docs)