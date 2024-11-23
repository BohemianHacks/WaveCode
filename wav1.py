import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import base64
import os

class WaveformEncoder:
    def __init__(self, dimensions=4, error_correction=True):
        self.dimensions = dimensions
        self.base_frequency = np.pi/8
        self.error_correction = error_correction
        self.color_map = plt.cm.viridis
        
    def char_to_waveforms(self, char):
        """Convert a character to multiple encoding dimensions with improved robustness"""
        ascii_val = ord(char)
        waves = []
        
        # Generate sample points
        t = np.linspace(0, 2*np.pi, 100)  # Increased resolution
        
        # 1. Amplitude-modulated sine wave
        sin_wave = (ascii_val / 255) * np.sin(t)
        waves.append(sin_wave)
        
        # 2. Frequency-modulated wave
        freq = self.base_frequency * (1 + ascii_val/128)
        freq_wave = np.sin(freq * t)
        waves.append(freq_wave)
        
        # 3. Phase-modulated wave
        phase = ascii_val / 255 * 2*np.pi
        phase_wave = np.sin(t + phase)
        waves.append(phase_wave)
        
        # 4. Harmonic encoding
        harmonic_wave = np.sin(t) + 0.5 * (ascii_val/255) * np.sin(2*t)
        waves.append(harmonic_wave)
        
        return np.array(waves)
    
    def add_error_correction(self, waveforms):
        """Enhanced error correction with multiple redundancy layers"""
        if not self.error_correction:
            return waveforms
            
        # Calculate checksum wave
        checksum = np.sum(waveforms, axis=0)
        normalized_checksum = checksum / np.max(np.abs(checksum))
        
        # Generate parity waves
        parity = np.mod(np.sum(waveforms > 0, axis=0), 2)
        
        # Create Reed-Solomon inspired redundancy
        reed_solomon = np.convolve(
            normalized_checksum, 
            np.ones(5)/5, 
            mode='same'
        )
        
        # Stack all components
        protected_data = np.vstack([
            waveforms,
            normalized_checksum,
            parity,
            reed_solomon
        ])
        
        return protected_data
    
    def encode_string(self, text):
        """Encode a string into a multi-dimensional waveform with error correction"""
        encoded = []
        for char in text:
            char_waves = self.char_to_waveforms(char)
            encoded.append(char_waves)
            
        combined = np.vstack(encoded)
        if self.error_correction:
            combined = self.add_error_correction(combined)
            
        return combined
    
    def visualize(self, text, output_file='encoded_waveforms.png'):
        """Create an enhanced visual representation of the encoded data"""
        encoded_data = self.encode_string(text)
        num_waves = len(encoded_data)
        
        # Create figure with improved styling
        plt.figure(figsize=(12, max(6, num_waves/2)))
        plt.style.use('dark_background')
        
        # Plot each waveform with enhanced visualization
        for i, wave in enumerate(encoded_data):
            ax = plt.subplot(num_waves, 1, i+1)
            
            # Create gradient color based on wave properties
            colors = self.color_map(np.linspace(0, 1, len(wave)))
            
            # Plot with gradient and shadow effect
            ax.plot(wave, color='white', linewidth=1, alpha=0.8)
            ax.fill_between(
                range(len(wave)), 
                wave, 
                alpha=0.3, 
                color=colors[0]
            )
            
            # Remove axes for cleaner look
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Add subtle grid
            ax.grid(True, alpha=0.1)
            
        plt.tight_layout()
        plt.savefig(
            output_file, 
            dpi=300, 
            bbox_inches='tight',
            facecolor='black',
            edgecolor='none'
        )
        plt.close()
        
        # Calculate and return metrics
        image_size = os.path.getsize(output_file)
        data_length = len(text)
        density = data_length / image_size
        
        return {
            'density': density,
            'dimensions': self.dimensions,
            'data_length': data_length,
            'image_size': image_size,
            'error_correction': self.error_correction
        }

def demonstrate_encoding():
    """Demonstrate the encoder with a sample text"""
    encoder = WaveformEncoder(dimensions=4, error_correction=True)
    sample_text = "Hello, World! 🌍"
    
    metrics = encoder.visualize(sample_text, 'waveform_demo.png')
    
    print("Encoding Metrics:")
    print(f"Data Density: {metrics['density']:.6f} characters/byte")
    print(f"Dimensions: {metrics['dimensions']}")
    print(f"Text Length: {metrics['data_length']} characters")
    print(f"Image Size: {metrics['image_size']} bytes")
    print(f"Error Correction: {'Enabled' if metrics['error_correction'] else 'Disabled'}")
    
if __name__ == "__main__":
    demonstrate_encoding()
