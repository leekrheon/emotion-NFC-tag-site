import streamlit as st
from datetime import datetime
import pandas as pd
import os

st.set_page_config(page_title="감정기록 키링", layout="centered")

# 📁 데이터 저장용 파일 경로
DATA_FILE = "emotion_log.csv"

if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["date", "emotion", "note", "latitude", "longitude"]).to_csv(DATA_FILE, index=False)

# 🧠 Custom JS로 GPS 위치 가져오기
st.markdown("""
    <script>
    navigator.geolocation.getCurrentPosition(
        function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            const coords = lat + "," + lon;
            window.parent.postMessage({type: "coords", value: coords}, "*");
        }
    );
    </script>
""", unsafe_allow_html=True)

# 📍 현재 위치 초기화
lat, lon = None, None

# 🧪 JS로부터 전달된 좌표 수신
coords = st.experimental_get_query_params().get("coords", None)
if coords:
    try:
        lat, lon = map(float, coords[0].split(','))
    except:
        pass

# 🌈 감정 입력
st.title("📍 감정을 NFC로 기록해요")
emotion = st.radio("지금 기분은 어때요?", ["😊 행복", "😢 슬픔", "😡 화남", "😌 평온"], horizontal=True)
note = st.text_area("기록하고 싶은 메모가 있다면 써보세요.")

# 🔘 저장 버튼
if st.button("감정 저장하기 💾"):
    if lat and lon:
        new_data = pd.DataFrame({
            "date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "emotion": [emotion],
            "note": [note],
            "latitude": [lat],
            "longitude": [lon]
        })
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("감정이 저장되었어요! 💖")
    else:
        st.warning("📍 위치 정보를 불러올 수 없어요. 브라우저에서 위치 접근을 허용해주세요.")

# 📊 기록 조회
st.markdown("---")
st.subheader("📅 지금까지 기록한 감정들")
df = pd.read_csv(DATA_FILE)
st.dataframe(df)
