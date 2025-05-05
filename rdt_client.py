import socket
import time

# Constantes para o protocolo
TIMEOUT = 1  # Timeout para esperar pelo ACK
SEQ_NUM = 0  # Número de sequência (0 ou 1)
MAX_SEQ_NUM = 1  # Máximo de números de sequência (0 ou 1)
SERVER_ADDRESS = ('localhost', 8080)

def create_packet(data, seq_num):
    # Criação de pacotes simples
    return f"{seq_num}:{data}".encode()

def send_packet(client_socket, data):
    global SEQ_NUM
    packet = create_packet(data, SEQ_NUM)
    
    while True:
        # Enviar pacote
        client_socket.sendto(packet, SERVER_ADDRESS)
        print(f"Enviado pacote: {packet}")
        
        # Esperar pelo ACK
        client_socket.settimeout(TIMEOUT)
        try:
            ack, _ = client_socket.recvfrom(1024)
            if ack == f"ACK:{SEQ_NUM}".encode():
                print(f"Recebido ACK para seq {SEQ_NUM}")
                SEQ_NUM = (SEQ_NUM + 1) % (MAX_SEQ_NUM + 1)  # Alternar entre 0 e 1
                break
        except socket.timeout:
            print("Timeout! Retransmitindo...")

def main():
    # Criando o socket do cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Enviar pacotes com dados
    for i in range(5):
        data = f"Mensagem {i+1}"
        send_packet(client_socket, data)
    
    client_socket.close()

if __name__ == "__main__":
    main()
