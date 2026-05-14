
from utils.validators import determine_target_type
from utils.http_client import HTTPClient

# Test Validators
print(f"Target 'admin@nasa.gov' is: {determine_target_type('admin@nasa.gov')}")
print(f"Target 'google.com' is: {determine_target_type('google.com')}")
print(f"Target '+15551234567' is: {determine_target_type('+15551234567')}")
print(f"Target 'cyber_king' is: {determine_target_type('cyber_king')}")

# Test HTTP Client
client = HTTPClient()
response = client.get("https://api.github.com/zen")
if response['error']:
    print(f"HTTP Error: {response['error']}")
else:
    print(f"GitHub Zen: {response['data']}")