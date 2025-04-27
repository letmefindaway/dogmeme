
import base64
import requests
import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

API_KEY = "sk-tzWetLxbCjrBynasNLnMtlVzgEjcQVu4NV1CccwF0WPZc5QY"  

url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"

def generate_image(prompt):
    body = {
        "steps": 40,
        "width": 512,
        "height": 512,
        "seed": 0,
        "cfg_scale": 5,
        "samples": 1,
        "style_preset": "analog-film",  # analog film style
        "text_prompts": [
            {
                "text": prompt,
                "weight": 1
            },
            {
                "text": "blurry, bad",
                "weight": -1
            }
        ],
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    if not os.path.exists("./static/images"):
        os.makedirs("./static/images")

    for i, image in enumerate(data["artifacts"]):
        img_data = base64.b64decode(image["base64"])
        file_path = f'./static/images/bonk_meme_{image["seed"]}.png'
        with open(file_path, "wb") as f:
            f.write(img_data)

        return f"/static/images/bonk_meme_{image['seed']}.png"

# Endpoint for generating meme
@app.route('/generate-meme', methods=['POST'])
def generate_meme():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        final_prompt = f"dog {prompt}"
        image_path = generate_image(final_prompt)
        return jsonify({'image_url': image_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Root endpoint (serves HTML frontend)
@app.route('/')
def index():
    return render_template('index.html', bg1="/static/images/bg1.png", bg2="/static/images/bg2.png", bg3="/static/images/bg3.png", bg4="/static/images/bg4.png")


if __name__ == '__main__':
    app.run(debug=True)
