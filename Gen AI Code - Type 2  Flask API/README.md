Absolutely! Let’s **turn the local Gen AI for C coding into a Flask API**.

This way, you can send an HTTP request with a prompt, and get generated C code back — all running **locally, no third-party API**.

---

## ✅ Step-by-step: Convert to Flask API

### ✏️ Step 1: Install dependencies

```bash
pip install flask transformers torch
```

---

### 🛠 Step 2: Create `app.py`

Here’s the **full** Python code for the Flask API:

```python
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = Flask(__name__)

# Load model and tokenizer once when starting the server
print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-350M-mono")
model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-350M-mono")
print("Model loaded!")

@app.route('/generate', methods=['POST'])
def generate_c_code():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

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

## 🚀 Step 3: Run the Flask API

```bash
python app.py
```

It will run at:

```
http://127.0.0.1:5000
```

---

## 📡 Step 4: Use the API

### ✅ Example cURL request:

```bash
curl -X POST http://127.0.0.1:5000/generate \
     -H "Content-Type: application/json" \
     -d '{"prompt": "/* Write a C program to find the sum of digits */"}'
```

---

### ✅ Example Python request:

```python
import requests

response = requests.post('http://127.0.0.1:5000/generate', json={
    'prompt': '/* Write a C program to check if a number is prime */'
})

data = response.json()
print("Generated C code:\n")
print(data['generated_code'])
```

---

## 🌱 **Now you have:**

✅ Local Gen AI
✅ No external API
✅ Flask API endpoint `/generate`
✅ Takes prompt, returns generated C code

---

If you'd like, I can also help add:

* Streaming output (for large code)
* Save to `.c` file automatically
* Web frontend to call this API

Just let me know! 🚀


Sure! Here’s how you can **test your local Flask Gen AI API in Postman** step by step.

---

## ✅ Step-by-step: Test `/generate` Flask API in Postman

### 🛠 Step 1: Make sure your Flask API is running

Run:

```bash
python app.py
```

By default, it should be available at:

```
http://127.0.0.1:5000
```

---

### ✏️ Step 2: Open Postman and create a new request

1. Open Postman.
2. Click **"New" → "HTTP Request"**.
3. Change method to **POST**.
4. Enter the URL:

```
http://127.0.0.1:5000/generate
```

---

### 🧩 Step 3: Add request body

1. Go to the **Body** tab.
2. Select **raw**.
3. Select **JSON** (from the dropdown on the right).
4. Enter this JSON:

```json
{
    "prompt": "/* Write a C program to print Fibonacci series */"
}
```

---

### 📦 Step 4: Send request & see response

1. Click **Send**.
2. You should get a JSON response like:

```json
{
    "generated_code": "/* Write a C program to print Fibonacci series */\n#include <stdio.h>\n..."
}
```

---

✅ **That’s it!**
You’ve successfully tested your local Gen AI for C coding using Postman.

---

## ⭐ **Extra:**

If you'd like, I can also help you:

* Export this Postman request as a **collection**
* Document the API in Postman
* Create an environment for local / production

Just tell me! 🚀
