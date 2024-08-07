import streamlit as st
import requests
import os

st.title("Receipt Management and Expense Tracking")

st.header("Upload Receipt")
uploaded_file = st.file_uploader("Choose a receipt image...", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    file_path = f"./uploads/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    files = {'file': open(file_path, 'rb')}
    response = requests.post('http://localhost:5000/upload', files=files)
    receipt_info = response.json()
    
    st.success("Receipt uploaded and analyzed successfully!")
    st.json(receipt_info)

st.header("Monthly Expense Report")
month = st.selectbox("Month", [f"{i:02}" for i in range(1, 13)])
year = st.selectbox("Year", [str(i) for i in range(2020, 2025)])

if st.button("Generate Report"):
    params = {'month': month, 'year': year}
    response = requests.get('http://localhost:5000/report', params=params)
    report_data = response.json()
    
    st.write(f"Total Expense for {month}/{year}: ${report_data['total_expense']}")
    st.write(report_data['expense_by_merchant'])
    
    st.image(report_data['report_image'], caption=f'Expense Report for {month}/{year}')
