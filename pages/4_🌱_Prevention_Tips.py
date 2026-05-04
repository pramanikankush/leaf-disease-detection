"""
🌱 Disease Prevention Tips & Best Practices Guide
"""

import streamlit as st

st.set_page_config(page_title="Prevention Tips", page_icon="🌱", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
p, span, label { font-size: 1.1rem !important; line-height: 1.6; }
h1 { font-size: 2.5rem !important; font-weight: 800 !important; }
h2 { font-size: 1.8rem !important; font-weight: 700 !important; }
h3 { font-size: 1.3rem !important; font-weight: 600 !important; }
.prevention-card { background: #F1F8E9; border-left: 5px solid #2E7D32; padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem; }
.practice-list { background: #FFFFFF; border: 2px solid #E0E0E0; padding: 1.2rem; border-radius: 10px; margin: 0.8rem 0; }
.practice-list li { font-size: 1.05rem !important; }
</style>
""", unsafe_allow_html=True)

st.title("🌱 Disease Prevention & Best Practices")
st.write("Learn how to prevent common plant diseases before they occur.")

# Disease input
disease_input = st.text_input(
    "Enter a disease name to view prevention strategies:",
    placeholder="e.g., powdery mildew, early blight, rust",
    help="Any plant disease"
)

if disease_input and st.button("🛡️ Get Prevention Tips", type="primary", use_container_width=True):
    try:
        with st.spinner(f"🌍 Fetching prevention strategies for '{disease_input}'..."):
            from services.gemini_service_enhanced import get_disease_info, GeminiServiceError
            
            disease_data = get_disease_info(disease_input)
            
            # Header section
            st.markdown(f"""
            <div class="prevention-card">
                <h3>{disease_data.get('disease_name', disease_input)}</h3>
                <p><strong>{disease_data.get('description', 'Disease management guide')}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Prevention and management tips
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🛡️ Prevention Tips")
                for tip in disease_data.get("prevention", []):
                    st.markdown(f"• {tip}")
            
            with col2:
                st.subheader("📋 Management Practices")
                for practice in disease_data.get("management_practices", []):
                    st.markdown(f"• {practice}")
            
            # Additional info
            st.markdown("---")
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.subheader("✅ Resistant Varieties")
                for var in disease_data.get("resistant_varieties", []):
                    st.markdown(f"• {var}")
            
            with col4:
                st.subheader("📅 Seasonal Alert")
                season_info = disease_data.get("season_alert", "Monitor throughout growing season")
                st.info(f"⚠️ {season_info}")
            
            # Causes and symptoms reference
            st.markdown("---")
            
            tab1, tab2, tab3 = st.tabs(["Causes", "Symptoms", "Treatment"])
            
            with tab1:
                st.markdown("**What causes this disease:**")
                for cause in disease_data.get("causes", []):
                    st.markdown(f"• {cause}")
            
            with tab2:
                st.markdown("**Visual symptoms to look for:**")
                for symptom in disease_data.get("symptoms", []):
                    st.markdown(f"• {symptom}")
            
            with tab3:
                st.markdown("**Treatment options:**")
                for treatment in disease_data.get("treatment", []):
                    st.markdown(f"• {treatment}")
                
    except GeminiServiceError as e:
        st.error(f"❌ Could not fetch prevention tips: {str(e)}")
        st.info("Check ⚙️ Settings to verify API configuration")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")

# Quick reference section
st.markdown("---")
st.subheader("📚 Universal Disease Prevention Strategies")

# General prevention tips applicable to all diseases
st.markdown("""
### Best Practices for All Crops

**Watering:**
- Water at soil level, never overhead
- Water in early morning (reduces disease spread)
- Maintain consistent moisture (1-2 inches/week)
- Use drip irrigation when possible

**Spacing & Airflow:**
- Space plants 18-24 inches apart
- Prune lower foliage for better circulation
- Thin dense canopy
- Avoid touching wet plants

**Sanitation:**
- Sterilize pruning tools between cuts
- Remove fallen leaves and debris
- Don't compost diseased material
- Clean tools with 10% bleach solution

**Nutrition & Health:**
- Maintain balanced fertilization
- Don't over-fertilize (excess nitrogen = weak growth)
- Provide adequate calcium (prevents some diseases)
- Keep pH in optimal range for crop

**Monitoring:**
- Scout plants 2-3 times weekly
- Check undersides of leaves regularly
- Remove infected leaves immediately
- Act at first sign of disease
""")

# Common diseases to explore
st.markdown("---")
st.subheader("💡 Quick Reference Diseases")

col1, col2, col3 = st.columns(3)

common_diseases = [
    "Early Blight",
    "Powdery Mildew",
    "Leaf Spot",
    "Septoria Leaf Blotch",
    "Blight",
    "Rust"
]

with col1:
    st.markdown("**Common Diseases:**")
    for disease in common_diseases[:2]:
        st.markdown(f"• {disease}")

with col2:
    for disease in common_diseases[2:4]:
        st.markdown(f"• {disease}")

with col3:
    for disease in common_diseases[4:]:
        st.markdown(f"• {disease}")

st.info("👆 Type any of these diseases above to learn detailed prevention strategies!")

