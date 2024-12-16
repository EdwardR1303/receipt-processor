import uuid
import markdown
from flask import jsonify, request, Flask, abort

from receipt_processor import ReceiptProcessor

app = Flask(__name__)

RECEIPTS = {}
RECEIPT_POINTS = {}

@app.route('/')
def home():
    with open("README.md", 'r') as f:
        text = f.read()
        html = markdown.markdown(text)
    return html

@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):

    total_points = RECEIPT_POINTS.get(id, 'N/A')

    if total_points == 'N/A':
        abort(404, description='No receipt found for that ID.')
        response = {
            'message': 'No receipt found for that ID.'
        }
    else:
        response = {
            'points': total_points
        }

    return jsonify(response)

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt = request.json

    try:
        rp = ReceiptProcessor(receipt)
    except Exception as e:
        print(e)
        abort(400, description='The receipt is invalid.')
    
    receipt_id = str(uuid.uuid4())
    RECEIPTS[receipt_id] = receipt
    RECEIPT_POINTS[receipt_id] = rp.total_points
    print(f'New receipt created, {receipt_id}')

    return jsonify({'id': receipt_id})

@app.route('/receipts/getall', methods=['GET'])
def get_all():
    return jsonify(RECEIPTS)

if __name__ == '__main__':
    with app.test_request_context():
        print(app.url_map)
    app.run(debug=True, host='0.0.0.0', port=5000)