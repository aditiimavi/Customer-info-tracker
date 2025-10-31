import streamlit as st
import csv
from datetime import date

FILENAME = r"C:\Users\Aditi Mavi\PycharmProjects\Projects real\Customer_app"


st.title("🧾 Customer Info Tracker")

# Input form
name = st.text_input("Customer Name")
last_date = st.date_input("Last Date Attended", date.today())
help_with = st.text_area("What did you help the customer with?")
resources = st.text_input("Resources used")

if st.button("Add Customer"):
    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, last_date, help_with, resources])
    st.success(f"Customer '{name}' added successfully!")

if st.button("View All Customers"):
    try:
        with open(FILENAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                st.write(f"**Name:** {row[0]}")
                st.write(f"**Last Date:** {row[1]}")
                st.write(f"**Helped With:** {row[2]}")
                st.write(f"**Resources:** {row[3]}")
                st.markdown("---")
    except FileNotFoundError:
        st.warning("No customer records found yet.")
