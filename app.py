from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import joblib
import os
import setuptools.dist

app = FastAPI(
    title="Symptom Recommendation System API",
    description="API for recommending medical conditions based on patient symptoms",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass  # Static directory might not exist

# Pydantic models
class SymptomInput(BaseModel):
    gender: str
    age: int
    symptoms: List[str]
    search_terms: Optional[str] = ""

class RecommendationResponse(BaseModel):
    recommendations: List[Dict[str, Any]]
    confidence_scores: List[float]
    similar_cases: List[Dict[str, Any]]

class HealthCheck(BaseModel):
    status: str
    message: str

# Global variables for the recommendation system
symptom_data = None
tfidf_vectorizer = None
symptom_vectors = None
scaler = None

def load_and_preprocess_data():
    """Load and preprocess the symptom data"""
    global symptom_data, tfidf_vectorizer, symptom_vectors, scaler
    
    try:
        # Load the CSV data
        df = pd.read_csv('ai_symptom_picker.csv')
        
        # Extract symptoms from JSON summary
        def extract_symptoms(row):
            try:
                summary = json.loads(row['summary'])
                yes_symptoms = summary.get('yes_symptoms', [])
                symptoms = [symptom['text'] for symptom in yes_symptoms]
                return ' '.join(symptoms)
            except:
                return ""
        
        df['extracted_symptoms'] = df.apply(extract_symptoms, axis=1)
        
        # Combine symptoms with search terms for better matching
        df['combined_text'] = df['extracted_symptoms'] + ' ' + df['search_term'].fillna('')
        
        # Create TF-IDF vectors
        tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words=None,  # Keep medical terms
            ngram_range=(1, 2),
            min_df=2
        )
        
        symptom_vectors = tfidf_vectorizer.fit_transform(df['combined_text'])
        
        # Prepare age scaler
        scaler = StandardScaler()
        age_scaled = scaler.fit_transform(df[['age']].values)
        df['age_scaled'] = age_scaled
        
        symptom_data = df
        print(f"Data loaded successfully: {len(df)} records")
        
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

def get_symptom_similarity(input_symptoms: str, top_k: int = 5):
    """Get similar cases based on symptoms"""
    if tfidf_vectorizer is None or symptom_vectors is None:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    # Vectorize input symptoms
    input_vector = tfidf_vectorizer.transform([input_symptoms])
    
    # Calculate similarity
    similarities = cosine_similarity(input_vector, symptom_vectors).flatten()
    
    # Get top similar cases
    top_indices = similarities.argsort()[-top_k:][::-1]
    
    similar_cases = []
    for idx in top_indices:
        if similarities[idx] > 0:  # Only include cases with some similarity
            case = symptom_data.iloc[idx]
            similar_cases.append({
                'id': int(idx),
                'gender': case['gender'],
                'age': int(case['age']),
                'symptoms': case['extracted_symptoms'],
                'search_terms': case['search_term'],
                'similarity_score': float(similarities[idx])
            })
    
    return similar_cases

def analyze_symptom_patterns(symptoms: List[str]) -> Dict[str, Any]:
    """Analyze symptom patterns and provide insights"""
    if symptom_data is None:
        return {}
    
    # Count symptom frequencies
    all_symptoms = []
    for _, row in symptom_data.iterrows():
        if row['extracted_symptoms']:
            all_symptoms.extend(row['extracted_symptoms'].split())
    
    symptom_counts = pd.Series(all_symptoms).value_counts()
    
    # Find common co-occurring symptoms
    input_symptom_set = set(symptoms)
    co_occurring = {}
    
    for _, row in symptom_data.iterrows():
        if row['extracted_symptoms']:
            case_symptoms = set(row['extracted_symptoms'].split())
            if input_symptom_set.intersection(case_symptoms):
                for symptom in case_symptoms - input_symptom_set:
                    co_occurring[symptom] = co_occurring.get(symptom, 0) + 1
    
    return {
        'common_symptoms': symptom_counts.head(10).to_dict(),
        'co_occurring_symptoms': dict(sorted(co_occurring.items(), key=lambda x: x[1], reverse=True)[:5])
    }

