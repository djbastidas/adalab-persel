from flask import Flask, request, jsonify
import pickle
import json
import numpy as np
import os

app = Flask(__name__)

# Load model and preprocessing objects
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'rental_price_model.pkl')
PROVINCIA_ENCODER_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'provincia_encoder.pkl')
LUGAR_ENCODER_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'lugar_encoder.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'scaler.pkl')
METADATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'metadata.json')

# Load artifacts
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

with open(PROVINCIA_ENCODER_PATH, 'rb') as f:
    provincia_encoder = pickle.load(f)

with open(LUGAR_ENCODER_PATH, 'rb') as f:
    lugar_encoder = pickle.load(f)

with open(SCALER_PATH, 'rb') as f:
    scaler = pickle.load(f)

with open(METADATA_PATH, 'r') as f:
    metadata = json.load(f)


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict rental price based on property features.
    
    Expected JSON input:
    {
        "provincia": "Pichincha",
        "lugar": "Quito",
        "num_dormitorios": 3,
        "num_banos": 2,
        "area": 120,
        "num_garages": 1
    }
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['provincia', 'lugar', 'num_dormitorios', 
                          'num_banos', 'area', 'num_garages']
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'required_fields': required_fields
                }), 400
        
        # Extract features
        provincia = str(data['provincia']).strip()
        lugar = str(data['lugar']).strip()
        num_dormitorios = float(data['num_dormitorios'])
        num_banos = float(data['num_banos'])
        area = float(data['area'])
        num_garages = float(data['num_garages'])
        
        # Validate numerical features
        if not all([isinstance(x, (int, float)) for x in 
                   [num_dormitorios, num_banos, area, num_garages]]):
            return jsonify({
                'error': 'Numerical features must be numbers'
            }), 400
        
        if area <= 0 or num_dormitorios < 0 or num_banos < 0 or num_garages < 0:
            return jsonify({
                'error': 'Area must be positive, other features must be non-negative'
            }), 400
        
        # Handle unknown categories
        try:
            provincia_encoded = provincia_encoder.transform([provincia])[0]
        except:
            # If provincia is not in training data, use the most common one
            provincia_encoded = provincia_encoder.transform([provincia_encoder.classes_[0]])[0]
        
        try:
            lugar_encoded = lugar_encoder.transform([lugar])[0]
        except:
            # If lugar is not in training data, use the most common one
            lugar_encoded = lugar_encoder.transform([lugar_encoder.classes_[0]])[0]
        
        # Create feature array
        features = np.array([[
            provincia_encoded,
            lugar_encoded,
            num_dormitorios,
            num_banos,
            area,
            num_garages
        ]])
        
        # Scale numerical features
        numerical_indices = [2, 3, 4, 5]
        features_scaled = features.copy()
        features_scaled[:, numerical_indices] = scaler.transform(
            features[:, numerical_indices]
        )
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        return jsonify({
            'prediction': round(float(prediction), 2),
            'input': {
                'provincia': provincia,
                'lugar': lugar,
                'num_dormitorios': num_dormitorios,
                'num_banos': num_banos,
                'area': area,
                'num_garages': num_garages
            },
            'model_info': {
                'type': metadata['model_type'],
                'r2_score': metadata['r2_score'],
                'rmse': metadata['rmse']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_type': metadata['model_type'],
        'features': metadata['features'],
        'r2_score': metadata['r2_score'],
        'rmse': metadata['rmse']
    }), 200


@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        'api': 'Ecuador Real Estate Rental Price Prediction',
        'version': '1.0.0',
        'endpoints': {
            'predict': {
                'method': 'POST',
                'url': '/predict',
                'description': 'Predict rental price based on property features',
                'example_input': {
                    'provincia': 'Pichincha',
                    'lugar': 'Quito',
                    'num_dormitorios': 3,
                    'num_banos': 2,
                    'area': 120,
                    'num_garages': 1
                },
                'example_output': {
                    'prediction': 650.50,
                    'input': {},
                    'model_info': {}
                }
            },
            'health': {
                'method': 'GET',
                'url': '/health',
                'description': 'Check API health status'
            }
        }
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
