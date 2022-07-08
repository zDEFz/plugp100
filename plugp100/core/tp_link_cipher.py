import base64

from Crypto.Cipher import AES
from . import helpers
from .pkcs7 import PKCS7Encoder


class TpLinkCipher:
    def __init__(self, b_arr: bytearray, b_arr2: bytearray):
        self.iv = b_arr2
        self.key = b_arr

    def encrypt(self, data):
        data = PKCS7Encoder().encode(data)
        data: str
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(data.encode("UTF-8"))
        return helpers.mime_encoder(encrypted).replace("\r\n", "")

    def decrypt(self, data: str):
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        pad_text = aes.decrypt(base64.b64decode(data.encode("UTF-8"))).decode("UTF-8")
        return PKCS7Encoder().decode(pad_text)