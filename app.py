import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---------------- 页面基础设置 ----------------
st.set_page_config(page_title="S2B2C 数智化驾驶舱", layout="wide", initial_sidebar_state="expanded")

# ================= 注入“深空星云”科技风 CSS (暴力提亮版) =================
st.markdown("""
<style>
    /* 1. 隐藏顶部白色导航条 */
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        background: transparent !important;
    }

    /* 2. 动态星云背景 */
    @keyframes bgShift {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }
    .stApp {
        background-color: #050A15 !important;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(0, 229, 255, 0.15), transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(179, 136, 255, 0.15), transparent 40%),
            radial-gradient(circle at 50% 50%, rgba(0, 255, 136, 0.1), transparent 50%) !important;
        background-size: 200% 200% !important;
        animation: bgShift 15s ease-in-out infinite !important;
        color: #FFFFFF !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* 3. 标题微微发光 */
    h1, h2, h3, h4 {
        color: #FFFFFF !important;
        text-shadow: 0 2px 10px rgba(0, 229, 255, 0.4) !important;
        font-weight: 700 !important;
    }

    /* 4. 侧边栏 */
    [data-testid="stSidebar"] {
        background-color: rgba(9, 14, 26, 0.85) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0, 229, 255, 0.2);
    }
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important; 
    }
    [data-testid="stSidebar"] [aria-checked="true"] * {
        color: #00E5FF !important; 
        font-weight: bold !important;
        text-shadow: 0 0 10px rgba(0, 229, 255, 0.8);
    }

    /* 5. 指标卡片 */
    [data-testid="stMetric"] {
        background: rgba(15, 25, 45, 0.7) !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        border-color: #00E5FF !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.4);
        transform: translateY(-2px);
    }
    [data-testid="stMetricLabel"] p {
        color: #A0AAB5 !important;
        font-size: 15px !important;
    }
    [data-testid="stMetricValue"] div {
        color: #FFFFFF !important;
        font-size: 36px !important;
        text-shadow: 0 0 15px rgba(255,255,255,0.2);
    }

    /* 6. 【暴力修复】Tab 标签栏文字彻底提亮 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    /* 覆盖所有 Tab 内部元素的文字颜色 */
    .stTabs [data-baseweb="tab-list"] button,
    .stTabs [data-baseweb="tab-list"] button p,
    .stTabs [data-baseweb="tab-list"] button div,
    .stTabs [data-baseweb="tab-list"] button span {
        color: #E2E8F0 !important; /* 未选中时强制为亮灰白 */
        background-color: transparent !important;
        font-weight: 500 !important;
    }
    /* 选中的 Tab 强制为高亮青色 */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"],
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] p,
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] div,
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] span {
        color: #00E5FF !important;
        font-weight: bold !important;
    }
    /* 选中的底部发光下划线 */
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #00E5FF !important;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.8) !important;
    }

    /* 7. 普通按钮 */
    .stButton > button {
        background-color: rgba(0, 229, 255, 0.15) !important;
        color: #00E5FF !important;
        border: 1px solid #00E5FF !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.2) !important;
    }
    .stButton > button:hover {
        background-color: rgba(0, 229, 255, 0.4) !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.8) !important;
        color: #FFFFFF !important;
    }
    .stButton > button:active { transform: scale(0.95); }

    /* 8. 【暴力修复】所有输入框、下拉框、表单、副标题 */
    /* 包括顶部的 st.caption 等灰色文字，全部提亮 */
    [data-testid="stCaption"], .stCaption, [data-testid="stMarkdownContainer"] p {
        color: #E2E8F0 !important; 
    }

    /* 文本框 */
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(10, 15, 29, 0.9) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(0, 229, 255, 0.4) !important;
        font-size: 15px !important;
    }
    .stTextArea textarea::placeholder, .stTextInput input::placeholder {
        color: #A0AAB5 !important;
        opacity: 1 !important;
    }
    
    /* 表单标签 */
    label[data-testid="stWidgetLabel"] p {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }

    /* 下拉框 */
    div[data-baseweb="select"] > div {
        background-color: rgba(10, 15, 29, 0.9) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(0, 229, 255, 0.4) !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: #FFFFFF !important;
    }
    ul[data-baseweb="menu"] {
        background-color: #0F192D !important;
    }
    ul[data-baseweb="menu"] li {
        color: #FFFFFF !important;
    }
    ul[data-baseweb="menu"] li:hover {
        background-color: rgba(0, 229, 255, 0.2) !important;
    }

    /* 表单提交按钮 */
    [data-testid="stFormSubmitButton"] > button {
        background-color: rgba(0, 229, 255, 0.15) !important;
        color: #00E5FF !important;
        border: 1px solid #00E5FF !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        width: 100%;
        transition: all 0.3s ease !important;
    }
    [data-testid="stFormSubmitButton"] > button:hover {
        background-color: rgba(0, 229, 255, 0.4) !important;
        color: #FFFFFF !important;
    }

    /* 9. 底部聊天输入框 */
    [data-testid="stBottom"] {
        background-color: transparent !important; 
        background: transparent !important;
    }
    [data-testid="stChatInput"] {
        background-color: rgba(15, 25, 45, 0.9) !important;
        border: 1px solid #00E5FF !important;
        border-radius: 8px !important;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.3) !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #A0AAB5 !important;
        opacity: 1 !important;
    }

    /* 10. 聊天气泡 */
    .stChatMessage {
        background: rgba(15, 25, 45, 0.8) !important;
        border: 1px solid rgba(0, 229, 255, 0.2) !important;
        border-radius: 12px;
        padding: 15px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    .stChatMessage p { color: #FFFFFF !important; font-size: 15px !important; }

    /* 11. 自定义提示框 */
    .custom-alert { padding: 16px; border-radius: 8px; margin-bottom: 16px; font-size: 15px; line-height: 1.5; backdrop-filter: blur(10px); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
    .custom-info { background: rgba(0, 229, 255, 0.1); border: 1px solid #00E5FF; color: #E2E8F0 !important; }
    .custom-info strong { color: #00E5FF !important; }
    .custom-warning { background: rgba(255, 234, 0, 0.1); border: 1px solid #FFEA00; color: #E2E8F0 !important; }
    .custom-warning strong { color: #FFEA00 !important; }
    .custom-error { background: rgba(255, 64, 129, 0.1); border: 1px solid #FF4081; color: #E2E8F0 !important; }
    .custom-error strong { color: #FF4081 !important; }
    .custom-success { background: rgba(0, 255, 136, 0.1); border: 1px solid #00FF88; color: #E2E8F0 !important; }
    .custom-success strong { color: #00FF88 !important; }

    /* 12. 客户画像标签 */
    .tag-cyan { background: rgba(0, 229, 255, 0.15) !important; color: #00E5FF !important; padding: 8px 16px; border-radius: 8px; margin-right: 10px; font-weight: bold; border: 1px solid #00E5FF; box-shadow: 0 0 15px rgba(0, 229, 255, 0.4); display: inline-block; }
    .tag-green { background: rgba(0, 255, 136, 0.15) !important; color: #00FF88 !important; padding: 8px 16px; border-radius: 8px; margin-right: 10px; font-weight: bold; border: 1px solid #00FF88; box-shadow: 0 0 15px rgba(0, 255, 136, 0.4); display: inline-block; }
    .tag-purple { background: rgba(179, 136, 255, 0.15) !important; color: #B388FF !important; padding: 8px 16px; border-radius: 8px; margin-right: 10px; font-weight: bold; border: 1px solid #B388FF; box-shadow: 0 0 15px rgba(179, 136, 255, 0.4); display: inline-block; }
</style>
""", unsafe_allow_html=True)
# =======================================================

