"""
📊 Disease Severity Timeline
Track disease progression over time with visual charts
"""

import streamlit as st
import json
from datetime import datetime, timedelta
from utils.history_manager import get_history
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Disease Timeline", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
p, span, label { font-size: 1.1rem !important; line-height: 1.6; }
h1 { font-size: 2.5rem !important; font-weight: 800 !important; }
h2, h3 { font-size: 1.3rem !important; font-weight: 700 !important; }
[data-testid="metric-container"] { background: #F5F5F5; border-radius: 10px; padding: 1.2rem; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Disease Severity Timeline")
st.write("Track how your plants are recovering with visual progression charts.")

# Get history
history = get_history()

if not history:
    st.info("📋 No scan history yet. Start by analyzing plant leaves to build your timeline!")
else:
    # Extract unique diseases
    diseases = {}
    for record in history:
        disease = record.get("disease_name", "Unknown")
        if disease != "Unknown" and not record.get("is_healthy"):
            if disease not in diseases:
                diseases[disease] = []
            
            # Add severity estimation based on confidence
            confidence_str = record.get("confidence", "0%").replace("%", "")
            try:
                confidence = int(confidence_str)
                # Severity inversely related to confidence (low confidence = more uncertainty = higher severity risk)
                severity = 100 - confidence if not record.get("is_healthy") else 0
            except:
                severity = 50
            
            diseases[disease].append({
                "timestamp": record.get("timestamp"),
                "date": datetime.strptime(record.get("timestamp"), "%Y-%m-%d %H:%M"),
                "confidence": confidence,
                "severity": severity,
                "symptoms": record.get("symptoms", []),
                "treatment": record.get("treatment", []),
                "severity_score": record.get("severity_score", 50)
            })
    
    if not diseases:
        st.info("No diseased plants in your history. All recent scans show healthy plants!")
    else:
        # Select disease to view timeline
        selected_disease = st.selectbox(
            "Select disease to view timeline:",
            sorted(list(diseases.keys()))
        )
        
        if selected_disease:
            disease_records = sorted(diseases[selected_disease], key=lambda x: x["date"])
            
            # Calculate progression
            st.subheader(f"📈 {selected_disease} - Progression Timeline")
            
            # Timeline stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Scans", len(disease_records))
            
            with col2:
                first_record = disease_records[0]
                st.metric("First Detected", first_record["date"].strftime("%b %d"))
            
            with col3:
                last_record = disease_records[-1]
                st.metric("Latest Scan", last_record["date"].strftime("%b %d"))
            
            with col4:
                days_span = (disease_records[-1]["date"] - disease_records[0]["date"]).days
                st.metric("Days Tracked", days_span if days_span > 0 else "Same day")
            
            # Create timeline charts
            st.markdown("---")
            
            tab1, tab2, tab3 = st.tabs(["📊 Severity Trend", "🎯 Confidence Score", "📋 Scan Details"])
            
            with tab1:
                # Severity timeline chart
                if len(disease_records) > 1:
                    fig = go.Figure()
                    
                    dates = [r["date"].strftime("%m/%d %H:%M") for r in disease_records]
                    severity_scores = [r["severity_score"] for r in disease_records]
                    
                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=severity_scores,
                        mode='lines+markers',
                        name='Severity Score',
                        line=dict(color='#FF6B6B', width=3),
                        marker=dict(size=10)
                    ))
                    
                    # Add trend line
                    if len(severity_scores) >= 2:
                        import numpy as np
                        z = np.polyfit(range(len(severity_scores)), severity_scores, 1)
                        p = np.poly1d(z)
                        trend = p(range(len(severity_scores)))
                        fig.add_trace(go.Scatter(
                            x=dates,
                            y=trend,
                            mode='lines',
                            name='Trend',
                            line=dict(color='rgba(255,107,107,0.3)', width=2, dash='dash')
                        ))
                    
                    fig.update_layout(
                        title=f"{selected_disease} - Severity Score Over Time",
                        xaxis_title="Date & Time",
                        yaxis_title="Severity Score (0-100)",
                        hovermode='x unified',
                        height=400,
                        template='plotly_white'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Interpretation
                    if severity_scores[-1] < severity_scores[0]:
                        st.success("✅ **Improving** - Severity is decreasing! Your treatment plan is working.")
                    elif severity_scores[-1] > severity_scores[0]:
                        st.warning("⚠️ **Worsening** - Severity is increasing. Consider intensifying treatment.")
                    else:
                        st.info("→ **Stable** - No significant change in severity. Continue current treatment.")
                else:
                    st.info("Only one scan available. Track multiple scans over time to see progression.")
            
            with tab2:
                # Confidence score chart
                if len(disease_records) > 1:
                    fig = go.Figure()
                    
                    dates = [r["date"].strftime("%m/%d %H:%M") for r in disease_records]
                    confidence = [r["confidence"] for r in disease_records]
                    
                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=confidence,
                        mode='lines+markers',
                        name='Confidence %',
                        line=dict(color='#4ECDC4', width=3),
                        marker=dict(size=10),
                        fill='tozeroy'
                    ))
                    
                    fig.update_layout(
                        title=f"Diagnosis Confidence Score Over Time",
                        xaxis_title="Date & Time",
                        yaxis_title="Confidence (%)",
                        yaxis=dict(range=[0, 100]),
                        hovermode='x unified',
                        height=400,
                        template='plotly_white'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    avg_confidence = sum(confidence) / len(confidence)
                    st.info(f"Average diagnosis confidence: **{avg_confidence:.1f}%**")
                else:
                    st.info("Only one scan available. Track multiple scans to compare confidence trends.")
            
            with tab3:
                # Detailed scan records
                st.subheader("📋 Detailed Scan History")
                
                for idx, record in enumerate(reversed(disease_records)):
                    with st.expander(f"Scan {len(disease_records)-idx} - {record['date'].strftime('%b %d, %Y at %H:%M')}", expanded=idx==0):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Severity Score", record["severity_score"])
                        with col2:
                            st.metric("Confidence", f"{record['confidence']}%")
                        with col3:
                            st.metric("Detected Disease", selected_disease)
                        
                        if record.get("symptoms"):
                            st.write("**Symptoms detected:**")
                            for symptom in record["symptoms"]:
                                st.markdown(f"• {symptom}")
                        
                        if record.get("treatment"):
                            st.write("**Recommended treatment:**")
                            for treatment in record["treatment"]:
                                st.markdown(f"• {treatment}")
            
            # Recommendations
            st.markdown("---")
            st.subheader("💡 Recommendations")
            
            latest = disease_records[-1]
            
            if latest["severity_score"] < 30:
                st.success("""
                ✅ **Great Progress!**
                - Continue current treatment for 1-2 more weeks
                - Monitor weekly to ensure disease doesn't return
                - Consider preventive measures for next season
                """)
            elif latest["severity_score"] < 60:
                st.info("""
                📋 **Moderate Status**
                - Continue treatment as recommended
                - Increase monitoring frequency
                - Ensure proper plant care (watering, spacing, etc.)
                - Re-scan in 5-7 days to check progress
                """)
            else:
                st.warning("""
                ⚠️ **Intensive Care Needed**
                - Consider strengthening treatment approach
                - Check environmental conditions (humidity, airflow, watering)
                - Scan again in 2-3 days to monitor closely
                - Consult Treatment Planner for step-by-step care guide
                """)

# Summary for healthy plants
if history:
    healthy_records = [r for r in history if r.get("is_healthy")]
    if healthy_records:
        st.markdown("---")
        st.success(f"✅ **{len(healthy_records)} healthy plant scan(s) in your history**")
