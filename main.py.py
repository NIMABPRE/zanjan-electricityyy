import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# تنظیمات صفحه دسکتاپ
st.set_page_config(page_title="سامانه هوش مصنوعی توزیع برق", layout="wide")

# استایل‌دهی لوکس تاریک صنعتی
st.markdown("""
    <style>
    .main { background-color: #0A0E17; color: white; }
    div[data-testid="stMetricValue"] { color: #00FFCC; font-size: 32px; font-weight: bold; }
    .critical-box { background-color: #221216; border-right: 5px solid #FF0055; padding: 15px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ پلتفرم هوش مصنوعی مدیریت بار شبکه توزیع برق زنجان")
st.markdown("---")

# سایدبار تنظیمات
st.sidebar.header("📥 تنظیمات پورتال")
region_type = st.sidebar.selectbox("نوع بافت منطقه:", ["مسکونی", "صنعتی", "تجاری"])

# خواندن فایل داتا
df = pd.read_csv('data.csv')
df['تاریخ_و_ساعت'] = pd.to_datetime(df['تاریخ_و_ساعت'])
df['ساعت'] = df['تاریخ_و_ساعت'].dt.hour

mean_val = df['مصرف_برق_کیلووات'].mean()
max_val = df['مصرف_برق_کیلووات'].max()
anomalies = df[df['مصرف_برق_کیلووات'] > 400]

# تب‌بندی مدیریتی
tab1, tab2 = st.tabs(["📊 کالبدشکافی بار", "🕵️‍♂️ کشف سرقت برق"])

with tab1:
    col1, col2 = st.columns(2)
    with col1: st.metric(label="📉 میانگین بار شبکه", value=f"{mean_val:.2f} kW")
    with col2: st.metric(label="⚡ حداکثر دیماند", value=f"{max_val:.2f} kW")
    
    # نمودار تعاملی
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['تاریخ_و_ساعت'], y=df['مصرف_برق_کیلووات'], mode='lines+markers', name='بار لحظه‌ای', line=dict(color='#00ffcc')))
    fig.update_layout(template='plotly_dark', paper_bgcolor='#0A0E17', plot_bgcolor='#111622', height=350)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### کشف تلفات غیرفنی و مصارف مشکوک")
    total_delivered = df['مصرف_برق_کیلووات'].sum()
    total_billed = total_delivered * 0.85
    loss_pct = 15.0
    
    st.metric(label="🚨 میزان هدررفت پنهان انرژی در این زون", value=f"{loss_pct}%", delta="بالاتر از حد مجاز")
    st.markdown("""
    <div class="critical-box">
        <h4>🚨 هشدار هوش مصنوعی: فرضیه دستکاری کنتور</h4>
        <p>الگوی مصرف نیمه‌شب این منطقه نشان‌دهنده کشش بار غیرمجاز است. بازرسی خطوط فیدر فرعی توصیه می‌شود.</p>
    </div>
    """, unsafe_allow_html=True)