import streamlit as st
from PIL import Image

st.set_page_config(page_title="AI Akciğer Kanseri Demo", layout="centered")
st.title("AI Destekli Akciğer Kanseri Risk Tahmin Sistemi")

st.write("Bu demo sistem, hasta verilerine göre akciğer kanseri riski tahmini yapar ve öneriler sunar.")

with st.form("risk_form"):
    st.subheader("🧾 Hasta Bilgileri")
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Yaş", 35, 90, 60)
        gender = st.radio("Cinsiyet", ["Erkek", "Kadın"])
        smoking = st.selectbox("Sigara Geçmişi (paket-yıl)", ["<10", "10-30", ">30"])
    with col2:
        symptom = st.multiselect("Şikayetler", ["Öksürük", "Nefes Darlığı", "Göğüs Ağrısı", "Kilo Kaybı", "Ateş", "Yok"])
        xray_nodule = st.selectbox("Radyolojik Nodül Durumu", ["Yok", "<1 cm", "1-3 cm", ">3 cm"])
        image_upload = st.file_uploader("X-ray Görüntüsü (opsiyonel)", type=["png", "jpg", "jpeg"])
    submit = st.form_submit_button("🔍 Riski Hesapla")

if submit:
    score = 0
    if age > 65: score += 15
    if gender == "Erkek": score += 10
    if smoking == ">30": score += 25
    elif smoking == "10-30": score += 15
    if "Öksürük" in symptom or "Nefes Darlığı" in symptom: score += 10
    if xray_nodule == "1-3 cm": score += 20
    elif xray_nodule == ">3 cm": score += 30

    st.markdown("---")
    st.subheader("📊 Sonuçlar")
    st.metric("Tahmini Kanser Riski", f"%{min(score, 95)}")

    if score >= 60:
        st.warning("Yüksek Risk: PET/BT ve Biyopsi önerilir.")
    elif score >= 30:
        st.info("Orta Risk: 3 ay içinde tekrar görüntüleme önerilir.")
    else:
        st.success("Düşük Risk: Rutin izlem yeterlidir.")

    st.markdown("---")
    if image_upload:
        st.image(image_upload, caption="Yüklenen X-ray", use_column_width=True)
    else:
        st.image("sahte_xray_goruntusu.png", caption="Simülasyon X-ray", use_column_width=True)
