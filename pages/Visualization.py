import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("ESG Ratings Visualization")

# File path to the CSV
csv_file_path = "companies_esg.csv"

# Check if the file exists
if not os.path.exists(csv_file_path):
    st.error(f"CSV file not found at: {csv_file_path}. Please verify the path.")
    st.stop()

# Load the pre-stored company ratings
try:
    stored_companies_df = pd.read_csv(csv_file_path)
except Exception as e:
    st.error(f"Failed to load CSV file: {e}")
    st.stop()

# Ensure the CSV contains the required columns
required_columns = ["Company", "Environmental Score", "Social Score", "Governance Score"]
if not all(col in stored_companies_df.columns for col in required_columns):
    st.error(f"The CSV file must contain the columns: {', '.join(required_columns)}")
    st.stop()

# Retrieve User-Entered Results from Session State
if "esg_results" in st.session_state and st.session_state["esg_results"]:
    user_results_df = pd.DataFrame(st.session_state["esg_results"])
else:
    user_results_df = pd.DataFrame(columns=["Company", "Environmental Score", "Social Score", "Governance Score"])

# Combine both datasets for visualization
stored_companies_df["Source"] = "Pre-stored"
user_results_df["Source"] = "User"
combined_df = pd.concat([stored_companies_df, user_results_df], ignore_index=True)

# Display Data Tables
st.markdown("### Pre-stored Company Ratings")
st.dataframe(stored_companies_df)

if not user_results_df.empty:
    st.markdown("### User-Entered ESG Ratings")
    st.dataframe(user_results_df)
else:
    st.warning("No user-entered ESG ratings found! Please calculate and save results in the Calculator page.")

# Scatter Plot Visualization
if not combined_df.empty:
    st.markdown("### ESG Scatter Plot")
    scatter_fig = px.scatter(
        combined_df,
        x="Environmental Score",
        y="Social Score",
        color="Source",  # Different colors for user and pre-stored data
        hover_data=["Company", "Governance Score"],  # Tooltip data
        title="Scatter Plot of ESG Scores",
        labels={
            "Environmental Score": "Environmental Score",
            "Social Score": "Social Score"
        },
    )
    # Customize marker colors and styles
    scatter_fig.for_each_trace(
        lambda trace: trace.update(marker=dict(color="orange")) if trace.name == "User" else trace.update(marker=dict(color="blue"))
    )
    scatter_fig.update_traces(marker=dict(size=10, line=dict(width=1)), opacity=0.7)
    scatter_fig.update_layout(legend_title="Source")
    st.plotly_chart(scatter_fig, use_container_width=True)
