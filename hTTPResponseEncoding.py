import requests

# Your URL (replace with your actual URL)
url = "https://neolook.com/archives/20230802d"

# Send a GET request and get the response
response = requests.get(url)

# Check the HTTP response encoding (Content-Type header)
content_type = response.headers.get('Content-Type')
if content_type:
    content_type_parts = content_type.split(';')
    if len(content_type_parts) > 1 and 'charset=' in content_type_parts[1]:
        encoding = content_type_parts[1].split('charset=')[1].strip()
    else:
        # Default to 'utf-8' if no charset is specified
        encoding = 'utf-8'
    print(f"The HTTP response encoding is: {encoding}")
else:
    print("The 'Content-Type' header is missing in the HTTP response.")
