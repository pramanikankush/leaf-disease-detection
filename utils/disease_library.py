"""
Offline disease library with prevention tips and care guides.
"""

DISEASE_DATABASE = {
    "Early Blight": {
        "description": "Fungal disease causing circular brown spots on leaves",
        "prevention": [
            "Remove lower leaves from plant (6-8 inches)",
            "Water at the base, not from overhead",
            "Ensure proper air circulation between plants",
            "Mulch soil to prevent spore splash",
            "Rotate crops yearly",
            "Remove infected leaves immediately"
        ],
        "best_practices": [
            "Space plants 18-24 inches apart",
            "Prune suckers to improve airflow",
            "Avoid handling wet plants",
            "Sterilize pruning tools between cuts",
            "Water in early morning only",
            "Keep garden clean of debris"
        ],
        "resistant_varieties": ["Defiant", "Mountain Fresh", "Iron Lady"],
        "season_alert": "Most common in warm, wet summers"
    },
    
    "Powdery Mildew": {
        "description": "White coating on leaves reducing photosynthesis",
        "prevention": [
            "Ensure proper spacing for air circulation",
            "Avoid overhead watering",
            "Remove infected leaves promptly",
            "Apply sulfur-based fungicides preventively",
            "Keep humidity below 50% when possible",
            "Prune dense foliage"
        ],
        "best_practices": [
            "Monitor plants weekly during warm season",
            "Clean tools after each use",
            "Avoid touching infected plants",
            "Maintain steady watering schedule",
            "Remove weeds near base",
            "Use drip irrigation system"
        ],
        "resistant_varieties": ["Delicious", "Gala", "Freedom"],
        "season_alert": "Peaks in spring and fall with cool nights and warm days"
    },
    
    "Leaf Spot": {
        "description": "Various fungal/bacterial spots reducing leaf viability",
        "prevention": [
            "Practice crop rotation (3-4 year cycle)",
            "Water directly at soil level",
            "Apply copper or sulfur fungicides",
            "Remove and destroy infected leaves",
            "Keep foliage dry during evening",
            "Thin canopy for better air flow"
        ],
        "best_practices": [
            "Scout plants 2-3 times weekly",
            "Sanitize pruning equipment",
            "Avoid overhead irrigation",
            "Mulch to 3-4 inches depth",
            "Feed plant calcium (prevents some spots)",
            "Compost only healthy plant material"
        ],
        "resistant_varieties": ["Keepsake", "Priscilla", "Sterling"],
        "season_alert": "Most active in humid conditions during growing season"
    },
    
    "Septoria Leaf Blotch": {
        "description": "Circular spots with dark borders and gray centers",
        "prevention": [
            "Remove infected leaves below first fruit cluster",
            "Mulch soil with 3-4 inches of organic matter",
            "Space plants for maximum air circulation",
            "Water only at base in early morning",
            "Use fungicide at first sign of disease",
            "Clean up plant debris at season end"
        ],
        "best_practices": [
            "Don't handle plants when wet",
            "Wash hands/tools between plants",
            "Stake plants to improve airflow",
            "Maintain consistent moisture (1-2 inches/week)",
            "Fertilize every 2-3 weeks",
            "Avoid high nitrogen fertilizers"
        ],
        "resistant_varieties": ["Mountain Magic", "Defiant", "Mountain Merit"],
        "season_alert": "Spreads rapidly in warm, wet weather"
    },
    
    "Blight": {
        "description": "Severe fungal disease causing rapid plant death",
        "prevention": [
            "Plant resistant varieties",
            "Avoid planting near infected areas",
            "Remove infected plants immediately",
            "Apply preventive copper fungicide weekly",
            "Ensure excellent drainage",
            "Mulch heavily to prevent soil splash"
        ],
        "best_practices": [
            "Check plants daily during growing season",
            "Remove lower 8-12 inches of foliage",
            "Don't work in wet garden",
            "Use drip irrigation only",
            "Prune branches touching ground",
            "Sanitize tools after each cut"
        ],
        "resistant_varieties": ["Jewell", "Katahdin", "Kennebec"],
        "season_alert": "Critical risk during cool, wet springs and falls"
    },
    
    "Rust": {
        "description": "Orange/brown pustules on leaf underside",
        "prevention": [
            "Water only at soil level",
            "Improve air circulation",
            "Remove infected leaves immediately",
            "Apply sulfur-based fungicide weekly",
            "Avoid handling wet foliage",
            "Clean up fallen leaves"
        ],
        "best_practices": [
            "Scout plants 2x weekly for early detection",
            "Space plants wide apart",
            "Prune lower foliage regularly",
            "Maintain consistent watering",
            "Keep surrounding areas weed-free",
            "Dispose of infected material in trash"
        ],
        "resistant_varieties": ["Resilient", "Defender", "Guard"],
        "season_alert": "Most problematic in humid conditions"
    },
    
    "Healthy": {
        "description": "Plant is in good health with no visible disease",
        "prevention": [
            "Continue regular watering schedule",
            "Monitor for early disease signs weekly",
            "Maintain proper spacing for airflow",
            "Keep area clean of dead leaves/debris",
            "Provide balanced nutrition monthly",
            "Prune as needed to maintain shape"
        ],
        "best_practices": [
            "Water 1-2 inches per week consistently",
            "Fertilize every 2-3 weeks during growing season",
            "Inspect new growth regularly",
            "Remove lower yellowing leaves",
            "Provide support structures as needed",
            "Keep mulch 2-3 inches from base"
        ],
        "resistant_varieties": ["All healthy plants are doing great!"],
        "season_alert": "Maintain prevention routine year-round"
    }
}


def get_prevention_tips(disease_name: str) -> dict:
    """Retrieve prevention tips for a specific disease."""
    return DISEASE_DATABASE.get(disease_name, DISEASE_DATABASE.get("Healthy", {}))


def get_all_diseases() -> list:
    """Get list of all diseases in library."""
    return sorted(list(DISEASE_DATABASE.keys()))


def search_diseases(query: str) -> list:
    """Search disease database by keyword."""
    query = query.lower()
    results = []
    for disease, info in DISEASE_DATABASE.items():
        if (query in disease.lower() or 
            query in info["description"].lower()):
            results.append(disease)
    return results
