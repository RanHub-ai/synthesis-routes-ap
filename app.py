# ---------------------------
# Streamlit-приложение: Построение маршрутов синтеза
# ---------------------------
import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw
import requests
from PIL import Image
from io import BytesIO
import json

st.set_page_config(page_title="Пути синтеза", layout="wide")

st.title("🧪 Построение маршрутов синтеза биомедицинских соединений")
st.markdown("""
Это приложение позволяет предсказывать возможные пути синтеза заданной молекулы с использованием современных AI-инструментов.
Введите **SMILES** строку интересующего соединения и запустите предсказание.
""")

smiles = st.text_input("Введите SMILES молекулы", "CC(=O)Oc1ccccc1C(=O)O")

if st.button("🔍 Построить маршрут синтеза"):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            st.error("Неверная SMILES строка")
        else:
            st.subheader("🔬 Структура молекулы")
            st.image(Draw.MolToImage(mol, size=(300, 300)))

            st.subheader("🧠 Предсказанный путь синтеза с помощью RXNMapper API")
            try:
                api_url = "https://rxnmapper.ai/api/route"
                headers = {"Content-Type": "application/json"}
                payload = json.dumps({"smiles": smiles})

                response = requests.post(api_url, headers=headers, data=payload)
                if response.status_code == 200:
                    data = response.json()
                    if "image_url" in data:
                        img_response = requests.get(data["image_url"])
                        if img_response.status_code == 200:
                            img = Image.open(BytesIO(img_response.content))
                            st.image(img, caption="Синтетический маршрут от RXNMapper")
                        else:
                            st.warning("Не удалось загрузить изображение результата")
                    else:
                        st.warning("Ответ не содержит изображения пути")
                else:
                    st.warning("Ошибка при обращении к RXNMapper API")
            except Exception as api_error:
                st.error(f"Ошибка при обращении к RXNMapper: {api_error}")

    except Exception as e:
        st.error(f"Ошибка при обработке: {e}")

st.markdown("---")
st.caption("Разработка: AI-платформа для синтеза биомедицинских соединений © 2025")