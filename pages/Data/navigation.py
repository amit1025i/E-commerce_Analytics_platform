import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.markdown(
            """
            <div style="
                font-size:24px;
                font-weight:700;
                margin-bottom:5px;
                color:#111827;
            ">
                🛒 E-Commerce
            </div>

            <div style="
                font-size:14px;
                color:#6b7280;
                margin-bottom:25px;
            ">
                Analytics Platform
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.markdown(
            """
            <div style="
                font-size:16px;
                font-weight:600;
                color:#111827;
                margin-bottom:12px;
            ">
                 Navigation
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "  Executive Dashboard",
            use_container_width=True
        ):
            st.switch_page("app.py")

        if st.button(
            "  Data Studio",
            use_container_width=True
        ):
            st.switch_page("pages/data_upload.py")

        if st.button(
            "  Sales Insights",
            use_container_width=True
        ):
            st.switch_page("pages/sales_analysis.py")

        if st.button(
            "  Profit Insights",
            use_container_width=True
        ):
            st.switch_page("pages/profit_analysis.py")

        if st.button(
            "  Customer Insights",
            use_container_width=True
        ):
            st.switch_page("pages/customer_analysis.py")

        if st.button(
            "  Sales vs Profit",
            use_container_width=True
        ):
            st.switch_page("pages/sales_vs_profit.py")

        if st.button(
            "  Data Explorer",
            use_container_width=True
        ):
            st.switch_page("pages/data_explorer.py")

        st.markdown("---")

        st.markdown(
            """
            <div style="
                font-size:16px;
                font-weight:600;
                color:#111827;
                margin-bottom:10px;
            ">
                ⚙️ Settings
            </div>
            """,
            unsafe_allow_html=True
        )

        show_advanced = st.checkbox(
            "Show advanced metrics"
        )

        st.markdown("---")

        st.markdown(
            """
            <div style="
                font-size:12px;
                color:#6b7280;
            ">
                E-Commerce Analytics v1.0
            </div>
            """,
            unsafe_allow_html=True
        )

    return show_advanced