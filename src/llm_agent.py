import threading
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class TrafficEfficiencyLLMAgent:
    """
    LLM-based agent that estimates traffic efficiency.
    Thread-safe calculation for Streamlit integration.
    """

    def __init__(self):
        # Initialize Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2
        )

    def calculate_efficiency(self, total_cars: int, avg_wait_time: float, max_wait_time: float) -> float:
        """
        Calculate traffic efficiency using Gemini LLM.
        Returns a float between 0 and 100.
        """
        prompt = f"""
You are an intelligent traffic management assistant.

Given:
- Total cars at intersection: {total_cars}
- Average waiting time (seconds): {avg_wait_time}
- Maximum waiting time (seconds): {max_wait_time}

Return ONLY a single number between 0 and 100
representing traffic efficiency.

Rules:
- Higher cars and higher waiting times reduce efficiency
- Balanced and low waiting times increase efficiency
- Do NOT explain anything
- Output ONLY the number
"""
        try:
            response = self.llm.invoke([{"role": "user", "content": prompt}])
            text = response.content.strip()
            return float(text)
        except Exception:
            # Fallback if LLM fails
            return max(0.0, min(100.0, 100 - total_cars * 0.1 - avg_wait_time))


def calculate_llm_efficiency_async(agent):
    """
    Threaded function to calculate efficiency delta using the LLM.
    Saves result to Streamlit session_state.
    """
    if 'llm_agent' not in st.session_state:
        st.session_state.llm_agent = TrafficEfficiencyLLMAgent()

    llm_agent = st.session_state.llm_agent

    total_cars = sum(agent.traffic_counts.values())
    avg_wait = sum(agent.green_timings[d]['last'] for d in agent.green_timings) / 4
    max_wait = max(agent.green_timings[d]['last'] for d in agent.green_timings)

    try:
        delta_efficiency = llm_agent.calculate_efficiency(
            total_cars=total_cars,
            avg_wait_time=avg_wait,
            max_wait_time=max_wait
        )
        st.session_state.llm_efficiency = delta_efficiency
    except Exception as e:
        st.session_state.llm_efficiency = None
        st.error(f"LLM Error: {e}")


def run_llm_thread(agent):
    """
    Start the LLM efficiency calculation in a background thread.
    """
    thread = threading.Thread(target=calculate_llm_efficiency_async, args=(agent,), daemon=True)
    thread.start()
