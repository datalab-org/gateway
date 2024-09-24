import qrcode
from PIL import Image, ImageDraw, ImageFont


def create_qr_img(url: str, box_size: float = 5):
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=0,
    )
    QRcode.add_data(url)
    QRcode.make()
    # adding color to QR code
    QRimg = QRcode.make_image(fill_color="Black", back_color="white").convert("RGB")
    # return the QR code generated
    return QRimg


def create_label(url, item_id: str = None, name: str = None, hcodes: list = []):
    qr_img = create_qr_img(url)
    # resize ito size of label printer
    qr_img = qr_img.resize((106, 106))
    qr_img.save("qr_only.png")

    background_img = Image.new("RGB", (500, 106), color="white")
    background_img.paste(qr_img, (0, 0), qr_img.convert("RGBA"))
    d = ImageDraw.Draw(background_img)

    header_font = ImageFont.truetype("resources/fonts/Figtree-Light.ttf", size=36)
    small_font = ImageFont.truetype("resources/fonts/Figtree-Light.ttf", size=26)

    d.text((120, 0), item_id, fill="black", font=header_font)
    d.text((120, 40), name, fill="black", font=small_font)
    d.text((120, 72), " ".join([h for h in hcodes]), fill="black", font=small_font)

    background_img.save("test.png")
    return background_img
