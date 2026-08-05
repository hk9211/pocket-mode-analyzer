# 🚀 클라우드 배포 가이드 (Streamlit Cloud)

## 📋 5분만에 배포 완료!

---

## 단계 1️⃣: GitHub 계정 만들기

### 이미 GitHub 계정이 있다면 "단계 2"로 건너뛰세요

1. https://github.com/signup 접속
2. 이메일 입력 → 비밀번호 → 사용자명 입력
3. 이메일 인증 (메일함 확인)
4. ✅ GitHub 계정 완료!

---

## 단계 2️⃣: 파일 준비

다음 **3개 파일**을 GitHub에 올릴 준비:

```
📁 pocket-mode-analyzer
  ├─ streamlit_app.py       (웹앱 코드)
  ├─ requirements.txt        (필요 라이브러리)
  └─ README.md              (설명서)
```

---

## 단계 3️⃣: GitHub에 저장소(Repository) 만들기

### 3-1) GitHub 로그인
- https://github.com 접속
- 우측 상단 프로필 → **New repository** 클릭

### 3-2) 저장소 만들기
```
Repository name: pocket-mode-analyzer
Description: 주머니 오동작 로그 분석기
Public 선택 (중요!)
```

**"Create repository" 클릭** ✅

### 3-3) 파일 업로드

GitHub 화면에서:
1. **"Add file"** → **"Upload files"** 클릭
2. 다음 3개 파일을 드래그&드롭:
   - `streamlit_app.py`
   - `requirements.txt`
   - `README.md`
3. **"Commit changes"** 클릭

---

## 단계 4️⃣: Streamlit Cloud에 배포

### 4-1) Streamlit Cloud 접속
- https://streamlit.io/cloud 접속
- **"Sign up"** (GitHub 로그인)

### 4-2) 앱 배포
1. **"New app"** 버튼 클릭
2. 다음 정보 입력:
   ```
   Repository: pocket-mode-analyzer
   Branch: main
   Main file path: streamlit_app.py
   ```
3. **"Deploy"** 클릭

### 4-3) 배포 대기
```
🟡 배포 중...  → 🟢 배포 완료! (1-2분 소요)
```

---

## 🎉 배포 완료!

자동으로 생성된 **공개 URL** 확인:

```
https://pocket-mode-analyzer-xxxxx.streamlit.app/
```

이 링크를 **브라우저에 열면** 바로 사용 가능합니다! 🚀

---

## 💾 파일 내용 (복사해서 만들기)

### 파일 1: `streamlit_app.py`
→ 위에서 생성한 코드 사용

### 파일 2: `requirements.txt`
```
streamlit==1.35.0
pandas==2.1.4
```

### 파일 3: `README.md`
```markdown
# 주머니 오동작 로그 분석기

## 사용 방법
1. 로그 파일 업로드
2. 자동 분석
3. 결과 확인 및 다운로드

## 지원 센서
- STM
- Synaptics  
- Goodix

## 분석 항목
- 둔감모드 진입/해제
- 주머니 내 터치 횟수
```

---

## 🔗 공유 방법

배포 후 링크를 팀원들과 공유:

```
💬 카톡: https://pocket-mode-analyzer-xxxxx.streamlit.app/
📧 메일: 링크 복사해서 전송
📋 문서: 링크 추가
```

**아무나 클릭하면 바로 사용 가능!** ✅

---

## ⚙️ 자동 업데이트

파일을 수정하면 자동으로 반영됩니다:

1. GitHub의 파일 수정
2. Commit & Push
3. 1-2분 후 웹사이트 자동 업데이트 ✅

---

## 🆘 문제 해결

### Q: "Repository not found" 오류
**A:** 저장소가 **Public**으로 설정되어 있는지 확인
- GitHub → Settings → Change repository visibility → Public

### Q: 배포가 실패했어요
**A:** 
1. `requirements.txt` 파일 확인
2. `streamlit_app.py`의 파일명 확인
3. Streamlit Cloud에서 재배포 시도

### Q: 파일을 수정했는데 반영이 안 돼요
**A:** 
1. GitHub에 정상 커밋되었는지 확인
2. Streamlit Cloud에서 재배포 클릭
3. 5분 정도 기다렸다가 새로고침

---

## 📊 배포 후 사용 흐름

```
사용자 방문
    ↓
로그 파일 업로드
    ↓
자동 분석 (서버에서)
    ↓
결과 화면 표시
    ↓
CSV 다운로드
```

---

## 💡 팁

### 1️⃣ 로그 파일 한번에 여러 개 분석
- 여러 번 업로드해서 각각 분석 가능
- 결과 비교 가능

### 2️⃣ 성능 개선
- 매우 큰 로그 파일(500MB+)은 분석에 시간 소요
- 필요한 부분만 추출해서 업로드 권장

### 3️⃣ 팀 공유
- 링크만 공유하면 권한 설정 필요 없음
- 누구나 접속 가능

---

## 🎯 완전한 배포 체크리스트

- [ ] GitHub 계정 생성
- [ ] 저장소(Repository) 생성
- [ ] 파일 3개 업로드
- [ ] Streamlit Cloud 계정 생성
- [ ] 앱 배포
- [ ] 배포된 링크 확인
- [ ] 로그 파일로 테스트
- [ ] 팀원에게 링크 공유

---

## 📝 배포된 앱 정보

```
앱 이름: Pocket Mode Analyzer
플랫폼: Streamlit Cloud
비용: 무료 🎉
특징: 
  - 자동 업데이트
  - 항상 최신 버전
  - 어디서나 접속 가능
  - 모바일도 지원
```

---

## 🚀 배포 후 확인사항

배포 후 다음을 확인하세요:

1. **로그 파일 업로드 테스트**
   ```
   당신의 로그 파일 업로드 → 결과 확인
   ```

2. **CSV 다운로드 테스트**
   ```
   다운로드 버튼 클릭 → 파일 저장 → Excel에서 열기
   ```

3. **모바일 테스트**
   ```
   핸드폰에서 링크 접속 → 파일 업로드 가능한지 확인
   ```

---

## 📞 추가 지원

문제가 있으면:

1. **Streamlit 문서**: https://docs.streamlit.io
2. **GitHub Issues**: 저장소의 Issues 탭
3. **우리팀**: 개발팀에 연락

---

**배포 완료 후 URL을 팀원들과 공유하세요!** 🎉

---

*Last Updated: 2026-07-15*
