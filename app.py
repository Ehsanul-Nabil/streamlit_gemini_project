import streamlit as st 
import os,re
from dotenv import load_dotenv
from api_calling import note_generator, audio_transcription, quiz_generator
from PIL import Image


load_dotenv()

st.title("Note Summary and Quiz Generator")
st.markdown("This app summarizes your notes and generates a quiz based on the content.")
st.divider()

with st.sidebar:
    st.header("Controls")
    images = st.file_uploader("Upload the photos of your notes",
                     ['jpg','jpeg','png'],
                     accept_multiple_files=True)

    # images=[ Image.open(img) for img in images ] 
    pil_images = []
    for img in images:
        pil_images.append(Image.open(img))


    if images:
        if len(images)>3:
            st.error("Upload at max 3 images")
        # st.image(images)
        else:
            st.subheader("Uploaded images")
            col = st.columns(len(images))
            for i,img in enumerate(images):
                with col[i]:
                    st.image(img)
            # with col[1]:
            #     st.image(images[1])
            # print(type(images))
    
    #deficulty
    selected_option = st.selectbox(
        "Enter the difficulty of your quiz",
        ("Easy","Medium","Hard"),
        index = None # no option is pre-selected when the page first loads 
    )
    # if selected_option:
    #     st.markdown(f"You selected ***{selected_option}*** as difficulty of your quiz")
    # else :
    #     st.error("You must select a difficulty")

    pressed = st.button("Click the button to initiate AI",type="primary")

if pressed:
    if not images:
        st.error("You must upload atleast 1 image")
    if not selected_option:
        st.error("You must set difficulty level")

    if images and selected_option:
        # Notes
        with st.container(border=True):
            st.subheader("Your Note")
            with st.spinner("AI is writing notes for you"):
                generate_text = note_generator( pil_images)
                st.markdown(generate_text)

        # Audio
        with st.container(border=True):
            st.subheader("Audio Transcription")
            with st.spinner("Audio try to ready"):

                # generate_text=generate_text.replace("#","") 
                # re.sub(pattern, replacement, text)
                generate_text = re.sub(r'[^a-zA-Z0-9\s.,:;!?()-]', '', generate_text)     #Remove anything that is NOT a letter, number, whitespace, or . , : ; ! ? ( ) -.
                generate_audio=audio_transcription(generate_text)
                st.audio(generate_audio)

        # Quiz
        with st.container(border=True):
            st.subheader(f"Quiz {selected_option} Difficulty")
            with st.spinner("Your try to ready"):
                quizzes = quiz_generator(pil_images,selected_option)
                st.markdown(quizzes)
        