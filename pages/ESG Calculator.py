import streamlit as st
import pandas as pd


st.title("ESG Score Calculator and Rating")


st.markdown("### Enter Company Details")
company_name = st.text_input("Company Name", value="", placeholder="Enter the company name")


st.markdown("### Enter ESG Scores")
environmental_score = st.slider("Environmental Score (0-100)", 0, 100, 0)  
social_score = st.slider("Social Score (0-100)", 0, 100, 0)  
governance_score = st.slider("Governance Score (0-100)", 0, 100, 0)  


if company_name:
    overall_score = (environmental_score + social_score + governance_score) / 3
else:
    overall_score = None  

def get_esg_rating(score):
    if score is None:
        return None
    elif score >= 90:
        return "AAA"
    elif score >= 80:
        return "AA"
    elif score >= 70:
        return "A"
    elif score >= 60:
        return "BBB"
    elif score >= 50:
        return "BB"
    elif score >= 40:
        return "B"
    elif score >= 30:
        return "CCC"
    else:
        return "D"

rating = get_esg_rating(overall_score)
if company_name:
    st.markdown("### Results")
    st.write(f"**Overall ESG Score:** {overall_score:.2f}")
    st.write(f"**ESG Rating:** {rating}")
else:
    st.warning("Enter a valid company name to see the results.")

# Initialize session state for ESG results
if "esg_results" not in st.session_state:
    st.session_state["esg_results"] = []

# Save the Result
if st.button("Save Result"):
    if not company_name:
        st.error("Please enter a company name before saving!")
    else:
        st.session_state["esg_results"].append({
            "Company": company_name,
            "Environmental Score": environmental_score,
            "Social Score": social_score,
            "Governance Score": governance_score,
            "Overall Score": overall_score,
            "Rating": rating
        })
        st.success(f"Result for {company_name} saved successfully!")

# Display Saved Results (conditionally)
if st.session_state["esg_results"]:
    st.markdown("### Saved Results")
    results_df = pd.DataFrame(st.session_state["esg_results"])
    st.dataframe(results_df)
else:
    st.info("No saved results yet. Enter details and save to view results.")
