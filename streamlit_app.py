"""
This program stores users' phone numbers
Converted from Tkinter to Streamlit
"""

import sqlite3
import streamlit as st

# --------------------------
# Database Setup
# --------------------------
conn = sqlite3.connect("phonelist.db", check_same_thread=False)
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS contact(
    firstname VARCHAR(20),
    lastname VARCHAR(20),
    email VARCHAR(100),
    phonenumber VARCHAR(20) PRIMARY KEY,
    address TEXT, 
    organization VARCHAR(100),
    notes TEXT, 
    mygroup VARCHAR(125), 
    age INTEGER,
    birthday DATE, 
    worknumber VARCHAR(20),
    pronouns VARCHAR(20), 
    nickname VARCHAR(10),
    website TEXT
)
''')
conn.commit()

# --------------------------
# Helper Functions
# --------------------------

def add_contact(data):
    try:
        cur.execute("INSERT OR REPLACE INTO contact VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
        conn.commit()
        st.success(f"Contact {data[0]} {data[1]} added/updated successfully!")
    except Exception as e:
        st.error(f"Error: {e}")

def get_all_contacts():
    cur.execute("SELECT firstname, lastname, phonenumber FROM contact")
    return cur.fetchall()

def get_contact(phone):
    cur.execute("SELECT * FROM contact WHERE phonenumber = ?", (phone,))
    return cur.fetchone()

def delete_contact(phone):
    cur.execute("DELETE FROM contact WHERE phonenumber = ?", (phone,))
    conn.commit()
    st.warning(f"Contact with phone {phone} deleted.")

def update_contact(data, phone):
    cur.execute(''' UPDATE contact SET firstname=?, lastname=?, email=?, phonenumber=?, 
                address=?, organization=?, notes=?, mygroup=?, age=?, birthday=?, 
                worknumber=?, pronouns=?, nickname=?, website=? WHERE phonenumber=? ''',
                data + [phone])
    conn.commit()
    st.success("Contact updated successfully!")

# --------------------------
# Streamlit App
# --------------------------

st.title("📒 My Contacts App ")

menu = ["Home", "View All", "Add Contact", "Find Contact"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Welcome to the Contacts App")
    st.write("Use the sidebar to navigate.")

elif choice == "Add Contact":
    st.subheader("➕ Add a New Contact")

    with st.form("add_form"):
        firstname = st.text_input("First Name")
        lastname = st.text_input("Last Name")
        email = st.text_input("Email")
        phonenumber = st.text_input("Phone Number")
        address = st.text_area("Home Address")
        organization = st.text_input("Organization")
        notes = st.text_area("Notes")
        mygroup = st.text_input("Group")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        birthday = st.date_input("Birthday")
        worknumber = st.text_input("Work Number")
        pronouns = st.text_input("Pronouns")
        nickname = st.text_input("Nickname")
        website = st.text_input("Website")

        submitted = st.form_submit_button("Save Contact")
        if submitted:
            data = [firstname, lastname, email, phonenumber, address, organization, notes,
                    mygroup, age, str(birthday), worknumber, pronouns, nickname, website]
            add_contact(data)

elif choice == "Find Contact":
    st.subheader("🔍 Find a Contact")
    phone = st.text_input("Enter Phone Number")
    if st.button("Search"):
        contact = get_contact(phone)
        if contact:
            labels = ["First Name", "Last Name", "Email", "Phone Number", "Address",
                      "Organization", "Notes", "Group", "Age", "Birthday",
                      "Work Number", "Pronouns", "Nickname", "Website"]
            st.table({labels[i]: [contact[i]] for i in range(len(labels))})

            if st.button("Delete Contact"):
                delete_contact(phone)

        else:
            st.error("No contact found.")

elif choice == "View All":
    st.subheader("📋 All Contacts")
    contacts = get_all_contacts()
    if contacts:
        st.table(contacts)
    else:
        st.info("No contacts available. Add one from the menu.")
