
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Energy Dashboard: Solar & Heat Pump Sizing")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    electricity_df = pd.read_excel(xls, sheet_name='Electricity', skiprows=2)
    gas_df = pd.read_excel(xls, sheet_name='Gas', skiprows=2)

    electricity_df.columns = [
        "Index", "Date", "MPAN Consumption (kWh)", "Env Charges (kWh)", 
        "Energy Charge/KWh", "Energy Charge", "Energy Bill Relief", 
        "RO Obligation/KWh", "RO Obligation", "FiT/KWh", "FiT", 
        "Mutualisation", "DUoS Charges", "TUoS Charges", 
        "Metering Charge", "CFD & CM Charges", "TUoS Charge Rate", 
        "CCL Charge", "Total Monthly Charge", "Incl CCL Rate"
    ]
    gas_df.columns = [
        "Index", "Date", "Consumption (kWh)", "Cost/KWh", "Total Cost", 
        "Energy Bill Relief", "CCL Rate", "CCL Charge", "Standard Charge/Day", "Total Costs"
    ]

    st.subheader("Electricity Usage Summary")
    electricity_df["Date"] = pd.to_datetime(electricity_df["Date"])
    electricity_df["MPAN Consumption (kWh)"] = pd.to_numeric(electricity_df["MPAN Consumption (kWh)"], errors='coerce')
    monthly_electricity = electricity_df[["Date", "MPAN Consumption (kWh)"]].dropna()

    st.line_chart(monthly_electricity.set_index("Date"))

    st.subheader("Gas Usage Summary")
    gas_df["Date"] = pd.to_datetime(gas_df["Date"])
    gas_df["Consumption (kWh)"] = pd.to_numeric(gas_df["Consumption (kWh)"], errors='coerce')
    monthly_gas = gas_df[["Date", "Consumption (kWh)"]].dropna()

    st.line_chart(monthly_gas.set_index("Date"))

    st.subheader("Solar PV Sizing Tool")
    location = st.text_input("Enter location (for reference only)")
    roof_area = st.number_input("Roof Area (m²)", value=50.0)
    panel_efficiency = st.number_input("Panel Efficiency (%)", value=18.0)

    if roof_area > 0 and panel_efficiency > 0:
        kwp = (roof_area * (panel_efficiency / 100)) * 1.0
        yearly_generation = kwp * 950  # UK average ~950 kWh/kWp
        st.write(f"Estimated System Size: **{kwp:.2f} kWp**")
        st.write(f"Estimated Annual Generation: **{yearly_generation:.0f} kWh**")

    st.subheader("Heat Pump Sizing Tool")
    if not gas_df.empty:
        avg_gas = gas_df["Consumption (kWh)"].mean()
        heating_fraction = st.slider("Estimated % of gas used for heating", 0, 100, 70)
        cop = st.slider("Estimated COP (Coefficient of Performance)", 2, 5, 3)
        heat_demand = avg_gas * (heating_fraction / 100)
        required_elec = heat_demand / cop
        st.write(f"Estimated Annual Heat Demand: **{heat_demand:.0f} kWh**")
        st.write(f"Estimated Electric Consumption with Heat Pump: **{required_elec:.0f} kWh**")
