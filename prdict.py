import pandas as pd
import streamlit as st

df = pd.read_csv("shimoga_colleges_cutoff.csv")

df_long = df.melt(
    id_vars=["College", "Course"],
    var_name="Category",
    value_name="Closing Rank"
)

df_long = df_long.dropna(subset=["Closing Rank"])
df_long["Closing Rank"] = df_long["Closing Rank"].astype(float)

df_long = df_long.rename(columns={"Course": "Branch"})

st.set_page_config(page_title="DCET 2025 Predictor", layout="wide")
st.title("🎓 DCET 2025  College Predictor")
st.markdown(" 🔖NOTE : its Only and Predict , Not exacat its may varies !")

name = st.text_input("👤 Enter your name")
rank = st.number_input("🏆 Enter your DCET Rank", min_value=1)


available_categories = sorted(df_long["Category"].dropna().unique())
selected_categories = st.multiselect(
    "📛 Select your Category/Categories (GM, 2AG, SCG etc.)",
    available_categories
)

available_branches = sorted(df_long["Branch"].dropna().unique())
selected_branches = st.multiselect(
    "📚 Select Preferred Branches (CSE, AIML, etc.)",
    available_branches
)

if selected_categories and selected_branches:
    eligible_df = df_long[
        (df_long["Category"].isin(selected_categories)) &
        (df_long["Branch"].isin(selected_branches)) &
        (df_long["Closing Rank"] >= rank)
    ].sort_values(by="Closing Rank")

    if not eligible_df.empty:
        st.success(f"🎯 Hi {name}, based on your rank {rank}, here are your {len(eligible_df)} eligible college options:")
        st.dataframe(
            eligible_df[["College", "Branch", "Category", "Closing Rank"]],
            use_container_width=True,
            height=600
        )
    else:
        st.warning("😕 No matching colleges found for your rank, category, and branch preferences.")
else:
    st.info("ℹ️ Please select at least one category and one branch to view results.")
