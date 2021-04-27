import base64
import pyDes


class TripleDesUtils:
    def encryption(self, data: str, key, iv) -> str:
        """3des 加密
        """
        _encryption_result = pyDes.triple_des(key, pyDes.CBC, iv, None, pyDes.PAD_PKCS5).encrypt(data)
        _encryption_result = self._base64encode(_encryption_result).decode()
        return _encryption_result

    def decrypt(self, data: str, key, iv) -> str:
        """3des 解密
        """
        data = self._base64decode(data)
        _decrypt_result = pyDes.triple_des(key, pyDes.CBC, iv, None, pyDes.PAD_PKCS5).decrypt(data).decode('utf-8')
        return _decrypt_result

    @staticmethod
    def _base64encode(data):
        try:
            _b64encode_result = base64.b64encode(data)
        except Exception as e:
            raise Exception(f"base64 encode error:{e}")
        return _b64encode_result

    @staticmethod
    def _base64decode(data):
        try:
            _b64decode_result = base64.b64decode(data)
        except Exception as e:
            raise Exception(f"base64 decode error:{e}")
        return _b64decode_result
