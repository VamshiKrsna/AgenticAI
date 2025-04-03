import streamlit as st
from summarizer import setup_gemini_api, summarize_image

def main():
    print("hello there!")
    st.title("Image Summarizer")
    st.markdown("Powered By Gemini Flash")
    gemini_api_key = st.text_input("Enter your Gemini API key",type="password")
    if gemini_api_key:
        model = setup_gemini_api(gemini_api_key)
        print(model)
    else:
        st.warning("Please enter your Gemini API key.")
    img = st.file_uploader("Upload an image to summarize it", type=["jpg", "png"])
    print(img)
    if img is not None:
        st.image(img, caption="Uploaded Image", use_column_width=True)
        if st.button("Summarize"):
            summary = summarize_image(img, model)
            st.markdown("### Summary:")
            st.write(summary)


if __name__ == "__main__":
    main()