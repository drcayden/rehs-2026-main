from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

ki_hex = "4c96e7927095c3453e3c3d0f3cd969b0"  # Replace with your Ki
op_hex = "a04067bc3777d878faaec6c3a0fb3efd"  # Replace with your OP

ki = bytes.fromhex(ki_hex)
op = bytes.fromhex(op_hex)

cipher = Cipher(algorithms.AES(ki), modes.ECB())
encryptor = cipher.encryptor()
aes_out = encryptor.update(op) + encryptor.finalize()

opc = bytes(a ^ b for a, b in zip(aes_out, op))
print("OPc:", opc.hex())
