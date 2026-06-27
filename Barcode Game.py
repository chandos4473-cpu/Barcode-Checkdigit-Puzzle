import random
import streamlit as st

st.set_page_config(page_title="Barcode Fallback Protocol", layout="centered")
st.title("Barcode Fallback Protocol")
st.markdown("The scanner is broken! Use the barcode checksum formula to find the missing digit.")

if "score" not in st.session_state:
    st.session_state.score = 0
if "barcode" not in st.session_state:
    st.session_state.barcode = [random.randint(0,9) for _ in range(11)]
    st.session_state.hidden_idx = random.randint(0,10)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

digits = st.session_state.barcode
hidden_idx = st.session_state.hidden_idx

blind_digits = list(digits)
blind_digits[hidden_idx] = 0

blind_odd_sum = sum(blind_digits[i] for i in range(0,11,2)) * 3
blind_even_sum = sum(blind_digits[i] for i in range(1,11,2))
blind_total_sum = blind_odd_sum + blind_even_sum

true_odd_sum = sum(digits[i] for i in range(0,11,2)) * 3
true_even_sum = sum(digits[i] for i in range(1,11,2))
true_total_sum = true_odd_sum + true_even_sum

checkdig = true_total_sum % 10
if checkdig != 0:
    checkdig = 10 - checkdig
else:
    checkdig = 0

col_score, col_att = st.columns(2)
with col_score:
    st.subheader(f"Score: {st.session_state.score}")
with col_att:
    strikes = "🔴 " * st.session_state.attempts + "⚪ " * (3-st.session_state.attempts)
    st.subheader(f"Strikes: {strikes}")

display_list = []
for i in range(11):
    if i == hidden_idx:
        display_list.append("?")
    else:
        display_list.append(str(digits[i]))

display_string = "  ".join(display_list) + f"  |  [Check Digit: {checkdig}]"
st.info(f"### `{display_string}`")

with st.expander("? Need help? Reveal Modulo-10 checksum process"):
    st.markdown("### Live checksum calculation matrix (Treating missing slot as 0)")

    st.markdown("**1. Sum the digits in the 1st, 3rd, 5th, 7th, 9th, and 11th positions and multiply by 3:**")
    odd_breakdown = " + ".join([f"**{digits[i]}**" if i != hidden_idx else "0 (❓)" for i in range(0, 11, 2)])
    st.code(f"({odd_breakdown}) × 3 = {blind_odd_sum}")

    st.markdown("**2. Sum the digits in the 2nd, 4th, 6th, 8th, and 10th positions (do not multiply by 3):**")
    even_breakdown = " + ".join([f"**{digits[i]}**" if i != hidden_idx else "0 (❓)" for i in range(1, 11, 2)])
    st.code(f"{even_breakdown} = {blind_even_sum}")

    st.markdown("**3. Combined total:**")
    st.code(f"{blind_odd_sum} + {blind_even_sum} = {blind_total_sum}")

    st.markdown("**4. Modulo (mod(%)) the remainder:**")
    st.code(f"{blind_total_sum} % 10 = {blind_total_sum % 10}")

    st.markdown("**5. Final Complement Derivation:**")
    blind_remainder = blind_total_sum % 10
    blind_check = (10 - blind_remainder) % 10
    st.code(f"(10 - {blind_remainder}) % 10 = {blind_check}")
    
    st.markdown("---")
    st.markdown("### How to solve this layout using algebra:")
    st.markdown(f"Your goal is to bring the current total (**{blind_total_sum}**) up to a number where the final check digit matches **{checkdig}**.")
    
    if hidden_idx % 2 == 0:
        st.info(f"Since the missing number sits in an **ODD position** (Position #{hidden_idx + 1}), every 1 digit you add will increase the total by **3**!")
    else:
        st.info(f"Since the missing number sits in an **EVEN position** (Position #{hidden_idx + 1}), every 1 digit you add will increase the total by **1**!")

    st.markdown("Use these steps in reverse to find the missing digit on the next puzzle!")

st.markdown("---")

if not st.session_state.game_over:
    player_guess = st.number_input("Enter the missing digit (0-9):", min_value=0, max_value=9, step=1, key="guess_input")
    
    if st.button("Submit"):
        correct_answer = digits[hidden_idx]
        
        if player_guess == correct_answer:
            if st.session_state.attempts == 0:
                points = 10
                st.success("PERFECT SCAN! Protocol verified instantly (+10 pts)!")
            elif st.session_state.attempts == 1:
                points = 5
                st.success("SECOND ATTEMPT! Handshake stabilized (+5 pts)!")
            else:
                points = 1
                st.success("MANUAL OVERRIDE SUCCESS! System accepted entry (+1 pt)!")
                
            st.session_state.score += points
            st.session_state.attempts = 0
            st.session_state.barcode = [random.randint(0,9) for _ in range(11)]
            st.session_state.hidden_idx = random.randint(0,10)
            st.rerun()
            
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts >= 3:
                st.session_state.game_over = True
            st.rerun()
else:
    st.error(f"TERMINAL LOCKOUT! 3/3 Checksum Failures. The missing digit was: {digits[hidden_idx]}")
    
    if st.button("Initialize Next Puzzle Sequence"):
        st.session_state.game_over = False
        st.session_state.attempts = 0
        st.session_state.barcode = [random.randint(0,9) for _ in range(11)]
        st.session_state.hidden_idx = random.randint(0,10)
        st.rerun()
