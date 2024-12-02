import socket

# Глобальний словник
data = {}


def handle_request(request):
    global data
    try:
        command, *args = request.split()
        if command == "get":
            key = args[0].strip('"')
            if key in data:
                return f"Result: {data[key]}"
            return "Error: empty value"
        elif command == "set":
            key = args[0].strip('"')
            value = args[1]
            if value.isdigit():
                data[key] = int(value)
                return f"Result: {value}"
            return "Error: not a number"
        elif command == "getkeys":
            return " ".join(data.keys())
        else:
            return "Error: invalid command"
    except Exception as e:
        return f"Error: {str(e)}"


def start_server(host="0.0.0.0", port=53554):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server is listening on {host}:{port}")

        while True:
            client_socket, addr = server_socket.accept()
            with client_socket:
                print(f"Connected by {addr}")
                request = client_socket.recv(1024).decode()
                print(f"Received: {request}")
                response = handle_request(request)
                client_socket.sendall(response.encode())


if __name__ == "__main__":
    start_server()
