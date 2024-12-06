import requests

def is_google_analytics_installed(url):
    """
    Check if Google Analytics is installed on a given website.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        # Basic patterns to detect Google Analytics
        patterns = [
            "gtag('config',",      # For gtag.js
            "GoogleAnalyticsObject",  # For analytics.js
            "_gaq.push",          # For legacy ga.js
            "googletagmanager.com",  # Google Tag Manager
        ]

        for pattern in patterns:
            if pattern in html_content:
                return True

        return False

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    website_url = input("Enter website URL (include http or https): ")
    if not website_url.startswith("http"):
        website_url = "https://" + website_url

    if is_google_analytics_installed(website_url):
        print("Google Analytics is installed!")
    else:
        print("Google Analytics is NOT installed.")
