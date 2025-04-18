import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import os

st.set_page_config(page_title="감정기록 키링", layout="centered")

DATA_FILE = "emotion_log.csv"

# 파일 없으면 새로 생성
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["date", "emotion", "note", "latitude", "longitude"]).to_csv(DATA_FILE, index=False)

st.title("📍 감정을 기록해요 (NFC 키링)")

# JavaScript로 GPS 정보 받아오기
st.markdown("""
<script>
navigator.geolocation.getCurrentPosition(
    function(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        const query = "?lat=" + lat + "&lon=" + lon;
        window.location.href = window.location.pathname + query;
    }
);
</script>
""", unsafe_allow_html=True)

# 현재 좌표 가져오기
query_params = st.experimental_get_query_params()
lat = float(query_params.get("lat", [0])[0])
lon = float(query_params.get("lon", [0])[0])

if lat != 0 and lon != 0:
    st.success(f"📍 현재 위치: 위도 {lat:.5f}, 경도 {lon:.5f}")

# 감정 입력
emotion = st.radio("지금 기분은 어떤가요?", ["😊 행복", "😢 슬픔", "😡 화남", "😌 평온"], horizontal=True)
note = st.text_area("오늘의 메모를 남겨보세요")

# 감정 저장 버튼
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
        st.warning("위치 정보를 불러오지 못했습니다.")

# 저장된 기록 읽기
df = pd.read_csv(DATA_FILE)

# 🌍 지도 시각화
st.subheader("🗺 감정이 기록된 장소들")
if not df.empty:
    m = folium.Map(location=[df.iloc[-1]["latitude"], df.iloc[-1]["longitude"]], zoom_start=12)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"{row['date']}<br>{row['emotion']}<br>{row['note']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    folium_static(m)
else:
    st.info("아직 감정 기록이 없습니다. 먼저 기록해보세요!")

# 📊 감정 테이블
st.subheader("📅 감정 기록 테이블")
st.dataframe(df)

