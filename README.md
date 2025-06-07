
# Lab 5 - Edge Cloud Offloading (TECHIN 515 - Spring 2025)

This lab demonstrates an edge-cloud offloading system for gesture inference. A lightweight CNN model is used to classify gesture videos, and inference can be performed either locally (edge) or remotely via an Azure cloud server (cloud).

---

## Project Goal

- Deploy a gesture recognition model using Flask.
- Run inference:
  - Locally on the **edge device** (e.g., your laptop).
  - Remotely on an **Azure VM** for cloud offloading.
- Measure the system’s ability to offload and receive inference results from both sources.

---

## Project Structure

```
lab5/
├── app.py                # Flask server for upload + prediction
├── model.py              # CNN model for classification
├── utils.py              # Frame extraction and preprocessing
├── requirements.txt      # Python dependencies
├── client/
│   ├── upload_client.py      # Upload video to server
│   └── predict_client.py     # Request prediction result
└── video_samples/        # Sample gesture videos
```

---

## Local (Edge) Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/lab5-gesture-offloading.git
cd lab5
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Flask server

```bash
python app.py
```

Server starts at `http://localhost:5000`

### 4. Upload video and run prediction

```bash
python client/upload_client.py --file video_samples/sample1.mp4 --server http://localhost:5000
python client/predict_client.py --server http://localhost:5000
```

---

## Cloud (Azure VM) Setup

### 1. Create Azure VM (Ubuntu 20.04 or later)

- Use a B1s or B2s instance.
- Allow **inbound port 5000** in Networking > NSG rules.

### 2. SSH into the VM

```bash
ssh azureuser@YOUR_AZURE_IP
```

### 3. Install dependencies

```bash
sudo apt update
sudo apt install python3-pip git -y
git clone https://github.com/YOUR_USERNAME/lab5-gesture-offloading.git
cd lab5
pip3 install -r requirements.txt
```

### 4. Run the Flask server (public-facing)

```bash
python3 app.py --host 0.0.0.0 --port 5000
```

> Now the server is available at: `http://YOUR_AZURE_IP:5000`

---

## 🌐 Cloud Inference (from your laptop)

Run these commands **on your local machine**, replacing `YOUR_AZURE_IP` with your Azure VM’s IP address:

```bash
python client/upload_client.py --file video_samples/sample1.mp4 --server http://YOUR_AZURE_IP:5000
python client/predict_client.py --server http://YOUR_AZURE_IP:5000
```

---

## Screenshots

### Edge Inference

![Edge Inference](screenshots/edge_inference.png)

### ☁️ Cloud Inference (Azure VM)

![Cloud Inference](screenshots/cloud_inference.png)

---

## ✅ Deliverables

- ✅ GitHub repo with complete setup instructions
- ✅ Flask app for inference
- ✅ Successful edge and cloud inference
- ✅ Screenshots uploaded

---

## Author Information

- **Name:** Your Name  
- **UW NetID:** yournetid  
- **Azure VM IP:** `YOUR_AZURE_IP`

---

## Notes

- Sample gesture videos are provided in `video_samples/`
- The CNN is trained to recognize simple gestures (e.g., up/down)
- Network latency and offloading delay can be measured by timing client requests

---
