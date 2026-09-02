import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv('cars.csv')

df = load_data()

st.title('자동차 데이터')
st.markdown('<p style="font-weight:bold; color:green;">자동차 데이터 테이블</p>',
            unsafe_allow_html=True)

# st.dataframe(df)
manufacturer = st.selectbox(
    '제조사 선택',
    options=df['Manufacturer'].unique()
)
filtered_df = df[df['Manufacturer'] == manufacturer]

# print(filtered_df)

sort_column = st.selectbox('정렬할 컬럼 선택', options=df.columns)
sort_order = st.radio('정렬 순서 선택', options=['오름차순', '내림차순'])
ascending = True if sort_order == '오름차순' else False
sorted_df = filtered_df.sort_values(by=sort_column, ascending=ascending)

st.dataframe(sorted_df)