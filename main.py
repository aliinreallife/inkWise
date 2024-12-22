import streamlit as st
import cv2
import numpy as np
from PIL import Image
import base64

st.set_page_config(
    page_title="InkWise",  # The title of your app
    page_icon="wolf.ico"  # Path to your icon file
)

def process_image_for_edge_detection(image, low_threshold, high_threshold, kernel_size, sigma):
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian Blur
    blurred_image = cv2.GaussianBlur(gray_image, (kernel_size, kernel_size), sigma)
    # Perform edge detection
    edges = cv2.Canny(blurred_image, low_threshold, high_threshold)
    # Invert edges for printing
    inverted_edges = cv2.bitwise_not(edges)
    return inverted_edges

def process_image_for_low_ink(image):
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Increase the brightness by adding a constant value
    low_ink_image = cv2.add(gray_image, 64)  # Add 64 to each pixel value
    return low_ink_image

def download_image(image, filename):
    """Function to download the image."""
    _, buffer = cv2.imencode(".png", image)
    img_bytes = buffer.tobytes()
    b64 = base64.b64encode(img_bytes).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

def main():
    st.title("InkWise")

    # Upload multiple images
    uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        # Switch for edge detection
        edge_detection_enabled = st.checkbox("Edge Detection", value=False)

        for uploaded_file in uploaded_files:
            # Read the image
            image = np.array(Image.open(uploaded_file))

            if edge_detection_enabled:
                # Set parameters for Canny edge detection
                low_threshold = 100
                high_threshold = 200
                kernel_size = 5  # Must be odd
                sigma = 1

                # Process the image for edge detection
                processed_image = process_image_for_edge_detection(image, low_threshold, high_threshold, kernel_size, sigma)
            else:
                # Process the image for low ink consumption
                processed_image = process_image_for_low_ink(image)

            # Create two columns for side-by-side display
            col1, col2 = st.columns(2)

            with col1:
                st.image(image, caption=f"Original Image: {uploaded_file.name}", use_container_width=True)

            with col2:
                st.image(processed_image, caption=f"Processed Image: {uploaded_file.name}", use_container_width=True, channels="GRAY")

            # Download button for each processed image
            download_link = download_image(processed_image, f"processed_{uploaded_file.name}")
            st.markdown(download_link, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
