import google.generativeai as genai
from IPython.display import Markdown
#from google.colab import userdata


#GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')
# Configure sua chave de API diretamente aqui
GOOGLE_API_KEY = "AIzaSyCafFNOXupnBY0rCT2NlKzcxbCDl61yqoU"

genai.configure(api_key=GOOGLE_API_KEY)

# Exibe a chave de API para verificação (não use MessageBox no Colab, apenas para exemplo)
print(f"Chave de API configurada: {GOOGLE_API_KEY}")

video_file_name = "video.mp4"

print(f"Uploading file...")
video_file = genai.upload_file(path=video_file_name)
print(f"Completed upload: {video_file}")
print(f"Completed upload: {video_file.uri}")

import time

while video_file.state.name == "PROCESSING":
    print('.', end='')
    time.sleep(10)
    video_file = genai.get_file(video_file.name)

if video_file.state.name == "FAILED":
  raise ValueError(video_file.state.name)

# Create the prompt.
prompt = "Describe this video."

# The Gemini 1.5 models are versatile and work with multimodal prompts
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Make the LLM request.
print("Making LLM inference request...")
response = model.generate_content([video_file, prompt],
                                  request_options={"timeout": 600})
print(response.text)