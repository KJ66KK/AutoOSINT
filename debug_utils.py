import sys
import os

# Add current directory to path just in case
sys.path.append(os.getcwd())

try:
    from utils.validators import determine_target_type
    from utils.http_client import HTTPClient
    print("✅ Successfully imported utils!")
    
    # Test Validators
    email_type = determine_target_type("admin@nasa.gov")
    print(f"Test 1 (Email): {email_type}")
    
    # Test HTTP Client
    client = HTTPClient()
    print("Testing connection to GitHub API...")
    response = client.get("https://api.github.com/zen")
    if response['error']:
        print(f"❌ HTTP Error: {response['error']}")
    else:
        print(f"✅ GitHub Zen: {response['data']}")

except ImportError as e:
    print(f"❌ Import Error: {e}")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"System Path: {sys.path}")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
