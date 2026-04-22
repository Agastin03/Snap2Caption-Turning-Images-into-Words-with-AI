📸 Snap2Caption – Turning Images into Words with AI

An AI-powered web application that generates captions for images using advanced vision models. Built with a Flask backend, this project allows users to upload images and receive descriptive, creative, technical, or social-media-ready captions instantly.


🚀 Features
🔐 User Authentication (Login & Register)
🖼️ Image Upload (JPG, PNG, JPEG, WEBP)
🤖 AI-Based Caption Generation
🎭 Multiple Caption Styles:
Descriptive
Creative
Technical
Social Media
⚡ Real-time Processing
📱 Simple and User-Friendly Interface


🛠️ Tech Stack
Backend: Flask (Python)
Frontend: HTML, CSS (Templates)
AI Model: OpenAI GPT-4 Vision API
Authentication: Session-based login system
Image Processing: Base64 Encoding


📂 Project Structure
├── app.py
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
├── uploads/
├── static/
└── README.md


⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/ai-image-caption-generator.git
cd ai-image-caption-generator

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install flask werkzeug requests

4️⃣ Set OpenAI API Key
export OPENAI_API_KEY=your_api_key_here

# On Windows:
set OPENAI_API_KEY=your_api_key_here

5️⃣ Run the Application
python app.py

👉 Open browser: http://localhost:5000

🔑 Demo Credentials
Email: demo@example.com
Password: demo123

📸 How It Works
User logs into the system
Uploads an image
Selects caption style & detail level
Image is processed and sent to AI model
AI generates caption and displays result

🎯 Use Cases
Social Media Content Creation
Image Description for Accessibility
Content Writing Assistance
Photography Analysis

⚠️ Note
Requires a valid OpenAI API key
Max file size: 5MB
Supported formats: PNG, JPG, JPEG, WEBP

🔮 Future Enhancements
🌐 Deploy to cloud (AWS / Render / Vercel)
📱 Mobile-friendly UI
🗂️ Caption history storage
🎙️ Voice-based caption generation
🌍 Multi-language captions
