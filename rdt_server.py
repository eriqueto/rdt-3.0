import socket

# Constantes para o protocolo
MAX_SEQ_NUM = 1  # Máximo de números de sequência (0 ou 1)
SEQ_NUM = 0  # Número de sequência esperado
SERVER_ADDRESS = ('localhost', 8080)

def handle_packet(packet, expected_seq_num):
    # Verifica se o número de sequência está correto
    seq_num, data = packet.split(b":", 1)
    seq_num = int(seq_num)

    if seq_num == expected_seq_num:
        print(f"Recebido pacote válido: {data.decode()}")
        return f"ACK:{seq_num}".encode()
    else:
        print("Erro de sequência, ignorando pacote.")
        return f"NAK:{expected_seq_num}".encode()

def main():
    # Criando o socket do servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(SERVER_ADDRESS)

    print("Servidor aguardando pacotes...")

    while True:
        packet, client_address = server_socket.recvfrom(1024)
        ack = handle_packet(packet, SEQ_NUM)
        
        # Enviar ACK ou NAK para o cliente
        server_socket.sendto(ack, client_address)
        
        # Alterar o número de sequência esperado
        if ack.startswith(b"ACK"):
            SEQ_NUM = (SEQ_NUM + 1) % (MAX_SEQ_NUM + 1)

if __name__ == "__main__":
    main()
