"# SPIDAM_Project" 
SPIDAM (Scientific Python Interactive Data Acoustic Modeling)
Project Overview
The SPIDAM project is an interactive audio analysis tool designed for the computation of RT60 (Reverberation Time) and other acoustic features in audio files. It uses advanced audio processing techniques to help users visualize and analyze audio data, compute RT60 for different frequency bands, and explore the highest resonance frequency.

This tool is built using Python and the following key libraries: Librosa, PyDub, Matplotlib, NumPy, and SciPy.

Features
Load Audio Files: Supports WAV, MP3, and M4A formats. The tool automatically converts non-WAV files to WAV.
Compute RT60: Calculates RT60 for low, mid, and high-frequency bands using the energy decay method.
RT60 Visualization: Displays RT60 plots, energy decay curves, and compares RT60 values over time.
Waveform Display: Visualize the waveform of the audio file.
Highest Resonance Frequency: Detect and display the highest resonance frequency of the audio.
RT60 Difference: Calculate and display the difference between the calculated RT60 and a target RT60 value (e.g., 0.5 seconds).
Installation
Clone the repository:

bash
git clone https://github.com/MatheusDiazz/SPIDAM_Project.git
cd SPIDAM_Project
Create a virtual environment (optional but recommended):

bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
Install required dependencies: Ensure that you have the necessary Python libraries installed:

bash
pip install -r requirements.txt
Usage Instructions
Run the application: To start the application, simply run:

bash
python main.py
Load an audio file:

Click the "Load Audio File" button to open a file dialog.
Choose an audio file in WAV, MP3, or M4A format. The tool will automatically convert non-WAV formats to WAV.
Compute RT60:

After the audio file is loaded, click the "Compute RT60" button.
The RT60 for low, mid, and high-frequency bands will be calculated and displayed in the results section.
Alternate RT60 Plots:

Click the "Alternate RT60 Plots" button to visualize the RT60 plots for different frequency bands (low, mid, high). The application will cycle through the frequency bands on each button click.
Combine RT60 Plots:

Click the "Combine RT60 Plots" button to view the RT60 plots for all frequency bands on the same graph for easier comparison.
View Highest Resonance Frequency:

Click the "Show Highest Resonance" button to compute and display the highest resonance frequency of the loaded audio file.
RT60 Difference:

Click the "RT60 Difference" button to calculate and display the difference between the computed RT60 and a target RT60 value (e.g., 0.5 seconds).
Example of Output
When you load an audio file and compute RT60, you will see results like:

yaml
RT60 Low: 1.23s, Mid: 0.89s, High: 0.65s
RT60 Low (125-500 Hz): Reverberation time for the low-frequency band.
RT60 Mid (500-2000 Hz): Reverberation time for the mid-frequency band.
RT60 High (2000-4000 Hz): Reverberation time for the high-frequency band.
Requirements
Python 3.x
Libraries: The application uses the following libraries (installed via requirements.txt):
librosa: For audio loading and processing
numpy: For numerical computations
scipy: For signal processing tasks like filtering
pydub: For audio format conversion
matplotlib: For plotting RT60 curves and waveforms
tkinter: For GUI elements
Troubleshooting
Error: "Audio file not loaded":
Ensure that the file is in the correct format (WAV, MP3, or M4A) and is properly loaded into the tool.
Error with RT60 Calculation:
If the RT60 calculation fails, check that the audio file is not silent or too short.
Ensure that the audio file contains enough reverberation for RT60 to be computed.
GUI Freezing:
If the GUI freezes during processing, it may be due to a large audio file or slow processing. Try using smaller files for testing.
