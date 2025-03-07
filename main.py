import streamlit as st
import re
import string
import random

# Set page layout
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="centered")

# Apply dark mode styling
st.markdown(
    """
    <style>
    /* Set full app background color */
    body, .stApp {
        background-color: #121212 !important;
        color: white !important;
    }

    /* Style input fields */
    .stTextInput>div>div>input {
        border: 2px solid #ffcc00;
        border-radius: 8px;
        padding: 10px;
        background-color: #1e1e1e;
        color: white !important;
    }

    /* Ensure placeholder text is white */
    .stTextInput>label {
        color: white !important;
    }

    .stTextInput>div>div>input::placeholder {
        color: white !important;
        opacity: 1 !important;
    }
    
    /* Style buttons */
    .stButton>button {
        background: linear-gradient(90deg, #ffcc00, #ff8800);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 15px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #ff8800, #ff4400);
    }
    
    /* Change text color */
    .stMarkdown, .stTitle, .stSubheader, .stText , .stTextInput {
        color: white !important;
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔐 Password Strength Meter")
st.subheader("🔎 **Check your password security**")

st.markdown(
    """
    <h4>✅ **Password Strength Criteria**</h4>
    <ul>
        <li>At least <strong>8 characters</strong> long</li>
        <li>Includes <strong>uppercase & lowercase</strong> letters</li>
        <li>Contains at least <strong>one number (0-9)</strong></li>
        <li>Has at least <strong>one special character (!@#$%^&*)</strong></li>
    </ul>
    """,
    unsafe_allow_html=True,
)

common_passwords = ["password", "123456", "qwerty", "admin", "letmein", "abc123", "iloveyou"]

def password_checker(password):
    score = 0
    feedback = []  

    if password.lower() in common_passwords:
        st.error("❌ This password is too common. Please choose a stronger one.")
        return 0, feedback  

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password must be at least **8 characters long**.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include **both uppercase and lowercase letters**.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least **one number (0-9).**")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least **one special character (!@#$%^&*).**")

    return score, feedback

password = st.text_input("🔑 Enter a password:", type="password", placeholder="Type your password here...")

if st.button("🔍 Check Password"):
    if password:
        score, feedback = password_checker(password)

        if feedback:
            for issue in feedback:
                st.warning(issue)

        if score >= 4:
            st.success("✅ **Strong Password!** 🟢")
        elif score == 3:
            st.warning("⚠️ **Moderate Password** - Consider making it stronger. 🟠")
        else:
            st.error("❌ **Weak Password** - Improve it using the suggestions above. 🔴")
    else:
        st.warning("⚠️ Please enter a password to check.")

def generate_strong_password():
    length = 12
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        score, _ = password_checker(password)
        if score >= 4:
            return password

if st.button("⚡ Suggest Strong Password"):
    strong_password = generate_strong_password()
    st.success("🔑 **Suggested Strong Password:**")
    st.code(strong_password, language="bash")  

if st.button("📌 Save & Generate Password"):
    if password:
        score, _ = password_checker(password)
        if score >= 4:
            st.success(f"🔑 **Your Saved Password:** `{password}`")
        else:
            st.warning("⚠️ Strengthen your password before saving.")
    else:
        st.warning("⚠️ Please enter a password to save.")
