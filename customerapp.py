import streamlit as st
import csv
from datetime import date
import os

FILENAME = "customers.csv"

st.title("🧾 Customer Info Tracker")

# --- Section: Add a New Customer ---
st.header("➕ Add Customer Details")

name = st.text_input("Customer Name")
phone = st.text_input("Phone Number")
amount_paid = st.number_input("Amount Paid (₹)", min_value=0.0, step=0.01)
last_date = st.date_input("Last Date Attended", date.today())
help_with = st.text_area("What did you help the customer with?")
resources = st.text_input("Resources used")

if st.button("Add Customer"):
    if name and phone:
        file_exists = os.path.exists(FILENAME)
        with open(FILENAME, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Name", "Phone", "Amount Paid", "Last Date", "Helped With", "Resources"])
            writer.writerow([name, phone, amount_paid, last_date, help_with, resources])
        st.success(f"✅ Customer '{name}' added successfully!")
    else:
        st.warning("⚠️ Please enter both Name and Phone Number.")


# --- Helper Function ---
def read_customers():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as file:
        return list(csv.DictReader(file))


def write_customers(customers):
    with open(FILENAME, "w", newline="") as file:
        writer = csv.DictWriter(file,
                                fieldnames=["Name", "Phone", "Amount Paid", "Last Date", "Helped With", "Resources"])
        writer.writeheader()
        writer.writerows(customers)


# --- Section: Search Customer ---
st.header("🔍 Search or Edit Customer")

search_query = st.text_input("Enter Name or Phone Number to Search")

if st.button("Search"):
    customers = read_customers()
    found = [c for c in customers if search_query.lower() in c["Name"].lower() or search_query in c["Phone"]]

    if not found:
        st.error("❌ No matching customer found.")
    else:
        for i, c in enumerate(found):
            st.subheader(f"Result #{i + 1}")
            st.write(f"**Name:** {c['Name']}")
            st.write(f"**Phone:** {c['Phone']}")
            st.write(f"**Amount Paid:** ₹{c['Amount Paid']}")
            st.write(f"**Last Date:** {c['Last Date']}")
            st.write(f"**Helped With:** {c['Helped With']}")
            st.write(f"**Resources:** {c['Resources']}")
            st.markdown("---")

            # --- Edit Section ---
            with st.expander(f"✏️ Edit Record for {c['Name']}"):
                new_name = st.text_input(f"New Name (currently {c['Name']})", c["Name"], key=f"name_{i}")
                new_phone = st.text_input(f"New Phone (currently {c['Phone']})", c["Phone"], key=f"phone_{i}")
                new_amount = st.number_input(f"New Amount Paid (currently ₹{c['Amount Paid']})",
                                             value=float(c["Amount Paid"]), step=0.01, key=f"amt_{i}")
                new_date = st.date_input(f"New Last Date (currently {c['Last Date']})",
                                         date.fromisoformat(c["Last Date"]), key=f"date_{i}")
                new_help = st.text_area("What did you help with?", c["Helped With"], key=f"help_{i}")
                new_resources = st.text_input("Resources used", c["Resources"], key=f"res_{i}")

                if st.button(f"💾 Save Changes for {c['Name']}", key=f"save_{i}"):
                    # Update record
                    for cust in customers:
                        if cust["Phone"] == c["Phone"]:
                            cust.update({
                                "Name": new_name,
                                "Phone": new_phone,
                                "Amount Paid": str(new_amount),
                                "Last Date": str(new_date),
                                "Helped With": new_help,
                                "Resources": new_resources
                            })
                            write_customers(customers)
                            st.success(f"✅ Record for {new_name} updated successfully!")
                            st.experimental_rerun()

# --- Section: View All Customers ---
st.header("📋 View All Customers")

if st.button("Show All Records"):
    customers = read_customers()
    if not customers:
        st.warning("No customer records found yet.")
    else:
        for row in customers:
            st.write(f"**Name:** {row['Name']}")
            st.write(f"**Phone:** {row['Phone']}")
            st.write(f"**Amount Paid:** ₹{row['Amount Paid']}")
            st.write(f"**Last Date:** {row['Last Date']}")
            st.write(f"**Helped With:** {row['Helped With']}")
            st.write(f"**Resources:** {row['Resources']}")
            st.markdown("---")
