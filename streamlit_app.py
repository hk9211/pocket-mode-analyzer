import streamlit as st

st.set_page_config(page_title="주머니 오동작 분석기", layout="wide")

st.title("🔍 주머니 오동작 로그 분석기")

st.write("테스트 중...")

uploaded_file = st.file_uploader("📂 로그 파일을 업로드하세요", type=['log', 'txt'])

if uploaded_file is not None:
    st.success("✅ 파일이 업로드되었습니다!")
    st.write(f"파일명: {uploaded_file.name}")
    
    file_content = uploaded_file.read().decode('utf-8', errors='ignore')
    st.write(f"파일 크기: {len(file_content)} bytes")
else:
    st.info("로그 파일을 업로드해주세요")
