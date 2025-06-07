import requests
import argparse

def upload_video(server_url, video_path):
    with open(video_path, 'rb') as f:
        files = {'file': (video_path, f, 'video/mp4')}
        response = requests.post(f"{server_url}/upload", files=files)
    if response.status_code == 200:
        print("[✅] Upload successful:", response.json())
    else:
        print("[❌] Upload failed:", response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', type=str, default='http://localhost:5000', help='Flask server URL')
    parser.add_argument('--file', type=str, required=True, help='Path to .mp4 video file')
    args = parser.parse_args()

    upload_video(args.server, args.file)
