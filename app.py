
import streamlit as st
from fpdf import FPDF
import base64

st.set_page_config(page_title="Propwealth Cashflow Calculator", layout="wide")
st.title("🏠 Propwealth Cashflow Calculator")

# Capture all user inputs
with st.expander("1️⃣ Property Purchase Details", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        address = st.text_input("Address", "1 Murtoa St Dallas")
        purchase_price = st.number_input("Purchase Price", value=550000)
        deposit = st.number_input("Deposit (20%)", value=110000)
    with col2:
        loan_amount = st.number_input("Loan Amount", value=440000)
        loan_interest_rate = st.number_input("Loan Interest Rate (%)", value=6.0)
        stamp_duty = st.number_input("Stamp Duty", value=0)
    with col3:
        lmi = st.number_input("LMI", value=0)
        legals = st.number_input("Legal Fees", value=2000)
        reno_cost = st.number_input("Renovation Cost", value=0)
        total_capital = deposit + stamp_duty + lmi + legals + reno_cost
        st.success(f"💰 Total Capital Required: ${total_capital:,.2f}")

with st.expander("2️⃣ Rental Yield & Income", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        low_rent = st.number_input("Low Rent ($/week)", value=350)
        low_yield = (low_rent * 52 / purchase_price) * 100
        st.metric("Yield (Low Rent)", f"{low_yield:.2f}%")
    with col2:
        high_rent = st.number_input("High Rent ($/week)", value=370)
        high_yield = (high_rent * 52 / purchase_price) * 100
        st.metric("Yield (High Rent)", f"{high_yield:.2f}%")

with st.expander("3️⃣ Expense Breakdown", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        council = st.number_input("Council Fees ($/week)", value=38.46)
        insurance = st.number_input("Insurance ($/week)", value=19.23)
    with col2:
        mgmt_fee_percent = st.number_input("Management Fee (%)", value=5.5)
        mgmt_fees = ((low_rent + high_rent) / 2) * (mgmt_fee_percent / 100)
        st.number_input("Management Fees ($/week)", value=mgmt_fees, step=1.0, format="%.2f", disabled=True)
        landlord_insurance = st.number_input("Landlord Insurance ($/week)", value=9.62)
    with col3:
        loan_repayment_weekly = ((loan_amount * (loan_interest_rate / 100)) / 12) / 4.33
        st.number_input("Loan Repayments ($/week)", value=loan_repayment_weekly, step=1.0, format="%.2f", disabled=True)

    total_expenses = council + insurance + mgmt_fees + landlord_insurance + loan_repayment_weekly
    st.warning(f"💸 Total Weekly Expenses: ${total_expenses:.2f}")

with st.expander("4️⃣ Estimated Cashflow", expanded=True):
    cashflow_low = low_rent - total_expenses
    cashflow_high = high_rent - total_expenses
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Weekly Cashflow (Low Rent)", f"${cashflow_low:.2f}")
    with col2:
        st.metric("Weekly Cashflow (High Rent)", f"${cashflow_high:.2f}")

with st.expander("5️⃣ Property Specifications", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        vacant_leased = st.text_input("Vacant / Leased", "Vacant")
        bedrooms = st.number_input("Bedrooms", value=3)
        bathrooms = st.number_input("Bathrooms", value=1)
    with col2:
        garages = st.number_input("Lock-up Garage / Carport", value=2)
        size = st.text_input("Size of Property", "588 sqm")
        age = st.number_input("Age of Property (Years)", value=50)
    with col3:
        construction_type = st.text_input("Construction Type", "Brick Veneer")
        units_in_block = st.text_input("# of Units in Block", "2")
        work_needed = st.text_area("Work Needed", "")

# Button to generate PDF
st.header("📄 Download Report")
if st.button("Generate PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Propwealth Cashflow Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Address: {address}", ln=True)
    pdf.cell(200, 10, txt=f"Purchase Price: ${purchase_price:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Loan Amount: ${loan_amount:,.2f} @ {loan_interest_rate:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"Deposit: ${deposit:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Stamp Duty: ${stamp_duty:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Renovation Cost: ${reno_cost:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Total Capital: ${total_capital:,.2f}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Low Rent: ${low_rent}/week - Yield: {low_yield:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"High Rent: ${high_rent}/week - Yield: {high_yield:.2f}%", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total Weekly Expenses: ${total_expenses:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Weekly Cashflow (Low): ${cashflow_low:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Weekly Cashflow (High): ${cashflow_high:.2f}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Vacant/Leased: {vacant_leased}", ln=True)
    pdf.cell(200, 10, txt=f"Bedrooms: {bedrooms}, Bathrooms: {bathrooms}, Garage: {garages}", ln=True)
    pdf.cell(200, 10, txt=f"Construction: {construction_type}, Age: {age} years", ln=True)
    pdf.cell(200, 10, txt=f"Size: {size}, Units: {units_in_block}", ln=True)
    if work_needed.strip():
        pdf.ln(5)
        pdf.multi_cell(0, 10, txt=f"Work Needed: {work_needed}")

    pdf_output = pdf.output(dest='S').encode('latin-1')
    b64 = base64.b64encode(pdf_output).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="Propwealth_Cashflow_Report.pdf">📥 Download your PDF</a>'
    st.markdown(href, unsafe_allow_html=True)
