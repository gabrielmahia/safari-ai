import streamlit as st
import urllib.request, json

st.set_page_config(page_title="Safari AI — Usafiri Kenya", page_icon="🚌", layout="centered")
st.markdown("""<style>
.stApp{background:#0a0c10;color:#e8edf5}
.s-card{background:#0d1117;border:1px solid #30363d;border-radius:10px;padding:14px 18px;margin:8px 0}
.stButton>button{background:#f0883e;color:#0d1117;border:none;border-radius:8px;padding:10px 24px;font-weight:800;width:100%}
</style>""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY","")
SYSTEM = "Wewe ni mshauri wa usafiri Kenya. Jibu kwa Kiswahili. Toa: njia za usafiri, bei za makadirio, muda wa safari, vidokezo vya usalama."

def ask(q):
    if not API_KEY: return "❌ API key not configured."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    body = {"contents":[{"role":"user","parts":[{"text":q}]}],
            "systemInstruction":{"parts":[{"text":SYSTEM}]},
            "generationConfig":{"temperature":0.3,"maxOutputTokens":700}}
    try:
        req = urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r:
            return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e: return f"❌ {e}"

st.markdown("# 🚌 Safari AI")
st.markdown("**Msaada wa Usafiri Kenya**")
tab1,tab2,tab3,tab4 = st.tabs(["🗺️ Njia ya Safari","🚂 SGR","🚗 NTSA","⛽ Bei za Mafuta"])

with tab1:
    origin = st.text_input("Kutoka:", placeholder="Mfano: Nairobi CBD")
    dest = st.text_input("Kwenda:", placeholder="Mfano: Kisumu")
    transport = st.multiselect("Aina ya usafiri:", ["Matatu","Basi","SGR","Ndege","Meli/ferry"], default=["Matatu","Basi"])
    if st.button("🗺️ Pata Njia", key="route_btn") and origin and dest:
        with st.spinner("..."): result = ask(f"Safari kutoka {origin} kwenda {dest} kwa {', '.join(transport)} Kenya. Toa: njia, bei, muda, terminals/stages, vidokezo vya usalama.")
        st.markdown(f'<div class="s-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab2:
    sgr_q = st.selectbox("Swali la SGR:", ["Bei za tiketi Nairobi-Mombasa","Ratiba ya treni","Jinsi ya kufanya booking online","Tiketi za SGR — masharti","Safari Nairobi-Kisumu kwa SGR"])
    if st.button("🚂 Pata Habari za SGR", key="sgr_btn"):
        with st.spinner("..."): result = ask(sgr_q + " Kenya SGR (Standard Gauge Railway). Toa habari za kisasa zaidi.")
        st.markdown(f'<div class="s-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab3:
    ntsa_q = st.selectbox("Huduma ya NTSA:", ["Jinsi ya kupata leseni ya udereva","Jinsi ya kulipa faini ya NTSA","Smart DL — jinsi ya kuomba","Usajili wa gari jipya","Uhamisho wa umiliki wa gari","Tathmini ya hali ya gari (vehicle inspection)"])
    if st.button("🚗 Habari za NTSA", key="ntsa_btn"):
        with st.spinner("..."): result = ask(ntsa_q + " Kenya. Toa hatua, gharama, muda, na mahali pa kwenda.")
        st.markdown(f'<div class="s-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab4:
    if st.button("⛽ Bei za Mafuta Leo", key="fuel_btn"):
        with st.spinner("..."): result = ask("Bei za mafuta Kenya leo (petrol, diesel, kerosene). Toa bei kwa EPRAsettings, ni nani anayeweka bei, na jinsi unavyobadilika kila mwezi.")
        st.markdown(f'<div class="s-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("🚌 Safari AI v1.0 | NTSA: ntsa.go.ke | SGR: krc.co.ke | CC BY-NC-ND 4.0")
