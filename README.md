# ✋ Gesture Controlled Menu

A modern **Gesture-Controlled Menu System** built with **Python**, **Flask**, **OpenCV**, and **MediaPipe**. This project enables users to interact with a virtual on-screen menu using **hand gestures** captured through a webcam, providing a touch-free and intuitive human-computer interaction experience.

> **Navigate digital menus naturally using the power of hand gestures and Artificial Intelligence.**

---

# ✨ Features

- 🖐️ Real-time hand tracking
- 📋 Gesture-controlled virtual menu
- 🎯 Cursor movement using hand gestures
- 👆 Finger-based menu selection
- 🎥 Live webcam processing
- 🤖 AI-powered hand landmark detection
- 🌐 Flask web application
- ⚡ Smooth and responsive interaction
- 💻 Browser-based interface
- 📱 Lightweight and easy to use

---

# 🛠️ Tech Stack

## Backend

- Python 3.x
- Flask

## Computer Vision

- OpenCV
- MediaPipe Hands

## Data Processing

- NumPy

## Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap
- Jinja2 Templates

---

# 📚 Main Libraries Used

| Library | Purpose |
|----------|---------|
| **Flask** | Web framework for serving pages and streaming processed video |
| **OpenCV** | Webcam capture, image processing, drawing UI elements, and video streaming |
| **MediaPipe** | Real-time hand landmark detection using AI |
| **NumPy** | Fast numerical computations and image manipulation |

---

# 📂 Project Structure

```text
Gesture_Controlled_Menu/
│
├── app.py
├── requirements.txt
├── README.md
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── assets/
│
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── contact.html
│   ├── menu.html
│   └── base.html
│
└── ...
```

---

# 🚀 Features Overview

- ✋ AI Hand Tracking
- 🎯 Virtual Cursor Control
- 📋 Gesture-Based Menu Navigation
- 👆 Finger Selection
- 🎥 Live Webcam Streaming
- 🌐 Flask Video Streaming
- ⚡ Real-Time Processing
- 💻 Browser-Based Interface
- 🤖 AI-Powered Interaction
- 📱 Responsive Design

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/subham-paul/Gesture_Controlled_Menu.git
```

```bash
cd Gesture_Controlled_Menu
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
python app.py
```

or

```bash
flask run
```

---

# 🌐 Open in Browser

```
http://127.0.0.1:5000
```

---

# 🏗️ System Architecture

```text
Webcam
   │
   ▼
OpenCV
   │
   ▼
MediaPipe Hands
   │
   ▼
Hand Landmark Detection
   │
   ▼
Gesture Recognition
   │
   ▼
Virtual Cursor
   │
   ▼
Menu Selection
   │
   ▼
Flask Video Streaming
   │
   ▼
Browser Interface
```

---

# ⚙️ How It Works

### Step 1 — Webcam Input

The webcam captures live video frames continuously.

---

### Step 2 — Hand Detection

MediaPipe Hands detects **21 hand landmarks** in every frame.

---

### Step 3 — Hand Tracking

The application tracks the user's index finger and other landmarks to determine hand position and gestures.

---

### Step 4 — Cursor Control

The detected finger coordinates are translated into a virtual cursor that moves across the on-screen menu.

---

### Step 5 — Gesture Recognition

Specific gestures (such as pointing or pinching) are recognized to interact with menu items.

---

### Step 6 — Menu Selection

The selected menu option is highlighted and executed, allowing users to navigate without touching a keyboard or mouse.

---

# 📊 Processing Pipeline

```text
Webcam
   │
   ▼
OpenCV Capture
   │
   ▼
MediaPipe Hands
   │
   ▼
21 Hand Landmarks
   │
   ▼
Gesture Recognition
   │
   ▼
Virtual Cursor
   │
   ▼
Menu Interaction
   │
   ▼
Flask Stream
   │
   ▼
Browser
```

---

# ✋ Supported Gestures

| Gesture | Action |
|----------|--------|
| ☝️ Index Finger | Move Virtual Cursor |
| 👌 Pinch Gesture | Select Menu Item |
| ✋ Open Palm | Reset / Idle |
| ✌️ Two Fingers | Navigate Menu *(Optional)* |
| 👍 Custom Gesture | Trigger Action *(Optional)* |

> **Note:** Supported gestures may vary depending on your implementation.

---

# 📊 Applications

- Smart Kiosks
- Touch-Free User Interfaces
- Interactive Presentations
- Smart Classroom Systems
- Accessibility Solutions
- AI Demonstrations
- Human-Computer Interaction Research
- Interactive Displays

---

# 🚀 Future Enhancements

- 🧠 Deep Learning Gesture Recognition
- 🎤 Voice Command Integration
- 👥 Multi-Hand Detection
- 🎮 Gesture-Controlled Games
- 📱 Mobile Device Support
- 🖥️ Multi-Screen Navigation
- 🌍 Multi-language UI
- ☁️ Cloud Deployment
- 📊 User Interaction Analytics
- 🎨 Customizable Gesture Mapping

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository.

2. Create a feature branch.

```bash
git checkout -b feature/NewFeature
```

3. Commit your changes.

```bash
git commit -m "Add New Feature"
```

4. Push your changes.

```bash
git push origin feature/NewFeature
```

5. Open a Pull Request.

---

# 🐞 Reporting Issues

Found a bug or have a feature request?

Please create an issue with a detailed explanation.

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

## **Subham Paul**

Passionate about **Artificial Intelligence, Computer Vision, Python, Automation, Flask, and Human-Computer Interaction.**

- GitHub: https://github.com/subham-paul
- LinkedIn: https://www.linkedin.com/in/subham-paul-india/

---

# ⭐ Show Your Support

If you found this project useful:

- ⭐ Star this repository
- 🍴 Fork the project
- 🤝 Contribute
- 💬 Share your feedback


---

## 🙏 Acknowledgements

Special thanks to the open-source communities behind:

- Python
- Flask
- OpenCV
- MediaPipe
- NumPy

for making real-time gesture recognition and interactive applications possible.

---

> **"Reimagining user interaction with touch-free gesture-controlled interfaces."** ✋🤖💻
