import streamlit as st
import pickle, os, faiss
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# ============= CONFIG GEMINI =================
# La API key se lee de st.secrets para no exponerla en el repo público
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

# ============= CARGA DE BASE DOCUMENTAL =================
def cargar_base():
    ruta_base = "Asistente GDPR/"
    with open(ruta_base + "gdpr_chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    indice_faiss = faiss.read_index(ruta_base + "gdpr_faiss.index")
    with open(ruta_base + "gdpr_metadata.pkl", "rb") as f:
        metadata = pickle.load(f)
    modelo_embeddings = SentenceTransformer(metadata["modelo_embeddings"])
    return chunks, indice_faiss, modelo_embeddings, metadata

def responder_con_rag_gemini(pregunta, indice, chunks, modelo_embeddings, k=4):
    embedding_pregunta = modelo_embeddings.encode([pregunta])
    distancias, indices = indice.search(embedding_pregunta.astype("float32"), k)
    fuentes = [chunks[i] for i in indices[0]]
    contexto = "\n".join([f"{f['titulo']}:\n{f['contenido']}" for f in fuentes])

    prompt = f"""
Eres un asistente experto en el Reglamento General de Protección de Datos (GDPR).
Responde SOLO con base en el contexto y cita los artículos.

Pregunta: {pregunta}

Contexto:
{contexto}

Respuesta:
"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text, fuentes

# ============= INTERFAZ STREAMLIT =================
def main():
    st.title("⚖️ Asistente GDPR (RAG + Gemini)")
    st.write("Haz preguntas sobre la normativa GDPR, recibirás citas de artículos o considerandos.")

    if "chunks" not in st.session_state:
        with st.spinner("Cargando GDPR..."):
            chunks, indice, modelo, metadata = cargar_base()
            st.session_state["chunks"] = chunks
            st.session_state["indice"] = indice
            st.session_state["modelo"] = modelo

    pregunta = st.text_input("Escribe tu pregunta:")
    if pregunta:
        with st.spinner("Consultando..."):
            respuesta, fuentes = responder_con_rag_gemini(
                pregunta,
                st.session_state["indice"],
                st.session_state["chunks"],
                st.session_state["modelo"]
            )
        st.subheader("🤖 Respuesta")
        st.write(respuesta)
        st.subheader("📚 Fuentes")
        for f in fuentes[:3]:
            st.markdown(f"- **{f['titulo']}**")

if __name__ == "__main__":
    main()
