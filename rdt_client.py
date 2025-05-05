import socket, time
from utils import make_packet, should_drop_packet, corrupt_packet, parse_packet, calculate_checksum

RTT_EST = 1.0 #tempo que leva pro pacote ir e voltar com o ACK
ALPHA = 0.125
PORT = 5001
PROB_PERDA= 0.1
PROB_CORROMP = 0.1

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(RTT_EST)
server_address = ('127.0.0.1', PORT)

seq = 0
rtt_est = RTT_EST

def send_data(data):
    global seq, rtt_est
    packet = make_packet(seq, data)

    while True:
        start = time.time()
        if not should_drop_packet(PROB_PERDA):
            to_send = corrupt_packet(packet, PROB_CORROMP)
            client.sendto(to_send, server_address)
            print(f"[SEND] Seq={seq} | Data={data}")
        else:
            print(f"[DROP] Simulated loss: Seq={seq}")

        try:
            response, _ = client.recvfrom(1024)
            ack_seq, ack_flag, recv_checksum, _ = parse_packet(response)

            if recv_checksum != calculate_checksum(response[4:]):
                print("[CORRUPT] ACK corrompido. Ignorando.")
                continue

            if ack_flag == 1 and ack_seq == seq:
                rtt_sample = time.time() - start
                rtt_est = (1 - ALPHA) * rtt_est + ALPHA * rtt_sample #formula de cálculo de tempo
                client.settimeout(rtt_est) #atualiza o timeout para o novo
                print(f"[ACK] Recebido ACK {ack_seq} | RTT: {rtt_sample:.4f} | Timeout: {rtt_est:.4f}")
                seq ^= 1
                break
        except socket.timeout:
            print(f"[TIMEOUT] Retransmitindo seq={seq}")

for i in range(10):
    send_data(f"Msg {i}".encode())
