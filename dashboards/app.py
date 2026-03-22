import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

st.set_page_config(
    page_title="Data Governance Control Tower",
    page_icon="???",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
.metric-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 18px 18px 14px 18px;
    min-height: 120px;
}
.metric-label {
    font-size: 0.92rem;
    color: #a9b3c1;
    margin-bottom: 8px;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 8px;
}
.metric-sub {
    font-size: 0.86rem;
    color: #c9d1d9;
}
.section-note {
    color: #a9b3c1;
    font-size: 0.92rem;
    margin-top: -8px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

def load_csv(relative_path):
    path = BASE_DIR / relative_path
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    return pd.read_csv(path)

def metric_card(title, value, subtitle):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def safe_count(df):
    return 0 if df.empty else len(df)

assets = load_csv("metadata/data_asset_register.csv")
kpis = load_csv("governance/governance_kpis.csv")
issues = load_csv("governance/issue_log.csv")
quality_results = load_csv("data/curated/quality_check_results.csv")
ai_use_cases = load_csv("ai_governance/ai_use_case_register.csv")
ai_risk = load_csv("ai_governance/ai_risk_assessment.csv")

quality_display = quality_results.copy()
if not quality_display.empty:
    quality_display["pass_rate_pct"] = (quality_display["pass_rate"] * 100).round(1)
    quality_display["outcome"] = quality_display["passed"].map({True: "Passed", False: "Failed"})
    quality_display["pass_rate_label"] = quality_display["pass_rate_pct"].astype(str) + "%"

open_issues = issues.copy()
if not open_issues.empty and "status" in open_issues.columns:
    open_issues = open_issues[open_issues["status"].astype(str).str.lower() != "closed"]

avg_pass_rate = 0.0
if not quality_display.empty:
    avg_pass_rate = round(quality_display["pass_rate_pct"].mean(), 1)

open_high_issues = 0
if not open_issues.empty and "severity" in open_issues.columns:
    open_high_issues = len(open_issues[open_issues["severity"].astype(str).str.lower() == "high"])

reviewed_ai = 0
if not ai_use_cases.empty and "status" in ai_use_cases.columns:
    reviewed_ai = len(ai_use_cases[ai_use_cases["status"].isin(["Approved", "In Review"])])

metadata_completeness = None
if not kpis.empty and "kpi_name" in kpis.columns:
    match = kpis[kpis["kpi_name"] == "Metadata completeness"]
    if not match.empty:
        metadata_completeness = match.iloc[0]["kpi_value"]

st.title("Data Governance Control Tower")
st.caption("Operational view of metadata, data quality controls, issue management, stewardship, and AI governance")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Data Quality",
    "Issues",
    "Assets",
    "AI Governance"
])

