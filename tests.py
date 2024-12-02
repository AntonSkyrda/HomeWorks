from rpc_client import RpcClient, RpcVal

rpc_client = RpcClient(host="127.0.0.1", port="53554")
rpc_client["x"] = 4
rpc_client.add_val(RpcVal("y"))
rpc_client["y"] = 5
rpc_client["y"] += 4
result = rpc_client["x"] + rpc_client["y"]
