import base64
print(base64.b64encode(b'y2="17"></line>').decode())
print(base64.b64encode(b'y2="17;"></line>').decode())
