from mindee import Client, product


class ReceiptParser:
    def __init__(self, api_key):
        self.mindee_client = Client(api_key=api_key)

    def extract_bill_details(self, receipt_data):
        output = {
            "Name": receipt_data.document.inference.prediction.supplier_name.value or '',
            "Invoice No": receipt_data.document.inference.prediction.receipt_number.value or '',
            "Amount": receipt_data.document.inference.prediction.total_amount.value,
            "Tax": receipt_data.document.inference.prediction.total_tax.value,
            "Net": receipt_data.document.inference.prediction.total_net.value,
            "Category": receipt_data.document.inference.prediction.category.value,
            "Date": receipt_data.document.inference.prediction.date.value,
            "Mode": "Credit Card",
        }
        print(f"Bill details: {output}")
        return output

    def parse_reciept_from_base64(self, base64_string, image_name):
        input_doc = self.mindee_client.source_from_b64string(base64_string, image_name)
        receipt_data = self.mindee_client.parse(product.ReceiptV5, input_doc)
        result = self.extract_bill_details(receipt_data)
        return result

