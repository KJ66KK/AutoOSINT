from core.models import ModuleResult
from utils.http_client import HTTPClient
import re

class SocialScanModule:
    """
    Advanced social media scanner inspired by the Sherlock project.
    Uses multi-factor detection (Status Code + Error Text) to ensure accuracy.
    """
    def __init__(self):
        self.http_client = HTTPClient()
        # Expanded platform list with specific "Not Found" strings to prevent false positives
        self.platforms = {
            "GitHub": {"url": "https://github.com/{}", "error": "Not Found"},
            "Twitter": {"url": "https://nitter.net/{}", "error": "not found"},
            "Reddit": {"url": "https://www.reddit.com/user/{}", "error": "page not found"},
            "Instagram": {"url": "https://www.instagram.com/{}/", "error": "Login"},
            "Facebook": {"url": "https://www.facebook.com/{}", "error": "content isn't available"},
            "LinkedIn": {"url": "https://www.linkedin.com/in/{}", "error": "Page Not Found"},
            "TikTok": {"url": "https://www.tiktok.com/@{}", "error": "Couldn't find this account"},
            "Twitch": {"url": "https://www.twitch.tv/{}", "error": "content is unavailable"},
            "Spotify": {"url": "https://open.spotify.com/user/{}", "error": "Page not found"},
            "SoundCloud": {"url": "https://soundcloud.com/{}", "error": "SoundCloud doesn't recognize"},
            "GitLab": {"url": "https://gitlab.com/{}", "error": "404"},
            "Bitbucket": {"url": "https://bitbucket.org/{}/", "error": "404"},
            "Medium": {"url": "https://medium.com/@{}", "error": "404"},
            "Behance": {"url": "https://www.behance.net/{}", "error": "404"},
            "Dribbble": {"url": "https://dribbble.com/{}", "error": "404"},
            "Pinterest": {"url": "https://www.pinterest.com/{}/", "error": "404"},
            "Snapchat": {"url": "https://www.snapchat.com/add/{}", "error": "404"},
            "Telegram": {"url": "https://t.me/{}", "error": "If you have Telegram"}, # Check for bio text
            "Keybase": {"url": "https://keybase.io/{}", "error": "404"},
            "Steam": {"url": "https://steamcommunity.com/id/{}", "error": "The specified profile could not be found"},
            "Xbox": {"url": "https://www.xboxgamertag.com/search/{}", "error": "not found"},
            "PlayStation": {"url": "https://psnprofiles.com/{}", "error": "404"},
            "HackerNews": {"url": "https://news.ycombinator.com/user?id={}", "error": "No such user"},
            "Venmo": {"url": "https://venmo.com/u/{}", "error": "404"},
            "CashApp": {"url": "https://cash.app/${}", "error": "404"},
            "Roblox": {"url": "https://www.roblox.com/user.aspx?username={}", "error": "404"},
            "WordPress": {"url": "https://{}.wordpress.com", "error": "doesn’t exist"},
            "Tumblr": {"url": "https://{}.tumblr.com", "error": "404"},
            "Flickr": {"url": "https://www.flickr.com/people/{}", "error": "404"},
            "ProductHunt": {"url": "https://www.producthunt.com/@{}", "error": "404"},
            "Kaggle": {"url": "https://www.kaggle.com/{}", "error": "404"},
            "Quora": {"url": "https://www.quora.com/profile/{}", "error": "404"},
            "Goodreads": {"url": "https://www.goodreads.com/user/show/{}", "error": "404"}
        }

    def scan(self, username: str) -> ModuleResult:
        found_on = []
        profile_links = {}
        error_msg = None
        pivots = []

        for platform, config in self.platforms.items():
            url = config["url"].format(username)
            response = self.http_client.get(url)
            
            if response["status_code"] == 200:
                page_content = str(response["data"])
                
                # REFINED DETECTION: Check for specific "Not Found" error strings
                # If the error string IS found, it means the user DOES NOT exist.
                if config["error"].lower() in page_content.lower():
                    continue
                    
                found_on.append(platform)
                profile_links[platform] = url
                
                # EXTRACT DATA FOR DEEP SCAN (-D)
                # Emails
                emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", page_content)
                for email in set(emails):
                    if email not in [p["value"] for p in pivots]:
                        pivots.append({"type": "email", "value": email})
                
                # Phone Numbers
                phones = re.findall(r"[\+\(]?[1-9][0-9 .\-\(\)]{8,15}[0-9]", page_content)
                for phone in set(phones):
                    if phone not in [p["value"] for p in pivots]:
                        pivots.append({"type": "phone", "value": phone})

        success = len(found_on) > 0
        return ModuleResult(
            module_name="SocialScan",
            target=username,
            success=success,
            data={
                "platforms_searched": len(self.platforms),
                "platforms_found": len(found_on),
                "profile_links": profile_links
            },
            pivots=pivots,
            confidence="HIGH" if len(found_on) > 0 else "LOW",
            error=error_msg
        )
