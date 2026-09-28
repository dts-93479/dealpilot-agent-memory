# 💼 DealPilot: Autonomous Enterprise Sales Copilot

> An AI agent that eliminates enterprise deal amnesia by learning, retaining, and synthesizing buyer constraints across long sales cycles using Vectorize Hindsight and Groq.

---

## 📌 Problem Overview

Enterprise B2B sales cycles typically run across weeks or months with multiple touchpoints[cite: 1]. Critical customer requirements—such as regional data compliance, security mandates, and strict billing structures—frequently get lost between discovery calls and contract generation[cite: 1].

Stateless LLMs suffer from operational amnesia, causing them to generate generic or conflicting terms that jeopardize high-value deals[cite: 1, 2]. Simple context window stuffing results in latency spikes, high inference costs, and attention drift[cite: 2]. 

**DealPilot** solves this by pairing low-latency reasoning via Groq with persistent, structured long-term memory powered by **Vectorize Hindsight**[cite: 1].

---

## 🧠 How Hindsight Memory Powers DealPilot

DealPilot integrates Hindsight's core primitives directly into its execution loop[cite: 1]:

1. **`retain()` (Learning Facts):** As call notes, meeting transcripts, and stakeholder objections are captured, DealPilot stores them into a dedicated account memory bank[cite: 1].
2. **`recall()` (Context Retrieval):** When a rep prompts the agent to draft proposals or emails, DealPilot semantically fetches relevant historical constraints tied to that specific deal[cite: 1].
3. **`reflect()` (Strategic Synthesis):** Hindsight synthesizes disparate feedback and interactions over time into clear, actionable guardrails (e.g., non-negotiable compliance rules, billing constraints) that prevent the agent from making costly negotiation mistakes[cite: 1].

---

## 🏗️ System Architecture

```text
       [Sales Rep / Deal Notes]
                  │
                  ▼
         [Streamlit Workspace]
                  │
                  ▼
         [DealPilot Agent Core]
        ▲                      │
(Recall)│                      │ (Store constraints)
        │                      ▼
  [Vectorize Hindsight] ◄───► [Groq LPU Engine]
     (Memory Bank)             (Fast Inference)

```

---

## 🚀 Features

* **Split-Screen Deal Workspace:** Manage proposal drafting on the left while monitoring the real-time **Hindsight Brain Inspector** on the right.
* **Inspectable State:** Complete visibility into exact facts retrieved via `recall` and synthesized via `reflect`.
* **Dynamic Policy Adaptation:** The agent automatically respects historical constraints (e.g., regional hosting rules, annual billing mandates) without requiring manual reminders in the prompt.


* **High-Speed Inference:** Powered by Groq's LPU infrastructure for instant execution.



---

## 🛠️ Tech Stack

* **Memory Layer:** [Vectorize Hindsight](https://hindsight.vectorize.io/?utm_source=gemini)

* **LLM Reasoning:** [Groq](https://groq.com/?utm_source=gemini) (`llama-3.3-70b-versatile` / `qwen-2.5-32b`)


* **Frontend / UI:** Streamlit
* **Runtime:** Python 3.10+

---

## 📦 Getting Started

### 1. Prerequisites

* Python 3.10 or higher installed.
* A Hindsight Cloud account and API key.


* A Groq Cloud API key.



### 2. Clone the Repository

```bash
git clone [https://github.com/dts-93479/dealpilot-agent-memory.git](https://github.com/dts-93479/dealpilot-agent-memory.git)
cd dealpilot-agent-memory

```

### 3. Create and Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

```

### 4. Install Dependencies

```bash
pip install -r requirements.txt

```

### 5. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env

```

Open `.env` and fill in your actual credentials:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
HINDSIGHT_API_KEY=your_hindsight_api_key_here
HINDSIGHT_BASE_URL=[https://api.hindsight.vectorize.io](https://api.hindsight.vectorize.io)

```

### 6. Run the Application

```bash
streamlit run app.py

```

Open your browser and navigate to `http://localhost:8501`.

---

## 🎬 Demo Workflow (Before vs. After)

1. **Step 1 (Cold Baseline):** Run the action prompt `"Draft an enterprise closing proposal email for Acme Corp."` without ingesting notes. The agent produces standard SaaS terms (US cloud hosting, quarterly billing).


2. **Step 2 (Retain):** Use the Ingest panel to add discovery notes:
> "Call with CFO Sarah: Firm requirement that all customer data must reside in Frankfurt (EU), SOC2 Type II report must be attached, and quarterly billing is strictly rejected in favor of annual invoicing."


3. **Step 3 (The Payoff):** Re-run the draft prompt. The agent queries Hindsight (`recall` and `reflect`), automatically detects Sarah's constraints, sets up Frankfurt hosting, attaches the SOC2 report, and configures annual billing without prompt hinting.



---

## 🔗 Official References

* [Vectorize Hindsight GitHub Repository](https://github.com/vectorize-io/hindsight?utm_source=gemini)

* [Hindsight Official Documentation](https://hindsight.vectorize.io/?utm_source=gemini)

* [What is Agent Memory? (Vectorize Guide)](https://vectorize.io/what-is-agent-memory?utm_source=gemini)


```

```
