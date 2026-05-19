import requests, json

url = "http://127.0.0.1:5000/api/text_filter"

body = {
    "text": "This is a VERYBADWORD example!@#$",
    "target_keywords": ["verybadword"],
    "transformations": [
        "lowercase",
        "remove_punctuation",
        "censor_keywords",
        "a_fake_transformation"
    ]
}

response = requests.post(url, json=body)

print(response.status_code)
print(response.text)