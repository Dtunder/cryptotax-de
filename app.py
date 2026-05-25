import streamlit as st
import pandas as pd
from datetime import datetime
from src.trade_importer import parse_trades
from src.tax_calculator import calculate_gains
from src.report_generator import generate_pdf
import tempfile
import os

st.title("CryptoTax-DE MVP")
st.subheader("German §23 EStG crypto tax report generator")

st.markdown("""
    **Rules:**
    - Strict FIFO matching per asset.
    - Crypto held > 365 days is tax-free (*steuerfrei*).
    - Partial lots are handled correctly.
""")

uploaded_file = st.file_uploader("Upload Binance/Bybit CSV file", type=["csv"])

if uploaded_file is not None:
    # 1. Parse Trades
    st.write("### Parsing Trades...")
    try:
        trades = parse_trades(uploaded_file)
        st.write(f"Successfully loaded {len(trades)} valid trades.")

        # 2. Calculate Gains
        tax_events = calculate_gains(trades)

        if tax_events:
            st.write("### Taxable Events")

            df_events = pd.DataFrame(tax_events)
            st.dataframe(df_events)

            # Metrics
            total_gain = sum(e['gain_eur'] for e in tax_events)
            total_taxable_gain = sum(e['gain_eur'] for e in tax_events if e['taxable'])

            col1, col2 = st.columns(2)
            col1.metric("Total Gain", f"{total_gain:.2f} EUR")
            col2.metric("Taxable Gain (>365 days excluded)", f"{total_taxable_gain:.2f} EUR")

            # 3. Generate PDF Report
            st.write("### Export Report")
            tax_year = datetime.now().year - 1 # Default to last year
            year_input = st.number_input("Tax Year", min_value=2010, max_value=2050, value=tax_year)

            # Generate the PDF in memory / temp file first to provide a direct download button
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                output_path = tmp.name

            generate_pdf(tax_events, year_input, output_path)

            with open(output_path, "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name=f"cryptotax_{year_input}.pdf",
                mime="application/pdf"
            )

            # Cleanup temp file
            os.remove(output_path)
        else:
            st.write("No taxable events found from the uploaded trades.")

    except Exception as e:
        st.error(f"Error processing file: {e}")
