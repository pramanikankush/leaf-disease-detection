import streamlit as st
import json

st.set_page_config(page_title="Crop News", page_icon="📰", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
p, span, label { font-size: 1.1rem !important; }
h1 { font-size: 2.5rem !important; font-weight: 800 !important; }
h2 { font-size: 1.8rem !important; font-weight: 700 !important; }
h3 { font-size: 1.3rem !important; font-weight: 600 !important; }
.news-card {
    background: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 10px;
    padding: 1.2rem; margin-bottom: 1rem; box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.news-card h3 { margin-top: 0; margin-bottom: 0.6rem; font-size: 1.25rem !important; }
.news-card p { font-size: 1.05rem !important; line-height: 1.6; color: #444; }
.news-card .category { 
    display: inline-block; padding: 0.4rem 0.8rem; border-radius: 20px; 
    font-size: 0.85rem; font-weight: 600; margin-top: 0.8rem;
}
.category-disease { background: #FFEBEE; color: #C62828; }
.category-weather { background: #E1F5FE; color: #0277BD; }
.category-technology { background: #F3E5F5; color: #6A1B9A; }
.category-market { background: #FFF3E0; color: #E65100; }
.category-policy { background: #E8F5E9; color: #2E7D32; }
</style>
""", unsafe_allow_html=True)

st.title("📰 Latest Crop & Agriculture News")
st.write("AI-generated latest trends, tips, and news in the agricultural world.")

# Region selector
region = st.selectbox("Select Region:", ["Global", "North America", "Europe", "Asia", "Africa", "South America"])

# Generate news button
if st.button("🔄 Refresh News", type="primary", use_container_width=True):
    from services.gemini_service_enhanced import clear_cache
    clear_cache(f"news_{region}_10")
    st.rerun()

try:
    with st.spinner("🌍 Generating latest agricultural news..."):
        from services.gemini_service_enhanced import generate_agriculture_news, GeminiServiceError
        
        news_items = generate_agriculture_news(count=10, region=region)
        
        if news_items:
            st.success(f"✅ Generated {len(news_items)} news articles")
            st.markdown("---")
            
            for item in news_items:
                category = item.get("category", "general")
                category_class = f"category-{category}"
                
                st.markdown(f"""
                <div class="news-card">
                    <h3>📌 {item.get('title', 'News Item')}</h3>
                    <p>{item.get('summary', 'No summary available')}</p>
                    <span class="category {category_class}">{category.upper()}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No news generated. Please try again.")

except GeminiServiceError as e:
    st.error(f"❌ Could not generate news: {str(e)}")
    st.info("""
    **Troubleshooting:**
    - Check your API key in ⚙️ Settings
    - Verify internet connection
    - Try a different region
    - Wait a moment and refresh
    """)

except Exception as e:
    st.error(f"❌ Unexpected error: {str(e)}")
    st.info("Please refresh or try again later.")

# Info section
st.markdown("---")
st.info("""
💡 **About AI-Generated News:**
- News is generated in real-time using AI
- Content is relevant to selected region
- Mix of diseases, weather, technology, and policy
- Practical and actionable for farmers
""")