# 统一 Plotly 图表配置
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", template="plotly_dark",
    font=dict(color="#FFFFFF", size=14), title=dict(font=dict(color="#FFFFFF", size=18)),
    legend=dict(font=dict(color="#FFFFFF")),
    xaxis=dict(tickfont=dict(color="#FFFFFF"), title_font=dict(color="#FFFFFF"), gridcolor="rgba(255,255,255,0.1)"),
    yaxis=dict(tickfont=dict(color="#FFFFFF"), title_font=dict(color="#FFFFFF"), gridcolor="rgba(255,255,255,0.1)"),
    margin=dict(l=40, r=40, t=60, b=40)
)
COLOR_SEQ = ['#00E5FF', '#00FF88', '#B388FF', '#FF4081', '#FFEA00']

@st.cache_data
def load_data():
    return (pd.read_csv("data/students.csv"), pd.read_csv("data/learning_logs.csv"),
            pd.read_csv("data/rules.csv"), pd.read_csv("data/tasks.csv"),
            pd.read_csv("data/feedback.csv"))

students, logs, rules, tasks, feedback = load_data()

if "tasks" not in st.session_state:
    st.session_state.tasks = tasks.copy()

st.sidebar.title("🌐 S2B2C 驾驶舱")
st.sidebar.markdown("---")
role = st.sidebar.radio(
    "请选择您的视角：", 
    ["💼 B端：顾问/渠道", "👤 C端：家长/学员", "🏢 S端：教研总部", "📊 财务与风险沙盘", "🌐 全局：数据飞轮闭环"]
)

