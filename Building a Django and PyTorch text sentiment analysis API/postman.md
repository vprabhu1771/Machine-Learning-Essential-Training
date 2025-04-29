To test your **`SentimentAnalysisView` API** in Postman, follow these steps:

---

### ✅ 1. **Start Django Server**
In your terminal:
```bash
python manage.py runserver
```

---

### ✅ 2. **Postman Setup**

#### 🔹 **HTTP Method**: `POST`

#### 🔹 **URL**:
```http
http://127.0.0.1:8000/api/sentiment/   # or your actual route
```

> Make sure this URL matches the one you configured in `urls.py`.

#### 🔹 **Headers**:
```http
Content-Type: application/json
```

#### 🔹 **Body (raw → JSON)**:
```json
{
  "text": "I love this product. It's amazing!"
}
```

---

### ✅ 3. **Expected Response (Example)**:
```json
{
  "sentiment": "Positive"
}
```

---

### ✅ 4. **Sample `urls.py` Configuration**
Make sure your `SentimentAnalysisView` is connected properly in `urls.py`:

```python
from django.urls import path
from .views import SentimentAnalysisView

urlpatterns = [
    path('api/sentiment/', SentimentAnalysisView.as_view(), name='sentiment-analysis'),
]
```

---

Would you like help writing the `simple_tokenizer` function or testing with real tokenization logic?
