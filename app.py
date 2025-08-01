import streamlit as st
import requests
import json
import locale

def get_prediction(data):
    print(json.dumps(data))
    endpoit = st.secrets["API-ENDPOINT"]
    headers = {
        "Content-Type": "application/json",
        "x-api-key": st.secrets["API-KEY"]
    }
    response = requests.post(endpoit, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        result = response.json()
        print(result)
        
        """
            Preço estimado para compra
            De acordo com os dados fornceidos, seu laptop podera ser comprado pelo seguinte valor abaixo
        """
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        
        predicted_value_formatted = locale.format_string("%d", result['prediction'], grouping=True)
        
        st.markdown("Valor para compra: ** " + predicted_value_formatted + " BRL (Brazilian Real) **")
    else:
        st.markdown("Erro ao obter a previsão. Por favor, revise seus dados")

"""
## Predição de Preço de Laptop

Este modelo é capaz de prever o preço de um laptop dada algumas características.

A aplicação é para ser utilizada em uma loja eletronica que avalia laptops usados como parte do pagamento de um novo,
por tal razão a avaliação não é tão exaustiva e se baseia em caracteristicas comuns, como marca, processador, memória etc.
sem nenhuma outra avaliação visual, pelo menos por enquanto.

## Caracteristicas do Laptop
"""
brand = st.selectbox(
    "Qual a marca?",
    ("Dell", "Lenovo", "Asus", "HP", "Outro"))

touchscreen = st.selectbox(
    "Possui touchscreen (tela sensive ao toque)?",
    ("Sim", "Não"))

processor_brand = st.selectbox(
    "Qual a marca do processador?",
    ("Intel", "AMD", "M1"))

warranty = st.number_input(
    "Qual o tempo de garantia restante (em meses)?",
    step=1,placeholder="Coloque 0, se nao houver garantia.")

brand_option = st.selectbox(
    "Qual o nome do processador?",
    ("Core i3", "Core i5", "Core i7", "Ryzen 5", "Outro"))

os_bit = st.radio(
    "Qual a arquitetura do sistema operacional?",
    ("32 bits", "64 bits"))

os_brand = st.radio(
    "Qual a marca do sistema operacional?",
    ("Windows", "Outro"))

weight = st.radio(
    "Qual o peso do laptop?",
    ["Casual","Gaming","Thinlight"],
    captions= ["Peso Padrão", "Leve","Pesado"])

ram_type = st.radio(
    "Qual o tipo de memória RAM?",
    ["DDR4", "Outro"])

ram_size = st.number_input(
    "Qual o tamanho da memória RAM (em GB)?",step=4)

graphics_card = st.number_input(
    "Qual o tamanho da placa de vídeo (em GB)?",step=4)

hdd_size = st.number_input(
    "Qual o tamanho do HD (em GB)?",step=512,placeholder="Coloque 0, se nao houver apenas HD.")

ssd_size = st.number_input(
    "Qual o tamanho do SSD (em GB)?",step=128,placeholder="Coloque 0, se nao houver apenas SSD.")

if brand_option == "Outro":
    brand_option = "other"
    
if os_brand == "Outro":
    os_brand = "other"
    
if ram_type == "Outro":
    ram_type = "other"
    
os_bit = os_bit.replace(" bits", "")

if touchscreen == "Sim":
    touchscreen = 1
else:
    touchscreen = 0

payload = { "data": {
        "brand": brand.lower(),  
        "processor_brand": processor_brand.lower(),
        "processor_name": brand_option.lower(),
        "os": os_brand.lower(),
        "weight": weight.lower(),
        "warranty": warranty,
        "touchscreen": touchscreen,
        "ram_gb": ram_size,
        "hdd": hdd_size,
        "ssd": ssd_size,
        "graphic_card": graphics_card,
        "ram_type": ram_type.lower(),
        "os_bit": os_bit
    }
}

if st.button("Estimar Preço"):
    with st.spinner("Calculando..."):
        get_prediction(payload)