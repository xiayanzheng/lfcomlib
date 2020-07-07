from cryptography.fernet import Fernet


class Core:

    @staticmethod
    def encrypt(key, str_i):
        f = Fernet(key)
        e_token = f.encrypt(bytes(str_i, encoding='utf-8'))
        return e_token

    @staticmethod
    def decrypt(key, token):
        f = Fernet(key)
        d_str = f.decrypt(bytes(token, encoding='utf-8'))
        return d_str
