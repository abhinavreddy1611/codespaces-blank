import streamlit as st
import pandas as pd
import plotly.express as px

st.title("ESG Ratings Visualization")

# Step 1: Load Pre-stored Company Ratings
data = {
    "Company": ["Company A", "Company B", "Company C", "Company D"],
    "Environmental Score": [85, 60, 90, 50],
    "Social Score": [80, 55, 85, 45],
    "Governance Score": [75, 65, 88, 50],
}
stored_companies_df = pd.DataFrame(data)
stored_companies_df["Overall Score"] = (
    stored_companies_df["Environmental Score"]
    + stored_companies_df["Social Score"]
    + stored_companies_df["Governance Score"]
) / 3
stored_companies_df["Rating"] = stored_companies_df["Overall Score"].apply(
    lambda x: "AAA" if x >= 90 else
              "AA" if x >= 80 else
              "A" if x >= 70 else
              "BBB" if x >= 60 else
              "BB" if x >= 50 else
              "B" if x >= 40 else
              "CCC" if x >= 30 else "D"
)

# Step 2: Retrieve User-Entered Results from Session State
if "esg_results" in st.session_state and st.session_state["esg_results"]:
    user_results_df = pd.DataFrame(st.session_state["esg_results"])
else:
    user_results_df = pd.DataFrame(columns=["Company", "Environmental Score", "Social Score", "Governance Score", "Overall Score", "Rating"])

# Combine both datasets for visualization
stored_companies_df["Source"] = "Pre-stored"
user_results_df["Source"] = "User"
combined_df = pd.concat([stored_companies_df, user_results_df], ignore_index=True)

# Step 3: Display Data Tables
st.markdown("### Pre-stored Company Ratings")
st.dataframe(stored_companies_df)

if not user_results_df.empty:
    st.markdown("### User-Entered ESG Ratings")
    st.dataframe(user_results_df)
else:
    st.warning("No user-entered ESG ratings found! Please calculate and save results in the Calculator page.")

# Step 4: Scatter Plot Visualization
if not combined_df.empty:
    st.markdown("### ESG Scatter Plot")
    scatter_fig = px.scatter(
        combined_df,
        x="Environmental Score",
        y="Social Score",
        size="Overall Score",  # Bubble size represents overall score
        color="Source",        # Different colors for user and pre-stored
        hover_data=["Company", "Governance Score", "Overall Score", "Rating"],
        title="Scatter Plot of ESG Scores",
        labels={
            "Environmental Score": "Environmental Score",
            "Social Score": "Social Score"
        },
    )
    # Customizing marker colors
    scatter_fig.update_traces(marker=dict(line=dict(width=1)), opacity=0.7)
    scatter_fig.update_layout(legend_title="Source")
    st.plotly_chart(scatter_fig, use_container_width=True)
