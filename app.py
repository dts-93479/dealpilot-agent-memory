import streamlit as st
from agent import DealPilotAgent

st.set_page_config(page_title="DealPilot - Persistent Sales Agent", layout="wide")

@st.cache_resource
def get_agent():
    return DealPilotAgent()

agent = get_agent()

st.title("💼 DealPilot: Sales Agent with Hindsight Memory")
st.caption("Powered by Vectorize Hindsight & Groq LPU")

# Account identifier acts as the bank_id
col1, col2 = st.columns([1, 2])
with col1:
    bank_id = st.text_input("Active Deal Bank ID", value="deal-acmecorp-2026")

# Layout: Workspace on the left, Hindsight Inspector on the right
left_col, right_col = st.columns([1.2, 0.8])

with left_col:
    st.subheader("📝 Deal Workspace")
    
    with st.expander("➕ Ingest Call Notes / Prospect Constraint", expanded=False):
        new_note = st.text_area("Paste new call transcript snippet or objection:", 
                                placeholder="e.g., CFO rejected quarterly billing. SOC2 Type II is mandatory. All hosting must remain in EU region.")
        save_btn = st.button("Store into Hindsight Memory")
        if save_btn and new_note:
            success = agent.memory.retain(bank_id=bank_id, content=new_note)
            if success:
                st.success("Successfully written to Hindsight persistent memory!")
            else:
                st.error("Failed to write to Hindsight.")

    user_query = st.text_area(
        "Action Prompt:", 
        value="Draft an executive closing proposal email for Acme Corp's legal and procurement team.",
        height=100
    )
    run_btn = st.button("🚀 Run Agent Task", type="primary")

with right_col:
    st.subheader("🧠 Hindsight Brain Inspector")
    st.info("Judges: This panel displays persistent state retrieved live from Hindsight APIs.")
    memory_placeholder = st.empty()
    reflect_placeholder = st.empty()

if run_btn:
    with st.spinner("Querying Hindsight & Groq..."):
        result = agent.process_turn(bank_id=bank_id, user_prompt=user_query)
        
        with left_col:
            st.markdown("### 📄 Generated Deal Output")
            st.markdown(result["response"])

        with right_col:
            memory_placeholder.markdown("#### 🔍 Recalled Memories (`recall`)")
            if result["recalled_memories"]:
                for m in result["recalled_memories"]:
                    st.write(f"• {m}")
            else:
                st.write("*(No specific memories indexed yet)*")

            reflect_placeholder.markdown("#### 💡 Strategic Synthesis (`reflect`)")
            st.write(result["reflection"])