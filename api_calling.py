from google import genai
import os,io
from dotenv import load_dotenv
from gtts import gTTS #Google text to speech

load_dotenv()

api_keyy = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_keyy)

#note generator
# def note_generator(images):
#     prompt="""Summarize the picture in note format at max 100 words,
#       make sure to add necessary markdown to differentiate different section"""
#     response = client.models.generate_content(
#         # model="gemini-3-flash-preview",
#         model="gemini-3.8-flash",
#         contents=[*images,prompt]
#     )
#     return response.text


def note_generator(images):

    prompt = """
    Summarize the picture in note format at a maximum of 100 words.
    Use Markdown to differentiate different sections.
    """

    models = [
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.6-flash"
    ]

    for model in models:

        try:
            response = client.models.generate_content(
                model=model,
                contents=[*images, prompt]
            )
            print(f"Successfull on {model}")
            return response.text

        except Exception as e:
            print(f"{model} failed: {e}")

    return "All Gemini models are currently unavailable."


def audio_transcription(text):
    speech = gTTS(text,lang='en',slow=False)
    # speech.save("Welcome.mp3")#save to local storage
    # st.audio("Welcome.mp3")# audio playing
    audio_buffer=io.BytesIO()# create space in ram
    speech.write_to_fp(audio_buffer)# save to ram
    return audio_buffer

def quiz_generator(images,difficulty):
    prompt = f"Generate 3 quizzes based on the {difficulty}. Make sure to add markdown to differentiate the option. Add correct answer on all these question below"

    models = [
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.6-flash"
    ]

    for model in models:

        try:
            response = client.models.generate_content(
                model=model,
                contents=[*images, prompt]
            )

            return response.text

        except Exception as e:
            print(f"{model} failed: {e}")

    return "All Gemini models are currently unavailable."