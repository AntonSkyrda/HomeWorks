import socket
import argparse


class RpcVal:
    def __init__(self, key):
        self.key = key


class RpcClient:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.local_data = {}

    def _send_request(self, request):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.host, self.port))
                client_socket.sendall(request.encode())
                response = client_socket.recv(1024).decode()
            return response
        except Exception as e:
            return f"Error: {str(e)}"

    def __getitem__(self, key):
        if key in self.local_data:
            return self.local_data[key]
        response = self._send_request(f'get "{key}"')
        if response.startswith("Result:"):
            return int(response.split(":")[1].strip())
        elif "Error" in response:
            return response
        else:
            raise ValueError("Unexpected server response")

    def __setitem__(self, key, value):
        if key in self.local_data:
            self.local_data[key] = value
        else:
            if not isinstance(value, int):
                raise ValueError("Only integers are allowed for remote values")
            response = self._send_request(f'set "{key}" {value}')
            if "Error" in response:
                raise ValueError(response)

    def add_val(self, rpc_val):
        if not isinstance(rpc_val, RpcVal):
            raise ValueError("Expected an RpcVal instance")
        self.local_data[rpc_val.key] = None

    def __iadd__(self, other):
        if isinstance(other, int):
            key = next(iter(self.local_data), None)
            if key:
                self[key] += other
        return self

    def __repr__(self):
        return f"RpcClient(host={self.host}, port={self.port}, local_data={self.local_data})"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RPC Client")
    parser.add_argument("--host", required=True, help="Server host")
    parser.add_argument("--port", required=True, help="Server port")
    args = parser.parse_args()

    rpc_client = RpcClient(host=args.host, port=args.port)
    print("Client initialized.")
