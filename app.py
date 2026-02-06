import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder
import os

# 화면을 넓게 쓰고 제목을 정함
st.set_page_config(page_title="나만의 4개국어 선생님", layout="wide")

# 1. 언어 설정 (국기, 이름, 번역 코드)
LANGS = {
    "한국어": ["🇰🇷", "ko"],
    "영어": ["🇺🇸", "en"],
    "중국어": ["🇨🇳", "zh-CN"],
    "일본어": ["🇯🇵", "ja"]
}

st.title("🌐 4개국어 한눈에 공부하기")
st.write("---")

# 2. 입력창 (글자 입력과 음성 인식)
input_text = st.text_input("학습할 한글 문장을 입력하세요", placeholder="예: 오늘 날씨가 정말 좋아!")
audio_data = mic_recorder(start_prompt="🎤 목소리로 입력하기", stop_prompt="🛑 녹음 중지", key='recorder')

if input_text:
    # 4개의 칸을 나란히 만듦
    cols = st.columns(len(LANGS))
    
    for i, (name, info) in enumerate(LANGS.items()):
        with cols[i]:
            flag, code = info
            
            # 번역 실행 (한국어에서 해당 언어로)
            translated = GoogleTranslator(source='ko', target=code).translate(input_text)
            
            # 화면 디자인 (국기, 이름, 큰 자막)
            st.markdown(f"### {flag} {name}")
            
            # 브라우저 번역 방지를 위한 HTML 코드와 큰 글자 설정
            st.markdown(f"""
                <div class="notranslate" style="
                    background-color: #f0f2f6; 
                    padding: 20px; 
                    border-radius: 10px; 
                    font-size: 24px; 
                    font-weight: bold; 
                    color: #1f77b4;
                    min-height: 100px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    margin-bottom: 10px;
                ">
                    {translated}
                </div>
            """, unsafe_allow_html=True)
            
            # 음성 파일 생성 및 재생 (일시정지/다시듣기 가능)
            try:
                tts = gTTS(text=translated, lang=code)
                filename = f"{code}.mp3"
                tts.save(filename)
                with open(filename, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
                os.remove(filename) # 임시 파일 삭제
            except:
                st.error("소리를 만들 수 없어요.")

st.write("---")
st.caption("💡 팁: 영어 자막이 한글로 보인다면 브라우저 주소창 오른쪽의 '번역 아이콘'을 눌러 '원본 보기'를 선택하세요!")