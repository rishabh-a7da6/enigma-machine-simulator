
from typing import List, Dict, Tuple

class Plugboard:
    """
    Represents the Enigma Plugboard (Steckerbrett).
    Swaps letters before they enter the rotors and after they exit.
    """
    def __init__(self, settings: List[Tuple[str, str]]):
        """
        Initialize the plugboard with a list of pairs to swap.
        Example: [('A', 'B'), ('C', 'D')] means A<->B and C<->D.
        """
        self.mapping = {chr(i): chr(i) for i in range(65, 91)}
        for a, b in settings:
            a, b = a.upper(), b.upper()
            self.mapping[a] = b
            self.mapping[b] = a

    def forward(self, char: str) -> str:
        return self.mapping.get(char, char)


class Reflector:
    """
    Represents the Reflector (Umkehrwalze).
    Reflects the signal back through the rotors.
    """
    def __init__(self, wiring: str, name: str):
        self.wiring = wiring
        self.name = name

    def forward(self, char: str) -> str:
        encoded_index = ord(char) - 65
        return self.wiring[encoded_index]


class Rotor:
    """
    Represents an Enigma Rotor.
    Handles internal wiring, rotation, and ring settings.
    """
    def __init__(self, wiring: str, notch: str, name: str, ring_setting: int = 1, position: str = 'A'):
        self.wiring = wiring
        self.notch = notch
        self.name = name
        self.ring_setting = ring_setting  # 1-26 (translates to 0-25 offset)
        self.position = ord(position.upper()) - 65
        
        # Create inverse wiring for the return path
        self.inverse_wiring = [''] * 26
        for i, char in enumerate(self.wiring):
            self.inverse_wiring[ord(char) - 65] = chr(i + 65)
        self.inverse_wiring = ''.join(self.inverse_wiring)

    def step(self):
        """Rotate the rotor by one position."""
        self.position = (self.position + 1) % 26

    def is_at_notch(self) -> bool:
        """Check if the rotor is currently at its notch position."""
        # Notch is the character visible in window when turnover happens.
        # Logic: If current position matches the notch letter.
        current_char = chr(self.position + 65)
        return current_char in self.notch

    def forward(self, char: str) -> str:
        """
        Signal passes right to left (entering).
        Calculation: 
        1. Apply offset (position - ring_setting).
        2. Map through wiring.
        3. Remove offset.
        """
        offset = self.position - (self.ring_setting - 1)
        
        # Enter rotor (add offset)
        input_index = (ord(char) - 65 + offset) % 26
        
        # Pass through wiring
        output_char = self.wiring[input_index]
        
        # Exit rotor (subtract offset)
        output_index = (ord(output_char) - 65 - offset) % 26
        
        return chr(output_index + 65)

    def backward(self, char: str) -> str:
        """
        Signal passes left to right (returning).
        """
        offset = self.position - (self.ring_setting - 1)
        
        # Enter rotor (add offset)
        input_index = (ord(char) - 65 + offset) % 26
        
        # Pass through inverse wiring
        output_char = self.inverse_wiring[input_index]
        
        # Exit rotor (subtract offset)
        output_index = (ord(output_char) - 65 - offset) % 26
        
        return chr(output_index + 65)

    def set_position(self, position: str):
        self.position = ord(position.upper()) - 65


class EnigmaMachine:
    """
    Represents the full Enigma Machine I (Wehrmacht/Heer).
    """
    def __init__(self, rotors: List[Rotor], reflector: Reflector, plugboard: Plugboard):
        """
        rotors: List[Rotor] - [Left, Middle, Right]
        """
        if len(rotors) != 3:
            raise ValueError("Enigma usually has 3 rotors.")
        self.rotors = rotors # [Left, Middle, Right]
        self.reflector = reflector
        self.plugboard = plugboard

    def press_key(self, char: str) -> str:
        if not char.isalpha():
            return char
        
        char = char.upper()
        
        # 1. Rotate Rotors (Stepping Mechanism)
        # Double stepping mechanic:
        # If Middle rotor is at notch, it turns over AND turns the Left rotor.
        # If the Right rotor is at notch, it turns over the Middle rotor.
        # Right rotor always steps.
        
        left, middle, right = self.rotors[0], self.rotors[1], self.rotors[2]
        
        middle_at_notch = middle.is_at_notch()
        right_at_notch = right.is_at_notch()
        
        if middle_at_notch:
            left.step()
            middle.step()
        elif right_at_notch:
            middle.step()
            
        right.step()
        
        # 2. Pass through Plugboard
        signal = self.plugboard.forward(char)
        
        # 3. Pass through Rotors (Right -> Middle -> Left)
        signal = right.forward(signal)
        signal = middle.forward(signal)
        signal = left.forward(signal)
        
        # 4. Pass through Reflector
        signal = self.reflector.forward(signal)
        
        # 5. Pass back through Rotors (Left -> Middle -> Right)
        signal = left.backward(signal)
        signal = middle.backward(signal)
        signal = right.backward(signal)
        
        # 6. Pass through Plugboard
        signal = self.plugboard.forward(signal)
        
        return signal

    def process_text(self, text: str) -> str:
        result = []
        for char in text:
            if char.isalpha():
                result.append(self.press_key(char))
            else:
                result.append(char)
        return "".join(result)


# Configurations
ROTOR_CONFIGS = {
    'I':   {'wiring': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'notch': 'Q', 'name': 'I'},
    'II':  {'wiring': 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'notch': 'E', 'name': 'II'},
    'III': {'wiring': 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'notch': 'V', 'name': 'III'},
    'IV':  {'wiring': 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'notch': 'J', 'name': 'IV'},
    'V':   {'wiring': 'VZBRGITYUPSDNHLXAWMJQOFECK', 'notch': 'Z', 'name': 'V'},
}

REFLECTOR_CONFIGS = {
    'B': {'wiring': 'YRUHQSLDPXNGOKMIEBFZCWVJAT', 'name': 'UKW-B'},
    'C': {'wiring': 'FVPJIAOYEDRZXWGCTKUQSBNMHL', 'name': 'UKW-C'},
}

def create_enigma(rotor_names: List[str], ring_settings: List[int], initial_positions: List[str], plugboard_pairs: List[Tuple[str, str]], reflector_name: str = 'B') -> EnigmaMachine:
    """
    Factory function to create an Enigma machine instance.
    rotor_names: e.g. ['I', 'II', 'III'] (Left to Right)
    ring_settings: e.g. [1, 1, 1] (Left to Right)
    initial_positions: e.g. ['A', 'A', 'A'] (Left to Right)
    """
    rotors = []
    for i in range(3):
        config = ROTOR_CONFIGS[rotor_names[i]]
        r = Rotor(
            wiring=config['wiring'],
            notch=config['notch'],
            name=config['name'],
            ring_setting=ring_settings[i],
            position=initial_positions[i]
        )
        rotors.append(r)
        
    ref_config = REFLECTOR_CONFIGS[reflector_name]
    reflector = Reflector(wiring=ref_config['wiring'], name=ref_config['name'])
    
    plugboard = Plugboard(plugboard_pairs)
    
    return EnigmaMachine(rotors, reflector, plugboard)
