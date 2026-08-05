import streamlit as st
import re
from collections import defaultdict
import csv
from io import StringIO
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="주머니 오동작 분석기", layout="wide")

# CSS 스타일
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .header-style {
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success {
        color: #00a86b;
        font-weight: bold;
    }
    .warning {
        color: #ff9500;
        font-weight: bold;
    }
    .error {
        color: #ff4444;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 제목
st.markdown('<div class="header-style">🔍 주머니 오동작 로그 분석기</div>', unsafe_allow_html=True)
st.markdown("**Pocket Mode Log Analyzer** - 둔감모드 진입 및 터치 횟수 자동 분석")

st.markdown("---")

class PocketModeAnalyzer:
    def __init__(self):
        self.sensor_type = None
        self.low_sensitivity_events = []
        self.touch_count = 0
        self.status_logs = []
        
    def detect_sensor_type(self, log_content):
        """로그에서 센서 타입 감지"""
        if 'stm_ts_status_event' in log_content:
            return 'STM'
        elif 'synaptics_ts_status_event' in log_content:
            return 'Synaptics'
        elif 'goodix_parse_status' in log_content:
            return 'Goodix'
        return 'Unknown'
    
    def parse_low_sensitivity_logs(self, log_content):
        """둔감모드 진입 로그 분석"""
        pattern = r'(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+)\s+.+\[sec_input\]\s+low_sensitivity_mode_enable:\s+(enable|disable)'
        
        matches = re.finditer(pattern, log_content)
        for match in matches:
            timestamp = match.group(1)
            status = match.group(2)
            
            event = {
                'timestamp': timestamp,
                'status': 'Enable' if status == 'enable' else 'Disable',
                'raw_status': status
            }
            self.low_sensitivity_events.append(event)
        
        return len(self.low_sensitivity_events) > 0
    
    def parse_stm_touch_logs(self, log_content):
        """STM 센서 터치 카운트 분석"""
        pattern = r'\[sec_input\]\s+stm_ts_status_event:\s+STATUS\s+49\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)'
        
        matches = re.finditer(pattern, log_content)
        for match in matches:
            hex_byte1 = match.group(5)
            hex_byte2 = match.group(6)
            last_byte = match.group(7)
            
            if last_byte == '1':
                try:
                    hex_combined = hex_byte1 + hex_byte2
                    touch_count = int(hex_combined, 16)
                    self.status_logs.append({
                        'sensor': 'STM',
                        'hex': hex_combined,
                        'count': touch_count
                    })
                except ValueError:
                    pass
        
        if self.status_logs:
            self.touch_count = max([log['count'] for log in self.status_logs])
        
        return len(self.status_logs) > 0
    
    def parse_synaptics_touch_logs(self, log_content):
        """Synaptics 센서 터치 카운트 분석"""
        pattern = r'\[sec_input\]\s+synaptics_ts_status_event:\s+STATUS\s+1d\s+86\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)'
        
        matches = re.finditer(pattern, log_content)
        for match in matches:
            hex_byte1 = match.group(4)
            hex_byte2 = match.group(5)
            
            try:
                hex_combined = hex_byte1 + hex_byte2
                touch_count = int(hex_combined, 16)
                self.status_logs.append({
                    'sensor': 'Synaptics',
                    'hex': hex_combined,
                    'count': touch_count
                })
            except ValueError:
                pass
        
        if self.status_logs:
            self.touch_count = max([log['count'] for log in self.status_logs])
        
        return len(self.status_logs) > 0
    
    def parse_goodix_touch_logs(self, log_content):
        """Goodix 센서 터치 카운트 분석"""
        pattern = r'goodix_parse_status:\s+status\s+:\s+type\(7\),\s+id\(116\),\s+data\[0x0\s+0x0\s+(0x[\da-f]+)\s+(0x[\da-f]+)\s+0x[\da-f]+\]'
        
        matches = re.finditer(pattern, log_content, re.IGNORECASE)
        for match in matches:
            hex_byte1 = match.group(1).replace('0x', '')
            hex_byte2 = match.group(2).replace('0x', '')
            
            try:
                hex_combined = hex_byte1 + hex_byte2
                touch_count = int(hex_combined, 16)
                self.status_logs.append({
                    'sensor': 'Goodix',
                    'hex': hex_combined,
                    'count': touch_count
                })
            except ValueError:
                pass
        
        if self.status_logs:
            self.touch_count = max([log['count'] for log in self.status_logs])
        
        return len(self.status_logs) > 0
    
    def analyze(self, log_content):
        """전체 로그 분석"""
        self.sensor_type = self.detect_sensor_type(log_content)
        
        # 둔감모드 분석
        has_low_sensitivity = self.parse_low_sensitivity_logs(log_content)
        
        # 터치 카운트 분석
        has_touch_logs = (self.parse_stm_touch_logs(log_content) or 
                         self.parse_synaptics_touch_logs(log_content) or 
                         self.parse_goodix_touch_logs(log_content))
        
        return {
            'sensor_type': self.sensor_type,
            'has_low_sensitivity': has_low_sensitivity,
            'has_touch_logs': has_touch_logs
        }
    
    def get_report_data(self):
        """보고서 데이터 반환"""
        enable_count = sum(1 for e in self.low_sensitivity_events if e['status'] == 'Enable')
        disable_count = sum(1 for e in self.low_sensitivity_events if e['status'] == 'Disable')
        
        return {
            'sensor_type': self.sensor_type,
            'enable_count': enable_count,
            'disable_count': disable_count,
            'total_events': len(self.low_sensitivity_events),
            'touch_count': self.touch_count,
            'touch_logs_count': len(self.status_logs),
            'low_sensitivity_events': self.low_sensitivity_events,
            'status_logs': self.status_logs
        }

# 파일 업로드
uploaded_file = st.file_uploader("📂 로그 파일을 업로드하세요 (.log)", type=['log', 'txt'])

if uploaded_file is not None:
    # 파일 읽기
    file_content = uploaded_file.read().decode('utf-8', errors='ignore')
    
    # 분석 실행
    analyzer = PocketModeAnalyzer()
    result = analyzer.analyze(file_content)
    report = analyzer.get_report_data()
    
    st.success(f"✅ 파일 분석 완료!")
    
    # 결과 표시
    st.markdown("---")
    st.markdown("### 📊 분석 결과")
    
    # 센서 타입
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔍 센서 타입", report['sensor_type'])
    
    # 둔감모드 분석
    st.markdown("#### [1] 둔감모드(Low Sensitivity Mode) 분석")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("✅ 진입(Enable)", f"{report['enable_count']}회")
    with col2:
        st.metric("❌ 해제(Disable)", f"{report['disable_count']}회")
    with col3:
        st.metric("📊 총 이벤트", f"{report['total_events']}회")
    
    # 평가
    total = report['total_events']
    if total == 0:
        eval_text = "✅ **정상** - 주머니 감지 문제 없음"
        eval_color = "success"
    elif total <= 5:
        eval_text = "✅ **정상** - 가끔씩 감지"
        eval_color = "success"
    elif total <= 10:
        eval_text = "⚠️ **주의** - 주머니 오동작 빈번"
        eval_color = "warning"
    else:
        eval_text = "❌ **문제** - 주머니 오동작 심각"
        eval_color = "error"
    
    st.markdown(f'<div class="result-box"><span class="{eval_color}">{eval_text}</span></div>', 
                unsafe_allow_html=True)
    
    # 이벤트 타임라인
    if report['low_sensitivity_events']:
        st.markdown("**📅 최근 이벤트 (최대 10개):**")
        timeline_data = []
        for event in report['low_sensitivity_events'][-10:]:
            timeline_data.append({
                '시간': event['timestamp'],
                '상태': event['status']
            })
        st.dataframe(pd.DataFrame(timeline_data), use_container_width=True)
    
    # 터치 횟수 분석
    st.markdown("---")
    st.markdown("#### [2] 주머니 내 터치 횟수 분석")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🖱️ 최대 터치 횟수", f"{report['touch_count']}회")
    with col2:
        st.metric("📝 로그 개수", f"{report['touch_logs_count']}개")
    
    # 터치 횟수 평가
    touch = report['touch_count']
    if touch == 0:
        touch_eval = "✅ **정상** - 터치 오동작 없음"
        touch_color = "success"
    elif touch <= 500:
        touch_eval = "✅ **정상** - 경미한 오동작"
        touch_color = "success"
    elif touch <= 1000:
        touch_eval = "⚠️ **주의** - 적당한 수준의 오동작"
        touch_color = "warning"
    else:
        touch_eval = "❌ **문제** - 심각한 터치 오동작"
        touch_color = "error"
    
    st.markdown(f'<div class="result-box"><span class="{touch_color}">{touch_eval}</span></div>', 
                unsafe_allow_html=True)
    
    # 터치 통계
    if report['status_logs']:
        counts = [log['count'] for log in report['status_logs']]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("최소", f"{min(counts)}회")
        with col2:
            st.metric("평균", f"{sum(counts)/len(counts):.1f}회")
        with col3:
            st.metric("최대", f"{max(counts)}회")
        
        # 상세 로그 테이블
        st.markdown("**📝 상세 터치 로그 (최대 20개):**")
        log_data = []
        for log in sorted(report['status_logs'][-20:], key=lambda x: x['count'], reverse=True):
            log_data.append({
                '센서': log['sensor'],
                '16진수': f"0x{log['hex']}",
                '10진수': f"{log['count']}회"
            })
        st.dataframe(pd.DataFrame(log_data), use_container_width=True)
    
    # CSV 다운로드
    st.markdown("---")
    st.markdown("### 💾 보고서 다운로드")
    
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    
    writer.writerow(['분석 항목', '결과', '상세 정보'])
    writer.writerow(['센서 타입', report['sensor_type'], ''])
    writer.writerow(['둔감모드 진입', f"{report['enable_count']}회", 'Enable 이벤트'])
    writer.writerow(['둔감모드 해제', f"{report['disable_count']}회", 'Disable 이벤트'])
    writer.writerow(['둔감모드 총 이벤트', report['total_events'], ''])
    writer.writerow(['터치 카운트', f"{report['touch_count']}회", '최대값'])
    writer.writerow(['터치 로그 개수', report['touch_logs_count'], ''])
    
    if report['status_logs']:
        writer.writerow([''])
        writer.writerow(['센서', '16진수', '10진수(회)'])
        for log in sorted(report['status_logs'], key=lambda x: x['count'], reverse=True):
            writer.writerow([log['sensor'], log['hex'], log['count']])
    
    csv_content = csv_buffer.getvalue()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="📥 CSV 보고서 다운로드",
        data=csv_content,
        file_name=f"pocket_mode_analysis_{timestamp}.csv",
        mime="text/csv"
    )

else:
    st.info("""
    ### 📝 사용 방법
    
    1. **로그 파일 선택**: 위의 파일 업로더에서 `.log` 파일을 선택하세요
    2. **자동 분석**: 파일이 업로드되면 자동으로 분석됩니다
    3. **결과 확인**: 둔감모드 및 터치 횟수가 표시됩니다
    4. **보고서 다운로드**: CSV 형식으로 다운로드할 수 있습니다
    
    ### ✨ 지원 기능
    
    - 🔍 **자동 센서 감지**: STM, Synaptics, Goodix
    - 📊 **둔감모드 분석**: 진입/해제 횟수 자동 계산
    - 🖱️ **터치 횟수**: 16진수 → 10진수 자동 변환
    - 💾 **보고서 다운로드**: CSV 형식 저장
    
    ### 📧 지원하는 로그 파일
    
    - Samsung `dumpstate` 로그
    - 텍스트 기반 커널 로그
    - `.log`, `.txt` 확장자
    """)

st.markdown("---")
st.markdown("**Pocket Mode Log Analyzer v1.0** | Samsung SCM Team")
