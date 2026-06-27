# Barcode-Checkdigit-Puzzle
A python base game where a 12 digit UPC barcode is generated and one digit is removed and the player has to use barcode fallback logic to find the missing number.
Try it:
https://barcode-checkdigit-puzzle-psp2chtca8t3d9d7vfjngc.streamlit.app/

# Barcode Fallback Protocol Simulator

An interactive puzzle game and educational tool built using **Python 3.9** and **Streamlit**. This application simulates a retail terminal fallback system, challenging players to manually calculate and recover missing digits from damaged barcode sequences using real-world manufacturing logic.

Built as an official software entry for the **Hack Club Stardance Challenge** under handle `@chandos4473`.

---

## How It Works (The Engineering Logic)

Standard retail **UPC-A barcodes are exactly 12 digits long**. They are not random sequences; they operate on a strict mathematical **Modulo-10 Checksum Algorithm** to prevent scanning errors and manual key-in typos:

1. **The System Data (Digits 1–11):** The first 11 digits contain the manufacturer identity and item tracking codes.
2. **The Check Digit (Digit 12):** The final 12th digit is a mathematical anchor. A scanner adds up the weighted sums of the first 11 numbers—if the final total doesn't match the check digit, the system instantly flags a misread.

### The Fallback Protocol Formula
When a barcode is physically scratched or a laser scanner breaks, cashiers use the **Fallback Protocol** to key the numbers in by hand. The validation engine checks the entries using this sequence:
* Sum all digits in the **odd positions** (1st, 3rd, 5th, 7th, 9th, 11th) and multiply that sum by **3**.
* Sum all digits in the **even positions** (2nd, 4th, 6th, 8th, 10th).
* Add those two totals together to find the Grand Total.
* The **Check Digit** is the exact number required to bring that Grand Total up to the very next multiple of 10.

---

## Current Architecture (Chunk 1 Milestone)

The codebase is currently built out through the initial structural foundation phase:
- **Framework Initialization:** Configures the Streamlit wide-screen user viewport canvas.
- **Persistent State Memory:** Utilizes `st.session_state` memory blocks to generate a random 11-digit baseline array and safely freeze it on the screen so it doesn't re-randomize when the player interacts with buttons.
- **Dynamic Variable Blinding:** Selects a random index coordinate across the string array and hides it from the player viewport to establish the puzzle slot.

---

## Local Installation & Execution

1. Clone this repository to your machine.
2. Open a terminal inside the project workspace directory and install the necessary dependencies:
   ```bash
   pip install streamlit numpy
   ```
3. Boot up the local interactive web host server:
   ```bash
   python -m streamlit run "Barcode Game.py"
   ```

---

## Build Status & Project Checklist

- [x] Configure persistent `st.session_state` memory engines to store active game data
- [x] Build random array generation loops for the core 11 barcode digit slots
- [x] Integrate a dynamic coordinate index blinder to hide a variable slot from the canvas
- [x] Code the weighted Modulo-10 odd/even checksum math validation array
- [x] Format clean, non-stacking puzzle interface strings displaying the hidden `❓` slot
- [x] Connect interactive numerical input boxes and click-event submission buttons
- [x] Implement responsive score tracking states (+10 points per successful verification)
- [x] Inject automatic system re-runs to serve up fresh puzzle sequences upon local victory
- [x] Implement variable scores for guessing on 1st/2nd/3rd try
