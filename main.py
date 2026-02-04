import streamlit as st
from enigma import create_enigma, ROTOR_CONFIGS, REFLECTOR_CONFIGS

st.set_page_config(page_title="Enigma Machine Simulator", page_icon="🔐", layout="wide")

def main():
    st.title("🔐 Enigma Machine Simulator")
    st.markdown("""
    This is a fully functional simulator of the **Enigma I** (Wehrmacht/Heer) machine used during WWII.
    Configure the rotors, rings, and plugboard in the sidebar, then type your message below.
    """)

    # --- Sidebar Configuration ---
    st.sidebar.header("⚙️ Machine Settings")

    # Rotor Selection
    st.sidebar.subheader("Rotors")
    rotor_options = list(ROTOR_CONFIGS.keys())
    
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        rotor_l = st.selectbox("Left Rotor", rotor_options, index=0)
    with col2:
        rotor_m = st.selectbox("Middle Rotor", rotor_options, index=1)
    with col3:
        rotor_r = st.selectbox("Right Rotor", rotor_options, index=2)

    # Initial Rotor Positions
    st.sidebar.subheader("Initial Rotor Positions")
    pos_options = [chr(i) for i in range(65, 91)]
    
    col_p1, col_p2, col_p3 = st.sidebar.columns(3)
    with col_p1:
        pos_l = st.selectbox("Left Position", pos_options, index=0)
    with col_p2:
        pos_m = st.selectbox("Middle Position", pos_options, index=0)
    with col_p3:
        pos_r = st.selectbox("Right Position", pos_options, index=0)

    # Ring Settings
    st.sidebar.subheader("Ring Settings")
    ring_options = list(range(1, 27))
    
    col_rs1, col_rs2, col_rs3 = st.sidebar.columns(3)
    with col_rs1:
        ring_l = st.selectbox("Ring Left", ring_options, index=0)
    with col_rs2:
        ring_m = st.selectbox("Ring Middle", ring_options, index=0)
    with col_rs3:
        ring_r = st.selectbox("Ring Right", ring_options, index=0)

    # Reflector
    st.sidebar.subheader("Reflector")
    reflector = st.sidebar.selectbox("Reflector Type", list(REFLECTOR_CONFIGS.keys()), index=0)

    # Plugboard
    st.sidebar.subheader("Plugboard")
    st.sidebar.markdown("Enter pairs of letters to swap (e.g., `AB CD`). Max 13 pairs.")
    plugboard_input = st.sidebar.text_input("Plugboard Connections", value="").upper()

    # Process Plugboard Input
    plugboard_pairs = []
    if plugboard_input:
        cleaned = plugboard_input.replace(" ", "")
        if len(cleaned) % 2 != 0:
            st.sidebar.error("Plugboard settings must be in pairs.")
        else:
            # Check for duplicates
            seen = set()
            valid = True
            temp_pairs = []
            for i in range(0, len(cleaned), 2):
                pair = cleaned[i:i+2]
                if pair[0] == pair[1]:
                    st.sidebar.error(f"Cannot map letter to itself: {pair}")
                    valid = False
                    break
                if pair[0] in seen or pair[1] in seen:
                    st.sidebar.error(f"Letter used multiple times: {pair}")
                    valid = False
                    break
                seen.add(pair[0])
                seen.add(pair[1])
                temp_pairs.append((pair[0], pair[1]))
            
            if valid:
                plugboard_pairs = temp_pairs

    # --- Main Area ---
    
    # Input
    input_text = st.text_area("Input Message", height=150, help="Type your message here. Non-alphabetic characters will be preserved.")

    # Output
    if input_text:
        # Create Enigma Instance
        machine = create_enigma(
            rotor_names=[rotor_l, rotor_m, rotor_r],
            ring_settings=[ring_l, ring_m, ring_r],
            initial_positions=[pos_l, pos_m, pos_r],
            plugboard_pairs=plugboard_pairs,
            reflector_name=reflector
        )
        
        output_text = machine.process_text(input_text)
        
        st.subheader("Output")
        st.text_area("Encoded/Decoded Message", value=output_text, height=150, disabled=False)
        
        st.info("Note: To decode, copy the output text into the input box while keeping the SAME settings.")

if __name__ == "__main__":
    main()
