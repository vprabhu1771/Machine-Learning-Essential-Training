Got it — you want **not just code formatting**, but **fix the logic** between `predict(text)` and `simple_tokenizer(text)`.

Let’s break it down carefully:

---
### Your current situation:
- `predict(text)` → runs a **HuggingFace sentiment analysis model** on `text`.
- `simple_tokenizer(text)` → just **tokenizes manually** based on a dictionary.

**They are two different logics**:
- `predict()` works on *text as a whole sentence*.
- `simple_tokenizer()` *splits text manually into integers*, but **not** linked to real prediction.

---
### What you likely meant:

You want a **simple custom flow** like:
1. Tokenize input text.
2. Based on tokenized words (maybe basic logic like positive words = positive, negative words = negative) **predict manually**, not using the heavy HuggingFace pipeline.

---
### So here's the **real fix** for your logic:

I will fix it fully:

```python
# tokenizer.py
def simple_tokenizer(text):
    word2idx = {
        'i': 1, 'love': 2, 'hate': 3, 'this': 4, 'movie': 5,
        'is': 6, 'good': 7, 'bad': 8, 'job': 9
    }
    tokens = [word2idx.get(word.lower(), 0) for word in text.split()]
    return tokens

# predictor.py
def predict(text):
    positive_words = {'love', 'good'}
    negative_words = {'hate', 'bad'}

    words = text.lower().split()
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)

    if positive_count > negative_count:
        sentiment = 'POSITIVE'
    elif negative_count > positive_count:
        sentiment = 'NEGATIVE'
    else:
        sentiment = 'NEUTRAL'

    print(f"Predicted Sentiment: {sentiment}")
    return sentiment

# Main code
if __name__ == "__main__":
    text = "i love this job"
    
    tokens = simple_tokenizer(text)
    print(f"Tokens: {tokens}")
    
    predict(text)
```

---
### ✅ Output:
```
Tokens: [1, 2, 4, 9]
Predicted Sentiment: POSITIVE
```

---
### **Summary of the logic fix:**
- **`simple_tokenizer(text)`**: Only tokenizes words → list of numbers.
- **`predict(text)`**: Manually decides sentiment → based on counting positive and negative words.
- No mixing HuggingFace heavy pipeline if you want *simple*, *lightweight* logic.

---

If you still want to **use HuggingFace** but **also show the tokenized version** for learning, I can show a **combined version** too.  
Would you like that? 🔥 (HuggingFace + manual tokenizer together?)
