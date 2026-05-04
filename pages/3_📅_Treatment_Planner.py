import streamlit as st
from services.gemini_service_enhanced import generate_treatment_schedule, clear_cache, GeminiServiceError
from utils.history_manager import get_history

st.set_page_config(page_title="Treatment Planner", page_icon="📅", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
p, span, label { font-size: 1.1rem !important; }
h1 { font-size: 2.5rem !important; font-weight: 800 !important; }
h2 { font-size: 1.8rem !important; font-weight: 700 !important; }
h3 { font-size: 1.3rem !important; font-weight: 600 !important; }
.stSlider label { font-size: 1.15rem !important; font-weight: 600 !important; }
.stTextInput label, .stSelectbox label { font-size: 1.15rem !important; font-weight: 600 !important; }
.severity-low { background: #E8F5E9; padding: 1rem; border-radius: 5px; }
.severity-medium { background: #FFF3E0; padding: 1rem; border-radius: 5px; }
.severity-high { background: #FFEBEE; padding: 1rem; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

st.title("📅 Treatment Planner")
st.write("Generate a day-by-day actionable schedule to cure plant diseases with AI guidance.")

# Option to select from recent history
history = get_history()
recent_diseases = []
severity_scores = {}

for r in history:
    disease = r.get('disease_name')
    if not r.get('is_healthy', False) and disease != 'Unknown':
        if disease not in recent_diseases:
            recent_diseases.append(disease)
            severity_scores[disease] = r.get('severity_score', 50)

disease_options = ["Type custom disease..."] + recent_diseases
selected_option = st.selectbox("Select a disease from your history, or type a custom one:", disease_options)

disease_name = ""
if selected_option == "Type custom disease...":
    disease_name = st.text_input("Enter the disease name (e.g., Apple Scab):")
else:
    disease_name = selected_option

# Duration slider
duration = st.slider("Schedule Duration (Days)", min_value=3, max_value=21, value=7)

# Severity selector
st.markdown("**Disease Severity:**")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🟢 Mild", use_container_width=True):
        severity = "mild"
        st.session_state.severity = severity

with col2:
    if st.button("🟡 Moderate", use_container_width=True):
        severity = "moderate"
        st.session_state.severity = severity

with col3:
    if st.button("🔴 Severe", use_container_width=True):
        severity = "severe"
        st.session_state.severity = severity

# Get severity from session or default
severity = st.session_state.get('severity', 'moderate')

# Show severity explanation
if severity == "mild":
    st.markdown('<div class="severity-low"><strong>🟢 Mild:</strong> Early detection, minimal spread, quick recovery expected</div>', unsafe_allow_html=True)
elif severity == "high":
    st.markdown('<div class="severity-high"><strong>🔴 Severe:</strong> Wide spread, significant damage, intensive treatment needed</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="severity-medium"><strong>🟡 Moderate:</strong> Active infection, visible spread, standard treatment sufficient</div>', unsafe_allow_html=True)

if st.button("📝 Generate Schedule", type="primary", use_container_width=True):
    if not disease_name.strip():
        st.warning("Please enter or select a disease name.")
    else:
        try:
            with st.spinner(f"🤖 Generating expert treatment timeline for {disease_name} ({severity})..."):
                schedule = generate_treatment_schedule(disease_name, duration, severity)
                st.success("✅ Treatment Schedule Generated!")
                
                st.markdown("---")
                st.markdown(schedule)
                st.markdown("---")
                st.caption("ℹ️ This is an AI-generated timeline and does not replace professional agricultural advice.")
                
                # Option to refresh
                if st.button("🔄 Generate Different Plan", help="Get a new schedule with variations"):
                    cache_key = f"treatment_{disease_name}_{duration}_{severity}"
                    clear_cache(cache_key)
                    st.rerun()
                    
        except GeminiServiceError as e:
            st.error(f"❌ Could not generate schedule: {str(e)}")
            st.info("Check ⚙️ Settings to verify API configuration")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")

# Information section
st.markdown("---")
st.info("""
**📋 How to Use:**
1. Select a disease from your scan history or enter a custom disease name
2. Choose how many days to plan (3-21 days)
3. Indicate disease severity (Mild/Moderate/Severe)
4. Click Generate Schedule to create a detailed treatment plan
5. Follow the day-by-day recommendations with timing and actions

**💡 Tips:**
- Start treatment early for best results
- Follow the exact day recommendations for effectiveness
- Monitor plants daily and adjust if needed
- Use the Weather Guide to find optimal treatment days
- Combine with Prevention Tips for long-term disease management
""")

