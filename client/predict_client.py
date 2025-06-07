import requests
import argparse

def get_prediction(server_url):
    response = requests.get(f"{server_url}/predict")
    if response.status_code == 200:
        print("[✅] Prediction result:", response.json())
    else:
        print("[❌] Prediction failed:", response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', type=str, default='http://localhost:5000', help='Flask server URL')
    args = parser.parse_args()

    get_prediction(args.server)
