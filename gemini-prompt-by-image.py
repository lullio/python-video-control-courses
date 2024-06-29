import google.generativeai as genai
from IPython.display import Markdown
#from google.colab import userdata


#GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')
# Configure sua chave de API diretamente aqui
GOOGLE_API_KEY = "AIzaSyCafFNOXupnBY0rCT2NlKzcxbCDl61yqoU"

genai.configure(api_key=GOOGLE_API_KEY)

# Exibe a chave de API para verificação (não use MessageBox no Colab, apenas para exemplo)
print(f"Chave de API configurada: {GOOGLE_API_KEY}")

sample_file = genai.upload_file(path="background.png",
                            display_name="Sample drawing")

print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
print(f"Uploaded file '{sample_file.display_name}' as: {sample_file}") # json

# The Gemini 1.5 models are versatile and work with multimodal prompts
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

response = model.generate_content([sample_file, "Extraia todo o texto da imagem e explique sobre o que se trata."])
print(f'Deleted {response.text}.')

Markdown(">" + response.text)

genai.delete_file(sample_file.name)
print(f'Deleted {sample_file.display_name}.')