from django.core.management.base import BaseCommand
from receipts.models import Receipt, Item
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import unicodedata


def normalize_ukrainian(text: str) -> str:
    text = unicodedata.normalize('NFC', text).lower()
    replacements = {
        'i': 'і',  # Latin i → Cyrillic і
        # 'I': 'І',
        'e': 'е',  # Latin e → Cyrillic е
        # 'E': 'Е',
        'o': 'о',  # Latin o → Cyrillic о
        # 'O': 'О',
        'a': 'а',  # Latin a → Cyrillic а
        # 'A': 'А',
        'p': 'р',  # Latin p → Cyrillic р
        # 'P': 'Р',
        'c': 'с',  # Latin c → Cyrillic с
        # 'C': 'С',
        'x': 'х',  # Latin x → Cyrillic х
        # 'X': 'Х'
    }
    for latin, cyrillic in replacements.items():
        text = text.replace(latin, cyrillic)
    return text


def parse_product(element, discounts):
    n = int(element.attrib.get("N", 0))
    name = normalize_ukrainian(element.attrib.get("NM", ""))
    code = element.attrib.get("C", "")
    barcode = element.attrib.get("CD", "")
    price = float(element.attrib.get("PRC", "0")) / 100
    qty = float(element.attrib.get("Q", "1000")) / 1000  # grams → kg
    sm = float(element.attrib.get("SM", "0")) / 100

    # apply item-level discount
    discount = discounts.get(n, 0.0)
    final_amount = sm - discount
    try:
        final_price = final_amount / qty
    except ZeroDivisionError:
        print(name, final_amount, qty)

    if 'яйце' in name:
        if (price > 30) or price == 0:
            qty *= 10
            final_price = round(sm / qty, 2)
    return (name, code, barcode, final_price, qty, final_amount, discount)


def parse_receipt(xml_string):
    root = ET.fromstring(xml_string)
    dat = root.find("DAT")  # <Element 'DAT'>
    if dat is None:
        return None

    e = dat.find(".//E")

    if e is not None:
        total_amount = float(e.attrib.get("SM", "0")) / 100
        receipt_number = e.attrib.get("NO", 0)
        raw_tstime = e.attrib.get("TS")
        ts_obj = datetime.strptime(raw_tstime, "%Y%m%d%H%M%S")
        ts_iso = ts_obj.strftime("%Y-%m-%d %H:%M:%S")

    if not Receipt.objects.filter(receipt_number=receipt_number).exists():
        print(f"Receipt {receipt_number} is ready to set up")
        receipt = Receipt.objects.create(
            receipt_number=receipt_number,
            date_time=ts_iso,
            total_amount=total_amount
        )

        discounts = {
            int(d.attrib["NI"]): float(d.attrib["SM"]) / 100 for d in dat.findall(".//D")
        }

        for p in dat.findall(".//P"):
            name, code, barcode, price, qty, final_amount, discount = parse_product(
                p, discounts)

            Item.objects.create(
                name=name,
                code=code,
                barcode=barcode,
                price=price,
                quantity=qty,
                sum=final_amount,
                discount=discount,
                receipt=receipt
            )

        print(f"Receipt {receipt_number} was successfully added!")


class Command(BaseCommand):
    help = "Import XML receipts from a folder into the database"

    def add_arguments(self, parser):
        parser.add_argument('folder', type=str,
                            help='Folder with XML receipts')

    def handle(self, *args, **options):
        folder = Path(options['folder'])

        for file in folder.glob("*.xml"):
            with open(file, encoding='cp1251') as f:
                xml_string = f.read()
                parse_receipt(xml_string)
