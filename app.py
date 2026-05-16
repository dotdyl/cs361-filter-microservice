from flask import Flask, request, jsonify
import string
import re

app = Flask(__name__)
app.json.sort_keys = False

def lowercase(text, target_keywords):
    return text.lower()

def remove_punctuation(text, target_keywords):
    return text.translate(str.maketrans("", "", string.punctuation))

def censor_keywords(text, target_keywords):
    if target_keywords:
        for keyword in target_keywords:
            text = re.sub(rf"\b{re.escape(keyword)}\b", "***", text, flags=re.IGNORECASE)
    return text

# Add references to helper functions here
TRANSFORMATIONS = {
    "lowercase": lowercase,
    "remove_punctuation": remove_punctuation,
    "censor_keywords": censor_keywords,
}

@app.route('/api/text_filter', methods=['POST'])
def transform_text():
    req_data = request.get_json()
    
    if not req_data:
        return jsonify({"error": "Invalid JSON"}), 400

    text = req_data.get("text")
    requested_transforms = req_data.get("transformations", [])
    target_keywords = req_data.get("target_keywords", [])
 
    if not text:
        return jsonify({"error": "No text provided"}), 400

    if not requested_transforms:
        return jsonify({"error": "No requested transformations provided"}), 400   
    
    response = {
        "original_text": text,
        "filtered_text": text,
        "applied_transformations": [],
        "unknown_transformations": []
    }
    
    for transform in requested_transforms:
        if transform in TRANSFORMATIONS:
            response["applied_transformations"].append(transform)
            response["filtered_text"] = TRANSFORMATIONS[transform](response["filtered_text"], target_keywords)
        else:
            response["unknown_transformations"].append(transform)
            
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)