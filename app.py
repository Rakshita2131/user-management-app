import streamlit as st
import psycopg2
import os

# Database connection using environment variables
def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "userdb"),
        user=os.environ.get("DB_USER", "rakshita"),
        password=os.environ.get("DB_PASSWORD", "postgres"),
        port="5432"
    )

# Search user by username
def search_user(user_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_name = %s", (user_name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# Add new user to database
def add_user(card_id, user_name, company_name, department):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (card_id, user_name, company_name, department) VALUES (%s, %s, %s, %s)",
        (card_id, user_name, company_name, department)
    )
    conn.commit()
    cursor.close()
    conn.close()

# ---- UI ----
st.title("User Management App")

# ---- Section 1: Search User ----
st.header("Search User")
search_name = st.text_input("Enter Username to Search")

if st.button("Search"):
    if search_name.strip() == "":
        st.warning("Please enter a username to search.")
    else:
        user = search_user(search_name.strip())
        if user:
            st.session_state["user_found"] = True
            st.session_state["user_not_found"] = False
            st.session_state["searched_name"] = search_name.strip()
        else:
            st.session_state["user_found"] = False
            st.session_state["user_not_found"] = True
            st.session_state["searched_name"] = search_name.strip()

# Show user details if found
if st.session_state.get("user_found"):
    user = search_user(st.session_state["searched_name"])
    st.success("User found!")
    st.table({
        "Field": ["ID", "Card ID", "Username", "Company", "Department"],
        "Value": [user[0], user[1], user[2], user[3], user[4]]
    })

# Show Add User form only if user was NOT found
if st.session_state.get("user_not_found"):
    st.error(f"No user found with username '{st.session_state['searched_name']}'.")
    st.divider()
    st.header("Add New User")
    st.info("Fill in the details below to add this user.")

    card_id = st.text_input("Card ID")
    new_user_name = st.text_input("Username", value=st.session_state["searched_name"])
    company_name = st.text_input("Company Name")
    department = st.text_input("Team / Department")

    if st.button("Add User"):
        if card_id.strip() == "" or new_user_name.strip() == "":
            st.warning("Card ID and Username are required!")
        else:
            try:
                add_user(card_id.strip(), new_user_name.strip(), company_name.strip(), department.strip())
                st.success(f"User '{new_user_name}' added successfully!")
                st.session_state["user_not_found"] = False
            except Exception as e:
                st.error(f"Error: {e}")