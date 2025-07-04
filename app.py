import streamlit as st
import pdfplumber
import requests
import base64
from io import BytesIO

# === CONFIGURATION DE PAGE ===
st.set_page_config(page_title="Résumé PDF IA", page_icon="📄", layout="centered")

# === CSS DESIGN ===
st.markdown("""

<style>
html, body {
    height: 100%;
    margin: 0;
    font-family: "Segoe UI", sans-serif;
    background: linear-gradient(135deg, #1d0030 0%, #3f0f6d 50%, #c084fc 100%);
    background-attachment: fixed;
    background-size: cover;
    color: #f5f5f5;
}
.block-container {
    margin-top :70px ;
   background: linear-gradient(270deg, #e0bbff, #d1a4ff, #f5d5ff);
    background-size: 600% 600%;
    animation: animatedGradient 15s ease infinite;
    backdrop-filter: blur(10px);
    
    padding: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    
    border-radius: 15px;
    
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            }
            @keyframes animatedGradient {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
section, .main{
    background-color: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(8px);
    border-radius: 15px;
    
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

h1 {
    text-align: center;
    color: #d9b8ff;
    font-size: 36px;
    font-weight: bold;
    padding-top: -500px;
    animation: fadeIn 1s ease-in-out;
}

.subtitle {
    text-align: center;
    color: #4b0082;  /* Indigo foncé, très lisible */
    font-size: 17px;
    margin-bottom: 25px;
    animation: fadeIn 1.3s ease-in-out;
}

.summary {
    background: rgba(255, 255, 255, 0.85);  /* fond blanc très doux */
    padding: 20px;
    border-radius: 15px;
    color: #3b0a54;  /* texte violet foncé inspiré du logo */
    font-size: 16px;
    line-height: 1.6;
    margin-top: 20px;
    border: 1px solid #d8b4fe;  /* lavande clair */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    animation: slideUp 0.6s ease-in-out;
}


.stButton button {
    background: linear-gradient(135deg, #8e2de2, #4a00e0);
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 0.6em 1.5em;
    border: none;
    transition: background 0.3s ease;
}
.stButton button:hover {
    background: linear-gradient(135deg, #5f0fd6, #31007e);
}

.download-btn {
    display: flex;
    justify-content: center;
    margin-top: 20px;
    font-weight: bold;
    font-size: 16px;
    color: #fff;
    text-decoration: none;
}

a.download-btn:hover {
    color: #c084fc;
}

@keyframes fadeIn {
    0% {opacity: 0;}
    100% {opacity: 1;}
}
@keyframes slideUp {
    0% {opacity: 0; transform: translateY(20px);}
    100% {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# === LOGO ===
# === LOGO EN COIN GAUCHE ===
logo_path = "image-removebg-preview (5).png"
st.markdown(f"""
    <div style="position: absolute; top: -100px; left: -200px; width: 660px;">
        <img src="data:image/png;base64,{base64.b64encode(open("C:/Users/pc/Desktop/projets/resume_pdf/logo.png", "rb").read()).decode()}" width="100">
    </div>
""", unsafe_allow_html=True)

# === TITLE ===
st.markdown("<h1>Automatic PDF Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Choose your language and get a clear summary of your PDF content</div>", unsafe_allow_html=True)

# === LANGUAGE SELECTION ===
language = st.selectbox("🌍 Choose summary language", ["English", "Français"])

# === MODEL MAP ===
model_map = {
    "Français": "csebuetnlp/mT5_multilingual_XLSum",
    "English": "csebuetnlp/mT5_multilingual_XLSum"
}

model_id = model_map[language]
API_URL_SUMMARY = f"https://api-inference.huggingface.co/models/{model_id}"
headers = {"Authorization": "Bearer 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"}  # Remplace par ton token

# === EXTRACTION TEXTE PDF ===
def extract_text(file):
    text = ''
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + '\n'
    return text.strip()

# === CODES LANGUES ISO 639-1 ===
lang_codes = {
    "Français": "fr",
    "English": "en"}

# === FONCTION RÉSUMÉ VIA API HUGGINGFACE ===
def summarize_text_api(text):
    if len(text) > 1024:
        text = text[:1024]
    
    # On force résumé en français (pour avoir une base stable)
    input_text = f"fr {text}"

    response = requests.post(API_URL_SUMMARY, headers=headers, json={"inputs": input_text})
    
    if response.status_code == 200:
        return response.json()[0]["summary_text"]
    else:
        return "Erreur API résumé : " + response.text

# === FONCTION TRADUCTION VIA API HUGGINGFACE ===
def translate_text(text, source_lang, target_lang):
    model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
    API_URL_TRANSLATE = f"https://api-inference.huggingface.co/models/{model_name}"

    response = requests.post(API_URL_TRANSLATE, headers=headers, json={"inputs": text})

    if response.status_code == 200:
        return response.json()[0]['translation_text']
    else:
        return "Erreur API traduction : " + response.text

# === GÉNÉRATION DU LIEN DE TÉLÉCHARGEMENT ===
def generate_download_link(text):
    b = BytesIO()
    b.write(text.encode())
    b.seek(0)
    b64 = base64.b64encode(b.read()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="summary.txt" class="download-btn">📥 Download Summary</a>'
    return href

# === INTERFACE UTILISATEUR ===
uploaded_file = st.file_uploader("📎 Upload a PDF file", type="pdf")

if uploaded_file:
    with st.spinner("📄 Extracting text..."):
        text = extract_text(uploaded_file)

    if text:
        with st.spinner("🧠 Generating summary..."):
            summary_fr = summarize_text_api(text)  # Résumé en français

            if language != "Français":
                # Traduire résumé vers la langue choisie
                target_code = lang_codes[language]
                summary = translate_text(summary_fr, source_lang="fr", target_lang=target_code)
            else:
                summary = summary_fr

        st.success("✅ Summary generated!")
        st.markdown("### 📝 Summary:")
        st.markdown(f"<div class='summary'>{summary}</div>", unsafe_allow_html=True)

        # Bouton téléchargement
        st.markdown(generate_download_link(summary), unsafe_allow_html=True)
    else:
        st.warning("❗ No text found in the uploaded PDF.")