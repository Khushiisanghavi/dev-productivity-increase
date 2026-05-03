from fastapi import FastAPI
from datetime import datetime
import json

app = FastAPI()

with open("../data/mock_data.json") as f:
    data = json.load(f)

def days_between(start, end):
    d1 = datetime.strptime(start, "%Y-%m-%d")
    d2 = datetime.strptime(end, "%Y-%m-%d")
    return (d2 - d1).days


def calculate_change(values):
    if len(values) < 2:
        return 0
    mid = len(values) // 2
    first_half = sum(values[:mid]) / len(values[:mid])
    second_half = sum(values[mid:]) / len(values[mid:])
    if first_half == 0:
        return 0
    return round(((second_half - first_half) / first_half) * 100, 2)


def calculate_health_score(lead, cycle, deploy, bugs):
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


@app.get("/metrics")
def get_metrics():
    lead_times = []
    cycle_times = []
    total_bugs = 0
    deploy_dates = []

    lead_trend = []
    cycle_trend = []
    dates = []

    for pr in data:
        lead = days_between(pr["created_at"], pr["deployed_at"])
        cycle = days_between(pr["created_at"], pr["merged_at"])

        lead_times.append(lead)
        cycle_times.append(cycle)
        total_bugs += pr["bugs"]
        deploy_dates.append(pr["deployed_at"])

        lead_trend.append(lead)
        cycle_trend.append(cycle)
        dates.append(pr["created_at"])

    avg_lead = sum(lead_times) / len(lead_times)
    avg_cycle = sum(cycle_times) / len(cycle_times)

    unique_days = len(set(deploy_dates))
    deployment_freq = len(deploy_dates) / unique_days if unique_days else 0

    bug_rate = total_bugs / len(data)

    # 🔥 New features
    lead_change = calculate_change(lead_trend)
    cycle_change = calculate_change(cycle_trend)
    health_score = calculate_health_score(avg_lead, avg_cycle, deployment_freq, bug_rate)

    return {
        "avg_lead_time": round(avg_lead, 2),
        "avg_cycle_time": round(avg_cycle, 2),
        "deployment_frequency": round(deployment_freq, 2),
        "bug_rate": round(bug_rate, 2),

        "lead_trend": lead_trend,
        "cycle_trend": cycle_trend,
        "dates": dates,

        "lead_change": lead_change,
        "cycle_change": cycle_change,
        "health_score": health_score
    }