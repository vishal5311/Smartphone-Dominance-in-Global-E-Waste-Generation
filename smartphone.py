import os
os.system("pip install matplotlib")
import matplotlib.pyplot as plt

import streamlit as st


st.set_page_config(page_title="📱 Smartphone E-Waste Impact", layout="wide")
st.title("📱 Smartphone Dominance in Global E-Waste Generation")

st.markdown("""
Smartphones may not be the largest contributor to global e-waste by weight, but their **mass adoption rate**, **short lifecycle**, and **low recycling rate** make them one of the **fastest-growing sources of e-waste**.
""")

# Sample Data
years = [2023, 2024, 2025, 2026, 2027]
smartphone_e_waste =[13.2, 16.4, 19.7, 24.0, 27.3]  # million tons
total_e_waste = [53.6, 57.4, 62.0, 67.4, 73.0]

device_share = [27,33,25,15]
device_labels = ['Smartphones', 'Laptops/Tablets', 'TVs/Monitors', 'Others']
device_colors = ['#ff7f0e', '#1f77b4', '#2ca02c', '#d62728']

# Pie Chart: Contribution by Device Type
st.subheader("🌍 E-Waste Contribution by Device Type")
fig1, ax1 = plt.subplots()
ax1.pie(device_share, labels=device_labels, colors=device_colors, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio
st.pyplot(fig1)

# Bar Chart: Smartphone E-Waste Over Time
st.subheader("📈 Growth of Smartphone E-Waste (2023–2027)")
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.bar(years, smartphone_e_waste, color='#ff7f0e', label='Smartphones')
ax2.plot(years, total_e_waste, color='red', marker='o', linestyle='--', label='Total E-Waste')

ax2.set_xlabel("Year")
ax2.set_ylabel("E-Waste (Million Metric Tons)")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

# Key Insights
st.info("💡 **Insight for Judges**: Though smartphones only contribute ~8% of global e-waste, their short life cycle (~2 years), high replacement rate, and low recycling rate make them a critical focus for circular economy strategies.")