def get_age_based_recommendations(age: int, symptoms: List[str]) -> List[str]:
    """Get age-specific recommendations"""
    if symptom_data is None:
        return []
    
    # Filter data by age group
    age_group = 'young' if age < 30 else 'middle' if age < 60 else 'elderly'
    
    age_ranges = {
        'young': (0, 30),
        'middle': (30, 60),
        'elderly': (60, 120)
    }
    
    min_age, max_age = age_ranges[age_group]
    age_filtered = symptom_data[(symptom_data['age'] >= min_age) & (symptom_data['age'] <= max_age)]
    
    # Get common symptoms in this age group
    common_symptoms = []
    for _, row in age_filtered.iterrows():
        if row['extracted_symptoms']:
            common_symptoms.extend(row['extracted_symptoms'].split())
    
    symptom_counts = pd.Series(common_symptoms).value_counts()
    return symptom_counts.head(5).index.tolist()

@app.on_event("startup")
async def startup_event():
    """Initialize the recommendation system on startup"""
    load_and_preprocess_data()

@app.get("/")
async def root_redirect():
    """Redirect root to web interface"""
    return RedirectResponse(url="/web", status_code=302)

@app.get("/status", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Symptom Recommendation System API is running"
    }

@app.get("/web")
async def web_interface():
    """Serve the web interface"""
    try:
        return FileResponse("static/index.html")
    except:
        return {
            "message": "Web interface not available. Use /docs for API documentation."
        }

@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(input_data: SymptomInput):
    """Get symptom-based recommendations"""
    try:
        # Prepare input symptoms
        input_symptoms_text = ' '.join(input_data.symptoms)
        if input_data.search_terms:
            input_symptoms_text += ' ' + input_data.search_terms
        
        # Get similar cases
        similar_cases = get_symptom_similarity(input_symptoms_text, top_k=10)
        
        # Analyze patterns
        pattern_analysis = analyze_symptom_patterns(input_data.symptoms)
        
        # Get age-based recommendations
        age_recommendations = get_age_based_recommendations(input_data.age, input_data.symptoms)
        
        # Calculate confidence scores based on similarity
        confidence_scores = [case['similarity_score'] for case in similar_cases]
        
        # Prepare recommendations
        recommendations = []
        for i, case in enumerate(similar_cases):
            recommendations.append({
                'case_id': case['id'],
                'demographics': {
                    'gender': case['gender'],
                    'age': case['age']
                },
                'symptoms': case['symptoms'],
                'search_terms': case['search_terms'],
                'confidence': case['similarity_score'],
                'age_group': 'young' if case['age'] < 30 else 'middle' if case['age'] < 60 else 'elderly'
            })
        
        return RecommendationResponse(
            recommendations=recommendations,
            confidence_scores=confidence_scores,
            similar_cases=similar_cases
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.get("/symptoms/analysis")
async def analyze_symptoms(symptoms: str):
    """Analyze specific symptoms and provide insights"""
    try:
        symptom_list = [s.strip() for s in symptoms.split(',')]
        analysis = analyze_symptom_patterns(symptom_list)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing symptoms: {str(e)}")

@app.get("/demographics/age-group/{age}")
async def get_age_group_insights(age: int):
    """Get insights for specific age group"""
    try:
        age_recommendations = get_age_based_recommendations(age, [])
        return {
            "age": age,
            "age_group": 'young' if age < 30 else 'middle' if age < 60 else 'elderly',
            "common_symptoms": age_recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting age group insights: {str(e)}")

@app.get("/stats")
async def get_statistics():
    """Get dataset statistics"""
    try:
        if symptom_data is None:
            raise HTTPException(status_code=500, detail="Data not loaded")
        
        stats = {
            "total_records": len(symptom_data),
            "gender_distribution": symptom_data['gender'].value_counts().to_dict(),
            "age_statistics": {
                "mean": float(symptom_data['age'].mean()),
                "median": float(symptom_data['age'].median()),
                "min": int(symptom_data['age'].min()),
                "max": int(symptom_data['age'].max())
            },
            "unique_symptoms": len(set(' '.join(symptom_data['extracted_symptoms'].dropna()).split()))
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 