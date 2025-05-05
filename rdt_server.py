import socket
from utils import make_packet, parse_packet, calculate_checksum


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 5001))
print("[START] Servidor escutando na porta 5001")

expected_seq = 0

while True:
    data, addr = server.recvfrom(1024)
    seq, ack_flag, recv_checksum, payload = parse_packet(data)

    if calculate_checksum(payload) != recv_checksum:
        print(f"[CORRUPT] Pacote corrompido ignorado.")
        continue

    if seq == expected_seq:
        print(f"[RECEBIDO] Seq={seq} | Data={payload.decode()}")
        ack = make_packet(seq, b'')  # ACK tem flag 1
        ack = bytearray(ack)
        ack[1] = 1  # Define o campo ACK
        server.sendto(bytes(ack), addr)
        expected_seq ^= 1
    else:
        print(f"[DUPLICATA] Ignorado seq={seq}")
        ack = make_packet(seq ^ 1, b'')
        ack = bytearray(ack)
        ack[1] = 1
        server.sendto(bytes(ack), addr)
