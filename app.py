import requests
import streamlit as st

MODEL = "gemma3:1b"  # fast. use gemma3:4b if PC is good

st.set_page_config(page_title="Meal Planner for a Friend", page_icon="🍛")
st.title("🍛 Meal Planner for a Friend")
st.caption("Runs 100% local with open model Gemma. No cloud, no data shared.")

name = st.text_input("Friend's name", "Rahul")
allergies = st.text_input("Allergies (must avoid)", "peanuts, milk")
dislikes = st.text_input("Dislikes", "karela")
diet = st.selectbox("Diet", ["Vegetarian", "Non-veg", "Vegan"])
budget = st.selectbox("Budget", ["Low", "Medium", "High"])

if st.button("Make 7 day plan"):
    prompt = f"""Make a 7 day Indian meal plan (breakfast, lunch, dinner) for {name}.
Diet: {diet}. Budget: {budget}.
NEVER use these allergens or anything made from them: {allergies}.
Do not include: {dislikes}.
Keep dishes simple and cheap. Then give a short grocery list.
Use simple English."""
    with st.spinner("Gemma is cooking..."):
        try:
            r = requests.post(
                "http://localhost:11434/api/chat",
                json={"model": MODEL, "stream": False,
                      "messages": [{"role": "user", "content": prompt}]},
                timeout=300,
            )
            st.markdown(r.json()["message"]["content"])
            st.warning("Check ingredient labels yourself. AI can make mistakes.")
        except Exception as e:
            st.error(f"Start Ollama first. Error: {e}")