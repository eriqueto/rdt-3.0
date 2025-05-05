import random
import hashlib
import struct

# Simular perda e corrupção
def should_drop_packet(loss_prob):
    return random.random() < loss_prob

def corrupt_packet(packet, corruption_prob):
    if random.random() < corruption_prob:
        #inverte  um byte aleatório
        index = random.randint(0, len(packet) - 1)
        corrupted = bytearray(packet)
        corrupted[index] ^= 0xFF
        return bytes(corrupted)
    return packet

#checksum que checa se tem o mesmo tanto de bits 1
def calculate_checksum(data: bytes) -> int:
    count = 0
    for byte in data:
        count += bin(byte).count('1')  
    return count % 256 


def make_packet(seq, data: bytes, ack_flag=0) -> bytes:
    checksum = calculate_checksum(data)
    return struct.pack('!B B H', seq, ack_flag, checksum) + data


def parse_packet(packet: bytes):
    seq, ack, checksum = struct.unpack('!B B H', packet[:4])
    data = packet[4:]
    return seq, ack, checksum, data
