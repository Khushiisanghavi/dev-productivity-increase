import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Dev Productivity Dashboard", layout="wide")

# ---------- HEADER ----------
st.title("🚀 Developer Productivity Dashboard")
st.caption("Understand performance. Detect problems. Take action.")

# ---------- FETCH DATA ----------
response = requests.get("http://127.0.0.1:8000/metrics")
data = response.json()

# ---------- SIDEBAR ----------
st.sidebar.header("⚙️ Controls")

days = st.sidebar.slider("Select recent days", 3, len(data["dates"]), len(data["dates"]))

st.sidebar.markdown("---")

st.sidebar.write("### ℹ️ About")
st.sidebar.write(
    "This dashboard analyzes developer productivity using PR, deployment, and bug data."
)

# ---------- DATAFRAME ----------
df = pd.DataFrame({
    "Date": data["dates"],
    "Lead Time": data["lead_trend"],
    "Cycle Time": data["cycle_trend"]
})

df.set_index("Date", inplace=True)

# 🔥 APPLY FILTER
df = df.tail(days)

# ---------- RECOMPUTE METRICS BASED ON FILTER ----------
filtered_lead = df["Lead Time"].mean()
filtered_cycle = df["Cycle Time"].mean()

filtered_lead_list = df["Lead Time"].tolist()
filtered_cycle_list = df["Cycle Time"].tolist()

def calculate_change(values):
    if len(values) < 2:
        return 0
    mid = len(values) // 2
    first_half = sum(values[:mid]) / len(values[:mid])
    second_half = sum(values[mid:]) / len(values[mid:])
    if first_half == 0:
        return 0
    return round(((second_half - first_half) / first_half) * 100, 2)

filtered_lead_change = calculate_change(filtered_lead_list)
filtered_cycle_change = calculate_change(filtered_cycle_list)

def calculate_health(lead, cycle, deploy, bugs):
    score = 100
    if lead > 4:
        score -= 20
    if cycle > 3:
        score -= 20
    if deploy < 1:
        score -= 20
    if bugs > 1:
        score -= 20
    return max(score, 0)

filtered_health = calculate_health(
    filtered_lead,
    filtered_cycle,
    data["deployment_frequency"],
    data["bug_rate"]
)

# ---------- METRIC CARD ----------
def metric_card(title, value, good_threshold, reverse=False):
    if reverse:
        color = "#00C853" if value < good_threshold else "#FF5252"
    else:
        color = "#00C853" if value > good_threshold else "#FF5252"

    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1f1f1f, #2c2c2c);
            padding:20px;
            border-radius:12px;
            text-align:center;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
        ">
            <h4 style="color:gray;">{title}</h4>
            <h2 style="color:{color};">{round(value, 2)}</h2>
        </div>
    """, unsafe_allow_html=True)

# ---------- INFO ----------
st.info(f"Showing last {days} days of activity")

# ---------- TOP METRICS ----------
col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("Lead Time (days)", filtered_lead, 4, True)

with col2:
    metric_card("Cycle Time (days)", filtered_cycle, 3, True)

with col3:
    metric_card("Deployment Frequency", data["deployment_frequency"], 1)

with col4:
    metric_card("Bug Rate", data["bug_rate"], 1, True)

# ---------- HEALTH SCORE ----------
st.subheader("🏥 System Health")

score = filtered_health
color = "green" if score > 70 else "orange" if score > 40 else "red"

st.markdown(f"""
    <div style="text-align:center;">
        <h1 style="color:{color};">{score}/100</h1>
        <p>Overall Engineering Health Score</p>
    </div>
""", unsafe_allow_html=True)

# ---------- TRENDS ----------
st.subheader("📊 Trends")
st.line_chart(df)

# ---------- PERFORMANCE CHANGE ----------
st.subheader("📈 Recent Changes")

col1, col2 = st.columns(2)
col1.metric("Lead Time Change", f"{filtered_lead_change}%")
col2.metric("Cycle Time Change", f"{filtered_cycle_change}%")

# ---------- INSIGHTS ----------
st.subheader("🧠 Insights & Actions")

def insight_card(title, desc, action):
    st.markdown(f"""
        <div style="
            background-color:#1a1a1a;
            padding:18px;
            border-radius:10px;
            margin-bottom:12px;
            border-left:5px solid #FFA500;
        ">
            <h4>{title}</h4>
            <p style="color:#ccc;">{desc}</p>
            <p style="color:#00C853;"><b>💡 Action:</b> {action}</p>
        </div>
    """, unsafe_allow_html=True)

# ---------- SMART INSIGHTS ----------
if data["cycle_change"] > 0:
    insight_card(
        "⚠️ Cycle Time Increased",
        f"Increased by {data['cycle_change']}%",
        "Improve PR review speed or reduce PR size"
    )

if data["lead_change"] > 0:
    insight_card(
        "⏳ Lead Time Increased",
        f"Increased by {data['lead_change']}%",
        "Optimize CI/CD pipeline"
    )

if data["bug_rate"] > 1:
    insight_card(
        "🐞 High Bug Rate",
        "More bugs after deployment",
        "Increase automated testing"
    )

if data["deployment_frequency"] < 1:
    insight_card(
        "🚫 Low Deployment Frequency",
        "Releases are infrequent",
        "Improve deployment pipeline"
    )

# ---------- ALERT ----------
if data["cycle_change"] > 20:
    st.warning("🚨 Significant increase in cycle time detected!")