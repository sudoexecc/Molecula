# Molecula - Blood Smear Analysis Demo

**Molecula** is a prototype application demonstrating how AI (specifically YOLOv7) can be used to automate peripheral blood smear analysis.

> **⚠️ DISCLAIMER**: This project is a **SIMULATION** for educational and demonstration purposes only. It uses mock data and random generation. It does **NOT** perform real medical diagnosis and should **NOT** be used for clinical decision-making.

## Features
- **Automated Counting**: Simulates detection and counting of RBCs, WBCs, and Platelets.
- **WBC Classification**: Simulates classification of 11 WBC subtypes (Neutrophils, Lymphocytes, etc.).
- **Disease Flags**: Demonstrates how an AI system could flag potential anomalies (e.g., Malaria, Leukemia patterns).
- **WBC Gallery**: Automatically crops and displays detected WBCs for review.

## How to Run
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
3.  Upload a blood smear image (JPG/PNG) to see the demo in action.

## Technical Details
- **Frontend**: Streamlit (Python)
- **AI Simulation**: `simulated_detector.py` mocks the output of a YOLOv7 object detection model.
- **Visualization**: PIL (Python Imaging Library) for drawing bounding boxes.

## Future Roadmap (Real Implementation)
To convert this into a real medical AI tool:
1.  **Dataset**: Train YOLOv7 on a large, annotated dataset like BCCD or custom lab data.
2.  **Inference**: Replace `SimulatedDetector` with a real PyTorch inference engine loading the trained `.pt` weights.
3.  **Validation**: Rigorous clinical validation and regulatory approval (FDA/CE) would be required.
