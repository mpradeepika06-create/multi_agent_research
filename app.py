import streamlit as st
import time

from agents.orchestrator import OrchestratorAgent
from agents.research_agent import ResearchAgent
from agents.extraction_agent import InformationExtractionAgent
from agents.fact_checker import FactCheckingAgent
from agents.analysis_agent import AnalysisAgent
from agents.report_agent import ReportGenerationAgent


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .agent-card {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 10px;
    }

    .source-card {
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #ddd;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">🔬 Multi-Agent Autonomous Research System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Multiple AI agents collaborate to research, verify, analyze and report.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Research Settings")

    model = st.selectbox(
        "AI Model",
        [
            "llama3.1",
            "llama3.2",
            "mistral",
            "phi3"
        ],
        index=0
    )

    research_depth = st.selectbox(
        "Research Depth",
        [
            "Quick",
            "Standard",
            "Deep"
        ],
        index=1
    )

    source_count = st.slider(
        "Number of Sources",
        min_value=5,
        max_value=20,
        value=10
    )

    st.divider()

    st.markdown("### 🤖 Agents")

    st.markdown(
        """
        🧭 **1. Orchestrator**  
        Creates the research plan.

        🔎 **2. Web Research**  
        Searches the web.

        📑 **3. Information Extraction**  
        Extracts important facts.

        🔍 **4. Fact Checker**  
        Verifies claims.

        🧠 **5. Analysis**  
        Analyzes the evidence.

        📝 **6. Report Generator**  
        Creates the final report.
        """
    )

    st.divider()

    st.caption(
        "Powered by Python + Streamlit + Ollama"
    )


# ============================================================
# RESEARCH INPUT
# ============================================================

st.subheader("📚 Research Topic")

topic = st.text_area(
    "What would you like to research?",
    placeholder=(
        "Example: Impact of Artificial Intelligence "
        "on education"
    ),
    height=100
)


col1, col2 = st.columns([1, 5])

with col1:

    start_button = st.button(
        "🚀 Start Research",
        type="primary",
        use_container_width=True
    )


# ============================================================
# SESSION STATE
# ============================================================

if "report" not in st.session_state:
    st.session_state.report = None

if "sources" not in st.session_state:
    st.session_state.sources = []

if "fact_check" not in st.session_state:
    st.session_state.fact_check = None

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "extracted" not in st.session_state:
    st.session_state.extracted = None

if "plan" not in st.session_state:
    st.session_state.plan = None


# ============================================================
# RESEARCH EXECUTION
# ============================================================

if start_button:

    if not topic.strip():

        st.warning(
            "⚠️ Please enter a research topic."
        )

        st.stop()

    # Clear previous results
    st.session_state.report = None
    st.session_state.sources = []
    st.session_state.fact_check = None
    st.session_state.analysis = None
    st.session_state.extracted = None
    st.session_state.plan = None

    st.divider()

    st.subheader("🤖 Agent Activity")

    status_box = st.empty()

    progress_bar = st.progress(0)

    agent_status = {
        "Orchestrator": "⏳ Waiting",
        "Web Research": "⏳ Waiting",
        "Information Extraction": "⏳ Waiting",
        "Fact Checker": "⏳ Waiting",
        "Analysis": "⏳ Waiting",
        "Report Generator": "⏳ Waiting"
    }

    def update_ui(message):

        status_box.info(message)

    # ========================================================
    # 1. ORCHESTRATOR
    # ========================================================

    agent_status["Orchestrator"] = "🔄 Running"

    st.markdown(
        "### 🧭 1. Orchestrator Agent"
    )

    orchestrator = OrchestratorAgent(
        model=model
    )

    try:

        task = orchestrator.create_tasks(
            topic
        )

        st.session_state.plan = task["plan"]

        agent_status["Orchestrator"] = "✅ Completed"

        st.success(
            "Research plan created successfully."
        )

        with st.expander(
            "View Research Plan"
        ):

            st.markdown(
                st.session_state.plan
            )

        progress_bar.progress(16)

    except Exception as e:

        st.error(
            f"Orchestrator error: {e}"
        )

        st.stop()

    # ========================================================
    # 2. WEB RESEARCH
    # ========================================================

    st.markdown(
        "### 🔎 2. Web Research Agent"
    )

    research_agent = ResearchAgent(
        max_sources=source_count
    )

    try:

        sources = research_agent.research(
            topic,
            progress_callback=update_ui
        )

        st.session_state.sources = sources

        if not sources:

            st.error(
                "No web sources were found."
            )

            st.stop()

        agent_status["Web Research"] = "✅ Completed"

        st.success(
            f"Collected {len(sources)} web sources."
        )

        progress_bar.progress(32)

    except Exception as e:

        st.error(
            f"Web research error: {e}"
        )

        st.stop()

    # ========================================================
    # 3. INFORMATION EXTRACTION
    # ========================================================

    st.markdown(
        "### 📑 3. Information Extraction Agent"
    )

    extraction_agent = InformationExtractionAgent(
        model=model
    )

    try:

        extracted = extraction_agent.extract(
            topic,
            sources,
            progress_callback=update_ui
        )

        st.session_state.extracted = extracted

        agent_status["Information Extraction"] = "✅ Completed"

        st.success(
            "Important information extracted from sources."
        )

        progress_bar.progress(48)

    except Exception as e:

        st.error(
            f"Extraction error: {e}"
        )

        st.stop()

    # ========================================================
    # 4. FACT CHECKER
    # ========================================================

    st.markdown(
        "### 🔍 4. Fact Checking Agent"
    )

    fact_checker = FactCheckingAgent(
        model=model
    )

    try:

        fact_check = fact_checker.check(
            topic,
            extracted,
            progress_callback=update_ui
        )

        st.session_state.fact_check = fact_check

        agent_status["Fact Checker"] = "✅ Completed"

        st.success(
            "Fact checking completed."
        )

        progress_bar.progress(64)

    except Exception as e:

        st.error(
            f"Fact checking error: {e}"
        )

        st.stop()

    # ========================================================
    # 5. ANALYSIS
    # ========================================================

    st.markdown(
        "### 🧠 5. Analysis Agent"
    )

    analysis_agent = AnalysisAgent(
        model=model
    )

    try:

        analysis = analysis_agent.analyze(
            topic,
            extracted,
            fact_check,
            progress_callback=update_ui
        )

        st.session_state.analysis = analysis

        agent_status["Analysis"] = "✅ Completed"

        st.success(
            "Research analysis completed."
        )

        progress_bar.progress(80)

    except Exception as e:

        st.error(
            f"Analysis error: {e}"
        )

        st.stop()

    # ========================================================
    # 6. REPORT GENERATION
    # ========================================================

    st.markdown(
        "### 📝 6. Report Generation Agent"
    )

    report_agent = ReportGenerationAgent(
        model=model
    )

    try:

        report = report_agent.generate(
            topic,
            analysis,
            fact_check,
            sources,
            progress_callback=update_ui
        )

        st.session_state.report = report

        agent_status["Report Generator"] = "✅ Completed"

        progress_bar.progress(100)

        st.success(
            "🎉 Research report generated successfully!"
        )

    except Exception as e:

        st.error(
            f"Report generation error: {e}"
        )

        st.stop()


# ============================================================
# RESULTS
# ============================================================

if st.session_state.report:

    st.divider()

    st.header("📊 Final Research Report")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📄 Report",
            "🔍 Fact Checking",
            "🌐 Sources",
            "🧠 Analysis"
        ]
    )

    # ========================================================
    # REPORT TAB
    # ========================================================

    with tab1:

        st.markdown(
            st.session_state.report
        )

        st.divider()

        st.download_button(
            label="⬇️ Download Research Report",
            data=st.session_state.report,
            file_name="research_report.md",
            mime="text/markdown"
        )

    # ========================================================
    # FACT CHECK TAB
    # ========================================================

    with tab2:

        st.subheader(
            "🔍 Fact-Checking Results"
        )

        if st.session_state.fact_check:

            st.markdown(
                st.session_state.fact_check
            )

        else:

            st.info(
                "No fact-checking information available."
            )

    # ========================================================
    # SOURCES TAB
    # ========================================================

    with tab3:

        st.subheader(
            "🌐 Research Sources"
        )

        for source in st.session_state.sources:

            with st.expander(
                f"[{source['id']}] {source['title']}"
            ):

                st.write(
                    f"**URL:** {source['url']}"
                )

                if source.get("snippet"):

                    st.write(
                        source["snippet"]
                    )

                if source.get("content"):

                    st.write(
                        source["content"][:3000]
                    )

    # ========================================================
    # ANALYSIS TAB
    # ========================================================

    with tab4:

        st.subheader(
            "🧠 Analysis"
        )

        if st.session_state.analysis:

            st.markdown(
                st.session_state.analysis
            )

        else:

            st.info(
                "No analysis available."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Multi-Agent Autonomous Research System • "
    "Python + Streamlit + Ollama"
)