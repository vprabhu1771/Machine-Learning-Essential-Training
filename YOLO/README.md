`train.py`

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="construction-ppe.yaml",
    epochs=5,
    imgsz=640
)
```

`ppe2.py`

```python
from dotenv import load_dotenv
import os
import cv2
import requests
import time
import numpy as np
import streamlit as st
from ultralytics import YOLO

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Load model
model = YOLO("runs/detect/train2/weights/best.pt")

# Streamlit UI
st.title("🦺 PPE Detection System")
st.write("Capture image and detect PPE violations")

# Camera input
picture = st.camera_input("📷 Take a picture")

# Telegram alert functions
def send_telegram_alert_message():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": "⚠️ PPE Violation Detected!",
    }
    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        st.error(f"Telegram Error: {e}")


def send_telegram_alert(image):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    _, img_encoded = cv2.imencode('.jpg', image)

    files = {
        'photo': ('image.jpg', img_encoded.tobytes())
    }

    data = {
        "chat_id": CHAT_ID,
        "caption": "⚠️ PPE Violation Detected!",
    }

    try:
        requests.post(url, data=data, files=files, timeout=5)
    except Exception as e:
        st.error(f"Telegram Error: {e}")


# Process image when captured
if picture:
    # Convert image to OpenCV format
    file_bytes = np.asarray(bytearray(picture.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)

    results = model(frame, conf=0.5)

    person_detected = False
    has_helmet = False
    has_vest = False

    # Detection loop
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls].lower()

            if label == "person":
                person_detected = True
            elif label == "helmet":
                has_helmet = True
            elif label == "vest":
                has_vest = True

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            color = (0, 255, 0)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # PPE violation logic
    if person_detected and (not has_helmet or not has_vest):
        st.error("🚨 PPE Violation Detected!")
        send_telegram_alert_message()
        send_telegram_alert(frame)
    else:
        st.success("✅ No Violation Detected")

    # Show processed image
    st.image(frame, channels="BGR", caption="Detection Result")
```

`ppe3.py`
```python
from dotenv import load_dotenv
import os
import cv2
import requests
import numpy as np
import streamlit as st
from ultralytics import YOLO
import pandas as pd

# Load env
load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Load model
model = YOLO("runs/detect/train2/weights/best.pt")

st.title("🦺 PPE Detection Dashboard")

# Session state for tracking
if "person_id_count" not in st.session_state:
    st.session_state.person_id_count = 0

if "people_data" not in st.session_state:
    st.session_state.people_data = {}

# Camera input
picture = st.camera_input("📷 Capture Image")

def send_telegram_alert_message():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": "⚠️ PPE Violation Detected!"}
    requests.post(url, data=data)


def send_telegram_alert(image):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    _, img_encoded = cv2.imencode('.jpg', image)

    files = {'photo': ('image.jpg', img_encoded.tobytes())}
    data = {"chat_id": CHAT_ID, "caption": "⚠️ PPE Violation Detected!"}

    requests.post(url, data=data, files=files)


if picture:
    file_bytes = np.asarray(bytearray(picture.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)

    results = model(frame, conf=0.5)

    persons = []
    helmets = []
    vests = []

    # Collect detections
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls].lower()
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            if label == "person":
                persons.append((cx, cy, x1, y1, x2, y2))
            elif label == "helmet":
                helmets.append((cx, cy))
            elif label == "vest":
                vests.append((cx, cy))

    total_persons = len(persons)
    violations = 0

    table_data = []

    # Assign IDs and check PPE
    for person in persons:
        cx, cy, x1, y1, x2, y2 = person

        st.session_state.person_id_count += 1
        person_id = st.session_state.person_id_count

        has_helmet = any(abs(cx - hx) < 100 and abs(cy - hy) < 100 for hx, hy in helmets)
        has_vest = any(abs(cx - vx) < 100 and abs(cy - vy) < 100 for vx, vy in vests)

        status = "Safe"
        color = (0, 255, 0)

        if not has_helmet or not has_vest:
            status = "Violation"
            color = (0, 0, 255)
            violations += 1

            send_telegram_alert_message()
            send_telegram_alert(frame)

        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"ID:{person_id} {status}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        table_data.append({
            "Person ID": person_id,
            "Helmet": has_helmet,
            "Vest": has_vest,
            "Status": status
        })

    # 📊 DASHBOARD METRICS
    st.subheader("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👷 Persons", total_persons)
    col2.metric("🚨 Violations", violations)

    helmet_rate = 0 if total_persons == 0 else (sum([1 for p in table_data if p["Helmet"]]) / total_persons) * 100
    vest_rate = 0 if total_persons == 0 else (sum([1 for p in table_data if p["Vest"]]) / total_persons) * 100

    col3.metric("⛑ Helmet %", f"{helmet_rate:.1f}%")
    col4.metric("🦺 Vest %", f"{vest_rate:.1f}%")

    # 🧠 PERSON TABLE
    st.subheader("🧠 Person-wise Tracking")
    df = pd.DataFrame(table_data)
    st.dataframe(df)

    # Show image
    st.image(frame, channels="BGR", caption="Detection Result")
```
