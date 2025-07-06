import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_statistics():
    """Test the statistics endpoint"""
    print("Testing statistics endpoint...")
    response = requests.get(f"{BASE_URL}/stats")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"Total records: {stats['total_records']}")
        print(f"Gender distribution: {stats['gender_distribution']}")
        print(f"Age statistics: {stats['age_statistics']}")
        print(f"Unique symptoms: {stats['unique_symptoms']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_symptom_recommendations():
    """Test the main recommendation endpoint"""
    print("Testing symptom recommendations...")
    
    # Test case 1: Cough and fever
    test_case_1 = {
        "gender": "male",
        "age": 28,
        "symptoms": ["ไอ", "เสมหะ"],
        "search_terms": "มีเสมหะ, ไอ"
    }
    
    print("Test Case 1: Cough and phlegm")
    response = requests.post(f"{BASE_URL}/recommend", json=test_case_1)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Found {len(result['recommendations'])} similar cases")
        for i, rec in enumerate(result['recommendations'][:3]):
            print(f"  {i+1}. Confidence: {rec['confidence']:.3f}")
            print(f"     Demographics: {rec['demographics']}")
            print(f"     Symptoms: {rec['symptoms']}")
    else:
        print(f"Error: {response.text}")
    print()
    
    # Test case 2: Abdominal pain
    test_case_2 = {
        "gender": "female",
        "age": 26,
        "symptoms": ["ปวดท้อง"],
        "search_terms": "ปวดท้อง"
    }
    
    print("Test Case 2: Abdominal pain")
    response = requests.post(f"{BASE_URL}/recommend", json=test_case_2)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Found {len(result['recommendations'])} similar cases")
        for i, rec in enumerate(result['recommendations'][:3]):
            print(f"  {i+1}. Confidence: {rec['confidence']:.3f}")
            print(f"     Demographics: {rec['demographics']}")
            print(f"     Symptoms: {rec['symptoms']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_symptom_analysis():
    """Test the symptom analysis endpoint"""
    print("Testing symptom analysis...")
    
    symptoms = "ไอ,เสมหะ,น้ำมูกไหล"
    response = requests.get(f"{BASE_URL}/symptoms/analysis?symptoms={symptoms}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        analysis = response.json()
        print("Common symptoms:")
        for symptom, count in list(analysis['common_symptoms'].items())[:5]:
            print(f"  {symptom}: {count}")
        print("Co-occurring symptoms:")
        for symptom, count in analysis['co_occurring_symptoms'].items():
            print(f"  {symptom}: {count}")
    else:
        print(f"Error: {response.text}")
    print()

def test_age_group_insights():
    """Test the age group insights endpoint"""
    print("Testing age group insights...")
    
    ages = [25, 45, 70]
    for age in ages:
        response = requests.get(f"{BASE_URL}/demographics/age-group/{age}")
        print(f"Age {age}:")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            insights = response.json()
            print(f"  Age group: {insights['age_group']}")
            print(f"  Common symptoms: {insights['common_symptoms']}")
        else:
            print(f"  Error: {response.text}")
        print()

def test_comprehensive_scenarios():
    """Test comprehensive scenarios with different symptom combinations"""
    print("Testing comprehensive scenarios...")
    
    scenarios = [
        {
            "name": "Respiratory symptoms",
            "data": {
                "gender": "female",
                "age": 35,
                "symptoms": ["ไอ", "น้ำมูกไหล", "เจ็บคอ"],
                "search_terms": "ไอ, น้ำมูกไหล, เจ็บคอ"
            }
        },
        {
            "name": "Gastrointestinal symptoms",
            "data": {
                "gender": "male",
                "age": 42,
                "symptoms": ["ปวดท้อง", "ท้องเสีย", "อาเจียน"],
                "search_terms": "ปวดท้อง, ท้องเสีย"
            }
        },
        {
            "name": "Musculoskeletal symptoms",
            "data": {
                "gender": "female",
                "age": 55,
                "symptoms": ["ปวดหลัง", "ปวดข้อ"],
                "search_terms": "ปวดหลัง, ปวดข้อ"
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"\nScenario: {scenario['name']}")
        response = requests.post(f"{BASE_URL}/recommend", json=scenario['data'])
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Found {len(result['recommendations'])} similar cases")
            
            # Show top 3 recommendations
            for i, rec in enumerate(result['recommendations'][:3]):
                print(f"  {i+1}. Case ID: {rec['case_id']}")
                print(f"     Confidence: {rec['confidence']:.3f}")
                print(f"     Demographics: {rec['demographics']}")
                print(f"     Age Group: {rec['age_group']}")
                print(f"     Symptoms: {rec['symptoms'][:100]}...")
        else:
            print(f"Error: {response.text}")
        
        time.sleep(1)  # Small delay between requests

def main():
    """Run all tests"""
    print("Starting API tests...")
    print("=" * 50)
    
    try:
        # Test basic endpoints
        test_health_check()
        test_get_statistics()
        
        # Test main functionality
        test_symptom_recommendations()
        test_symptom_analysis()
        test_age_group_insights()
        
        # Test comprehensive scenarios
        test_comprehensive_scenarios()
        
        print("=" * 50)
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the server is running on localhost:8000")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main() 