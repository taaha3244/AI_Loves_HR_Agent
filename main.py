import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain.agents import Tool
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
os.environ["TAVILY_API_KEY"] =os.getenv("TAVILY_API_KEY")

def setup_agents_and_tasks():
    tavily_tool = Tool(
        name="Intermediate Answer",
        func=TavilySearchResults().run,
        description="Useful for search-based queries",
    )

    sales_rep_agent = Agent(
        role="Sales Representative",
        goal="Identify high-value leads that match our ideal customer profile",
        backstory=(
            "As a part of the dynamic sales team at AI LOVES HR, "
            "your mission is to scour the digital landscape for potential leads."
        ),
        allow_delegation=False,
        verbose=True
    )

    lead_sales_rep_agent = Agent(
        role="Lead Sales Representative",
        goal="Nurture leads with personalized, compelling communications",
        backstory=(
            "Within the vibrant ecosystem of AI Loves HR's sales department, "
            "you stand out as the bridge between potential clients and the solutions they need."
        ),
        allow_delegation=False,
        verbose=True
    )

    lead_profiling_task = Task(
        description=(
            "Conduct an in-depth analysis of {lead_name}, a company in the {industry} sector "
            "that recently showed interest in our solutions. "
            "Utilize all available data sources to compile a detailed profile."
        ),
        expected_output=(
            "A comprehensive report on {lead_name}, including company background, "
            "key personnel, recent milestones, and identified needs."
        ),
        tools=[tavily_tool],
        agent=sales_rep_agent,
    )

    personalized_outreach_task = Task(
        description=(
            "Using the insights gathered from the lead profiling report on {lead_name}, "
            "craft a personalized outreach campaign aimed at {key_decision_maker}."
        ),
        expected_output=(
            "A series of personalized email drafts tailored to {lead_name}, "
            "specifically targeting {key_decision_maker}."
        ),
        tools=[tavily_tool],
        agent=lead_sales_rep_agent
    )

    crew = Crew(
        agents=[sales_rep_agent, lead_sales_rep_agent],
        tasks=[lead_profiling_task, personalized_outreach_task],
        verbose=2,
        memory=True
    )

    return crew

def kickoff_crew(crew, inputs):
    return crew.kickoff(inputs=inputs)
