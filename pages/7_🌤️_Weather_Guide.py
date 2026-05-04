"""
🌤️ Weather-Based Treatment Guide
Get optimal treatment timing based on weather analysis
"""

import streamlit as st

st.set_page_config(page_title="Weather Guide", page_icon="🌤️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
p, span, label { font-size: 1.1rem !important; line-height: 1.6; }
h1 { font-size: 2.5rem !important; font-weight: 800 !important; }
h2, h3 { font-size: 1.3rem !important; font-weight: 700 !important; }
.risk-badge {
    display: inline-block; padding: 0.5rem 1rem; border-radius: 5px;
    font-weight: 600; margin: 0.3rem;
}
.risk-high { background: #FFEBEE; color: #C62828; }
.risk-medium { background: #FFF3E0; color: #E65100; }
.risk-low { background: #E8F5E9; color: #2E7D32; }
</style>
""", unsafe_allow_html=True)

st.title("🌤️ Weather-Based Treatment Guide")
st.write("AI-powered weather analysis for optimal farm treatment planning.")

st.info("""
💡 **How it works:**
- Enter your region or location
- Get AI-analyzed weather forecast
- Find the best days to apply treatments
- Understand disease risk based on weather patterns
""")

# Location input
location = st.text_input(
    "Enter your region or location:",
    value="your region",
    placeholder="e.g., New York, California, Kansas, etc.",
    help="Any location name - AI will analyze weather patterns"
)

if st.button("📡 Get Weather Analysis", type="primary", use_container_width=True):
    try:
        with st.spinner(f"🌍 Analyzing weather for '{location}'..."):
            from services.gemini_service_enhanced import get_weather_recommendations, GeminiServiceError
            
            weather_data = get_weather_recommendations(location)
            
            # Display forecast summary
            st.markdown("---")
            st.subheader("📊 Forecast Summary")
            st.write(weather_data.get('forecast_summary', 'N/A'))
            
            # Best treatment days
            st.markdown("---")
            st.subheader("🎯 Best Days for Treatment")
            
            optimal_days = weather_data.get('treatment_optimal_days', [])
            if optimal_days:
                st.success(f"✅ Identified {len(optimal_days)} optimal treatment days")
                for day in optimal_days:
                    st.markdown(f"• {day}")
            else:
                st.info("Check detailed recommendations below")
            
            # Disease risk assessment
            st.markdown("---")
            st.subheader("⚠️ Disease Risk by Weather")
            
            disease_risks = weather_data.get('disease_risks', [])
            if disease_risks:
                for risk_item in disease_risks:
                    disease = risk_item.get('disease', 'Unknown')
                    risk_level = risk_item.get('risk_level', 'MEDIUM')
                    reason = risk_item.get('reason', '')
                    
                    risk_class = f"risk-{risk_level.lower()}"
                    st.markdown(f"""
                    <span class="risk-badge {risk_class}">{risk_level}</span>
                    **{disease}**
                    """, unsafe_allow_html=True)
                    
                    st.caption(f"🔍 {reason}")
                    st.markdown("")
            
            # General recommendations
            st.markdown("---")
            st.subheader("💡 Treatment Recommendations")
            
            recommendations = weather_data.get('recommendations', [])
            if recommendations:
                for rec in recommendations:
                    st.markdown(f"• {rec}")
            
            # Best time to treat
            st.markdown("---")
            st.subheader("⏰ Best Time to Treat")
            st.info(weather_data.get('best_time_to_treat', 'Consult detailed analysis'))
            
            # Watering schedule
            st.markdown("---")
            st.subheader("💧 Watering Schedule")
            st.write(weather_data.get('watering_schedule', 'Monitor soil moisture regularly'))
            
    except GeminiServiceError as e:
        st.error(f"❌ Could not generate weather analysis: {str(e)}")
        st.info("""
        **Troubleshooting:**
        - Check your API key in ⚙️ Settings
        - Try a different location name
        - Verify internet connection
        """)
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")

# Treatment best practices
st.markdown("---")
st.subheader("💡 Treatment Timing Best Practices")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **✅ DO:**
    - Apply treatments early morning (5-9 AM)
    - Choose calm days (wind < 10 mph)
    - Treat when no rain forecast for 24 hours
    - Spray when temps are 60-80°F
    - Re-apply after rain per product label
    - Rotate fungicide types every 2 weeks
    """)

with col2:
    st.markdown("""
    **❌ DON'T:**
    - Spray in high winds (drifts off target)
    - Treat before/during/after rain
    - Spray in extreme heat (>85°F)
    - Spray in extreme cold (<50°F)
    - Apply multiple fungicides same day
    - Spray with high humidity (>90%)
    """)

# How to use this tool
st.markdown("---")
st.info("""
**📋 How to use this weather guide:**

1. **Enter your location** - Any region name (AI understands geography)
2. **Review treatment days** - Find optimal spray timing
3. **Check disease risks** - Know what threats weather patterns create
4. **Follow recommendations** - AI-powered tips for your region
5. **Monitor regularly** - Conditions change, check weekly during season

**Pro tip:** Combine with your Treatment Planner for maximum effectiveness!
""")

