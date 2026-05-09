import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 한글 폰트 설정 (데이터 내 한글이 있거나 그래프에 한글이 필요한 경우 대비)
plt.rcParams['font.family'] = 'NanumGothic' 
plt.rcParams['axes.unicode_minus'] = False

st.title("💔 심부전 데이터 분석 대시보드")

# 1. 데이터 로드 및 병합
@st.cache_data # 데이터를 매번 새로 읽지 않도록 캐싱 추가
def load_data():
    df_a = pd.read_json('heart_failure_a.json')
    df_b = pd.read_json('heart_failure_b.json')
    df = pd.merge(df_a, df_b, on='person_id', how='inner')
    return df

try:
    df = load_data()

    # 문제 1: 시각화 (jointplot)
    st.header("1. 박출계수와 나이의 상관관계")
    # jointplot은 특성상 st.pyplot()에 fig를 직접 넣어줘야 합니다.
    grid = sns.jointplot(data=df, x='ejection_fraction', y='age', hue='DEATH_EVENT')
    st.pyplot(grid.fig)

    # 문제 2: 시각화 (violinplot + 라디오 버튼)
    st.header("2. 죽음과 흡연의 상관관계")
    status = st.radio("표시 선택", ["전체", "흡연자", "비흡연자"])

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    if status == "전체":
        sns.violinplot(data=df, x='DEATH_EVENT', y='platelets', hue='smoking', split=True, ax=ax2)
    elif status == "흡연자":
        sns.violinplot(data=df[df['smoking']==1], x='DEATH_EVENT', y='platelets', ax=ax2)
    else:
        sns.violinplot(data=df[df['smoking']==0], x='DEATH_EVENT', y='platelets', ax=ax2)
    st.pyplot(fig2)

    # 문제 3: 시각화 (histplot + 슬라이더)
    st.header("3. 시간에 따른 사망 분포 (심박출 범위 선택)")
    # 심박출량(ejection_fraction) 범위를 슬라이더로 조절
    min_ef = int(df['ejection_fraction'].min())
    max_ef = int(df['ejection_fraction'].max())
    ef_range = st.slider("심박출량(ejection_fraction) 범위 선택", min_ef, max_ef, (min_ef, max_ef))

    # 선택된 범위로 데이터 필터링
    filtered_df = df[(df['ejection_fraction'] >= ef_range[0]) & (df['ejection_fraction'] <= ef_range[1])]

    fig3, ax3 = plt.subplots()
    sns.histplot(data=filtered_df, x='time', bins=20, hue='DEATH_EVENT', kde=True, ax=ax3)
    st.pyplot(fig3)

except FileNotFoundError:
    st.error("데이터 파일(JSON)을 찾을 수 없습니다. 깃허브 저장소에 파일이 있는지 확인해주세요.")