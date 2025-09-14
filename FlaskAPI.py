from flask import Flask, request, jsonify
import numpy as np
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances_argmin

app = Flask(__name__)

# Load Models and Scalers
with open('./classification_models/SVM_GAD.pkl', 'rb') as f:    
    svm_gad = pickle.load(f)

with open('./classification_models/SVM_PHQ.pkl', 'rb') as f:
    svm_phq = pickle.load(f)

with open('./scalers/scaler_gad.pkl', 'rb') as f:
    scaler_gad = pickle.load(f)

with open('./scalers/scaler_phq.pkl', 'rb') as f:
    scaler_phq = pickle.load(f)

with open('./scalers/encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

with open('./scalers/scaler_clusters.pkl', 'rb') as f:
    scaler_clusters = pickle.load(f)

with open('./clustering_models/Hierarchical_model.pkl', 'rb') as f:
    hierarchical_model = pickle.load(f)  # Load the saved Hierarchical model

# Load original data for clustering
original_data = pd.read_csv('./synthetic_mental_health_data.csv')
original_data['Cluster_Hierarchical'] = hierarchical_model.labels_  # Assign stored cluster labels

# Arrays to store answers
gad_input = []  # Stores GAD survey responses
phq_input = []  # Stores PHQ survey responses

# Dictionary to track pending questions per session
session_pending_question = {}

# List of survey-related intents
survey_intents = [
    "PersonalQuestions-1", "PersonalQuestions-2", "PersonalQuestions-3", 
    "PersonalQuestions-4", "PersonalQuestions-5",
    "GAD_Question-1", "GAD_Question-2-follow", "GAD_Question-3", 
    "GAD_Question-4", "GAD_Question-5", "GAD_Question-6", "GAD_Question-7",
    "PHQ_Question-1", "PHQ_Question-2", "PHQ_Question-3", "PHQ_Question-4", 
    "PHQ_Question-5", "PHQ_Question-6", "PHQ_Question-7", 
    "PHQ_Question-8", "PHQ_Question-9"
]

# Mapping of survey options to numeric values
option_mapping = {
    "Not at all": 0,
    "Several days": 1,
    "More than half the days": 2,
    "Nearly every day": 3
}

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    
    print(f"DialogFlow Response: {req}\n")

    # Extract session ID, intent, and user response
    session_id = req.get('session', '')  
    intent_name = req.get('queryResult', {}).get('intent', {}).get('displayName', '')
    user_response = req.get('queryResult', {}).get('queryText', '')

    print(f"Intent: {intent_name}")
    print(f"User Response: {user_response}")

    # Convert user response to numerical value
    user_response_value = option_mapping.get(user_response, None)

    if session_id in session_pending_question:
        last_question = session_pending_question.pop(session_id, None)  
        
        if last_question and user_response_value is not None:
            if "GAD_Question-" in last_question:
                gad_input.append(user_response_value)
                print(f"Stored in GAD: {user_response_value}")
            elif "PHQ_Question-" in last_question:
                phq_input.append(user_response_value)
                print(f"Stored in PHQ: {user_response_value}")
            else:
                print(f"Error: {last_question} is not recognized as GAD or PHQ")

    # Extract next question from fulfillment messages (to be stored for next request)
    if intent_name in survey_intents:
        fulfillment_messages = req.get('queryResult', {}).get('fulfillmentMessages', [])
        next_question = None  

        for message in fulfillment_messages:
            if isinstance(message, dict) and "payload" in message:
                rich_content = message["payload"].get("richContent", [])
                if rich_content:
                    for item in rich_content[0]:  
                        if "title" in item:
                            next_question = item["title"]
                            break  

        if next_question:
            session_pending_question[session_id] = intent_name  # Store intent name for tracking
            print(f"Next question stored for session {session_id}: {intent_name}")

    # Check if all questions are answered before allowing recommendation
    if "Get Recommendation" in user_response:
        if len(gad_input) == 7 and len(phq_input) == 9:
            print(f"GAD: {gad_input}")
            print(f"PHQ: {phq_input}")
            
            # Proceed with recommendation
            gad_result, phq_result = classify_mental_health(gad_input, phq_input)
            recommendations = get_combined_recommendations(gad_result, phq_result)

            print(f"Recommendations {session_id}: {recommendations}")
            
            return jsonify({
                'fulfillmentMessages': [
                    {
                        'text': {
                            'text': [
                                f"Recommendations: {recommendations}"
                            ]
                        }
                    }
                ]
            })
        else:
            return jsonify({
                'fulfillmentMessages': [
                    {
                        'text': {
                            'text': [
                                "Please complete the survey before getting recommendations."
                            ]
                        }
                    }
                ]
            }), 400

    return jsonify({})

def classify_mental_health(gad_input, phq_input):
    gad_input = scaler_gad.transform(np.array(gad_input).reshape(1, -1))
    phq_input = scaler_phq.transform(np.array(phq_input).reshape(1, -1))
    
    gad_result = svm_gad.predict(gad_input)[0].capitalize()
    phq_result = svm_phq.predict(phq_input)[0].capitalize()
    
    return gad_result, phq_result

def determine_help_type(diagnosis):
    diagnosis_lower = diagnosis.lower()
    if any(word in diagnosis_lower for word in ["mild", "minimal"]):
        return "Self help"
    elif "moderate" in diagnosis_lower:
        return np.random.choice(["Self help", "Self help + Professional"])
    elif any(word in diagnosis_lower for word in ["moderately", "severe"]):
        return np.random.choice(["Professional", "Professional + Emergency"])
    else:
        return "Professional"

def recommend_solution(diagnosis, help_type):
    input_data = encoder.transform([[diagnosis, help_type]]).toarray()
    input_scaled = scaler_clusters.transform(input_data)

    encoded_original = encoder.transform(original_data[['Diagnosis', 'Type of Help']]).toarray()
    scaled_original = scaler_clusters.transform(encoded_original)

    hierarchical_labels = hierarchical_model.fit_predict(scaled_original)
    
    closest_cluster = pairwise_distances_argmin(input_scaled, scaled_original)
    hierarchical_cluster = hierarchical_labels[closest_cluster[0]] 
    
    suggestions = original_data[original_data['Cluster_Hierarchical'] == hierarchical_cluster]['Suggestion'].tolist()
    
    return np.random.choice(suggestions) if suggestions else 'No suggestion found'

def get_combined_recommendations(gad_result, phq_result):
    help_type_gad = determine_help_type(gad_result)
    help_type_phq = determine_help_type(phq_result)
    
    recommendations_gad = recommend_solution(gad_result, help_type_gad)
    recommendations_phq = recommend_solution(phq_result, help_type_phq)

    combined_recommendations = f"Based on your survey responses, you have {gad_result}. For that you can {recommendations_gad.lower()} And you have {phq_result}, for that, you can {recommendations_phq.lower()}"
    return combined_recommendations

if __name__ == '__main__':
    app.run(debug=True)