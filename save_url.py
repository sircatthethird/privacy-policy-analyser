from flask import Blueprint, request
import polipy

save_url = Blueprint('save_url', __name__)

# Flask route to handle POST requests for saving URL
@save_url.route('/save_url', methods=['POST', 'GET'])
def save_url_route():
    # Get the URL from the request body
    url = request.data.decode('utf-8')
    
    # Perform any desired action with the URL
    result = polipy.get_policy(url)

    result.save(output_dir='policies')
    # Return a response indicating success
    return 'URL received successfully'