# =========================================================
# 视角 1：B端（顾问/渠道）
# =========================================================
if role == "💼 B端：顾问/渠道":
    st.title("💼 小B智能销售与交付工作台")
    st.caption("从“盲目推销”到“基于AI偏好的精准跟进”，让每一次交付都产生机制激励。")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 任务总览", "🛠️ 客户画像与跟进", "🤖 渠道服务助手 (Agent)", "🎯 AI试听与转化舱", "💰 渠道收益钱包"])
    
    with tab1:
        df = st.session_state.tasks
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("任务总数", len(df))
        c2.metric("待处理预警", len(df[df["status"] == "待处理"]), delta="-2", delta_color="inverse")
        c3.metric("已闭环任务", len(df[df["status"] == "已关闭"]))
        closed = len(df[df["status"] == "已关闭"])
        recovered = len(df[(df["status"] == "已关闭") & (df["recovered_booking"] == 1)])
        rate = recovered / closed if closed else 0
        c4.metric("7日恢复约课率", f"{rate:.0%}", delta="5%")
        c5.metric("误承诺拦截数", int(df["miscommit_flag"].sum()), delta="-100%", delta_color="inverse")

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(df["status"].value_counts().reset_index(), names="status", values="count", hole=0.6, title="任务状态分布", color_discrete_sequence=COLOR_SEQ)
            fig.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(df["signal"].value_counts().reset_index(), x="signal", y="count", title="信号类型分布", color="signal", text_auto=True, color_discrete_sequence=COLOR_SEQ)
            fig.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        df = st.session_state.tasks
        selected_label = st.selectbox("选择要跟进的任务", (df["task_id"] + " | " + df["student_name"] + " | " + df["signal"] + " | " + df["status"]).tolist())
        selected_id = selected_label.split(" | ")[0]
        task = df[df["task_id"] == selected_id].iloc[0]

        st.divider()
        left, right = st.columns([1.5, 1])

        with left:
            st.markdown(f"### 👤 {task['student_name']} 的 360° 客户画像")
            st.markdown("**🏷️ AI 行为偏好标签（SCRM 提取）：**")
            st.markdown("""
            <div>
                <span class="tag-cyan">💰 价格敏感型</span>
                <span class="tag-green">🌙 偏好晚间排课</span>
                <span class="tag-purple">🌍 偏好欧美外教</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("剩余课时", f"{task['evidence'].split('剩余')[1].split('课时')[0]} 节")
            col_b.metric("客单价", "¥4,500")
            col_c.metric("当前耗课率", task['evidence'].split('单元耗课')[1].split('%')[0] + "%")

            student_logs = logs[logs["student_id"] == task["student_id"]]
            fig = px.line(student_logs, x="date", y=["booked", "hours_consumed"], title="近14天行为记录", markers=True, color_discrete_sequence=COLOR_SEQ)
            fig.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### 🎯 RPA+AI 续课智能预测")
            st.progress(85, text="续费概率评估：85% (高意向)")
            st.markdown('<div class="custom-alert custom-info">💡 <strong>AI 干预建议</strong>：剩余 10 课时。建议在单元结束前 2 周，推送‘语法强化包’锁定续订。</div>', unsafe_allow_html=True)

            st.markdown("#### 💬 历史沟通记录")
            with st.chat_message("user"):
                st.write("家长：你们能不能保证固定外教啊？动不动就换老师。")
            with st.chat_message("assistant"):
                st.write("顾问：理解您的顾虑，我这次给您优先安排之前上过课的Sarah老师，您看周三晚8点行吗？")

        with right:
            st.markdown("### 📞 跟进操作与合规审核")
            script = st.text_area("输入将发送给家长的话术：", height=150, placeholder="在此输入跟进话术，系统将进行红线校验...")
            if script:
                hit = [w for w in ["随时退", "保证固定外教", "保证提分", "保证效果"] if w in script]
                if hit:
                    st.markdown(f'<div class="custom-alert custom-error">❌ <strong>触发合规红线！</strong>禁止承诺：{", ".join(hit)}。</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="custom-alert custom-success">✅ 话术合规，可以发送。</div>', unsafe_allow_html=True)
            if st.button("🤖 一键执行 AI 动作", use_container_width=True):
                st.markdown('<div class="custom-alert custom-success">已向家长微信推送《本周学情周报》。</div>', unsafe_allow_html=True)
                
            st.divider()
            with st.form("feedback_form"):
                recovered = st.selectbox("学员是否恢复约课？", ["否", "是"])
                submitted = st.form_submit_button("提交回填", use_container_width=True)
                if submitted:
                    idx = st.session_state.tasks[st.session_state.tasks["task_id"] == selected_id].index[0]
                    st.session_state.tasks.at[idx, "status"] = "已关闭"
                    st.session_state.tasks.at[idx, "recovered_booking"] = 1 if recovered == "是" else 0
                    if recovered == "是":
                        st.markdown('<div class="custom-alert custom-success">✅ <strong>任务闭环！</strong><br>🔄 <strong>数据回流</strong>：沟通语料已回流至 S 端 AI 话术库。</div>', unsafe_allow_html=True)

    with tab3:
        st.subheader("🤖 渠道服务助手 (AI Agent)")
        st.caption("AI 负责整理与建议，规则负责拦截，人工负责最终决策与承诺。")
        
        st.markdown("#### 📥 场景输入：家长反馈")
        with st.chat_message("user"):
            st.write("家长：“最近两次都没约到合适的老师，孩子都不想学了，到底怎么回事？”")
            
        if st.button("🚀 唤醒 Agent 开始梳理"):
            st.divider()
            with st.status("步骤一：正在提取多端数据事实...", expanded=True) as status:
                st.write("🔍 检索 SCRM 约课记录：近14天内 3 次预约失败。")
                st.write("🔍 检索原因字段：2 次为【外教不匹配】，1 次为【时段冲突】。")
                st.write("🔍 检索沟通记录：家长曾提及希望周五晚 7 点后上课。")
                st.markdown('<div class="custom-alert custom-warning">⚠️ <strong>发现信息缺失</strong>：排课系统中该外教未来一周已满，无备选排班数据。</div>', unsafe_allow_html=True)
                status.update(label="步骤一：事实梳理完成（存在缺失数据）", state="complete", expanded=False)
            
            st.markdown('<div class="custom-alert custom-info"><h3 style="margin-top:0;color:#00E5FF!important;">💡 方案生成（规则校验 + AI 建议）</h3><ul style="margin-bottom:0;"><li><strong>方案 A (调整时段)</strong>：建议沟通调整为周六上午（系统显示有 2 名优质外教可约）。</li><li><strong>方案 B (备选教师)</strong>：提供 1 名同资质中教，先行承接基础口语课。</li><li><strong>方案 C (升级处理)</strong>：提交总部排课专员，人工协调周五晚特定外教名额。</li></ul></div>', unsafe_allow_html=True)
            
            st.markdown('<div class="custom-alert custom-error">🚫 <strong>边界约束</strong>：排班库无数据，<strong>严禁</strong>向家长承诺“周五保证能约上”。</div>', unsafe_allow_html=True)
            
            st.markdown("#### ✍️ 人工确认与话术审核")
            col_a, col_b = st.columns([2, 1])
            with col_a:
                agent_script = st.text_area("AI 生成的跟进话术草稿（需人工审核）：", 
                    "家长您好，查到您近两次约课遇到了问题。非常抱歉！因为周五晚排课确实比较满，为了不耽误孩子，我为您协调了周六上午的VIP外教，以及一份AI伴学补偿方案，您看这周末方便试一下吗？", height=120)
            with col_b:
                if "保证" in agent_script or "随时退" in agent_script:
                    st.markdown('<div class="custom-alert custom-error">❌ 触发红线！禁止发送！</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="custom-alert custom-success">✅ 校验通过。等待人工点击发送。</div>', unsafe_allow_html=True)
            
            st.markdown("#### 📌 责任落实与结果追踪")
            col1, col2, col3 = st.columns(3)
            col1.markdown('<div class="custom-alert custom-info">👤 <strong>谁联系</strong>：渠道顾问-小B<br><br>(已分配)</div>', unsafe_allow_html=True)
            col2.markdown('<div class="custom-alert custom-info">⏱️ <strong>何时反馈</strong>：48小时内<br><br>(SLA 计时中)</div>', unsafe_allow_html=True)
            col3.markdown('<div class="custom-alert custom-info">👥 <strong>谁协调</strong>：排课专员-李老师<br><br>(已生成工单)</div>', unsafe_allow_html=True)
            
            if st.button("📤 人工点击发送"):
                st.markdown('<div class="custom-alert custom-success">✅ 已发送至家长。沟通语料与排课缺失问题已回流。</div>', unsafe_allow_html=True)
                st.balloons()

    with tab4:
        st.subheader("🎯 AI + 真人双轨试听舱")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🤖 AI 8分钟轻量快测")
            df_radar = pd.DataFrame(dict(r=[65, 80, 45, 70], theta=["发音", "词汇", "语法", "流利度"]))
            fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True, color_discrete_sequence=['#00E5FF'])
            fig.update_traces(fill='toself', fillcolor='rgba(0, 229, 255, 0.2)', line_color='#00E5FF')
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)")), **PLOTLY_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.markdown("#### 👤 真人面评与 AI 建议")
            st.markdown('<div class="custom-alert custom-error">🔴 <strong>薄弱项预警</strong>：语法正确率仅 45%。</div>', unsafe_allow_html=True)
            st.markdown('<div class="custom-alert custom-success">🟢 <strong>优势项</strong>：词汇量达标。</div>', unsafe_allow_html=True)
            st.markdown('<div class="custom-alert custom-info">🤖 <strong>学情快照</strong>：建议匹配【中教承中】补语法，搭配【AI打底】练口语。</div>', unsafe_allow_html=True)
            st.text_area("AI 自动生成的跟进话术：", "家长您好，外教反馈孩子口语感很好，但语法拖了后腿。建议先锁定 60 课时，用 AI 高频练口语。", height=100)

    with tab5:
        st.subheader("💰 渠道双层激励钱包")
        st.write("存量分成不动，增量激励向前。从‘卖课计账’转向‘交付计账’。")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📦 存量层（合同锁定）")
            st.metric("本月销售分成（45%）", "¥ 12,800", help="不受耗课影响")
        with col2:
            st.markdown("#### 🚀 增量层（总部单列预算）")
            st.metric("首课激励 (0.6%)", "¥ 120")
            st.metric("耗课激励 (1.0%)", "¥ 350", delta="本周上升 +50")
            st.metric("续费激励 (0.4%)", "¥ 80")
        st.divider()
        st.markdown('<div class="custom-alert custom-info">💡 <strong>机制解读</strong>：小B每完成一次任务卡，不仅挽回学员，更让渠道的‘增量钱包’鼓起来。</div>', unsafe_allow_html=True)

# =========================================================
# 视角 2：C端（家长/学员）
# =========================================================
elif role == "👤 C端：家长/学员":
    st.title("🎓 孩子的学习成长地图")
    st.caption("从‘课时消耗’转向‘能力进阶’。")
    c1, c2, c3 = st.columns(3)
    c1.metric("口语流利度", "82 分", "+5")
    c2.metric("语法错题重考", "0 次", "已清零")
    c3.metric("本周课外练习", "120 分钟", "+20%")
    
    df_radar = pd.DataFrame(dict(r=[85, 70, 90, 65, 80], theta=["发音", "语法", "词汇", "流利度", "开口意愿"]))
    fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True, color_discrete_sequence=['#00FF88']) 
    fig.update_traces(fill='toself', fillcolor='rgba(0, 255, 136, 0.2)', line_color='#00FF88')
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, gridcolor="rgba(255,255,255,0.1)")), **PLOTLY_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🤖 AI 伴学推荐")
    st.markdown('<div class="custom-alert custom-success">下一阶段建议：加强‘商务情景对话’模块。</div>', unsafe_allow_html=True)
    st.subheader("💬 真人+AI 社群跟课")
    st.markdown('<div class="custom-alert custom-info">👩‍🏫 社群老师：宝妈您好，孩子最近到了疲劳期。我已经在后台帮他调整了 AI 任务的难度。</div>', unsafe_allow_html=True)
    
    chat_input = st.chat_input("向 AI 助教提问...")
    if chat_input:
        st.chat_message("user").write(chat_input)
        st.chat_message("assistant").write("收到提问！已记录并反馈给专属老师。")

# =========================================================
# 视角 3：S端（总部）
# =========================================================
elif role == "🏢 S端：教研总部":
    st.title("🏢 S 端：数智化供给与教研中台")
    st.caption("将师资经验沉淀为可复用的 AI 资产。")
    col1, col2, col3 = st.columns(3)
    col1.markdown('<div class="custom-alert custom-info">🤖 <strong>AI 打底</strong><br><br>单词带背、发音跟读<br><br>边际成本趋近于零</div>', unsafe_allow_html=True)
    col2.markdown('<div class="custom-alert custom-success">👨‍🏫 <strong>中教承中</strong><br><br>语法基础、基础口语<br><br>不受境外外教限制</div>', unsafe_allow_html=True)
    col3.markdown('<div class="custom-alert custom-warning">🌍 <strong>外教居顶</strong><br><br>深度对话、复杂纠错<br><br>高客单价核心</div>', unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🧠 教师经验 AI 化沉淀")
    st.progress(68, text="68% - 正在学习【如何用鼓励的方式纠正语法错误】")
    
    df_module = pd.DataFrame({"模块": ["口语练习", "词汇语法", "考点专项", "场景任务"], "调用量(万次)": [450, 320, 180, 250]})
    fig = px.bar(df_module, x="模块", y="调用量(万次)", title="AI 课程模块调用分布", color="模块", color_discrete_sequence=COLOR_SEQ)
    fig.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 视角 4：财务与风险沙盘
# =========================================================
elif role == "📊 财务与风险沙盘":
    st.title("📊 商业模拟沙盘与风险熔断")
    st.subheader("1. 单群经济模型动态测算")
    group_size = st.slider("单群学员人数", min_value=10, max_value=50, value=50, step=5)
    total_revenue = group_size * 9600
    channel_share = total_revenue * 0.45
    hq_share = total_revenue * 0.55
    teacher_cost = hq_share * 0.20
    service_cost = 26000 
    
    col1, col2, col3 = st.columns(3)
    col1.metric("终端总流水", f"¥ {total_revenue:,}")
    col2.metric("渠道留存 (45%)", f"¥ {channel_share:,}")
    col3.metric("总部确认收入 (55%)", f"¥ {hq_share:,}")
    
    df_fin = pd.DataFrame({
        "环节": ["教师薪酬", "社群服务", "内容与研发", "总部净利"],
        "金额": [teacher_cost, service_cost, hq_share * 0.15, hq_share - teacher_cost - service_cost - (hq_share * 0.15)]
    })
    fig = px.pie(df_fin, names="环节", values="金额", hole=0.5, title="总部单群收益分配", color_discrete_sequence=COLOR_SEQ)
    fig.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("2. 政策风险熔断机制")
    st.write("**I级风险：课程定性失守**。一旦触发，政府指导价将压低至 17.6 元/30分钟。")
    risk_switch = st.toggle("🚨 模拟触发学科类定性失守")
    
    if risk_switch:
        st.markdown('<div class="custom-alert custom-error">⚠️ <strong>警告</strong>：定价被打回政府指导价，外教 1v1 成本结构崩溃！</div>', unsafe_allow_html=True)
        st.metric("当前单课时收入", "14.7 元/25分钟", delta="-63%", delta_color="inverse")
        st.markdown('<div class="custom-alert custom-warning">🤖 <strong>防御机制生效</strong>：切断外教排课，强制提升 AI+中教比例至 90%。</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="custom-alert custom-success">✅ 当前处于非学科类合规经营状态，市场调节价生效。</div>', unsafe_allow_html=True)

# =========================================================
# 视角 5：全局闭环飞轮
# =========================================================
elif role == "🌐 全局：数据飞轮闭环":
    st.title("🌐 S2B2C 数智化闭环飞轮")
    st.caption("打破数据孤岛，让服务、交付与激励机制在同一套系统里运转。")
    st.markdown("### 🔄 一次学习中断的完整数据流转")
    st.markdown('<div class="custom-alert custom-success">✅ <strong>步骤 1：C 端发现异常</strong> —— AI 伴学监测到学员练习断更，数据回流至 SCRM。</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-alert custom-info">💡 <strong>步骤 2：B 端精准介入</strong> —— 系统生成任务卡 + AI 行为偏好标签，小B通过合规话术恢复约课。</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-alert custom-warning">⚠️ <strong>步骤 3：S 端吸收经验</strong> —— 成功的沟通话术自动进入 AI 语料库。</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-alert custom-success">✅ <strong>步骤 4：机制反哺渠道</strong> —— 学员恢复耗课，触发里程碑，SCRM 自动计算增量激励下发。</div>', unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🏆 全链路核心指标（模拟）")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("试听转化率", "38%", "+12%")
    col2.metric("课程消耗率", "75%", "+10%")
    col3.metric("首单续费率", "45%", "+5%")
    col4.metric("学员转介绍率", "22%", "+8%")
    st.balloons()