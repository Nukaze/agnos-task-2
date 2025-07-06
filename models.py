import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import joblib
import json
from typing import List, Dict, Any, Tuple
import setuptools.dist

class SymptomClassifier:
    """Advanced symptom classification model"""
    # TF–IDF + RandomForest	แปลงข้อความ → จำแนกอาการ
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
        self.is_trained = False
        
    def prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features for training"""
        # Extract symptoms
        symptoms = []
        labels = []
        
        for _, row in df.iterrows():
            try:
                summary = json.loads(row['summary'])
                yes_symptoms = summary.get('yes_symptoms', [])
                symptom_text = ' '.join([s['text'] for s in yes_symptoms])
                
                if symptom_text.strip():
                    symptoms.append(symptom_text)
                    # Create a simple label based on primary symptom
                    primary_symptom = yes_symptoms[0]['text'] if yes_symptoms else 'unknown'
                    labels.append(primary_symptom)
            except:
                continue
        
        return np.array(symptoms), np.array(labels)
    
    def train(self, df: pd.DataFrame):
        """Train the symptom classifier"""
        symptoms, labels = self.prepare_features(df)
        
        if len(symptoms) == 0:
            raise ValueError("No valid symptoms found in data")
        
        # Vectorize symptoms
        X = self.vectorizer.fit_transform(symptoms)
        
        # Train model
        self.model.fit(X, labels)
        self.is_trained = True
        
        # Calculate accuracy
        y_pred = self.model.predict(X)
        accuracy = accuracy_score(labels, y_pred)
        print(f"Model trained with accuracy: {accuracy:.3f}")
        
    def predict(self, symptoms: List[str]) -> Dict[str, float]:
        """Predict symptom categories"""
        if not self.is_trained:
            raise ValueError("Model not trained")
        
        symptom_text = ' '.join(symptoms)
        X = self.vectorizer.transform([symptom_text])
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba(X)[0]
        classes = self.model.classes_
        
        # Create result dictionary
        predictions = {}
        for class_name, prob in zip(classes, probabilities):
            predictions[class_name] = float(prob)
        
        return dict(sorted(predictions.items(), key=lambda x: x[1], reverse=True))

class SymptomClusterer:
    """Clustering model for symptom patterns"""
    # TF–IDF + K-Means + PCA	จัดกลุ่มอาการ, ลดมิติข้อมูล    
    
    def __init__(self, n_clusters=5):
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.vectorizer = TfidfVectorizer(max_features=300)
        self.pca = PCA(n_components=2)
        self.is_fitted = False
        
    def fit(self, df: pd.DataFrame):
        """Fit the clustering model"""
        # Extract symptoms
        symptoms = []
        for _, row in df.iterrows():
            try:
                summary = json.loads(row['summary'])
                yes_symptoms = summary.get('yes_symptoms', [])
                symptom_text = ' '.join([s['text'] for s in yes_symptoms])
                if symptom_text.strip():
                    symptoms.append(symptom_text)
            except:
                continue
        
        if len(symptoms) == 0:
            raise ValueError("No valid symptoms found")
        
        # Vectorize and cluster
        X = self.vectorizer.fit_transform(symptoms)
        self.kmeans.fit(X)
        
        # Reduce dimensions for visualization
        self.pca.fit(X.toarray())
        self.is_fitted = True
        
        print(f"Clustering model fitted with {len(symptoms)} samples")
        
    def get_clusters(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Get cluster information"""
        if not self.is_fitted:
            raise ValueError("Model not fitted")
        
        symptoms = []
        valid_indices = []
        
        for idx, row in df.iterrows():
            try:
                summary = json.loads(row['summary'])
                yes_symptoms = summary.get('yes_symptoms', [])
                symptom_text = ' '.join([s['text'] for s in yes_symptoms])
                if symptom_text.strip():
                    symptoms.append(symptom_text)
                    valid_indices.append(idx)
            except:
                continue
        
        if not symptoms:
            return []
        
        X = self.vectorizer.transform(symptoms)
        clusters = self.kmeans.predict(X)
        
        # Group by cluster
        cluster_data = {}
        for i, cluster_id in enumerate(clusters):
            if cluster_id not in cluster_data:
                cluster_data[cluster_id] = []
            
            original_idx = valid_indices[i]
            cluster_data[cluster_id].append({
                'id': int(original_idx),
                'symptoms': symptoms[i],
                'demographics': {
                    'gender': df.iloc[original_idx]['gender'],
                    'age': int(df.iloc[original_idx]['age'])
                }
            })
        
        return [
            {
                'cluster_id': cluster_id,
                'size': len(cases),
                'cases': cases,
                'centroid_symptoms': self._get_centroid_symptoms(cluster_id)
            }
            for cluster_id, cases in cluster_data.items()
        ]
    
    def _get_centroid_symptoms(self, cluster_id: int) -> List[str]:
        """Get representative symptoms for a cluster"""
        centroid = self.kmeans.cluster_centers_[cluster_id]
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Get top features for this cluster
        top_indices = centroid.argsort()[-10:][::-1]
        return [feature_names[i] for i in top_indices if centroid[i] > 0]

