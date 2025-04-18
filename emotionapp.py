import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import os

st.set_page_config(page_title="감정기록 키링", layout="centered")

st.title("이모션 태그")

# JavaScript로 위치 자동 수집 → 쿼리 파라미터에 담기
st.markdown("""
<script>
navigator.geolocation.getCurrentPosition(
    function(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        const query = "?lat=" + lat + "&lon=" + lon;
        if (!window.location.search.includes("lat")) {
            window.location.href = window.location.pathname + query;
        }
    },
    function(error) {
        alert("❌ 위치 정보를 불러올 수 없습니다. 위치 접근을 허용해주세요.");
    }
);
</script>
""", unsafe_allow_html=True)

# 최신 방식으로 위치 파라미터 불러오기
lat = float(st.query_params.get("lat", [0])[0])
lon = float(st.query_params.get("lon", [0])[0])

if lat and lon:
    st.success(f"📍 현재 위치: 위도 {lat:.5f}, 경도 {lon:.5f}")
else:
    st.warning("위치 정보를 불러오는 중입니다... 브라우저 권한을 확인해주세요!")

# 감정 입력
emotion = st.radio("지금 기분은 어떤가요?", ["😊 많이 행복해", "😢 아 오늘은 좀 슬퍼", "😡 열 받고 화나", "😌 평온하게 차 한잔 하고 싶네 ㅎㅎ"], horizontal=True)
note = st.text_area("이 감정의 이유를 찾아 알려주세요.")

# CSV 데이터 파일 경로
DATA_FILE = "emotion_log.csv"

# 없으면 새로 생성
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["date", "emotion", "note", "latitude", "longitude"]).to_csv(DATA_FILE, index=False)

# 저장 버튼
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
        st.warning("위치 정보가 없어요. 저장이 불가능합니다.")

# 저장된 감정 데이터 불러오기
df = pd.read_csv(DATA_FILE)

# 지도 시각화
st.subheader("🗺 감정이 기록된 장소들")

if not df.empty:
    # 마지막 위치 중심으로 지도 생성
    m = folium.Map(location=[df.iloc[-1]["latitude"], df.iloc[-1]["longitude"]], zoom_start=12)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"{row['date']}<br>{row['emotion']}<br>{row['note']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    folium_static(m)
else:
    st.info("아직 감정 기록이 없습니다. 먼저 감정을 기록해보세요!")

# 기록 테이블 출력
st.subheader("📅 감정 기록 테이블")
st.dataframe(df)
