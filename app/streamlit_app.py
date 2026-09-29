import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from services.research import run_research


st.set_page_config(
    page_title="Stock Intelligence",
    page_icon="📈",
    layout="wide",
)


st.title("📈 Stock Intelligence")
st.caption(
    "AI-powered financial research and market intelligence"
)


query = st.text_input(
    "Research a stock",
    placeholder="AAPL, NVIDIA, or 'Why did NVDA fall today?'",
)


if st.button("Research", type="primary"):

    if not query.strip():
        st.warning("Please enter a stock or research question.")
        st.stop()

    with st.spinner("Researching..."):

        try:
            result = run_research(query)

        except Exception as e:
            st.error(f"Research failed: {e}")
            st.stop()


    company = result.company

    if company is None:
        st.error("Could not resolve the company.")
        st.stop()


    st.header(
        f"{company.company_name} ({company.ticker})"
    )

    st.caption(
        f"{company.exchange} · {company.country}"
    )


    if result.market_data:

        market = result.market_data

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Price",
            f"${market.price:,.2f}",
        )

        col2.metric(
            "Change",
            f"{market.percent_change:.2f}%",
        )

        col3.metric(
            "Volume",
            f"{market.volume:,}",
        )
    if result.movement_analysis:

        movement = result.movement_analysis

        st.divider()

        st.header("📊 Market Movement Analysis")

        st.write(movement.answer)

        if movement.contributing_factors:

            st.subheader("Contributing Factors")

            for factor in movement.contributing_factors:
                st.markdown(f"- {factor}")


        if movement.supporting_evidence:

            st.subheader("Supporting Evidence")

            for evidence in movement.supporting_evidence:
                st.markdown(f"- {evidence}")


        if movement.uncertainties:

            st.subheader("Uncertainties")

            for uncertainty in movement.uncertainties:
                st.markdown(f"- {uncertainty}")


        if movement.sources:

            st.subheader("Sources")

            for source in movement.sources:
                st.markdown(f"- {source}")


    if result.perspective:

        perspective = result.perspective

        st.subheader("🤖 AI Investment Perspective")

        view = perspective.overall_view.value.replace(
            "_", " "
        ).upper()

        st.info(
            f"**Overall View: {view}**  \n"
            f"Confidence: {perspective.confidence:.0%}"
        )

        st.write(perspective.reasoning)


        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Positive Factors")

            for factor in perspective.positive_factors:
                st.markdown(f"- {factor}")


        with col2:
            st.markdown("### Negative Factors")

            if perspective.negative_factors:
                for factor in perspective.negative_factors:
                    st.markdown(f"- {factor}")
            else:
                st.write("No clearly supported negative factors.")


        st.markdown("### Key Risks")

        for risk in perspective.key_risks:
            st.markdown(f"- {risk}")


        st.markdown("### Uncertainties")

        for uncertainty in perspective.key_uncertainties:
            st.markdown(f"- {uncertainty}")


        st.markdown("### Catalysts to Watch")

        for catalyst in perspective.catalysts_to_watch:
            st.markdown(f"- {catalyst}")


    if result.report:

        report = result.report

        st.divider()

        st.header("Research Report")

        st.subheader("Executive Summary")
        st.write(report.executive_summary)

        st.subheader("Market Snapshot")
        st.write(report.market_snapshot)


        st.subheader("Recent Developments")

        for development in report.recent_developments:
            st.markdown(f"- {development}")


        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Positive Factors")

            for factor in report.positive_factors:
                st.markdown(f"- {factor}")


        with col2:

            st.subheader("Negative Factors")

            if report.negative_factors:

                for factor in report.negative_factors:
                    st.markdown(f"- {factor}")

            else:
                st.write("None identified.")


        st.subheader("Uncertainties")

        for uncertainty in report.uncertainties:
            st.markdown(f"- {uncertainty}")


        st.subheader("Key Claims")

        for claim in report.key_claims:
            st.markdown(f"- {claim}")


        st.subheader("Sources")

        for source in report.sources:
            st.markdown(f"- {source}")