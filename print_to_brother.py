import os

from brother_ql.backends.helpers import send
from brother_ql.conversion import convert
from brother_ql.raster import BrotherQLRaster
from dotenv import load_dotenv

load_dotenv()

printer_vendor_id = os.environ["GATEWAY_PRINTER_VENDOR_ID"]
printer_product_id = os.environ["GATEWAY_PRINTER_PRODUCT_ID"]
printer_serial_no = os.environ["GATEWAY_PRINTER_SERIAL_NO"]

IDENTIFIER = f"usb://{printer_vendor_id}:{printer_product_id}/{printer_serial_no}"


def send_data_to_printer(instructions):
    identifier = IDENTIFIER
    selected_backend = "pyusb"
    send(
        instructions=instructions,
        printer_identifier=identifier,
        backend_identifier=selected_backend,
        blocking=True,
    )


def print_label_from_image(png_in, delete_after_print=False):
    printerdata_model = "QL-810W"

    qlr = BrotherQLRaster(printerdata_model)
    qlr.exception_on_warning = True
    # qlr.mlength = 0 # Trying to kill the margins
    # qlr.mlength(0) # Trying to kill the margins
    # qlr.mwidth = 0     # Trying to kill the margins
    # label_type_specs["12"]["feed_margin"] = 50  # modify settings of label type "62red"
    instructions = convert(
        qlr=qlr,
        images=[png_in],  # Takes a list of file names or PIL objects.
        label="12",
        rotate="90",  # 'auto', '0', '90', '270'
        threshold=70.0,  # Black and white threshold in percent.
        dither=False,
        compress=False,
        red=False,  # Only True if using Red/Black 62 mm label tape.
        dpi_600=False,
        hq=True,  # False for low quality.
        cut=True,
    )

    # The "feed_margin" data is taken from the label. In this case, the "62red" has a margin of 35. Thiis is then called in convert() where: qlr.add_margins(label_specs['feed_margin'])
    # I tried to then set it here with 0, but it seems to do nothing...
    qlr.add_margins(0)
    qlr.mlength = 0

    status = send_data_to_printer(
        instructions
    )  # This just adds the printer IP and tells it to send the request via the network.
    if delete_after_print:
        os.remove(png_in)
    return status
