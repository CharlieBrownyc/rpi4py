import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='localhost', help='IP address')
parser.add_argument('--port', type=int, default=10000, help='Port number')
args = parser.parse_args()
server_address = args.host
server_port = args.port
# 서버 설정
# server_address = "127.0.0.1"  # 서버의 실제 IP 주소 또는 도메인 이름
# server_port = 10000         # 서버 포트 번호

# 서버에 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_address, server_port))

# 데이터 전송
name = "hey server"
message = "안녕, 서버!"

request = f"{name}&&{message}"
client_socket.send(request.encode("utf-8"))

# 서버로부터 응답 받기
response = client_socket.recv(4096).decode("utf-8")
print(f"{name} : \n{message}")
print(f"서버 : \n{response}\n")

# 클라이언트 소켓 닫기
client_socket.close()