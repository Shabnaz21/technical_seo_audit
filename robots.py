import requests

def check_robots_txt(domain):
    """
    Check if robots.txt exists and whether it contains "User-agent: *".
    """
    robots_url = f"{domain}/robots.txt"  # Robots.txt URL

    try:
        # Step 1: Fetch robots.txt
        response = requests.get(robots_url, timeout=10)
        
        # Handle different HTTP responses
        if response.status_code == 200:
            print("✅ robots.txt file exists!")
            
            # Step 2: Check if "User-agent: *" is present in the file
            robots_content = response.text
            if "User-agent: *" in robots_content:
                print("✅ robots.txt file exists & Okay!")
            else:
                print("❌ robots.txt file is missing 'User-agent: *'.")
        
        elif response.status_code == 404:
            print("❌ robots.txt file not found (404 error).")
        else:
            print(f"❌ robots.txt file is inaccessible. HTTP status code: {response.status_code}")
    
    except requests.RequestException as e:
        print(f"❌ Failed to fetch robots.txt due to error: {e}")

# Replace with the domain you want to check
domain = "https://www.universepg.com/"  
check_robots_txt(domain)
