import streamlit as st
import os
from utils.history_manager import get_history, clear_history
from utils.pdf_generator import generate_pdf

st.set_page_config(page_title="Scan History", page_icon="🕒", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
p, span, label { font-size: 1.1rem !important; }
h1 { font-size: 2.5rem !important; font-weight: 800 !important; }
h2 { font-size: 1.8rem !important; font-weight: 700 !important; }
h3 { font-size: 1.3rem !important; font-weight: 600 !important; }
.history-header { background: linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem; }
.history-item { background: #FFFFFF; border-left: 5px solid #2E7D32; padding: 1.2rem; margin-bottom: 1rem; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.title("🕒 Scan History & Reports")
st.write("View past diagnoses and download professional PDF reports.")

records = get_history()

if not records:
    st.info("No scan history found. Go to the main page to analyze a leaf!")
else:
    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("🗑️ Clear All"):
            clear_history()
            st.rerun()

    for idx, record in enumerate(records):
        with st.expander(f"[{record.get('timestamp')}] {record.get('disease_name')} - {record.get('confidence')}"):
            # Create a layout for details and download button
            d_col1, d_col2 = st.columns([3, 1])
            
            with d_col1:
                st.write("**Symptoms:**")
                st.write(", ".join(record.get('symptoms', [])) if record.get('symptoms') else "None")
                st.write("**Treatment:**")
                st.write(", ".join(record.get('treatment', [])) if record.get('treatment') else "None")
                
            with d_col2:
                # Generate PDF path
                pdf_path = os.path.join("data", f"report_{record.get('id')}.pdf")
                
                # We generate the PDF on the fly if requested to save space
                try:
                    generate_pdf(record, pdf_path)
                    
                    with open(pdf_path, "rb") as pdf_file:
                        PDFbyte = pdf_file.read()
                        
                    st.download_button(
                        label="📄 Download PDF",
                        data=PDFbyte,
                        file_name=f"Diagnosis_{record.get('id')}.pdf",
                        mime="application/pdf",
                        key=f"dl_{idx}"
                    )
                except Exception as e:
                    st.error(f"Could not generate PDF: {e}")
