# Symptom Recommendation System API

A comprehensive medical symptom recommendation system built with FastAPI and machine learning. This system analyzes patient symptoms and provides intelligent recommendations based on similar cases from a large medical dataset.

## Features

- **Symptom-based Recommendations**: Find similar medical cases based on patient symptoms
- **Demographic Analysis**: Age and gender-specific insights
- **Pattern Recognition**: Identify common symptom combinations and co-occurrences
- **Machine Learning Models**: Advanced classification and clustering algorithms
- **RESTful API**: Easy-to-use endpoints for integration
- **Comprehensive Testing**: Built-in test suite for validation

## Technology Stack

- **Backend**: FastAPI (Python 3.9)
- **Machine Learning**: scikit-learn, pandas, numpy
- **Data Processing**: TF-IDF vectorization, cosine similarity
- **Model Persistence**: joblib
- **API Documentation**: Automatic OpenAPI/Swagger docs
- **Deployment**: Docker, Railway (Python 3.9 compatible)

## Installation

### Prerequisites
- **Python 3.9+** (required to avoid distutils issues in Python 3.12+)
- **Docker** (optional, for containerized deployment)

### Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd agnos-task-2
```

2. **Check Python version**:
```bash
python --version  # Should be 3.9+
python test_python_version.py  # Run compatibility test
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python app.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/` - Check API health status

### Main Recommendation
- **POST** `/recommend` - Get symptom-based recommendations

**Request Body**:
```json
{
  "gender": "male",
  "age": 28,
  "symptoms": ["ไอ", "เสมหะ"],
  "search_terms": "มีเสมหะ, ไอ"
}
```

**Response**:
```json
{
  "recommendations": [
    {
      "case_id": 123,
      "demographics": {
        "gender": "male",
        "age": 28
      },
      "symptoms": "ไอ เสมหะ",
      "search_terms": "มีเสมหะ, ไอ",
      "confidence": 0.85,
      "age_group": "young"
    }
  ],
  "confidence_scores": [0.85, 0.72, 0.68],
  "similar_cases": [...]
}
```

### Analysis Endpoints
- **GET** `/symptoms/analysis?symptoms=ไอ,เสมหะ` - Analyze symptom patterns
- **GET** `/demographics/age-group/{age}` - Get age-specific insights
- **GET** `/stats` - Get dataset statistics

## Usage Examples

### Python Client
```python
import requests

# Get recommendations
response = requests.post("http://localhost:8000/recommend", json={
    "gender": "female",
    "age": 35,
    "symptoms": ["ปวดท้อง", "อาเจียน"],
    "search_terms": "ปวดท้อง"
})

recommendations = response.json()
print(f"Found {len(recommendations['recommendations'])} similar cases")
```

### cURL Examples
```bash
# Health check
curl http://localhost:8000/

# Get recommendations
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "male",
    "age": 28,
    "symptoms": ["ไอ", "เสมหะ"],
    "search_terms": "มีเสมหะ, ไอ"
  }'

# Analyze symptoms
curl "http://localhost:8000/symptoms/analysis?symptoms=ไอ,เสมหะ,น้ำมูกไหล"

# Get statistics
curl http://localhost:8000/stats
```

## Testing

Run the comprehensive test suite:

```bash
python test_api.py
```

This will test all endpoints with various scenarios including:
- Health check
- Statistics retrieval
- Symptom recommendations
- Pattern analysis
- Age group insights
- Comprehensive scenarios

## Data Structure

The system processes medical data with the following structure:
- **gender**: Patient gender (male/female)
- **age**: Patient age
- **summary**: JSON containing symptoms and their details
- **search_term**: Search keywords for symptoms

### Sample Data Format
```csv
gender,age,summary,search_term
male,28,"{""diseases"": [], ""procedures"": [], ""no_symptoms"": [], ""idk_symptoms"": [], ""yes_symptoms"": [{""text"": ""เสมหะ"", ""answers"": [""ลักษณะ เสมหะเปลี่ยนสีเหลือง/เขียว""]}, {""text"": ""ไอ"", ""answers"": [""ระยะเวลา ไม่เกิน 1 สัปดาห์ (ไม่เกิน 7 วัน)""]}]}","มีเสมหะ, ไอ"
```

## Machine Learning Models

### SymptomClassifier
- Uses Random Forest for symptom classification
- TF-IDF vectorization for text processing
- Provides confidence scores for predictions

### SymptomClusterer
- K-means clustering for pattern discovery
- Identifies symptom clusters and centroids
- Helps understand common symptom combinations

### Similarity Matching
- Cosine similarity for symptom comparison
- Demographic weighting (age, gender)
- Multi-factor similarity scoring

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Configuration

The system can be configured through environment variables:
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

## Performance

- **Data Loading**: ~1000 records processed in <5 seconds
- **Recommendation Generation**: <1 second per request
- **Memory Usage**: ~200MB for full dataset
- **Concurrent Requests**: Supports multiple simultaneous users

## Error Handling

The API includes comprehensive error handling:
- Input validation with Pydantic models
- Graceful handling of malformed data
- Detailed error messages for debugging
- HTTP status codes for different error types

## 🚀 Deployment

This project can be deployed to various cloud platforms using GitHub Actions. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Quick Deploy Options:

1. **Railway** (Recommended - Free):
   ```bash
   # Connect your GitHub repo to Railway
   # Push to main branch for automatic deployment
   git push origin main
   ```

2. **Render** (Free):
   ```bash
   # Connect your GitHub repo to Render
   # Configure build command: pip install -r requirements.txt
   # Configure start command: uvicorn app:app --host 0.0.0.0 --port $PORT
   ```

3. **Heroku** (Paid):
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that:
- Runs tests on every push
- Deploys to Railway and Render on main branch
- Provides automatic CI/CD pipeline

### Docker Deployment

#### Quick Docker Deploy:
```bash
# Build and run with Docker
docker build -t symptom-recommendation-api .
docker run -p 8000:8000 symptom-recommendation-api
```

#### Docker Compose (Recommended for local testing):
```bash
# Start with docker-compose
docker-compose up --build

# Run in background
docker-compose up -d --build
```

#### Railway Docker Deploy:
```bash
# Use the Railway Docker deployment script
python deploy_railway.py
```

#### Manual Railway Docker Deploy:
1. Go to [railway.app](https://railway.app)
2. Create new project
3. Choose "Deploy from GitHub repo"
4. Railway will automatically detect Dockerfile
5. Deploy!

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This system is for educational and research purposes only. It should not be used for actual medical diagnosis or treatment decisions. Always consult with qualified healthcare professionals for medical advice.
