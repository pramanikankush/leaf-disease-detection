"""
📚 Disease Library & Gallery
AI-powered disease information database
"""

import streamlit as st

st.set_page_config(page_title="Disease Gallery", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
p, span, label { font-size: 1.1rem !important; line-height: 1.6; }
h1 { font-size: 2.5rem !important; font-weight: 800 !important; }
h2, h3 { font-size: 1.3rem !important; font-weight: 700 !important; }
.disease-card { background: #FFFFFF; border: 2px solid #E0E0E0; border-radius: 10px; padding: 1.2rem; transition: all 0.3s ease; }
.disease-card:hover { border-color: #2E7D32; box-shadow: 0 4px 12px rgba(46, 125, 50, 0.15); }
.disease-card h4 { margin: 0 0 0.8rem; color: #1B5E20; font-size: 1.2rem !important; }
.disease-card p { margin: 0; font-size: 1.05rem !important; color: #666; }
.severity-badge {
    display: inline-block; padding: 0.4rem 0.8rem; border-radius: 20px; 
    font-weight: 600; font-size: 0.9rem; margin-top: 0.5rem;
}
.severity-low { background: #E8F5E9; color: #2E7D32; }
.severity-medium { background: #FFF3E0; color: #E65100; }
.severity-high { background: #FFEBEE; color: #C62828; }
.severity-critical { background: #B71C1C; color: #FFFFFF; }
</style>
""", unsafe_allow_html=True)

st.title("📚 Plant Disease Library")
st.write("AI-powered database of plant diseases with real-time information.")

# View mode selection
view_mode = st.radio(
    "Browse Mode:",
    ["🔍 Search Disease", "📖 Common Diseases", "📊 Compare"],
    horizontal=True
)

if view_mode == "🔍 Search Disease":
    st.subheader("Search Disease Information")
    
    disease_search = st.text_input(
        "Enter disease name:",
        placeholder="e.g., powdery mildew, early blight, rust",
        help="Search any plant disease"
    )
    
    if disease_search and st.button("🔎 Get Information", type="primary", use_container_width=True):
        try:
            with st.spinner(f"🌍 Fetching information on '{disease_search}'..."):
                from services.gemini_service_enhanced import get_disease_info, GeminiServiceError
                
                disease_data = get_disease_info(disease_search)
                
                # Display disease information
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"### {disease_data.get('disease_name', disease_search)}")
                    st.write(f"**{disease_data.get('description', 'N/A')}**")
                
                with col2:
                    severity = disease_data.get('severity', 'MEDIUM').upper()
                    severity_class = f"severity-{severity.lower()}"
                    st.markdown(f"""
                    <span class="severity-badge {severity_class}">
                        {severity}
                    </span>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Information tabs
                tab1, tab2, tab3, tab4, tab5 = st.tabs(["Symptoms", "Prevention", "Treatment", "Resistant Varieties", "Details"])
                
                with tab1:
                    st.markdown("**🩺 Symptoms:**")
                    for symptom in disease_data.get('symptoms', []):
                        st.markdown(f"• {symptom}")
                
                with tab2:
                    st.markdown("**🛡️ Prevention:**")
                    for prevention in disease_data.get('prevention', []):
                        st.markdown(f"• {prevention}")
                
                with tab3:
                    st.markdown("**💊 Treatment:**")
                    for treatment in disease_data.get('treatment', []):
                        st.markdown(f"• {treatment}")
                
                with tab4:
                    st.markdown("**✅ Resistant Varieties:**")
                    for variety in disease_data.get('resistant_varieties', []):
                        st.markdown(f"• {variety}")
                
                with tab5:
                    st.markdown("**📋 Details:**")
                    st.write(f"**Affected Crops:** {', '.join(disease_data.get('affected_crops', []))}")
                    st.write(f"**Season Alert:** {disease_data.get('season_alert', 'Year-round')}")
                    st.write(f"**Causes:** {', '.join(disease_data.get('causes', []))}")
                
        except GeminiServiceError as e:
            st.error(f"❌ Could not fetch disease information: {str(e)}")
            st.info("Check ⚙️ Settings to verify API configuration")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")

elif view_mode == "📖 Common Diseases":
    st.subheader("Common Plant Diseases")
    
    common_diseases = [
        "Early Blight", "Powdery Mildew", "Leaf Spot", 
        "Septoria Leaf Blotch", "Blight", "Rust"
    ]
    
    selected_disease = st.selectbox("Select a disease:", common_diseases)
    
    if st.button("ℹ️ Get Details", type="primary", use_container_width=True):
        try:
            with st.spinner(f"🌍 Fetching information on '{selected_disease}'..."):
                from services.gemini_service_enhanced import get_disease_info, GeminiServiceError
                
                disease_data = get_disease_info(selected_disease)
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"### {selected_disease}")
                    st.write(disease_data.get('description', 'N/A'))
                with col2:
                    severity = disease_data.get('severity', 'MEDIUM').upper()
                    severity_class = f"severity-{severity.lower()}"
                    st.markdown(f"""
                    <span class="severity-badge {severity_class}">{severity}</span>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Prevention Tips:**")
                    for tip in disease_data.get('prevention', [])[:3]:
                        st.markdown(f"✓ {tip}")
                with col2:
                    st.markdown("**Resistant Varieties:**")
                    for var in disease_data.get('resistant_varieties', [])[:3]:
                        st.markdown(f"✓ {var}")
                
        except GeminiServiceError as e:
            st.error(f"❌ Error: {str(e)}")

else:  # Compare mode
    st.subheader("Compare Diseases")
    
    col1, col2 = st.columns(2)
    with col1:
        disease1 = st.text_input("First disease:", placeholder="e.g., powdery mildew")
    with col2:
        disease2 = st.text_input("Second disease:", placeholder="e.g., early blight")
    
    if disease1 and disease2 and st.button("🔄 Compare", type="primary", use_container_width=True):
        try:
            with st.spinner("🔍 Comparing diseases..."):
                from services.gemini_service_enhanced import compare_diseases, GeminiServiceError
                
                comparison = compare_diseases([disease1, disease2])
                
                st.markdown(f"## {disease1} vs {disease2}")
                st.write(comparison.get('overall_comparison', 'N/A'))
                
                st.markdown("---")
                
                st.subheader("Severity Analysis")
                st.write(comparison.get('which_is_more_severe', 'N/A'))
                
                st.markdown("---")
                
                st.subheader("Combined Management")
                st.write(comparison.get('combined_management', 'N/A'))
                
        except GeminiServiceError as e:
            st.error(f"❌ Comparison failed: {str(e)}")

# Footer
st.markdown("---")
st.info("""
💡 **About This Library:**
- All disease information is AI-generated
- Data is current and practical
- Based on real agricultural practices
- Results are cached for performance
""")

