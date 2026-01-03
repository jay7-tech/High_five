🖐️ High Five | Real-Time Voice Social Platform
High Five is a high-energy, production-ready social application designed for meaningful, five-minute voice-only connections. It prioritizes user privacy, safety, and engagement through an interactive, audio-reactive experience.

🌟 Brilliant Features
Audio-Reactive UX: The UI is alive; background gradients and visualizer rings pulse and shift colors in real-time based on voice frequency data.

Global Voice Engine: Powered by WebRTC with integrated STUN/TURN servers (OpenRelay) to ensure 100% audio reliability across 5G and restrictive firewalls.

Mutual Consent Reveal: A "Consent-First" architecture where social handles (Instagram/Snapchat) are only revealed if both participants "High Five" each other.

Synchronized Interactions: Real-time emoji broadcasting and AI-driven "Icebreaker Nukes" that automatically trigger during conversation lulls to keep the vibe going.

Mobile-First Design: A sleek, glassmorphic interface built with Tailwind CSS, optimized for a native app feel on mobile browsers.

🛠️ Tech Stack
Backend: Python, Flask, Flask-SocketIO (WebSockets)

Frontend: JavaScript (ES6+), Tailwind CSS, WebRTC API, Web Audio API

Networking: P2P Signaling, NAT Traversal (STUN/TURN)

Deployment: Railway (Cloud Hosting), GitHub CI/CD

🚀 Getting Started
1. Prerequisites
Python 3.12+

A browser with Microphone access (HTTPS required for production)

2. Installation
Bash

# Clone the repository
git clone https://github.com/your-username/high-five.git
cd high-five

# Install dependencies
pip install flask flask-socketio eventlet gunicorn
3. Running Locally
Bash

python app.py
Access the app at http://127.0.0.1:5000.

📱 Project Preview
The application features a "Thumb-Zone" optimized layout, ensuring all major actions like "Find Match" and "Give High Five" are easily accessible for one-handed mobile use.

🛡️ Safety & Privacy
Report System: Instant "Nuke/Report" button to terminate connections immediately for safety.

Privacy Layer: No personal information is shared until both users explicitly agree to a mutual reveal.
