```python
from dotenv import load_dotenv
import os
import cv2
import requests
import numpy as np
import streamlit as st
from ultralytics import YOLO
import pandas as pd
import time
from datetime import datetime


def get_timestamp():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# -------------------- CONFIG --------------------
load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Load model
model = YOLO("runs/detect/train/weights/best.pt")

st.set_page_config(page_title="PPE Dashboard", layout="wide")
st.title("🦺 PPE Detection Dashboard")

# -------------------- SESSION STATE --------------------
if "person_id_count" not in st.session_state:
    st.session_state.person_id_count = 0

if "last_alert" not in st.session_state:
    st.session_state.last_alert = 0

# -------------------- SIDEBAR --------------------
st.sidebar.title("🧭 Navigation")
mode = st.sidebar.radio("Select Mode", [
    "📷 Capture Image",
    "📁 Upload Image",
    "🎥 Live Tracking"
])

# -------------------- TELEGRAM ALERT --------------------
def send_telegram_alert(frame, message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        _, img_encoded = cv2.imencode('.jpg', frame)

        files = {'photo': ('image.jpg', img_encoded.tobytes())}
        data = {
            "chat_id": CHAT_ID,
            "caption": message
        }

        requests.post(url, data=data, files=files)
    except:
        pass


def is_helmet_on_head(px1, py1, px2, py2, helmets):
    for hx, hy in helmets:
        # helmet must be inside person width
        if px1 < hx < px2:
            # helmet must be in upper 40% of person
            if py1 < hy < (py1 + (py2 - py1) * 0.4):
                return True
    return False

# -------------------- CORE DETECTION FUNCTION --------------------
def process_frame(frame):
    # results = model(frame, conf=0.5)
    # print(results)
    results = model(frame, conf=0.25)
    results[0].show()

    persons, helmets, vests = [], [], []

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

    for person in persons:
        cx, cy, x1, y1, x2, y2 = person

        st.session_state.person_id_count += 1
        person_id = st.session_state.person_id_count

        # has_helmet = any(abs(cx - hx) < 100 and abs(cy - hy) < 100 for hx, hy in helmets)
        has_helmet = is_helmet_on_head(x1, y1, x2, y2, helmets)
        has_vest = any(abs(cx - vx) < 100 and abs(cy - vy) < 100 for vx, vy in vests)

        status = "Safe"
        color = (0, 255, 0)

        timestamp = get_timestamp()

        if not has_helmet or not has_vest:
            status = "Violation"
            color = (0, 0, 255)
            violations += 1

            message = f"""
        🚨 PPE VIOLATION
        👤 Person ID: {person_id}
        ⛑ Helmet: {'❌' if not has_helmet else '✅'}
        🦺 Vest: {'❌' if not has_vest else '✅'}
        📅 Time: {timestamp}
        """

        else:
            status = "Safe"
            color = (0, 255, 0)

            message = f"""
        ✅ PPE SAFE
        👤 Person ID: {person_id}
        ⛑ Helmet: ✅
        🦺 Vest: ✅
        📅 Time: {timestamp}
        """

        # Send alert with cooldown
        if time.time() - st.session_state.last_alert > 10:
            send_telegram_alert(frame, message)
            st.session_state.last_alert = time.time()

        # Draw box
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

    return frame, total_persons, violations, table_data


# -------------------- MODE 1: CAMERA CAPTURE --------------------
if mode == "📷 Capture Image":
    picture = st.camera_input("Capture Image")

    if picture:
        file_bytes = np.asarray(bytearray(picture.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)

        frame, total_persons, violations, table_data = process_frame(frame)

        st.image(frame, channels="BGR")

# -------------------- MODE 2: IMAGE UPLOAD --------------------
elif mode == "📁 Upload Image":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)

        frame, total_persons, violations, table_data = process_frame(frame)

        st.image(frame, channels="BGR")

# -------------------- MODE 3: LIVE TRACKING --------------------
elif mode == "🎥 Live Tracking":
    run = st.checkbox("Start Camera")

    FRAME_WINDOW = st.image([])
    cap = cv2.VideoCapture(0)

    while run:
        ret, frame = cap.read()
        if not ret:
            st.error("Camera not working")
            break

        frame, total_persons, violations, table_data = process_frame(frame)

        FRAME_WINDOW.image(frame, channels="BGR")

    cap.release()

# -------------------- DASHBOARD --------------------
if 'table_data' in locals():
    st.subheader("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👷 Persons", total_persons)
    col2.metric("🚨 Violations", violations)

    helmet_rate = 0 if total_persons == 0 else (
        sum([1 for p in table_data if p["Helmet"]]) / total_persons
    ) * 100

    vest_rate = 0 if total_persons == 0 else (
        sum([1 for p in table_data if p["Vest"]]) / total_persons
    ) * 100

    col3.metric("⛑ Helmet %", f"{helmet_rate:.1f}%")
    col4.metric("🦺 Vest %", f"{vest_rate:.1f}%")

    st.subheader("🧠 Person-wise Tracking")
    df = pd.DataFrame(table_data)
    st.dataframe(df)
```
