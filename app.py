import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title="AI Study Planner", layout="wide")

st.title("🎓 AI Personalized Study Planner")
st.markdown("Generate an intelligent study plan based on your marks, subject difficulty, and available study hours.")

subjects = ["Math","Physics","Chemistry","Biology","Computer Science"]

st.sidebar.header("📊 Student Inputs")

marks = {}
difficulty = {}

for sub in subjects:
    marks[sub] = st.sidebar.slider(f"{sub} Marks",0,100,60)
    difficulty[sub] = st.sidebar.selectbox(f"{sub} Difficulty",["Easy","Medium","Hard"],key=sub)

study_hours = st.sidebar.slider("Available Study Hours Per Day",1,12,5)

days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

generate = st.sidebar.button("Generate AI Study Plan")

# Difficulty weights
difficulty_map = {
    "Easy":1,
    "Medium":2,
    "Hard":3
}

def generate_plan(marks,difficulty,hours):

    df = pd.DataFrame({
        "Subject":marks.keys(),
        "Marks":marks.values(),
        "Difficulty":[difficulty_map[difficulty[s]] for s in marks]
    })

    # Weakness score
    df["Weakness"] = 100 - df["Marks"]

    # AI priority score
    df["Priority"] = df["Weakness"] * df["Difficulty"]

    total_priority = df["Priority"].sum()

    df["Daily Hours"] = (df["Priority"]/total_priority) * hours

    df["Daily Hours"] = df["Daily Hours"].round(2)

    return df.sort_values(by="Priority",ascending=False)

def generate_weekly_schedule(plan):

    schedule = []

    for day in days:

        shuffled = plan.sample(frac=1)

        for _,row in shuffled.iterrows():

            schedule.append({
                "Day":day,
                "Subject":row["Subject"],
                "Hours":row["Daily Hours"]
            })

    return pd.DataFrame(schedule)

def predict_score(marks):

    avg = np.mean(list(marks.values()))

    improvement = random.randint(8,18)

    return min(avg + improvement,100)

if generate:

    plan = generate_plan(marks,difficulty,study_hours)

    st.subheader("📊 Subject Priority Analysis")

    st.dataframe(plan)

    st.bar_chart(plan.set_index("Subject")["Daily Hours"])

    st.subheader("📅 Weekly Study Schedule")

    schedule = generate_weekly_schedule(plan)

    st.dataframe(schedule)

    st.bar_chart(schedule.groupby("Subject")["Hours"].sum())

    st.subheader("🧠 AI Performance Prediction")

    predicted = predict_score(marks)

    st.metric("Expected Average Score",f"{predicted}%")

    st.subheader("💡 Smart Study Suggestions")

    weak_subjects = plan.head(2)["Subject"].values

    st.write(f"Focus more on **{weak_subjects[0]}** and **{weak_subjects[1]}**.")

    st.write("✔ Use active recall while studying.")
    st.write("✔ Practice previous exam papers.")
    st.write("✔ Take short breaks every 45 minutes.")
    st.write("✔ Revise difficult topics at the end of the day.")

    st.subheader("⬇ Download Study Plan")

    csv = schedule.to_csv(index=False)

    st.download_button(
        label="Download Schedule CSV",
        data=csv,
        file_name="study_plan.csv",
        mime="text/csv"
    )
