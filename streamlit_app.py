import streamlit as st
import pandas as pd

# --- 1. THE 2025 DATABASE (Updated with Pricing) ---
racquet_db = [
    {
        "name": "Wilson Blade 98 v9",
        "head_size": 98,
        "weight": 305,
        "category": "Control",
        "stiffness": "Medium",
        "price": 269,
        "description": "The gold standard for feel and control."
    },
    {
        "name": "Babolat Pure Drive Gen11",
        "head_size": 100,
        "weight": 300,
        "category": "Power",
        "stiffness": "High",
        "price": 259,
        "description": "Explosive power for aggressive baseliners."
    },
    {
        "name": "Head Speed MP 2025",
        "head_size": 100,
        "weight": 300,
        "category": "Spin",
        "stiffness": "Medium",
        "price": 269,
        "description": "Fast through the air, perfect for modern spin."
    },
    {
        "name": "Yonex EZONE 100 (2025 Update)",
        "head_size": 100,
        "weight": 300,
        "category": "Power",
        "stiffness": "Medium-High",
        "price": 259,
        "description": "A mix of plush feel and easy power."
    },
    {
        "name": "Wilson Clash 100 v3",
        "head_size": 100,
        "weight": 295,
        "category": "Comfort",
        "stiffness": "Low",
        "price": 299,
        "description": "The most arm-friendly frame on the market."
    },
    {
        "name": "Babolat Boost Drive (Budget Model)",
        "head_size": 105,
        "weight": 260,
        "category": "Power",
        "stiffness": "Medium",
        "price": 119,
        "description": "Great value frame for improving players."
    },
    {
        "name": "Head Ti.S6 (Classic)",
        "head_size": 115,
        "weight": 225,
        "category": "Power",
        "stiffness": "High",
        "price": 99,
        "description": "The ultimate budget power racquet."
    },
    {
        "name": "Artengo TR960 Control Tour",
        "head_size": 98,
        "weight": 305,
        "category": "Control",
        "stiffness": "Medium",
        "price": 140,
        "description": "High performance at half the price of big brands."
    }
]

# --- 2. SESSION STATE MANAGEMENT ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'answers' not in st.session_state:
    st.session_state.answers = {}

def next_step():
    st.session_state.step += 1

def reset_app():
    st.session_state.step = 1
    st.session_state.answers = {}

# --- 3. THE INTERFACE ---
st.set_page_config(page_title="Tennis Gear Pro", page_icon="🎾")
st.title("🎾 The Tennis Gear Pro")
st.markdown("**Your expert equipment consultant for the 2025 season.**")
st.markdown("---")

# Question 1: Experience
if st.session_state.step == 1:
    st.header("Step 1: Experience Level")
    experience = st.radio("How would you describe your level?", ["Beginner", "Intermediate", "Advanced/Competitive"])
    if st.button("Next"):
        st.session_state.answers['experience'] = experience
        next_step()
        st.rerun()

# Question 2: Physicality
elif st.session_state.step == 2:
    st.header("Step 2: Physical Build")
    physique = st.radio("What is your physical build?", ["High-strength/Athletic", "Average", "Junior/Senior"])
    if st.button("Next"):
        st.session_state.answers['physique'] = physique
        next_step()
        st.rerun()

# Question 3: Swing Style
elif st.session_state.step == 3:
    st.header("Step 3: Swing Style")
    swing = st.radio("Describe your swing mechanics:", 
                     ["Long, fast swing (I create my own power)", "Short, compact swing (I need help with power)"])
    if st.button("Next"):
        st.session_state.answers['swing'] = swing
        next_step()
        st.rerun()

# Question 4: Priority
elif st.session_state.step == 4:
    st.header("Step 4: Primary Goal")
    priority = st.radio("What is your #1 goal on court?", ["Power", "Control", "Spin", "Comfort/Arm-Protection"])
    if st.button("Next"):
        st.session_state.answers['priority'] = priority
        next_step()
        st.rerun()

# Question 5: Current Gear/Pain
elif st.session_state.step == 5:
    st.header("Step 5: Health & History")
    pain = st.radio("Do you have any wrist or elbow pain history?", ["Yes, frequently", "No, I am healthy"])
    if st.button("Next"):
        st.session_state.answers['pain'] = pain
        next_step()
        st.rerun()

# Question 6: Budget (NEW)
elif st.session_state.step == 6:
    st.header("Step 6: Budget")
    budget = st.radio("What is your preferred price range?", 
                      ["Under $150 (Value)", "$150 - $250 (Mid-Range)", "Over $250 (Premium/Pro)"])
    if st.button("Find My Racquet"):
        st.session_state.answers['budget'] = budget
        next_step()
        st.rerun()

# --- 4. RECOMMENDATION LOGIC ---
elif st.session_state.step == 7:
    answers = st.session_state.answers
    df = pd.DataFrame(racquet_db)
    filtered_df = df.copy()
    
    # Logic 1: Budget Filter
    if answers['budget'] == "Under $150 (Value)":
        filtered_df = filtered_df[filtered_df['price'] <= 150]
    elif answers['budget'] == "$150 - $250 (Mid-Range)":
        filtered_df = filtered_df[(filtered_df['price'] > 150) & (filtered_df['price'] <= 250)]
    # Note: If "Over $250", we keep everything over 250.
    
    # Logic 2: Injury Override
    if answers['pain'] == "Yes, frequently":
        # If injured, we relax budget constraints slightly to ensure safety, or prioritize low stiffness
        filtered_df = filtered_df[filtered_df['stiffness'].isin(["Low", "Medium"])]
        fit_reason = "Prioritizing arm health and comfort."
    
    # Logic 3: Playstyle
    elif "Short" in answers['swing'] or answers['priority'] == "Power":
        filtered_df = filtered_df[(filtered_df['head_size'] >= 100)]
        fit_reason = "Selected for easy power and larger sweet spot."
    elif "Long" in answers['swing'] or answers['priority'] == "Control":
        filtered_df = filtered_df[(filtered_df['head_size'] <= 100)]
        fit_reason = "Selected for precision and control."
    elif answers['priority'] == "Spin":
        filtered_df = filtered_df[filtered_df['category'] == "Spin"]
        fit_reason = "Selected for aerodynamic spin generation."
    else:
        fit_reason = "Selected based on your overall profile."

    # Fallback: If logic is too strict and returns empty, show best fit from original DB ignoring budget
    if filtered_df.empty:
        st.warning(f"No exact matches found for {answers['budget']} with these specs. Showing closest matches regardless of price.")
        filtered_df = df.head(3)

    # --- OUTPUT ---
    st.balloons()
    st.subheader("### Your Tennis DNA")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Swing:** {answers['swing'].split('(')[0]}")
        st.write(f"**Priority:** {answers['priority']}")
    with col2:
        st.write(f"**Budget:** {answers['budget']}")
    
    st.markdown("---")
    st.subheader("### Top Recommendations")
    
    for index, row in filtered_df.head(3).iterrows():
        st.markdown(f"#### 🎾 {row['name']}")
        st.caption(f"Price: ${row['price']}")
        st.write(f"**Why:** {fit_reason}")
        st.write(f"_{row['description']}_")
        st.markdown("---")

    if st.button("Start Over"):
        reset_app()
        st.rerun()
