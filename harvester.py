import urllib.request, re, zipfile, io, json, base64

def harvest_vpnbook():
    servers = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    bundles = [
        {"country": "United States", "code": "US", "url": "https://www.vpnbook.com/free-openvpn-account/VPNBook.com-OpenVPN-US1.zip"},
        {"country": "United States", "code": "US", "url": "https://www.vpnbook.com/free-openvpn-account/VPNBook.com-OpenVPN-US2.zip"},
        {"country": "Canada", "code": "CA", "url": "https://www.vpnbook.com/free-openvpn-account/VPNBook.com-OpenVPN-CA198.zip"},
        {"country": "France", "code": "FR", "url": "https://www.vpnbook.com/free-openvpn-account/VPNBook.com-OpenVPN-FR1.zip"},
        {"country": "Germany", "code": "DE", "url": "https://www.vpnbook.com/free-openvpn-account/VPNBook.com-OpenVPN-DE4.zip"}
    ]

    for b in bundles:
        try:
            req = urllib.request.Request(b['url'], headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                zip_data = io.BytesIO(resp.read())
                with zipfile.ZipFile(zip_data) as z:
                    for filename in z.namelist():
                        if filename.endswith('.ovpn') and 'tcp443' in filename:
                            content = z.read(filename).decode('utf-8', errors='ignore')
                            match = re.search(r'remote\s+([^\s]+)\s+(\d+)', content)
                            if match:
                                host = match.group(1)
                                port = int(match.group(2))
                                servers.append({
                                    "id": f"vpnbook-{b['code'].lower()}-{port}",
                                    "country": b['country'],
                                    "code": b['code'],
                                    "host": host,
                                    "port": port,
                                    "config_base64": base64.b64encode(content.encode()).decode()
                                })
        except Exception as e:
            print(f"Error fetching {b['url']}: {e}")

    return servers

if __name__ == '__main__':
    data = harvest_vpnbook()
    with open('servers.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Harvested {len(data)} live servers.")
