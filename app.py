import streamlit as st

st.set_page_config(
    page_title="AI Voice Detector",
    page_icon="🎙️"
)

st.title("🎙️ AI Voice Cloning Detector")

st.write(
    "Upload an audio file to check "
    "whether it is genuine or AI-generated."
)

st.divider()

uploaded_file = st.file_uploader(
    "Upload your audio file",
    type=["wav", "mp3"]
)

if uploaded_file is not None:

    st.success("Audio uploaded successfully!")

    st.audio(uploaded_file)

    if st.button("Analyze Audio"):
        st.info(
            "AI model integration will be added soon!"
        )
else:
    st.warning("Please upload an audio file.")
