"""
Streamlit UI for the multi-agent research pipeline.

Run with:
    streamlit run streamlit_app.py

Place this file in your project root (same level as main.py / config.py).
Replace pipeline/research_pipeline.py with the updated version that
accepts an optional `on_step` callback (fully backward compatible).
"""

import queue
import threading
from datetime import datetime
import streamlit as st
from pipeline.research_pipeline import run_research_pipeline

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Multi Agentic Research",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------
STAGES = [
    {"key": "search", "code": "01_SEARCH_AGENT", "label": "Search", "color": "#35C9C1"},
    {"key": "read", "code": "02_READER_AGENT", "label": "Read", "color": "#5B8DEF"},
    {"key": "write", "code": "03_WRITER_CHAIN", "label": "Write", "color": "#F5A623"},
    {"key": "critique", "code": "04_CRITIC_CHAIN", "label": "Critique", "color": "#8B7CF6"},
]

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root{
  --bg:#0A0E14;
  --bg-elevated:#10151D;
  --surface:#161C26;
  --surface-hover:#1D2430;
  --border:#242B38;
  --text-primary:#EDF1F7;
  --text-secondary:#8D97A8;
  --text-dim:#5B6472;
}

html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
.stApp { background: var(--bg); }
#MainMenu, footer, header { visibility: hidden; }

/* ---- Hero ---- */
.rc-hero{
  padding: 8px 0 28px 0;
  border-bottom: 1px solid var(--border);
  margin-bottom: 28px;
}
.rc-eyebrow{
  font-family:'JetBrains Mono', monospace;
  font-size:12px;
  letter-spacing:2px;
  color: var(--text-dim);
  text-transform:uppercase;
  margin-bottom:6px;
}
.rc-title{
  font-family:'Space Grotesk', sans-serif;
  font-weight:700;
  font-size:34px;
  color: var(--text-primary);
  letter-spacing:-0.5px;
  margin:0;
}
.rc-subtitle{
  font-size:14.5px;
  color: var(--text-secondary);
  margin-top:8px;
  max-width:560px;
  line-height:1.5;
}

/* ---- Pipeline tracker ---- */
.rc-tracker{ display:flex; align-items:flex-start; gap:0; margin: 6px 0 30px 0; }
.rc-node{ flex:1; display:flex; flex-direction:column; align-items:center; position:relative; }
.rc-dot{
  width:16px; height:16px; border-radius:50%;
  background: var(--surface);
  border:2px solid var(--border);
  z-index:2;
  transition: all .25s ease;
}
.rc-dot.done{ background: var(--dot-color); border-color: var(--dot-color); box-shadow: 0 0 0 4px color-mix(in srgb, var(--dot-color) 18%, transparent); }
.rc-dot.running{ background: var(--dot-color); border-color: var(--dot-color); animation: rc-pulse 1.1s ease-in-out infinite; }
.rc-line{
  position:absolute; top:7px; left:-50%; width:100%; height:2px;
  background: var(--border); z-index:1;
}
.rc-line.filled{ background: var(--dot-color); }
.rc-node:first-child .rc-line{ display:none; }
.rc-code{
  font-family:'JetBrains Mono', monospace;
  font-size:10.5px;
  color: var(--text-dim);
  margin-top:10px;
  letter-spacing:0.5px;
}
.rc-node.active .rc-code{ color: var(--dot-color); }
.rc-label{
  font-family:'Space Grotesk', sans-serif;
  font-size:14px;
  font-weight:600;
  color: var(--text-secondary);
  margin-top:2px;
}
.rc-node.active .rc-label{ color: var(--text-primary); }

@keyframes rc-pulse{
  0%{ box-shadow: 0 0 0 0 color-mix(in srgb, var(--dot-color) 45%, transparent); }
  70%{ box-shadow: 0 0 0 9px color-mix(in srgb, var(--dot-color) 0%, transparent); }
  100%{ box-shadow: 0 0 0 0 color-mix(in srgb, var(--dot-color) 0%, transparent); }
}

/* ---- Terminal-style input ---- */
.rc-prompt-label{
  font-family:'JetBrains Mono', monospace;
  font-size:12px;
  color: var(--text-dim);
  margin-bottom:6px;
  letter-spacing:1px;
}
div[data-testid="stTextInput"] input{
  background: var(--bg-elevated) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text-primary) !important;
  font-family:'JetBrains Mono', monospace !important;
  font-size: 14.5px !important;
  padding: 12px 14px !important;
}
div[data-testid="stTextInput"] input:focus{
  border-color:#35C9C1 !important;
  box-shadow: 0 0 0 1px #35C9C1 !important;
}
div[data-testid="stTextInput"] input::placeholder{ color: var(--text-dim) !important; }

