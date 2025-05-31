import cv2
import os
import numpy as np
from time import sleep
import serial

# Pasta onde os rostos serão salvos
PASTA_TREINO = "rosto_autorizados/"
ARQUIVO_MODELO = "modelo.yml"
os.makedirs(PASTA_TREINO, exist_ok=True)

# Carregador de rosto com HaarCascade
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Função para capturar rostos e salvar
def cadastrar_rosto(nome):
    webcam = cv2.VideoCapture(0)
    count = 0
    while count < 50:
        _, frame = webcam.read()
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostos = detector.detectMultiScale(cinza, 1.3, 5)
        for (x, y, w, h) in rostos:
            rosto = cinza[y:y+h, x:x+w]
            cv2.imwrite(f"{PASTA_TREINO}/{nome}_{count}.jpg", rosto)
            count += 1
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        cv2.imshow("Cadastro - Pressione ESC para cancelar", frame)
        if cv2.waitKey(1) == 27:
            break
    webcam.release()
    cv2.destroyAllWindows()
    print(f"Coletadas {count} imagens do rosto de {nome}")

# Função para treinar o modelo com os rostos salvos
def treinar_modelo():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    imagens, labels = [], []
    nomes = {}
    id_atual = 0

    for arquivo in os.listdir(PASTA_TREINO):
        if not arquivo.endswith(".jpg"):
            continue
        caminho = os.path.join(PASTA_TREINO, arquivo)
        imagem = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)
        nome = arquivo.split("_")[0]
        if nome not in nomes:
            nomes[nome] = id_atual
            id_atual += 1
        imagens.append(imagem)
        labels.append(nomes[nome])

    recognizer.train(imagens, np.array(labels))
    recognizer.save(ARQUIVO_MODELO)
    with open("rosto_autorizados/nomes.txt", "w") as f:
        for nome, idx in nomes.items():
            f.write(f"{idx}:{nome}\n")
    print("Modelo treinado com sucesso!")

# Função para reconhecer rostos ao vivo
def reconhecer_rosto():
    if not os.path.exists(ARQUIVO_MODELO):
        print("Modelo não treinado. Cadastre e treine primeiro.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(ARQUIVO_MODELO)

    nomes = {}
    with open("face_id/nomes.txt") as f:
        for linha in f:
            idx, nome = linha.strip().split(":")
            nomes[int(idx)] = nome

    porta = "/dev/ttyUSB0"  # ou "COM3" no Windows
    velocidade = 9600
    try:
        arduino = serial.Serial(porta, velocidade, timeout=1)
        sleep(2)
    except:
        print("Não foi possível conectar ao Arduino.")
        arduino = None

    webcam = cv2.VideoCapture(0)
    print("Pressione ESC para sair.")

    while webcam.isOpened():
        ret, frame = webcam.read()
        if not ret:
            break

        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostos = detector.detectMultiScale(cinza, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in rostos:
            rosto = cinza[y:y+h, x:x+w]
            id_predito, confianca = recognizer.predict(rosto)
            nome = nomes.get(id_predito, "Desconhecido")
            cor = (0, 255, 0) if confianca < 80 else (0, 0, 255)
            texto = f"{nome} ({int(confianca)})" if confianca < 80 else "Desconhecido"

            if arduino:
                if confianca < 80:
                    arduino.write(b'A')  # Acende LED
                else:
                    arduino.write(b'a')  # Apaga LED

            cv2.rectangle(frame, (x, y), (x+w, y+h), cor, 2)
            cv2.putText(frame, texto, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, cor, 2)

        cv2.imshow("Reconhecimento Facial + Arduino", frame)
        if cv2.waitKey(30) == 27:
            break

    webcam.release()
    cv2.destroyAllWindows()
    if arduino:
        arduino.close()


# Menu simples
def menu():
    while True:
        print("\n=== FACE ID COM OPENCV ===")
        print("1. Cadastrar rosto")
        print("2. Treinar modelo")
        print("3. Iniciar reconhecimento")
        print("0. Sair")
        op = input("Escolha: ")
        if op == "1":
            nome = input("Digite o nome da pessoa: ").strip().lower()
            sleep(3)
            cadastrar_rosto(nome)
        elif op == "2":
            treinar_modelo()
        elif op == "3":
            reconhecer_rosto()
        elif op == "0":
            break
        else:
            print("Opção inválida.")

menu()