with tab1:
    st.subheader("Executive Overview")
    st.markdown('<div class="section-note">This view is designed to summarize governance posture, quality performance, open risk, and AI oversight in one place.</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Governed Data Assets", safe_count(assets), "Assets currently registered in scope")
    with c2:
        metric_card("Average Rule Pass Rate", f"{avg_pass_rate}%", "Across configured data quality checks")
    with c3:
        metric_card("Open High Severity Issues", open_high_issues, "High-severity issues needing attention")
    with c4:
        metric_card("AI Use Cases Reviewed", reviewed_ai, "Approved or currently under review")

    c5, c6 = st.columns([1.15, 1])
    with c5:
        st.subheader("Rule Performance by Control")
        if not quality_display.empty:
            rule_chart_df = quality_display.sort_values("pass_rate_pct", ascending=True)
            fig_rules = px.bar(
                rule_chart_df,
                x="pass_rate_pct",
                y="rule_name",
                color="outcome",
                orientation="h",
                text="pass_rate_label",
                template="plotly_dark",
                labels={
                    "pass_rate_pct": "Pass Rate (%)",
                    "rule_name": "Rule",
                    "outcome": "Result"
                },
                title=""
            )
            fig_rules.update_traces(textposition="outside")
            fig_rules.update_layout(height=380, margin=dict(l=10, r=20, t=10, b=10), legend_title_text="Result")
            st.plotly_chart(fig_rules, use_container_width=True)
        else:
            st.info("No quality results available yet.")

    with c6:
        st.subheader("Governance KPI Status Mix")
        if not kpis.empty and "status" in kpis.columns:
            status_df = (
                kpis["status"]
                .value_counts()
                .rename_axis("status")
                .reset_index(name="count")
            )
            fig_status = px.bar(
                status_df,
                x="count",
                y="status",
                orientation="h",
                template="plotly_dark",
                text="count",
                labels={"count": "Count", "status": "KPI Status"},
                title=""
            )
            fig_status.update_traces(textposition="outside")
            fig_status.update_layout(height=380, margin=dict(l=10, r=20, t=10, b=10), showlegend=False)
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("No KPI status data available.")

    st.subheader("Leadership Watchlist")
    if not open_issues.empty:
        watchlist_cols = [col for col in [
            "issue_id", "asset_id", "issue_type", "severity", "owner", "status", "target_resolution_date"
        ] if col in open_issues.columns]
        st.dataframe(open_issues[watchlist_cols], use_container_width=True)
    else:
        st.info("No open issues available.")

with tab2:
    st.subheader("Data Quality Control Results")
    st.markdown('<div class="section-note">This section shows rule outcomes, pass rates, and where failures are concentrated.</div>', unsafe_allow_html=True)

    if not quality_display.empty:
        dq_cols = st.columns(3)
        with dq_cols[0]:
            metric_card("Configured Rules", safe_count(quality_display), "Rules evaluated in current run")
        with dq_cols[1]:
            failed_rules = safe_count(quality_display[quality_display["outcome"] == "Failed"])
            metric_card("Failed Rules", failed_rules, "Controls currently below threshold")
        with dq_cols[2]:
            metric_card("Average Pass Rate", f"{avg_pass_rate}%", "Across all configured rules")

        display_cols = [col for col in [
            "rule_id", "asset_id", "rule_name", "dimension", "severity",
            "rows_tested", "failed_rows", "pass_rate_pct", "outcome", "message"
        ] if col in quality_display.columns]
        st.dataframe(quality_display[display_cols], use_container_width=True)

        left, right = st.columns(2)

        with left:
            dimension_df = (
                quality_display.groupby("dimension", as_index=False)["failed_rows"]
                .sum()
                .sort_values("failed_rows", ascending=True)
            )
            fig_dimension = px.bar(
                dimension_df,
                x="failed_rows",
                y="dimension",
                orientation="h",
                template="plotly_dark",
                text="failed_rows",
                labels={"failed_rows": "Failed Rows", "dimension": "Quality Dimension"},
                title="Failed Rows by Quality Dimension"
            )
            fig_dimension.update_traces(textposition="outside")
            fig_dimension.update_layout(height=360, margin=dict(l=10, r=20, t=50, b=10), showlegend=False)
            st.plotly_chart(fig_dimension, use_container_width=True)

        with right:
            asset_quality_df = (
                quality_display.groupby("asset_id", as_index=False)["pass_rate_pct"]
                .mean()
                .round(1)
                .sort_values("pass_rate_pct", ascending=True)
            )
            asset_quality_df["label"] = asset_quality_df["pass_rate_pct"].astype(str) + "%"
            fig_asset_quality = px.bar(
                asset_quality_df,
                x="pass_rate_pct",
                y="asset_id",
                orientation="h",
                template="plotly_dark",
                text="label",
                labels={"pass_rate_pct": "Average Pass Rate (%)", "asset_id": "Asset"},
                title="Average Pass Rate by Asset"
            )
            fig_asset_quality.update_traces(textposition="outside")
            fig_asset_quality.update_layout(height=360, margin=dict(l=10, r=20, t=50, b=10), showlegend=False)
            st.plotly_chart(fig_asset_quality, use_container_width=True)
    else:
        st.info("No quality results file found. Run the quality checks first.")

with tab3:
    st.subheader("Issue Management")
    st.markdown('<div class="section-note">This section highlights governance and data quality issues that should be visible to stewards and managers.</div>', unsafe_allow_html=True)

    if not issues.empty:
        issue_cols = st.columns(3)
        with issue_cols[0]:
            metric_card("Open Issues", safe_count(open_issues), "Issues not yet closed")
        with issue_cols[1]:
            metric_card("High Severity Open", open_high_issues, "High-severity items requiring attention")
        with issue_cols[2]:
            owners_with_open = 0 if open_issues.empty or "owner" not in open_issues.columns else open_issues["owner"].nunique()
            metric_card("Active Issue Owners", owners_with_open, "Owners currently carrying open items")

        st.dataframe(issues, use_container_width=True)

        left, right = st.columns(2)

        with left:
            if "severity" in issues.columns:
                severity_df = (
                    issues["severity"]
                    .value_counts()
                    .rename_axis("severity")
                    .reset_index(name="count")
                    .sort_values("count", ascending=True)
                )
                fig_severity = px.bar(
                    severity_df,
                    x="count",
                    y="severity",
                    orientation="h",
                    template="plotly_dark",
                    text="count",
                    labels={"count": "Issue Count", "severity": "Severity"},
                    title="Issues by Severity"
                )
                fig_severity.update_traces(textposition="outside")
                fig_severity.update_layout(height=360, margin=dict(l=10, r=20, t=50, b=10), showlegend=False)
                st.plotly_chart(fig_severity, use_container_width=True)

        with right:
            if "issue_type" in issues.columns:
                issue_type_df = (
                    issues["issue_type"]
                    .value_counts()
                    .rename_axis("issue_type")
                    .reset_index(name="count")
                    .sort_values("count", ascending=True)
                )
                fig_issue_type = px.bar(
                    issue_type_df,
                    x="count",
                    y="issue_type",
                    orientation="h",
                    template="plotly_dark",
                    text="count",
                    labels={"count": "Issue Count", "issue_type": "Issue Type"},
                    title="Issues by Type"
                )
                fig_issue_type.update_traces(textposition="outside")
                fig_issue_type.update_layout(height=360, margin=dict(l=10, r=20, t=50, b=10), showlegend=False)
                st.plotly_chart(fig_issue_type, use_container_width=True)
    else:
        st.info("No issue log available.")

with tab4:
    st.subheader("Governed Data Assets")
    st.markdown('<div class="section-note">This section shows the in-scope asset inventory, sensitivity profile, and stewardship coverage.</div>', unsafe_allow_html=True)

    if not assets.empty:
        asset_cols = st.columns(3)
        with asset_cols[0]:
            metric_card("Registered Assets", safe_count(assets), "Assets in the current governance register")
        with asset_cols[1]:
            high_critical_assets = 0 if "criticality" not in assets.columns else len(assets[assets["criticality"].astype(str).str.lower() == "high"])
            metric_card("High Criticality Assets", high_critical_assets, "Assets marked as high criticality")
        with asset_cols[2]:
            confidential_assets = 0 if "data_classification" not in assets.columns else len(assets[assets["data_classification"].astype(str).str.lower() == "confidential"])
            metric_card("Confidential Assets", confidential_assets, "Assets requiring tighter handling")

        st.dataframe(assets, use_container_width=True)

        left, right = st.columns(2)

        with left:
            if "data_classification" in assets.columns:
                classification_df = (
                    assets["data_classification"]
                    .value_counts()
                    .rename_axis("data_classification")
                    .reset_index(name="count")
                )
                fig_class = px.pie(
                    classification_df,
                    names="data_classification",
                    values="count",
                    hole=0.5,
                    template="plotly_dark",
                    title="Asset Classification Mix"
                )
                fig_class.update_layout(height=380, margin=dict(l=10, r=20, t=50, b=10))
                st.plotly_chart(fig_class, use_container_width=True)

        with right:
            if "lineage_status" in assets.columns:
                lineage_df = (
                    assets["lineage_status"]
                    .value_counts()
                    .rename_axis("lineage_status")
                    .reset_index(name="count")
                    .sort_values("count", ascending=True)
                )
                fig_lineage = px.bar(
                    lineage_df,
                    x="count",
                    y="lineage_status",
                    orientation="h",
                    template="plotly_dark",
                    text="count",
                    labels={"count": "Asset Count", "lineage_status": "Lineage Status"},
                    title="Lineage Documentation Coverage"
                )
                fig_lineage.update_traces(textposition="outside")
                fig_lineage.update_layout(height=380, margin=dict(l=10, r=20, t=50, b=10), showlegend=False)
                st.plotly_chart(fig_lineage, use_container_width=True)
    else:
        st.info("No asset register available.")

with tab5:
    st.subheader("AI Governance")
    st.markdown('<div class="section-note">This section extends the control tower into AI and generative AI use case oversight, review status, and risk visibility.</div>', unsafe_allow_html=True)

    if not ai_use_cases.empty:
        ai_cols = st.columns(4)
        with ai_cols[0]:
            metric_card("AI Use Cases", safe_count(ai_use_cases), "Use cases currently in the register")
        with ai_cols[1]:
            high_risk_ai = 0 if "risk_level" not in ai_use_cases.columns else len(ai_use_cases[ai_use_cases["risk_level"].astype(str).str.lower() == "high"])
            metric_card("High Risk Use Cases", high_risk_ai, "Use cases needing stronger review")
        with ai_cols[2]:
            gen_ai_cases = 0 if "ai_type" not in ai_use_cases.columns else len(ai_use_cases[ai_use_cases["ai_type"].astype(str).str.contains("Generative", case=False, na=False)])
            metric_card("Generative AI Use Cases", gen_ai_cases, "GenAI use cases currently registered")
        with ai_cols[3]:
            metric_card("Risk Assessments Logged", safe_count(ai_risk), "Assessment entries recorded")

        st.dataframe(ai_use_cases, use_container_width=True)

        left, right = st.columns(2)

        with left:
            if "risk_level" in ai_use_cases.columns:
                ai_risk_df = (
                    ai_use_cases["risk_level"]
                    .value_counts()
                    .rename_axis("risk_level")
                    .reset_index(name="count")
                    .sort_values("count", ascending=True)
                )
                fig_ai_risk = px.bar(
                    ai_risk_df,
                    x="count",
                    y="risk_level",
                    orientation="h",
                    template="plotly_dark",
                    text="count",
                    labels={"count": "Use Case Count", "risk_level": "Risk Level"},
                    title="AI Use Cases by Risk Level"
                )
                fig_ai_risk.update_traces(textposition="outside")
                fig_ai_risk.update_layout(height=360, margin=dict(l=10, r=20, t=50, b=10), showlegend=False)
                st.plotly_chart(fig_ai_risk, use_container_width=True)

        with right:
            if "status" in ai_use_cases.columns:
                ai_status_df = (
                    ai_use_cases["status"]
                    .value_counts()
                    .rename_axis("status")
                    .reset_index(name="count")
                    .sort_values("count", ascending=True)
                )
                fig_ai_status = px.bar(
                    ai_status_df,
                    x="count",
                    y="status",
                    orientation="h",
                    template="plotly_dark",
                    text="count",
                    labels={"count": "Use Case Count", "status": "Review Status"},
                    title="AI Use Cases by Review Status"
                )
                fig_ai_status.update_traces(textposition="outside")
                fig_ai_status.update_layout(height=360, margin=dict(l=10, r=20, t=50, b=10), showlegend=False)
                st.plotly_chart(fig_ai_status, use_container_width=True)

        if not ai_risk.empty:
            st.subheader("AI Risk Assessment Log")
            risk_cols = [col for col in [
                "assessment_id", "use_case_id", "risk_dimension",
                "risk_rating", "control_summary", "assessment_status", "review_owner"
            ] if col in ai_risk.columns]
            st.dataframe(ai_risk[risk_cols], use_container_width=True)
    else:
        st.info("No AI use case register available.")
