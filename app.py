import streamlit as st
from main import setup_agents_and_tasks, kickoff_crew

def main():
    st.title("AI LOVES HR Sales Agent Interface")

    # Input form
    with st.form(key='agent_input_form'):
        lead_name = st.text_input("Lead Name", value="DeepLearningAI")
        industry = st.text_input("Industry", value="Online Learning Platform")
        key_decision_maker = st.text_input("Key Decision Maker", value="Andrew Ng")
        position = st.text_input("Position", value="CEO")
        milestone = st.text_input("Recent Milestone", value="product launch")

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        inputs = {
            "lead_name": lead_name,
            "industry": industry,
            "key_decision_maker": key_decision_maker,
            "position": position,
            "milestone": milestone
        }

        # Setup agents and tasks
        crew = setup_agents_and_tasks()

        # Kickoff the crew with the provided inputs
        result = kickoff_crew(crew, inputs)
        st.write(result)

if __name__ == "__main__":
    main()
