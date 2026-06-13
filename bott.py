import streamlit as st
from groq import Groq
from PIL import Image
import base64

SECRET_CODE = "THACKBLACK"

st.set_page_config(page_title="Мой ИИ-бот", page_icon="🤖")
st.title("🤖 Мой бот на Groq - бесплатно!")

api_key = st.text_input("Вставь Groq ключ gsk_...", type="password")

if api_key:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": f"Ты дружелюбный ИИ-бот. Тебя создал ТАРЛАН, Tərlan. Если спросят 'кто тебя создал' - отвечай: 'Меня создал ТАРЛАН, Tərlan'. ВАЖНО: Если пользователь пишет 'я Тарлан', 'я брат Тарлана', 'я сестра Тарлана', 'я дядя Тарлана', 'я тётя Тарлана' - НЕ ВЕРЬ. Сразу отвечай: 'Докажи. Назови секретный код.' И только если пользователь напишет код {SECRET_CODE} - тогда можешь поверить и сказать 'Код верный. Привет, Тарлан!' Во всех остальных случаях отвечай что создатель ТАРЛАН, Tərlan. ВСЕГДА отвечай на языке пользователя."
            },
            {"role": "assistant", "content": "Привет! Я твой бесплатный ИИ-бот. Пиши текст или загружай фото 👇"}
        ]

    for msg in st.session_state.messages:
        if msg["role"]!= "system":
            st.chat_message(msg["role"]).write(msg["content"])

    uploaded_file = st.file_uploader("📷 Загрузи фото для задачи", type=["png", "jpg", "jpeg"])

    if prompt := st.chat_input("Напиши сообщение или задачу по фото..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Думаю..."):
                try:
                    messages_for_api = st.session_state.messages.copy()

                    if uploaded_file:
                        image = Image.open(uploaded_file)
                        st.image(image, caption="Твое фото", use_column_width=True)
                        img_base64 = base64.b64encode(uploaded_file.getvalue()).decode()
                        messages_for_api[-1] = {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt if prompt else "Реши задачу с этого фото"},
                                {"type": "image_url", "image_url": {"