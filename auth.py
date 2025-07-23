import pyotp
import qrcode
from PIL import Image
import io
from config import SECRET_KEY

class AuthManager:
    def __init__(self):
        self.totp = pyotp.TOTP(SECRET_KEY)
        self.provisioning_uri = self.totp.provisioning_uri(
            name="ZVUKERBot",
            issuer_name="ZVUKER"
        )

    def generate_qr(self):
        # Создаем QR-код
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECTION_H,
            box_size=10,
            border=4,
        )
        qr.add_data(self.provisioning_uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        byte_io = io.BytesIO()
        img.save(byte_io, 'PNG')
        byte_io.seek(0)
        return byte_io

    def verify_code(self, code):
        return self.totp.verify(code)
