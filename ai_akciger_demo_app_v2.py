import streamlit as st
from PIL import Image
from fpdf import FPDF
import datetime

st.set_page_config(page_title="AI Akciğer Kanseri Demo", layout="centered")

# Logo görüntüleme
st.image("A_logo_for_an_AI-powered_lung_cancer_early_detecti.png", width=120)

st.title("AI Destekli Akciğer Kanseri Risk Tahmin Sistemi")

st.write("Bu demo sistem, hasta verilerine göre akciğer kanseri riski tahmini yapar ve öneriler sunar.")

# Hasta formu
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

    risk_note = ""
    if score >= 60:
        risk_note = "Yüksek Risk: PET/BT ve Biyopsi önerilir."
        st.warning(risk_note)
    elif score >= 30:
        risk_note = "Orta Risk: 3 ay içinde tekrar görüntüleme önerilir."
        st.info(risk_note)
    else:
        risk_note = "Düşük Risk: Rutin izlem yeterlidir."
        st.success(risk_note)

    if image_upload:
        st.image(image_upload, caption="Yüklenen X-ray", use_container_width=True)
    else:
        st.image("sahte_xray_goruntusu.png", caption="Simülasyon X-ray", use_container_width=True)

    # PDF çıktısı oluştur
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="AI Destekli Akciğer Kanseri Risk Tahmin Raporu", ln=1, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Tarih: {datetime.date.today()}", ln=1)
    pdf.cell(200, 10, txt=f"Yaş: {age}", ln=1)
    pdf.cell(200, 10, txt=f"Cinsiyet: {gender}", ln=1)
    pdf.cell(200, 10, txt=f"Sigara Geçmişi: {smoking}", ln=1)
    pdf.cell(200, 10, txt=f"Şikayetler: {', '.join(symptom)}", ln=1)
    pdf.cell(200, 10, txt=f"X-ray Nodül Durumu: {xray_nodule}", ln=1)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Tahmini Kanser Riski: %{min(score, 95)}", ln=1)
    pdf.multi_cell(0, 10, txt=f"Klinik Öneri: {risk_note}")
    pdf.ln(10)
    pdf.set_text_color(220, 50, 50)
    pdf.set_font("Arial", style="B", size=11)
    pdf.multi_cell(0, 10, txt="Bu çıktı AI sistemi tarafından öneri amaçlıdır. Doktorunuza gösteriniz.")
    pdf.output("/mnt/data/ai_risk_raporu.pdf")

    st.markdown("---")
    st.subheader("📄 PDF Çıktısı")
    with open("/mnt/data/ai_risk_raporu.pdf", "rb") as file:
        btn = st.download_button(label="📥 PDF Raporu İndir",
                                 data=file,
                                 file_name="AI_Risk_Raporu.pdf",
                                 mime="application/pdf")
