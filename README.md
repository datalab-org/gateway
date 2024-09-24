To install:
```uv sync```

You will also need libusb installed in order to use a usb printer. On mac, this can be done with:
```brew install libusb```

Printer details are specified via environment variables. See `dotenv_template` for an example.

To get the USB identifier for a printer on mac, use:

`system_profiler SPUSBDataType`

The format of the identifier is: "usb://{vendor id}:{product id}/{serial number}

To run the server:
```uv run fastapi dev main.py```

And some useful `curl` commands for testing:
```curl -X POST "http://127.0.0.1:8000/print-label" -F "file=@/resources/example_image.png"```
```curl -X POST "http://127.0.0.1:8000/print-label" -H "Content-Type: application/json" -d '{"item_id":"abc100", "name":"a laboratory sample","url":"https://datalab.bocarslygroup.com", "hcodes":["h101", "h202"], "dryrun":0}```