class SymptomRecommender:
    """Advanced symptom recommendation system"""
    # Similarity-based + insights	ร่วมผล classification + clustering + matching ในคิวเดียว
    
    def __init__(self):
        self.classifier = SymptomClassifier()
        self.clusterer = SymptomClusterer()
        self.symptom_data = None
        
    def train_models(self, df: pd.DataFrame):
        """Train all models"""
        self.symptom_data = df
        
        print("Training symptom classifier...")
        self.classifier.train(df)
        
        print("Training symptom clusterer...")
        self.clusterer.fit(df)
        
    def get_comprehensive_recommendations(self, 
                                        symptoms: List[str], 
                                        age: int, 
                                        gender: str) -> Dict[str, Any]:
        """Get comprehensive recommendations"""
        if not self.classifier.is_trained:
            raise ValueError("Models not trained")
        
        # Get classification predictions
        predictions = self.classifier.predict(symptoms)
        
        # Get cluster information
        clusters = self.clusterer.get_clusters(self.symptom_data)
        
        # Find similar cases in clusters
        similar_cases = self._find_similar_cases(symptoms, age, gender)
        
        # Generate recommendations
        recommendations = {
            'primary_diagnosis': list(predictions.keys())[:3],
            'confidence_scores': list(predictions.values())[:3],
            'cluster_insights': clusters,
            'similar_cases': similar_cases,
            'age_specific_insights': self._get_age_insights(age),
            'gender_specific_insights': self._get_gender_insights(gender)
        }
        
        return recommendations
    
    def _find_similar_cases(self, symptoms: List[str], age: int, gender: str) -> List[Dict[str, Any]]:
        """Find similar cases based on symptoms, age, and gender"""
        similar_cases = []
        symptom_text = ' '.join(symptoms)
        
        for _, row in self.symptom_data.iterrows():
            try:
                summary = json.loads(row['summary'])
                yes_symptoms = summary.get('yes_symptoms', [])
                case_symptoms = ' '.join([s['text'] for s in yes_symptoms])
                
                # Calculate similarity score
                similarity = self._calculate_similarity(
                    symptom_text, case_symptoms, age, int(row['age']), gender, row['gender']
                )
                
                if similarity > 0.3:  # Threshold for similarity
                    similar_cases.append({
                        'id': int(row.name),
                        'symptoms': case_symptoms,
                        'demographics': {
                            'gender': row['gender'],
                            'age': int(row['age'])
                        },
                        'similarity_score': similarity
                    })
            except:
                continue
        
        # Sort by similarity and return top 10
        similar_cases.sort(key=lambda x: x['similarity_score'], reverse=True)
        return similar_cases[:10]
    
    def _calculate_similarity(self, 
                            symptoms1: str, 
                            symptoms2: str, 
                            age1: int, 
                            age2: int, 
                            gender1: str, 
                            gender2: str) -> float:
        """Calculate similarity between two cases"""
        # Symptom similarity (simple word overlap)
        words1 = set(symptoms1.lower().split())
        words2 = set(symptoms2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        symptom_similarity = len(words1.intersection(words2)) / len(words1.union(words2))
        
        # Age similarity (normalized difference)
        age_diff = abs(age1 - age2) / 100.0  # Normalize by max age
        age_similarity = 1.0 - age_diff
        
        # Gender similarity
        gender_similarity = 1.0 if gender1 == gender2 else 0.0
        
        # Weighted combination
        total_similarity = (0.6 * symptom_similarity + 
                          0.3 * age_similarity + 
                          0.1 * gender_similarity)
        
        return total_similarity
    
    def _get_age_insights(self, age: int) -> Dict[str, Any]:
        """Get age-specific insights"""
        age_group = 'young' if age < 30 else 'middle' if age < 60 else 'elderly'
        
        # Filter data by age group
        age_ranges = {
            'young': (0, 30),
            'middle': (30, 60),
            'elderly': (60, 120)
        }
        
        min_age, max_age = age_ranges[age_group]
        age_filtered = self.symptom_data[
            (self.symptom_data['age'] >= min_age) & 
            (self.symptom_data['age'] <= max_age)
        ]
        
        return {
            'age_group': age_group,
            'total_cases': len(age_filtered),
            'common_symptoms': self._get_common_symptoms(age_filtered)
        }
    
    def _get_gender_insights(self, gender: str) -> Dict[str, Any]:
        """Get gender-specific insights"""
        gender_filtered = self.symptom_data[self.symptom_data['gender'] == gender]
        
        return {
            'total_cases': len(gender_filtered),
            'common_symptoms': self._get_common_symptoms(gender_filtered)
        }
    
    def _get_common_symptoms(self, df: pd.DataFrame) -> List[str]:
        """Get common symptoms from filtered data"""
        all_symptoms = []
        
        for _, row in df.iterrows():
            try:
                summary = json.loads(row['summary'])
                yes_symptoms = summary.get('yes_symptoms', [])
                symptoms = [s['text'] for s in yes_symptoms]
                all_symptoms.extend(symptoms)
            except:
                continue
        
        if not all_symptoms:
            return []
        
        symptom_counts = pd.Series(all_symptoms).value_counts()
        return symptom_counts.head(5).index.tolist()
    
    def save_models(self, filepath: str):
        """Save trained models"""
        model_data = {
            'classifier': self.classifier,
            'clusterer': self.clusterer
        }
        joblib.dump(model_data, filepath)
    
    def load_models(self, filepath: str):
        """Load trained models"""
        model_data = joblib.load(filepath)
        self.classifier = model_data['classifier']
        self.clusterer = model_data['clusterer'] 