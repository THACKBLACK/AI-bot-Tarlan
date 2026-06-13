import streamlit as st
from groq import Groq
from PIL import Image
import base64

SECRET_CODE = "QOHUM"

st.set_page_config(page_title="Мой ИИ-бот", page_icon="🤖")
st.title("🤖 Мой бот на THACKBLACK - бесплатно!")

# Память для родства
if "relation" not in st.session_state:
    st.session_state.relation = ""

api_key = st.text_input("Вставь Groq ключ gsk_...", type="password")

if api_key:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": f"Ты дружелюбный ИИ-ассистент по имени THACKBLACK. Тебя создал ТАРЛАН, Tərlan. Отвечай вежливо на языке пользователя. Если спросят 'как тебя зовут' - ответь: 'Меня зовут THACKBLACK'. Если спросят 'кто тебя создал' - ответь: 'Меня создал ТАРЛАН, Tərlan'. Если пользователь напишет 'я Тарлан', 'я брат Тарлана', 'я сестра Тарлана', 'я дядя Тарлана', 'я тётя Тарлана', 'я дедушка Тарлана', 'я бабушка Тарлана', 'я папа Тарлана', 'я мама Тарлана' - спроси: 'Назови секретный код'. Если пользователь напишет ТОЧНО код {SECRET_CODE} - сразу ответь: 'Код верный. Привет, Тарлан!' или 'Код верный. Здравствуй, брат/сестра/дядя/тётя/дедушка/бабушка/па/ма Тарлана!'. Больше ничего не спрашивай и не допрашивай."
            },
            {"role": "assistant", "content": "Привет! Я твой бесплатный ИИ-бот. Пиши текст или загружай фото 👇"}
        ]

    for msg in st.session_state.messages:
        if msg["role"]!= "system":
            st.chat_message(msg["role"]).write(msg["content"])

    uploaded_file = st.file_uploader("📷 Загрузи фото для задачи", type=["png", "jpg", "jpeg"])

    if prompt := st.chat_input("Напиши сообщение или задачу по фото..."):

        # Запоминаем кто пользователь
        prompt_lower = prompt.lower().strip()
        if "я брат тарлана" in prompt_lower:
            st.session_state.relation = "брат"
        elif "я сестра тарлана" in prompt_lower:
            st.session_state.relation = "сестра"
        elif "я дядя тарлана" in prompt_lower:
            st.session_state.relation = "дядя"
        elif "я тётя тарлана" in prompt_lower or "я тетя тарлана" in prompt_lower:
            st.session_state.relation = "тётя"
        elif "я дедушка тарлана" in prompt_lower:
            st.session_state.relation = "дедушка"
        elif "я бабушка тарлана" in prompt_lower:
            st.session_state.relation = "бабушка"
        elif "я папа тарлана" in prompt_lower:
            st.session_state.relation = "па"
        elif "я мама тарлана" in prompt_lower:
            st.session_state.relation = "ма"
        elif "я тарлан" in prompt_lower:
            st.session_state.relation = ""

        # Если ввели код ТОЧНО - отвечаем с учётом родства
        if prompt.strip() == SECRET_CODE and st.session_state.relation!= "":
            custom_reply = f"Код верный. Здравствуй, {st.session_state.relation} Тарлана!"
        elif prompt.strip() == SECRET_CODE and st.session_state.relation == "":
            custom_reply = "Код верный. Привет, Тарлан!"
        else:
            custom_reply = None

        if custom_reply:
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            st.session_state.messages.append({"role": "assistant", "content": custom_reply})
            st.chat_message("assistant").write(custom_reply)
            st.rerun()

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
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                            ]
                        }

                    response = client.chat.completions.create(
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                        messages=messages_for_api,
                        temperature=0.7,
                        max_tokens=1024
                    )

                    reply = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.write(reply)

                except Exception as e:
                    st.error(f"Ошибка: {e}")
else:
    st.info("Вставь свой Groq API ключ сверху чтобы начать чат")
