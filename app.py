from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import base64
import requests
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production-12345'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# Create uploads folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Simple user database
users_db = {
    'demo@example.com': {
        'password': generate_password_hash('demo123'),
        'name': 'Demo User'
    }
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in users_db and check_password_hash(users_db[email]['password'], password):
            session['user'] = email
            session['name'] = users_db[email]['name']
            session.permanent = True
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if email in users_db:
            flash('Email already registered', 'error')
        else:
            users_db[email] = {
                'password': generate_password_hash(password),
                'name': name
            }
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=session.get('name'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/generate-caption', methods=['POST'])
def generate_caption():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Read image and convert to base64
        image_data = file.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Get settings
        caption_style = request.form.get('style', 'descriptive')
        detail_level = int(request.form.get('detail', 2))
        
        # Determine media type
        media_type = f"image/{file.filename.rsplit('.', 1)[1].lower()}"
        if media_type == 'image/jpg':
            media_type = 'image/jpeg'
        
        # Build prompts
        prompts = {
            'descriptive': [
                'Provide a brief, one-sentence description of this image.',
                'Describe this image in 2-3 sentences, covering the main subjects and setting.',
                'Provide a detailed description of this image, including subjects, setting, colors, mood, and any notable details.'
            ],
            'creative': [
                'Create a short, creative caption for this image.',
                'Write a creative, engaging caption that captures the essence of this image in 2-3 sentences.',
                'Write a creative, evocative description that tells the story of this image, including imagery and emotional tone.'
            ],
            'technical': [
                'Provide a technical description of this image (composition, subjects, lighting).',
                'Give a technical analysis of this image covering composition, lighting, subjects, and visual elements.',
                'Provide a comprehensive technical analysis including composition, lighting, color palette, subjects, perspective, and photographic techniques.'
            ],
            'social': [
                'Create a catchy social media caption for this image.',
                'Write an engaging social media caption that would work well on Instagram or Facebook.',
                'Create an engaging social media post with a caption and relevant hashtags for this image.'
            ]
        }
        
        prompt = prompts.get(caption_style, prompts['descriptive'])[detail_level - 1]
        
        # Try OpenAI GPT-4 Vision API
        openai_key = os.environ.get('OPENAI_API_KEY', '')
        
        if openai_key:
            print("Using OpenAI GPT-4 Vision API...")
            api_response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {openai_key}'
                },
                json={
                    'model': 'gpt-4o',
                    'messages': [{
                        'role': 'user',
                        'content': [
                            {
                                'type': 'text',
                                'text': prompt
                            },
                            {
                                'type': 'image_url',
                                'image_url': {
                                    'url': f'data:{media_type};base64,{base64_image}'
                                }
                            }
                        ]
                    }],
                    'max_tokens': 500
                }
            )
            
            if api_response.status_code == 200:
                result = api_response.json()
                caption = result['choices'][0]['message']['content']
                return jsonify({'caption': caption})
            else:
                error_msg = f"OpenAI API Error: {api_response.status_code}"
                try:
                    error_data = api_response.json()
                    error_msg = error_data.get('error', {}).get('message', error_msg)
                except:
                    pass
                return jsonify({'error': error_msg}), 500
        
        # If no OpenAI key, return helpful error
        return jsonify({'error': 'No API key configured. Please set OPENAI_API_KEY environment variable. Get your key from https://platform.openai.com/api-keys'}), 500
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("AI Image Caption Generator")
    print("=" * 60)
    print("\n✓ Server starting...")
    print("✓ Open your browser to: http://localhost:5000")
    print("\nAPI Configuration:")
    if os.environ.get('OPENAI_API_KEY'):
        print("  ✓ OpenAI API key found")
    else:
        print("  ✗ No API key found")
        print("  Set your OpenAI API key:")
        print("    set OPENAI_API_KEY=your-key-here")
    print("\nDemo Account:")
    print("  Email: demo@example.com")
    print("  Password: demo123")
    print("\n" + "=" * 60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)