import requests
from google.oauth2 import service_account
import google.auth.transport.requests

# Function to obtain access token using service account
def get_access():
    credentials = service_account.Credentials.from_service_account_file(
        filename='gcp_creds/igp-genai-7220e3ec9be8.json',
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    credentials.refresh(google.auth.transport.requests.Request())
    return credentials.token

# Function to send the POST request and get chat response
def get_mental_health_support_response(context, user_message, project_id, temperature, max_output_tokens, top_p, candidate_count):
    API_ENDPOINT = "us-central1-aiplatform.googleapis.com"
    ENDPOINT_ID = "2946908865741979648"
    LOCATION_ID = "us-central1"
    url = f"https://{API_ENDPOINT}/v1/projects/{project_id}/locations/{LOCATION_ID}/endpoints/{ENDPOINT_ID}:predict"

    access_token = get_access()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    request_body = {
        "instances": [
            {
                "context": context,
                "examples": [],
                "messages": [
                    {
                        "author": "user",
                        "content": user_message
                    }
                ]
            }
        ],
        "parameters": {
            "candidateCount": candidate_count,
            "maxOutputTokens": max_output_tokens,
            "temperature": temperature,
            "topP": top_p
        }
    }

    response = requests.post(url, headers=headers, json=request_body)
    if response.status_code == 200:
        print("Request was successful.")
        return response.json()
    else:
        print("Request failed.")
        return f"Error: {response.status_code}, Message: {response.text}"

