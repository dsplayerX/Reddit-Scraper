import base64


def decodeCreds():
    encoded_msg = open("creds.txt", "r").read()
    bs64_bytes = encoded_msg.encode('ascii')
    msg_bytes = base64.b64decode(bs64_bytes)
    decoded_msg = msg_bytes.decode('ascii')
    access_secret = decoded_msg.splitlines()
    return access_secret


def encodeCreds(uID, uSec):
    access_secret = uID + "\n" + uSec
    msg_bytes = access_secret.encode('ascii')
    bs64_bytes = base64.b64encode(msg_bytes)
    encoded_msg = bs64_bytes.decode('ascii')
    file = open("creds.txt", "w")
    file.write(encoded_msg)
    file.close()

