from core.models import ModuleResult
from utils.http_client import HTTPClient

class SocialScanModule:
    """
    Checks for the existence of a username across multiple social platforms.
    """
    def __init__(self):
        self.http_client = HTTPClient()
        # EXPANSION POINT:
        # To add a NEW platform:
        # 1. Add the site name and its URL template to this dictionary.
        # 2. Ensure the {} is where the username should go.
        self.platforms = {
            "GitHub": "https://github.com/{}",
            "Twitter": "https://nitter.net/{}", 
            "Reddit": "https://www.reddit.com/user/{}",
            "Instagram": "https://www.instagram.com/{}/"
        }

    def scan(self, username: str) -> ModuleResult:
        found_on = []
        profile_links = {}
        error_msg = None

        for platform, url_template in self.platforms.items():
            url = url_template.format(username)
            # PRO TIP:
            # Some sites (like Instagram) might return 200 even if the user is missing
            # but has a 'Login' redirect. To be 100% sure, check for a 'Not Found' 
            # string in the response.text.
            response = self.http_client.get(url)
            
            if response["status_code"] == 200:
                found_on.append(platform)
                profile_links[platform] = url
            elif response["error"]:
                # Just log the first error if it happens, but continue
                error_msg = response["error"]

        success = len(found_on) > 0 or error_msg is None

        return ModuleResult(
            module_name="SocialScan",
            target=username,
            success=success,
            data={
                "found_on": found_on,
                "profile_links": profile_links
            },
            confidence="HIGH" if len(found_on) > 0 else "LOW",
            error=error_msg if not success else None
        )
