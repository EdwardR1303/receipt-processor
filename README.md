# receipt-processor
A simple receipt processor as specified by the Fetch challenge.

## Usage

To run the application, use one of the `dockerrun` scripts (.sh for bash and .ps1 for powershell)<br>
This will create a docker container and publish it to the local docker registry (Docker Desktop)<br>
The port exposed is 5000.<br>
Use one of the endpoints listed below.<br>

## ENDPOINTS:
    http://localhost:5000/

    GET: /receipts/{id}/points  pass in a receipt id to receive point amount\n
    GET: /receipts/getall       receive a list of all receipts in memory\n
    POST: /receipts/process     process a single receipt\n
    
