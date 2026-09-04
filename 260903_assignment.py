import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from plotly.subplots import make_subplots
from sqlalchemy import create_engine
import time

# SQLite DB연결
engine = create_engine('sqlite:///stocks.db')

# 데이터 조회
def load_data():
    with engine.connect() as conn:
        query = "SELECT * FROM stocks ORDER BY timestamp DESC LIMIT 100"
        return pd.read_sql(query, conn)

st_autorefresh(interval=1000) # 1초마다 갱신

data = load_data()

st.title("Real-Time Stock Dashboard")

# 메트릭 표시
col1, col2, col3 = st.columns(3) # 화면을 3개의 영역으로 나누기
with col1:
    latest_price = data['price'].iloc[0]
    st.metric('Latest Price', f'${latest_price:.2f}')

with col2:
    latest_volume = data['volume'].iloc[0]
    st.metric('Latest Volume', f'{latest_volume}')

with col3:
    price_change = data['price'].iloc[0] - data['price'].iloc[1]
    volume_change = data['volume'].iloc[0] - data['volume'].iloc[1]
    st.metric('Price Change', f'${price_change:.2f}', f'{price_change:.2f}')
    st.metric('Volume Change', f'{volume_change}', f'{volume_change}')

# 서브플롯 생성
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    row_heights=[0.7, 0.3],
    vertical_spacing=0.1,
    subplot_titles=((["Stock Price & Volume", ""]))
)

fig.add_trace(
    go.Scatter(x=data['timestamp'],
               y=data['price'],
               mode='lines',
               name='Price',
               line=dict(color='blue')),
               row=1,
               col=1
)

fig.add_trace(
    go.Bar(x=data['timestamp'],
           y=data['volume'],
           name='Volume',
           marker=dict(color='orange')),
           row=2,
           col=1
)

fig.update_layout(
    height=600,
    title='Stock Price and Volume',
    yaxis=dict(title='Price'),
    yaxis2=dict(title='Volume'),
    showlegend=False
)


st.plotly_chart(fig)

with st.expander("View Raw Data"):
    st.write(data)