import streamlit as st
import pandas as pd
import os
from datetime import datetime

from classifier import classify_ticket
from utils import save_ticket, route_ticket, generate_reply

st.set_page_config(layout="wide")

st.title("🤖 Smart Support Ticket Classifier")

DATA_PATH = "data/tickets.csv"

# -------- SIDEBAR FILTERS -------- #
st.sidebar.header("🔍 Filters")

try:
    df = pd.read_csv(DATA_PATH)
except:
    df = pd.DataFrame()

if not df.empty:
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    categories = ["All"] + list(df["Category"].dropna().unique())
    priorities = ["All"] + list(df["Priority"].dropna().unique())

    min_date = df["Timestamp"].min().date()
    max_date = df["Timestamp"].max().date()
else:
    categories = ["All"]
    priorities = ["All"]
    today = datetime.now().date()
    min_date = today
    max_date = today

selected_category = st.sidebar.selectbox("Category", categories)
selected_priority = st.sidebar.selectbox("Priority", priorities)

start_date, end_date = st.sidebar.date_input(
    "Date Range",
    [min_date, max_date]
)

if st.sidebar.button("Reset Filters"):
    st.rerun()

# -------- CSV UPLOAD -------- #
st.subheader("📁 Upload CSV")

file = st.file_uploader("Upload ticket CSV", type=["csv"])

if file:
    new_df = pd.read_csv(file)

    if not os.path.exists(DATA_PATH):
        new_df.to_csv(DATA_PATH, index=False)
    else:
        new_df.to_csv(DATA_PATH, mode="a", header=False, index=False)

    st.success("CSV uploaded successfully!")
    st.rerun()

# -------- MANUAL ENTRY -------- #
st.subheader("✍️ Manual Ticket Entry")

user_input = st.text_area("Enter customer message:")

if st.button("Submit Ticket"):
    if user_input.strip() == "":
        st.warning("Enter a message")
    else:
        result = classify_ticket(user_input)

        save_ticket(user_input, result)

        st.success("Ticket added!")

        st.write("**Category:**", result["category"])
        st.write("**Priority:**", result["priority"])
        st.write("**Reason:**", result["reason"])

        st.subheader("💬 Auto Response")
        st.write(generate_reply(result["category"]))

        st.rerun()

# -------- LOAD DATA AGAIN -------- #
try:
    df = pd.read_csv(DATA_PATH)
except:
    df = pd.DataFrame()

# -------- APPLY FILTERS -------- #
if not df.empty:
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    filtered_df = df.copy()

    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["Category"] == selected_category]

    if selected_priority != "All":
        filtered_df = filtered_df[filtered_df["Priority"] == selected_priority]

    filtered_df = filtered_df[
        (filtered_df["Timestamp"] >= pd.to_datetime(start_date)) &
        (filtered_df["Timestamp"] <= pd.to_datetime(end_date))
    ]

    filtered_df = filtered_df.sort_values(by="Timestamp", ascending=False)

else:
    filtered_df = pd.DataFrame()

# -------- TABS -------- #
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Ticket History",
    "📊 Category Analysis",
    "🥧 Priority Analysis",
    "⏳ Time Analysis"
])

# -------- TAB 1: HISTORY -------- #
with tab1:
    st.subheader("📋 Ticket History")

    if filtered_df.empty:
        st.warning("⚠️ No data after applying filters. Try resetting filters.")
    else:
        st.write(f"Showing {len(filtered_df)} tickets")
        st.dataframe(filtered_df.fillna("N/A"))

# -------- TAB 2: CATEGORY -------- #
with tab2:
    st.subheader("📊 Category Analysis")

    if not filtered_df.empty:

        cat_filter = st.selectbox(
            "Filter Category (Tab Level)",
            ["All"] + list(filtered_df["Category"].unique()),
            key="cat_tab_filter"
        )

        tab_df = filtered_df.copy()
        if cat_filter != "All":
            tab_df = tab_df[tab_df["Category"] == cat_filter]

        st.write("### Category Count")
        st.bar_chart(tab_df["Category"].value_counts())

        st.write("### Category Distribution")
        st.pyplot(tab_df["Category"].value_counts().plot.pie(autopct='%1.1f%%').figure)

        st.write("### Category vs Priority")
        pivot = tab_df.pivot_table(
            index="Category",
            columns="Priority",
            aggfunc="size",
            fill_value=0
        )
        st.dataframe(pivot)

# -------- TAB 3: PRIORITY -------- #
with tab3:
    st.subheader("🥧 Priority Analysis")

    if not filtered_df.empty:

        pr_filter = st.selectbox(
            "Filter Priority (Tab Level)",
            ["All"] + list(filtered_df["Priority"].unique()),
            key="priority_tab_filter"
        )

        tab_df = filtered_df.copy()
        if pr_filter != "All":
            tab_df = tab_df[tab_df["Priority"] == pr_filter]

        st.write("### Priority Count")
        st.bar_chart(tab_df["Priority"].value_counts())

        st.write("### Priority Distribution")
        st.pyplot(tab_df["Priority"].value_counts().plot.pie(autopct='%1.1f%%').figure)

        st.write("### Priority Trend Over Time")
        trend = tab_df.groupby(
            [tab_df["Timestamp"].dt.date, "Priority"]
        ).size().unstack(fill_value=0)

        st.line_chart(trend)

# -------- TAB 4: TIME -------- #
with tab4:
    st.subheader("⏳ Time Analysis")

    if not filtered_df.empty:

        tab_df = filtered_df.copy()
        tab_df["Date"] = tab_df["Timestamp"].dt.date

        st.write("### Tickets Per Day")
        daily = tab_df.groupby("Date").size()
        st.line_chart(daily)

        st.write("### Category Trend Over Time")
        area = tab_df.groupby(
            ["Date", "Category"]
        ).size().unstack(fill_value=0)

        st.area_chart(area)

        st.write("### Priority Trend Over Time")
        pr_trend = tab_df.groupby(
            ["Date", "Priority"]
        ).size().unstack(fill_value=0)

        st.line_chart(pr_trend)