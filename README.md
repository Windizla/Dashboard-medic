🧬 Futuristic Medical Dashboard
A high-fidelity, Sci-Fi inspired medical monitoring interface built entirely with Python and Streamlit.
This project demonstrates how to push the boundaries of Streamlit's UI capabilities, featuring a dark "Cyberpunk/HUD" aesthetic, custom SVG animations, and synthetic data generation for medical vitals.
<img width="1905" height="917" alt="Снимок экрана 2026-01-08 214059" src="https://github.com/user-attachments/assets/047be604-0210-4836-8090-604759c09172" />


(Replace the path above with your actual screenshot image)
🚀 Overview
This dashboard simulates a patient monitoring system similar to those seen in sci-fi movies or video games. It moves away from standard data tables, utilizing custom CSS and SVG manipulation to create an immersive "Glassmorphism" interface. It is designed for demonstration purposes, visualizing how health data (ECG, vitals, organ status) can be presented in a modern, dark-mode context.
✨ Key Features
🎨 Advanced Custom UI:
Heavily customized CSS for a neon/dark-mode aesthetic.
Transparent "glass" panels, custom gradients, and glowing effects.
Hidden default Streamlit headers and footers for a native app feel.
🩻 Interactive Body Map (HUD):
Dynamic SVG Rendering: Organs change color (Cyan vs. Red) and animation speed based on health status.
Custom Backgrounds: Users can upload their own X-ray or HUD background images.
Fine-Tuning Controls: A dedicated sidebar panel allows for precise positioning, scaling, and opacity adjustment of individual organs over the background.
❤️ Synthetic Data Generation:
Real-time ECG: Generates a synthetic P-QRS-T waveform using mathematical models (Gaussian functions) via NumPy.
Vitals Tracking: Randomly generated trends for blood pressure, pulse, and glucose.
🧠 Dynamic Logic:
Condition & Orders: The "Doctor's Orders" and "Condition" cards automatically update their text and advice based on the combination of inflamed organs selected in the sidebar.
🛠️ Tech Stack
Streamlit: Core framework for the web app.
Plotly: Rendering the ECG waveform graph.
Pandas & NumPy: Data handling and synthetic signal generation.
HTML/CSS/SVG: deeply embedded for custom styling and animations.
