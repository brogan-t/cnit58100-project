from django.http import JsonResponse
import requests, json

def get_ip():
    api_url = "https://api.ipgeolocation.io/getip"

    try:
        # Make the HTTP GET request to the API
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Get the IP address from the JSON response
        ip_address = data.get('ip', 'Unknown')

        # Return the IP address
        return ip_address

    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., connection error, timeout)
        return JsonResponse({'error': str(e)}, status=500)
        
def get_geo(ip):
    api_url = "https://api.ipgeolocation.io/ipgeo?apiKey=bd288e943bca4361b4adb3197eaedb05&ip=" + str(ip)
    
    #test_resp = "{\n    \"ip\": \"8.8.8.8\",\n    \"hostname\": \"dns.google\",\n    \"continent_code\": \"NA\",\n    \"continent_name\": \"North America\",\n    \"country_code2\": \"US\",\n    \"country_code3\": \"USA\",\n    \"country_name\": \"United States\",\n    \"country_capital\": \"Washington, D.C.\",\n    \"state_prov\": \"California\",\n    \"district\": \"Santa Clara\",\n    \"city\": \"Mountain View\",\n    \"zipcode\": \"94043-1351\",\n    \"latitude\": \"37.42240\",\n    \"longitude\": \"-122.08421\",\n    \"is_eu\": false,\n    \"calling_code\": \"+1\",\n    \"country_tld\": \".us\",\n    \"languages\": \"en-US,es-US,haw,fr\",\n    \"country_flag\": \"https://ipgeolocation.io/static/flags/us_64.png\",\n    \"geoname_id\": \"6301403\",\n    \"isp\": \"Google LLC\",\n    \"connection_type\": \"\",\n    \"organization\": \"Google LLC\",\n    \"asn\": \"AS15169\",\n    \"currency\": {\n        \"code\": \"USD\",\n        \"name\": \"US Dollar\",\n        \"symbol\": \"$\"\n    },\n    \"time_zone\": {\n        \"name\": \"America/Los_Angeles\",\n        \"offset\": -8,\n        \"current_time\": \"2020-12-17 07:49:45.872-0800\",\n        \"current_time_unix\": 1608220185.872,\n        \"is_dst\": false,\n        \"dst_savings\": 1\n    }\n}"
    
    #data = json.loads(test_resp)
    
    #return data
    #return data.get('city', 'Unknown City') + ', ' + data.get('state_prov', 'Unknown Province') + ', ' + data.get('country_name', 'Unknown Country')
    
    try:
        # Make the HTTP GET request to the API
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the JSON response
        data = response.json()
        
        return data

    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., connection error, timeout)
        return JsonResponse({'error': str(e)}, status=500)
        
def get_location(geo):
    return geo.get('city', 'Unknown City') + ', ' + geo.get('state_prov', 'Unknown Province') + ', ' + geo.get('country_name', 'Unknown Country')