import subprocess
import json 

# Funkcja do wykonywania żądania HTTP
def curl_request(url):
    try: 
        result = subprocess.run(["curl", "-s", "-w", "%{http_code}", url], capture_output=True, text=True, check=True)
        http_code = result.stdout[-3:]
        response_body = result.stdout[:-3]
        return http_code, response_body
    except subprocess.CalledProcessError as e:
        print(f"Request to {url} failed as: {e}")    
        return None
    
# Funkcja do sprawdzania odpowiedzi JSON
def check_response(response, expected_keys): 
    try: 
        data = json.loads(response)
        if all(key in data for key in expected_keys):
            print("Response contains all expected keys.")
            return True
        else: 
            print("Resposne doesn't contain all expected keys.")
    except json.JSONDecodeError:
        print("Failed to decode JSON response.")
        return False
    

endpoints = {
    "posts": "https://jsonplaceholder.typicode.com/posts/1",
    "comments": "https://jsonplaceholder.typicode.com/comments/1",
    "albums": "https://jsonplaceholder.typicode.com/albums/1"
}

expected_keys = {
    "posts": ["userId", "id", "title", "body"],
    "comments": ["postId", "id", "name", "email", "body"],
    "albums": ["userId", "id", "title"],
}

test_number = 1
for endpoint, url in endpoints.items():
    print(f"Testing {endpoint} endpoint: {url}")
    http_code, response = curl_request(url)
    if http_code == "200":
        if check_response(response, expected_keys[endpoint]):
            print(f"Test {test_number}: PASSED")
        else:
            print(f"Test {test_number}: FAILED - Key elements missing in response")
    else:
        print(f"Test {test_number}: FAILED - HTTP status {http_code}")
    test_number += 1
    print()