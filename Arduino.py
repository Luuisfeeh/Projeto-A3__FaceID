import serial
import time

porta = "COM3"
velocidade = 9600

try:
    conexao = serial.Serial(porta, velocidade, timeout=1)
    time.sleep(2)  # Dá tempo para o Arduino reiniciar

    while True:
        opcao = input("A-ACENDE -- a-APAGA: ")

        if opcao == "A":
            conexao.write(b'A')
        elif opcao == "a":
            conexao.write(b'a')

except serial.SerialException as e:
    print(f"Erro na conexão serial: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
finally:
    conexao.close()
    print("Conexão encerrada.")