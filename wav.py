import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import base64

class WaveformEncoder:
    def __init__(self, dimensions=4):
        self.dimensions = dimensions
        self.base_frequency = np.pi/8
        
    def char_to_waveforms(self, char):
        """Convert a character to multiple encoding dimensions"""
        ascii_val = ord(char)
        # Create different encodings for the same character
        waves = []
        
        # Sinusoidal encoding (amplitude varies with ascii value)
        t = np.linspace(0, 2*np.pi, 50)
        sin_wave = (ascii_val / 255) * np.sin(t)
        waves.append(sin_wave)
        
        # Frequency encoding
        freq_wave = np.sin(ascii_val/32 * t)
        waves.append(freq_wave)
        
        # Phase encoding
        phase = ascii_val / 255 * 2*np.pi
        phase_wave = np.sin(t + phase)
        waves.append(phase_wave)
        
        # Polynomial encoding
        poly_wave = ((ascii_val/255) * t/np.pi) ** 2
        waves.append(poly_wave)
        
        return waves
    
    def encode_string(self, text):
        """Encode a string into a multi-dimensional waveform"""
        encoded = []
        for char in text:
            encoded.extend(self.char_to_waveforms(char))
        return np.array(encoded)
    
    def visualize(self, text, output_file='encoded_data.png'):
        """Create a visual representation of the encoded data"""
        encoded_data = self.encode_string(text)
        num_waves = len(encoded_data)
        
        # Create a figure with a specific size
        plt.figure(figsize=(10, num_waves/2))
        
        # Plot each waveform in its own row
        for i, wave in enumerate(encoded_data):
            plt.subplot(num_waves, 1, i+1)
            plt.plot(wave, 'b-', linewidth=0.5)
            plt.axis('off')
            
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        # Calculate theoretical data density
        image_size = os.path.getsize(output_file)  # in bytes
        data_length = len(text)  # in characters
        density = data_length / image_size
        
        return density

# Example usage
encoder = WaveformEncoder()
text = "Hello, World!"
density = encoder.visualize(text)
print(f"Data density: {density:.6f} characters per byte")

# Function to add error correction
def add_error_correction(waveform, redundancy=0.1):
    """Add error correction by introducing controlled redundancy"""
    # Add checksum waves
    checksum = np.sum(waveform, axis=0)
    # Add parity waves
    parity = np.mod(waveform, 2)
    
    # Combine original data with error correction
    protected_data = np.vstack([waveform, checksum, parity])
    return protected_data
