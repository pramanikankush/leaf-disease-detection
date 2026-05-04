"""
🔄 Plant Disease Comparison Tool
AI-powered comparison of diseases and treatments
"""

import streamlit as st

st.set_page_config(page_title="Compare Diseases", page_icon="🔄", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
p, span, label { font-size: 1.1rem !important; line-height: 1.6; }
h1 { font-size: 2.5rem !important; font-weight: 800 !important; }
h2, h3 { font-size: 1.3rem !important; font-weight: 700 !important; }
.disease-comparison { background: #FFFFFF; border: 2px solid #E0E0E0; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

st.title("🔄 Plant Disease Comparison")
st.write("AI-powered comparison of symptoms, treatments, and prevention strategies.")

# Disease selector for comparison
st.subheader("Select diseases to compare")
col1, col2 = st.columns(2)

with col1:
    disease1 = st.text_input(
        "First disease:",
        placeholder="e.g., powdery mildew",
        key="disease1"
    )

with col2:
    disease2 = st.text_input(
        "Second disease:",
        placeholder="e.g., early blight",
        key="disease2"
    )

if disease1 and disease2 and st.button("🔄 Compare", type="primary", use_container_width=True):
    try:
        with st.spinner("🔍 Comparing diseases..."):
            from services.gemini_service_enhanced import compare_diseases, get_disease_info, GeminiServiceError
            
            # Get AI comparison
            comparison = compare_diseases([disease1, disease2])
            
            # Get individual disease info for detailed tabs
            info1 = get_disease_info(disease1)
            info2 = get_disease_info(disease2)
            
            st.markdown("---")
            st.subheader("📊 Overall Comparison")
            st.write(comparison.get('overall_comparison', 'N/A'))
            
            # Side-by-side disease info
            st.markdown("---")
            st.subheader("📋 Disease Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"### {info1.get('disease_name', disease1)}")
                st.write(f"**{info1.get('description', 'N/A')}**")
                
                st.markdown("**Symptoms:**")
                for symptom in info1.get('symptoms', [])[:3]:
                    st.markdown(f"• {symptom}")
                
                st.markdown("**Prevention:**")
                for prev in info1.get('prevention', [])[:3]:
                    st.markdown(f"• {prev}")
            
            with col2:
                st.markdown(f"### {info2.get('disease_name', disease2)}")
                st.write(f"**{info2.get('description', 'N/A')}**")
                
                st.markdown("**Symptoms:**")
                for symptom in info2.get('symptoms', [])[:3]:
                    st.markdown(f"• {symptom}")
                
                st.markdown("**Prevention:**")
                for prev in info2.get('prevention', [])[:3]:
                    st.markdown(f"• {prev}")
            
            # Severity and risk analysis
            st.markdown("---")
            st.subheader("⚠️ Severity Analysis")
            st.write(comparison.get('which_is_more_severe', 'N/A'))
            
            # Combined management
            st.markdown("---")
            st.subheader("🛠️ Combined Management Strategy")
            st.write(comparison.get('combined_management', 'N/A'))
            
            # Detailed tabs for full information
            st.markdown("---")
            
            tab1, tab2, tab3, tab4 = st.tabs([
                f"{disease1} - Full Info",
                f"{disease2} - Full Info",
                "Resistant Varieties",
                "Treatment Options"
            ])
            
            with tab1:
                st.markdown(f"### {disease1}")
                st.write(f"**Description:** {info1.get('description', 'N/A')}")
                st.write(f"**Season Alert:** {info1.get('season_alert', 'N/A')}")
                
                st.markdown("**Causes:**")
                for cause in info1.get('causes', []):
                    st.markdown(f"• {cause}")
                
                st.markdown("**Affected Crops:**")
                st.write(", ".join(info1.get('affected_crops', [])))
            
            with tab2:
                st.markdown(f"### {disease2}")
                st.write(f"**Description:** {info2.get('description', 'N/A')}")
                st.write(f"**Season Alert:** {info2.get('season_alert', 'N/A')}")
                
                st.markdown("**Causes:**")
                for cause in info2.get('causes', []):
                    st.markdown(f"• {cause}")
                
                st.markdown("**Affected Crops:**")
                st.write(", ".join(info2.get('affected_crops', [])))
            
            with tab3:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**{disease1} - Resistant Varieties:**")
                    for var in info1.get('resistant_varieties', []):
                        st.markdown(f"• {var}")
                
                with col2:
                    st.markdown(f"**{disease2} - Resistant Varieties:**")
                    for var in info2.get('resistant_varieties', []):
                        st.markdown(f"• {var}")
            
            with tab4:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**{disease1} - Treatment:**")
                    for treatment in info1.get('treatment', []):
                        st.markdown(f"• {treatment}")
                
                with col2:
                    st.markdown(f"**{disease2} - Treatment:**")
                    for treatment in info2.get('treatment', []):
                        st.markdown(f"• {treatment}")
            
    except GeminiServiceError as e:
        st.error(f"❌ Comparison failed: {str(e)}")
        st.info("Check ⚙️ Settings to verify API configuration")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")

# Information section
st.markdown("---")
st.info("""
💡 **Tip:** Use this tool to:
- Compare symptoms between similar diseases
- Find treatments suitable for multiple disease risks
- Understand environmental conditions favoring each disease
- Choose resistant varieties that work best for your region
- Plan integrated disease management strategies
""")

# Common disease pairs to compare
st.markdown("---")
st.subheader("📚 Popular Comparisons")

common_pairs = [
    ("Powdery Mildew", "Early Blight"),
    ("Leaf Spot", "Septoria Leaf Blotch"),
    ("Blight", "Rust"),
]

st.write("Try comparing these disease pairs:")
for pair in common_pairs:
    st.caption(f"• {pair[0]} vs {pair[1]}")

