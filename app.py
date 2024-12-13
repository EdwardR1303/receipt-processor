import uuid
from flask import jsonify, request, Flask

from receipt_processor import ReceiptProcessor

app = Flask(__name__)

RECEIPTS = {}

@app.route('/')
def home():
    return "Receipt Processor."

@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):

    rp = ReceiptProcessor(RECEIPTS[id])

    return jsonify({'message': f'Receipt processed successfully. Receipt id: {id}',
                    'points': rp.total_points,
                    "recepit": RECEIPTS[id]})

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt = request.json
    receipt_id = uuid.uuid4()
    RECEIPTS[str(receipt_id)] = receipt
    print(f'New receipt created, {receipt_id}')

    return jsonify({'id': receipt_id})

@app.route('/receipts/getall', methods=['GET'])
def get_all():
    return jsonify(RECEIPTS)

if __name__ == '__main__':
    with app.test_request_context():
        print(app.url_map)
    app.run(debug=True, host='0.0.0.0', port=5000)