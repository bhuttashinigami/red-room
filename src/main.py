import streamlit as st
import streamlit.components.v1 as components
import time
import random
from agent import TrafficIntersectionAgent
from database import save_cycle, init_db
from ui.visualization import create_visualization_html
from llm_agent import TrafficEfficiencyLLMAgent
from llm_agent import run_llm_thread

st.set_page_config(page_title="Traffic Intersection Agent", layout="wide")
init_db()

# --------------------------------------------------
# SESSION INITIALIZATION
# --------------------------------------------------
if "HIGH_TRAFFIC_ROAD" not in st.session_state:
    st.session_state.HIGH_TRAFFIC_ROAD = random.choice(
        ["north", "south", "east", "west"]
    )

if "agent" not in st.session_state:
    st.session_state.agent = TrafficIntersectionAgent(
        high_traffic_road=st.session_state.HIGH_TRAFFIC_ROAD
    )
    st.session_state.running = False
    st.session_state.last_cycle_data = None
    st.session_state.llm_agent = TrafficEfficiencyLLMAgent()

agent = st.session_state.agent
llm_agent = st.session_state.llm_agent

# --------------------------------------------------
# UI CONTROLS
# --------------------------------------------------
st.title("Adaptive Traffic Intersection Agent")
st.markdown(f"**High Traffic Road:** {agent.high_traffic_road.upper()}")

col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    if st.button("Start" if not st.session_state.running else "Pause"):
        st.session_state.running = not st.session_state.running
        st.rerun()

with col2:
    if st.button("Reset"):
        st.session_state.HIGH_TRAFFIC_ROAD = random.choice(
            ["north", "south", "east", "west"]
        )
        st.session_state.agent = TrafficIntersectionAgent(
            high_traffic_road=st.session_state.HIGH_TRAFFIC_ROAD
        )
        st.session_state.running = False
        st.session_state.last_cycle_data = None
        st.rerun()

# --------------------------------------------------
# STATUS
# --------------------------------------------------
status_col1, status_col2 = st.columns(2)
with status_col1:
    st.markdown(f"**Cycle Number:** {agent.cycle_number}")
with status_col2:
    st.markdown(
        f"**Status:** {'🟢 Running' if st.session_state.running else '🔴 Paused'}"
    )

# --------------------------------------------------
# ANALYTICS
# --------------------------------------------------
if st.session_state.last_cycle_data:
    st.success(
        f"✅ Cycle {st.session_state.last_cycle_data.cycle_number} completed"
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Cars", st.session_state.last_cycle_data.total_cars)
    c2.metric(
        "Avg Wait Time",
        f"{st.session_state.last_cycle_data.average_wait_time}s",
    )
    c3.metric(
        "Δ Efficiency (Adaptive − Static)",
        f"{st.session_state.last_cycle_data.efficiency_score:.2f}",
    )

# --------------------------------------------------
# SIMULATION LOOP
# --------------------------------------------------
if st.session_state.running:
    cycle_complete = agent.run_cycle()

    if cycle_complete:
        validated_data = save_cycle(agent)
        if validated_data:
            st.session_state.last_cycle_data = validated_data

            # Start LLM calculation in background
            run_llm_thread(agent)

    components.html(create_visualization_html(agent), height=600)
    time.sleep(1)
    st.rerun()

else:
    components.html(create_visualization_html(agent), height=600)
