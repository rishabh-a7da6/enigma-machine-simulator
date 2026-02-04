# How the Enigma Machine Works

The Enigma machine is an electromechanical rotor cipher machine famous for its use by Germany during World War II. It relies on a principle called **polyalphabetic substitution**, meaning the "alphabet" used to encrypt a letter changes with every single key press.

## The Signal Path

When you press a key on the Enigma keyboard (e.g., 'A'), an electrical signal follows this specific path:

1.  **Keyboard**: The key completes a circuit.
2.  **Plugboard (Steckerbrett)**: The signal passes through the plugboard, where it might be swapped with another letter (e.g., A <-> Z).
3.  **Entry Wheel**: Static interface into the rotors.
4.  **Rotors (Right -> Middle -> Left)**: The signal passes through three rotating wheels, each scrambling the letter.
5.  **Reflector (Umkehrwalze)**: The signal hits the reflector at the end, which performs a final swap and sends the signal **back** through the rotors.
6.  **Rotors (Left -> Middle -> Right)**: The signal returns through the rotors in reverse order, scrambled again.
7.  **Plugboard**: The signal passes through the plugboard one last time.
8.  **Output**: The final letter lights up on the lampboard.

## Key Components

### 1. The Plugboard (Steckerbrett)
The plugboard was the first and last stage of the encryption. It allowed operators to swap pairs of letters using cables.
- If 'A' is plugged to 'Z', an incoming 'A' becomes 'Z' before reaching the rotors.
- This added a huge number of possible settings (billions), making the machine much harder to brute-force than just using rotors alone.

### 2. The Rotors (Walzen)
The rotors are the heart of the machine. Each rotor is a wheel with 26 contacts on both sides, wired internally in a complex maze.
- **Scrambling**: If a signal enters at position 'A' on the right, it might exit at position 'J' on the left.
- **Rotation**: With every key press, the **Right Rotor** rotates one step (1/26th of a turn). This changes the electrical path for the *next* letter.
- **Stepping (The Odometer)**: Once the Right rotor completes a full turn, it "kicks" the Middle rotor forward. When the Middle rotor completes a turn, it kicks the Left rotor. 
    - *Note*: Enigma had a unique "double stepping" anomaly where the middle rotor could step twice in a row due to the mechanical pawl design.

#### Ring Setting (Ringstellung)
The "Ring Setting" allows the internal wiring core to be rotated relative to the alphabet ring on the outside.
- Changing the ring setting shifts the wiring.
- Crucially, it changes **where the turnover notch is** relative to the letters. This alters *when* the next rotor steps, completely changing the sequence of substitution alphabets.

### 3. The Reflector (Umkehrwalze)
The reflector is unique to the Enigma. It sits to the left of the rotors and has 13 wires connecting 26 contacts in pairs.
- **Reciprocity**: The reflector ensures that if `A` encrypts to `X`, then `X` will encrypt to `A` (given the same settings). This meant the machine could be used for both decoding and encoding without switching modes.
- **No Self-Encryption**: Because the reflector must send the signal back through a *different* wire, a letter can **never** encrypt to itself (A never becomes A). This was a major cryptographic weakness, used by Alan Turing and the Bletchley Park team to crack the code.

## The Daily Key
To communicate, both the sender and receiver had to set up their machines exactly the same way. The "Daily Key" consisted of:
1.  **Rotor Selection**: Which rotors (e.g., I, IV, II) are in the Left, Middle, and Right slots.
2.  **Ring Settings**: The offset for each rotor (e.g., 01, 15, 22).
3.  **Plugboard Connections**: Which pairs are swapped (e.g., AB, DH, CO...).
4.  **Initial Position**: The starting rotation of the rotors (e.g., Q, E, V). This was often chosen randomly for each message (and sent at the start).

## Example Flow
Imagine pressing 'A':
1.  **Plugboard**: A -> A (no plug).
2.  **Rotor 3 (Right)**: Takes 'A', scrambles it to 'C'.
3.  **Rotor 2 (Middle)**: Takes 'C', scrambles it to 'D'.
4.  **Rotor 1 (Left)**: Takes 'D', scrambles it to 'F'.
5.  **Reflector**: Takes 'F', swaps it to 'P'.
6.  **Rotor 1 (Inverse)**: Takes 'P', scrambles it back to 'S'.
7.  **Rotor 2 (Inverse)**: Takes 'S', scrambles it back to 'E'.
8.  **Rotor 3 (Inverse)**: Takes 'E', scrambles it back to 'Q'.
9.  **Plugboard**: Q -> L (plugged).
10. **Result**: 'L' lights up.

Next press? The Right rotor moves, changing the whole path!
