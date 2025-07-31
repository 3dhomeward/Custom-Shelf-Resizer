# Custom Shelf STL Resizer

Easily resize your floating shelf STL to fit your space—without distorting plug/connector ends or the front edge. The right plug is moved outward, the left plug and front are fixed, and the shelf’s middle and depth stretch smoothly for a perfect fit.

## Features

- Keeps left plug/connector and front edge unchanged for perfect fit
- Moves right plug to the new width
- Stretches only the shelf middle and back depth—no plug distortion
- Web-based interface, no installs needed (if using Streamlit Cloud)

## How to Use

### Option 1: Online (Recommended)
Try the app in your browser (no install): https://customshelfresizer.streamlit.app/ 

<img width="1069" height="602" alt="2025-07-31 (1)" src="https://github.com/user-attachments/assets/a06d50a5-2496-4708-b998-009be21339b8" />

### Option 2: Local (Python required)
1. Download `stretch_shelf_app.py` from this repo.
2. Install Python 3.8+ and these packages (in a terminal or command prompt): pip install streamlit numpy numpy-stl
3. Run the app: streamlit run stretch_shelf_app.py
4. Open the app in your browser (auto-opens, or go to http://localhost:8501).

## Instructions

1. **Upload your shelf STL file.**
2. **Set your desired shelf width and depth (in mm).**
3. **Download your resized STL.**
 - The left plug and front edge are unchanged for perfect fit.
 - The right plug is moved, and the shelf’s middle/back stretches or shrinks as needed.

> **Tip:** For best results, your STL should have plug regions at both ends and mesh edges (“loop cuts”) in the middle region.

## Troubleshooting

- If your STL isn’t stretching as expected, make sure it has faces/edges in the “middle” region.
- Only the right plug moves. If you need a version for the left plug or both, contact the author.

## Licensing

Apache License 2.0 

---


