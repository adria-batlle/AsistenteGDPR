# ⚖️ Asistente GDPR (RAG + Gemini)

Este proyecto implementa un **asistente jurídico para el Reglamento General de Protección de Datos (GDPR)** utilizando la técnica **RAG (Retrieval-Augmented Generation)** con el modelo **Gemini 1.5** de Google.

🚀 **Objetivo**: crear un chatbot que responda preguntas sobre el GDPR **citando los artículos y considerandos relevantes**, combinando:
- **Embeddings + Vector DB (FAISS)** → búsqueda semántica precisa en el texto del GDPR.  
- **Gemini** → generación de respuestas claras, profesionales y trazables.

---

## 🗂️ Estructura del repositorio

asistente-gdpr/
│
├── app.py # Aplicación Streamlit (chatbot)
├── requirements.txt # Librerías necesarias
├── Asistente GDPR/ # Base documental (ya procesada en vectores)
│ ├── gdpr_chunks.pkl
│ ├── gdpr_faiss.index
│ ├── gdpr_metadata.pkl
└── README.md # Este documento


---

## ⚡ Cómo funciona el asistente

1. El usuario introduce una pregunta (ej: *¿Qué dice el GDPR sobre consentimiento explícito?*).
2. El sistema convierte la pregunta a un **embedding** y busca los chunks relevantes en la base vectorial FAISS.
3. Los fragmentos más relevantes del **GDPR** se pasan como *contexto* a Gemini.
4. Gemini redacta una respuesta clara **citando artículos o considerandos** concretos.

---

## 🛠️ Instalación local (opcional)

```bash
git clone https://github.com/tuusuario/asistente-gdpr.git
cd asistente-gdpr
pip install -r requirements.txt
Crea un archivo .streamlit/secrets.toml con tu clave de Gemini:

toml
Copy
GEMINI_API_KEY="tu_api_key_aqui"
Ejecuta el chatbot en local:

bash
Copy
streamlit run app.py
👉 Abre en el navegador: http://localhost:8501
