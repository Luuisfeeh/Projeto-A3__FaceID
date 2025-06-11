

# 🔐 Face ID com Reconhecimento Facial + Arduino

Este projeto utiliza **visão computacional com Python** para reconhecimento facial e aciona um **LED conectado ao Arduino** como forma de verificação de identidade — como um **Face ID caseiro**!

---

## 📸 O que o projeto faz?

- Detecta rostos usando a webcam
- Reconhece rostos previamente cadastrados (você e/ou amigos)
- Se o rosto for reconhecido → Envia sinal para o Arduino acender o LED
- Se o rosto for desconhecido → LED permanece apagado

---

## ⚙️ Tecnologias utilizadas

- Python
  - OpenCV
  - Mediapipe (para detecção facial)
- Arduino
  - LED controlado via porta serial
- VS Code + Git
- GitHub (controle de versão)

---

## 🖥️ Como executar

### 1. Clone o repositório

git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo

2. Instale as dependências Python

pip install opencv-python mediapipe

3. Conecte seu Arduino

    Certifique-se de que está conectado à porta correta (ex: COM3 ou /dev/ttyUSB0)

    Faça o upload do código Arduino que espera os comandos A e a pela serial

4. Rode o código principal

python reconhecimento_facial.py

💡 Funcionamento do Arduino

    O Arduino recebe comandos pela porta serial:

        A → Acende o LED

        a → Apaga o LED

    O Python envia esses comandos com base no rosto detectado

📂 Estrutura sugerida do projeto

face-id-arduino/
├── reconhecimento_facial.py
├── arduino_led_serial.py
├── imagens_de_referencia/     # fotos dos rostos autorizados
├── README.md

🧠 Objetivo

Este projeto foi desenvolvido com foco em aprender mais sobre:

    Visão computacional e reconhecimento facial

    Integração entre hardware (Arduino) e software (Python)

    Aplicações reais de Machine Learning no dia a dia
