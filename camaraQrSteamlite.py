import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode

def leer_qr_code():

    # Open the webcam
    cap = cv2.VideoCapture(0)

    stframe = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to capture image")
            break

        # Convert frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Decode QR code
        decoded_objects = decode(frame_rgb)
        for obj in decoded_objects:
            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points

            n = len(hull)
            for j in range(0, n):
                cv2.line(frame_rgb, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

            x = obj.rect.left
            y = obj.rect.top

            qr_data = obj.data.decode("utf-8")
            qr_type = obj.type

            
            st.write(f"Detected {qr_type}: {qr_data}")
            cv2.putText(frame_rgb, qr_data, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Display the frame in Streamlit
        stframe.image(frame_rgb, channels="RGB")

        # Break the loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Create a Streamlit app 
    st.set_page_config(page_title="QR Lector", page_icon="🌐", layout="centered")
    st.image("images/encabezado.JPG", use_column_width=True)
    st.title("QR Code Scanner")

    if st.button("Leer QR Code"):
        leer_qr_code()
