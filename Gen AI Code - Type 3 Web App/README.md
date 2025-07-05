Sure! Let’s build a **simple web page** that calls your Flask Gen AI API and displays the generated C code.

This page will have:
✅ HTML form to enter the prompt
✅ CSS to style it nicely
✅ JavaScript (fetch) to call your local Flask API and show the result

All running **locally**, no external dependencies.

---

## 📦 Folder structure

```
project/
├── app.py                ← your Flask API
└── static/
    ├── index.html
    ├── style.css
    └── script.js
```

---

## 📝 `index.html`

Save this as `static/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Gen AI for Coding</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
  <div class="container">
    <h1>Gen AI: Generate C Code</h1>
    <textarea id="prompt" placeholder="Enter your prompt..."></textarea>
    <button onclick="generateCode()">Generate</button>
    <h3>Generated C Code:</h3>
    <pre id="output"></pre>
  </div>
  <script src="static/script.js"></script>
</body>
</html>
```

---

## 🎨 `style.css`

Save this as `static/style.css`:

```css
body {
    font-family: 'Segoe UI', sans-serif;
    background: #f4f4f4;
    margin: 0;
    padding: 0;
}

.container {
    max-width: 700px;
    margin: 50px auto;
    background: #fff;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

h1 {
    text-align: center;
    color: #333;
}

textarea {
    width: 100%;
    height: 100px;
    margin-top: 10px;
    padding: 10px;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
}

button {
    margin-top: 10px;
    padding: 10px 20px;
    font-size: 1rem;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background: #45a049;
}

pre {
    background: #272822;
    color: #f8f8f2;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
}
```

---

## ⚡ `script.js`

Save this as `static/script.js`:

```javascript
async function generateCode() {
    const prompt = document.getElementById('prompt').value;
    const outputEl = document.getElementById('output');
    outputEl.textContent = "Generating...";

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt })
        });

        const data = await response.json();

        if (response.ok) {
            outputEl.textContent = data.generated_code;
        } else {
            outputEl.textContent = data.error || "Error generating code";
        }
    } catch (err) {
        outputEl.textContent = "Request failed: " + err.message;
    }
}
```

---

## 🐍 Update `app.py` to serve HTML

Update your Flask API to serve this HTML page at `/`:

```python
from flask import Flask, request, jsonify, send_from_directory
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = Flask(__name__, static_folder='static')

# Load model and tokenizer once when starting the server
print("Loading model ....")
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-350M-mono")
model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-350M-mono")
print("Model loaded")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/generate', methods=['POST'])
def generate_c_code():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    # Encode the prompt
    inputs = tokenizer.encode(prompt, return_tensors="pt")

    # Generate code
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=256,
            do_sample=True,
            temperature=0.7
        )

    generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({'generated_code': generated_code})

if __name__ == '__main__':
    app.run(debug=True)
```

---

✅ Now:

* Run:

```bash
python app.py
```

* Open browser:

```
http://127.0.0.1:5000
```

You’ll see your HTML page, enter prompt, click **Generate**, and see the C code!

---

## 🚀 **Done!**

If you'd like:

* I can help add copy button
* Highlight syntax with highlight.js
* Deploy to server

Just say **“yes”**! 🌱
