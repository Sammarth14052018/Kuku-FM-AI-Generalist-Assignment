"""Streamlit interface for the LexAI legal research workspace."""

import logging
import sys

import streamlit as st

from research import DISCLAIMER, EXAMPLES, MAX_QUESTION_LENGTH, Answer, demo_answer


@st.cache_resource(show_spinner=False)
def get_live_engine():
    from providers import live_research

    return live_research()


def choose_example(example: str):
    st.session_state.question = example
    st.session_state.sample_question = example


def render_sources(result: Answer | None):
    sources = result.sources if result else ()
    research_leads = result and result.status == "insufficient" and any(not source.page for source in sources)
    st.subheader("Research leads" if research_leads else "Evidence", anchor=False)
    st.caption(f"{len(sources)} {'source' if len(sources) == 1 else 'sources'}")

    if not sources:
        st.write("No supporting sources were found." if result else "Sources will appear here after you ask a question.")
        return

    if research_leads:
        st.caption("These search results point to official resources for further reading.")

    for number, source in enumerate(sources, 1):
        with st.container(border=True):
            label = f"[{number}] {source.title}"
            if source.url and source.url.startswith("https://"):
                st.link_button(label, source.url)
            else:
                st.text(label)
            if source.page:
                provenance = f"PDF page {source.page}"
                if source.ocr:
                    provenance += " · OCR transcription"
                st.caption(provenance)
            st.text(source.excerpt)


def main():
    st.set_page_config(page_title="LexAI | Indian law research", page_icon="§", layout="wide")
    st.html("""
        <style>
        .stMainBlockContainer { max-width: 1160px; padding-top: 2.5rem; }
        h1 { font-family: Georgia, serif; font-weight: 500; letter-spacing: -.04em; }
        .stText, .stText div { white-space: pre-wrap; overflow-wrap: anywhere; }
        </style>
    """)

    live = "--live" in sys.argv[1:]
    heading, resources = st.columns([3, 1], vertical_alignment="bottom")
    with heading:
        st.caption("LexAI  /  " + ("Live research" if live else "Offline demo"))
        st.title("Research Indian law", anchor=False)
        st.write("Ask a question and review the sources behind the answer.")
    with resources:
        st.link_button("Browse India Code ↗", "https://indiacode.gov.in/")

    question_column, evidence_column = st.columns([1.65, 1], gap="medium")
    with question_column:
        with st.container(border=True):
            st.subheader("Ask a question", anchor=False)
            with st.form("research"):
                question = st.text_area(
                    "Your legal question",
                    key="question",
                    label_visibility="collapsed",
                    placeholder="What would you like to understand?",
                    max_chars=MAX_QUESTION_LENGTH,
                    height=120,
                    help="Leave out names, addresses, and other personal details.",
                )
                st.caption("Leave out names, addresses, and other personal details.")
                submitted = st.form_submit_button("Research", type="primary")

            with st.expander("Sample questions", expanded=not live):
                for index, example in enumerate(EXAMPLES):
                    st.button(example, key=f"sample_{index}", on_click=choose_example, args=(example,))

            sample = st.session_state.pop("sample_question", None)
            if submitted or sample:
                question = (sample or question).strip()
                st.session_state.pop("result", None)
                if not question:
                    st.warning("Enter a question to start your research.")
                else:
                    with st.spinner("Looking up sources…"):
                        try:
                            result = get_live_engine().answer(question) if live else demo_answer(question)
                        except Exception as exc:
                            logging.error("Research request failed (%s)", type(exc).__name__)
                            st.error("Live research is unavailable. Check the local provider configuration and try again.")
                        else:
                            st.session_state.result = result
                            st.session_state.answered_question = question

            result = st.session_state.get("result")
            if result:
                st.divider()
                st.subheader("Answer", anchor=False)
                st.text(st.session_state.answered_question)
                if result.status == "demo":
                    st.caption("Demo response")
                elif result.status == "insufficient":
                    st.caption("Insufficient evidence")
                st.text(result.text)

    with evidence_column:
        with st.container(border=True):
            render_sources(result)

    st.caption(DISCLAIMER)


if __name__ == "__main__":
    main()