/* ---- Buttons ---- */
div[data-testid="stFormSubmitButton"] button, div.stButton > button{
  background: linear-gradient(135deg, #35C9C1, #5B8DEF) !important;
  color: #05080C !important;
  border: none !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  font-family:'Space Grotesk', sans-serif !important;
  letter-spacing:0.3px;
  transition: opacity .15s ease, transform .15s ease;
}
div[data-testid="stFormSubmitButton"] button:hover, div.stButton > button:hover{
  opacity:0.88; transform: translateY(-1px);
}
div[data-testid="stFormSubmitButton"] button:disabled{
  background: var(--surface) !important; color: var(--text-dim) !important;
}

/* ---- Sidebar ---- */
section[data-testid="stSidebar"]{
  background: var(--bg-elevated);
  border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .rc-title{ font-size:20px; }
.rc-hist-item{
  font-family:'JetBrains Mono', monospace;
  font-size:12px;
  color: var(--text-secondary);
  padding:2px 0;
}
section[data-testid="stSidebar"] div.stButton > button{
  background: var(--surface) !important;
  color: var(--text-primary) !important;
  text-align:left !important;
  justify-content:flex-start !important;
  font-family:'Inter', sans-serif !important;
  font-weight:500 !important;
  border:1px solid var(--border) !important;
  border-radius:8px !important;
}
section[data-testid="stSidebar"] div.stButton > button:hover{
  background: var(--surface-hover) !important;
  border-color:#35C9C1 !important;
}

/* ---- Section headers ---- */
.rc-section-head{
  display:flex; align-items:center; gap:10px;
  margin: 26px 0 10px 0;
}
.rc-section-bar{ width:4px; height:18px; border-radius:2px; }
.rc-section-title{
  font-family:'Space Grotesk', sans-serif;
  font-size:16px; font-weight:600; color: var(--text-primary);
}
.rc-meta{
  font-family:'JetBrains Mono', monospace;
  font-size:11.5px; color: var(--text-dim); margin-bottom:18px;
}

/* ---- Tabs ---- */
div[data-testid="stTabs"] button{
  font-family:'Space Grotesk', sans-serif !important;
  color: var(--text-secondary) !important;
}
div[data-testid="stTabs"] button[aria-selected="true"]{
  color: var(--text-primary) !important;
  border-bottom-color:#35C9C1 !important;
}

/* status callouts */
div[data-testid="stStatusWidget"], div[data-testid="stAlert"]{
  border-radius: 8px !important;
  font-family:'Inter', sans-serif;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def render_tracker(statuses: dict) -> str:
    nodes_html = []
    for stage in STAGES:
        st_status = statuses.get(stage["key"], "pending")
        dot_class = "done" if st_status == "done" else ("running" if st_status == "running" else "")
        node_active = "active" if st_status in ("running", "done") else ""
        line_class = "filled" if st_status in ("running", "done") else ""
        nodes_html.append(f"""
        <div class="rc-node {node_active}" style="--dot-color:{stage['color']}">
          <div class="rc-line {line_class}" style="--dot-color:{stage['color']}"></div>
          <div class="rc-dot {dot_class}" style="--dot-color:{stage['color']}"></div>
          <div class="rc-code">{stage['code']}</div>
          <div class="rc-label">{stage['label']}</div>
        </div>
        """)
    return f'<div class="rc-tracker">{"".join(nodes_html)}</div>'


def section_head(title: str, color: str):
    st.markdown(
        f"""<div class="rc-section-head">
              <div class="rc-section-bar" style="background:{color}"></div>
              <div class="rc-section-title">{title}</div>
            </div>""",
        unsafe_allow_html=True,
    )


def _pipeline_worker(topic, q, result_holder):
    def on_step(step, status):
        q.put((step, status))

    try:
        state = run_research_pipeline(topic, on_step=on_step)
        result_holder["state"] = state
    except Exception as e:
        result_holder["error"] = str(e)
    finally:
        q.put(("__done__", None))


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "running" not in st.session_state:
    st.session_state.running = False
if "selected_run" not in st.session_state:
    st.session_state.selected_run = None

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """<div class="rc-eyebrow">MULTI-AGENT SYSTEM</div>
           <div class="rc-title">Research Console</div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="color:var(--text-secondary); font-size:13px; margin-top:6px;">'
        "search_agent → reader_agent → writer_chain → critic_chain</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="rc-eyebrow">RUN HISTORY</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown(
            '<div style="color:var(--text-dim); font-size:13px;">No runs yet — start one on the right.</div>',
            unsafe_allow_html=True,
        )
    else:
        for i, run in enumerate(reversed(st.session_state.history)):
            idx = len(st.session_state.history) - 1 - i
            label = f"{run['topic'][:34]}"
            if st.button(label, key=f"hist_{idx}", use_container_width=True):
                st.session_state.selected_run = idx
            st.markdown(
                f'<div class="rc-hist-item">{run["timestamp"]}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    if st.session_state.history and st.button("Clear history", use_container_width=True):
        st.session_state.history = []
        st.session_state.selected_run = None
        st.rerun()

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="rc-hero">
      <div class="rc-eyebrow">◆ AUTOMATED RESEARCH PIPELINE</div>
      <div class="rc-title">What do you want researched?</div>
      <div class="rc-subtitle">
        Give it a topic. Four agents take it from there — searching the web,
        reading the best source, drafting a report, and critiquing their own work.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Pipeline tracker
# ---------------------------------------------------------------------------
tracker_placeholder = st.empty()
status_placeholder = st.empty()
progress_placeholder = st.empty()

if not st.session_state.running:
    tracker_placeholder.markdown(
        render_tracker({}),
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------
with st.form("research_form", clear_on_submit=False):
    st.markdown('<div class="rc-prompt-label">&gt; TOPIC</div>', unsafe_allow_html=True)
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. latest advances in solid-state batteries",
        label_visibility="collapsed",
        disabled=st.session_state.running,
    )
    submitted = st.form_submit_button(
        "Run pipeline" if not st.session_state.running else "Running…",
        disabled=st.session_state.running,
        use_container_width=True,
    )

# ---------------------------------------------------------------------------
# Run pipeline (with live tracker)
# ---------------------------------------------------------------------------
if submitted:
    if not topic or not topic.strip():
        st.warning("Enter a topic first.")
    else:
        st.session_state.running = True
        topic_clean = topic.strip()

        q = queue.Queue()
        result_holder = {}

        thread = threading.Thread(
            target=_pipeline_worker,
            args=(topic_clean, q, result_holder),
            daemon=True,
        )

        thread.start()

        statuses = {
            "search": "pending",
            "read": "pending",
            "write": "pending",
            "critique": "pending",
        }

        tracker_placeholder.markdown(
            render_tracker(statuses),
            unsafe_allow_html=True,
        )

        status_placeholder.info("Starting research pipeline...")
        progress = progress_placeholder.progress(0)

        stage_progress = {
            "search": 25,
            "read": 50,
            "write": 75,
            "critique": 100,
        }

        stage_labels = {
            "search": "Search Agent",
            "read": "Reader Agent",
            "write": "Writer Chain",
            "critique": "Critic Chain",
        }

        while thread.is_alive() or not q.empty():
            try:
                step, status = q.get(timeout=0.2)
            except queue.Empty:
                continue

            if step == "__done__":
                break

            if step not in statuses:
                continue

            statuses[step] = status

            tracker_placeholder.markdown(
                render_tracker(statuses),
                unsafe_allow_html=True,
            )

            if status == "running":
                status_placeholder.info(
                    f"Running {stage_labels[step]}..."
                )

            elif status == "done":
                progress.progress(stage_progress[step])
                status_placeholder.success(
                    f"{stage_labels[step]} completed."
                )

        thread.join()

        st.session_state.running = False

        if "error" in result_holder:
            progress_placeholder.empty()
            status_placeholder.error(
                f"Pipeline failed: {result_holder['error']}"
            )

        else:
            progress_placeholder.progress(100)
            status_placeholder.success(
                "Research pipeline completed successfully."
            )

            st.session_state.history.append(
                {
                    "topic": topic_clean,
                    "timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    "state": result_holder["state"],
                }
            )

            st.session_state.selected_run = (
                len(st.session_state.history) - 1
            )

            st.rerun()
# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
selected_idx = st.session_state.selected_run

if selected_idx is not None and 0 <= selected_idx < len(st.session_state.history):
    run = st.session_state.history[selected_idx]
    state = run["state"]

    section_head(f'Results — "{run["topic"]}"', "#35C9C1")
    st.markdown(f'<div class="rc-meta">RUN AT {run["timestamp"]}</div>', unsafe_allow_html=True)

    tab_report, tab_critic, tab_search, tab_scraped = st.tabs(
        ["Report", "Critic feedback", "Search results", "Scraped content"]
    )

    def _text(v):
        return getattr(v, "content", v)

    with tab_report:
        report_display = str(_text(state.get("report", "")))
        st.markdown(report_display)
        st.download_button(
            "Download report (.md)",
            data=report_display,
            file_name=f"{run['topic'][:40].strip().replace(' ', '_')}_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with tab_critic:
        st.markdown(str(_text(state.get("feedback", "No feedback captured."))))

    with tab_search:
        st.code(state.get("search_results", "No search results captured."), language=None)

    with tab_scraped:
        st.code(state.get("scraped_content", "No scraped content captured."), language=None)

elif not st.session_state.history:
    st.markdown(
        '<div style="color:var(--text-dim); font-family:\'JetBrains Mono\',monospace; font-size:13px; margin-top:10px;">'
        "// awaiting first run"
        "</div>",
        unsafe_allow_html=True,
    )