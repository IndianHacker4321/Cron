# JSchallenge se bachne ke liye
def jschallenge(html, valueonly = False):
    # Step 1: Get the HTML
    # Step 2: Parse the HTMLusing BeautifulSoup
    from bs4 import BeautifulSoup
    from Crypto.Cipher import AES
    import re
    soup = BeautifulSoup(html, 'html.parser')
    # Attempt to find the script tag
    script = None
    for s in soup.find_all('script'):
        if 'toNumbers' in s.string if s.string else '':
            # Check if the script contains 'toNumbers'
            script = s.string
            break
    if not script:
        raise ValueError("No script containing 'toNumbers' found on the page.")
        # Step 3: Extract the hex values (a, b, c) using regex
    # Assuming a, b, c are different and are fetched uniquely from the script
    matches = re.findall(r'toNumbers\("([0-9a-f]+)"\)', script)
    if len(matches) < 3:
        raise ValueError("Could not extract the required number of hex values (a, b, c).")

    a_hex = matches[0]
    b_hex = matches[1]
    c_hex = matches[2]

    # Helper functions
    def to_numbers(hex_str):
        return [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]

    def to_hex(byte_array):
        return ''.join(f'{byte:02x}' for byte in byte_array)

    # Step 4: Convert the hex values to byte arrays
    a = to_numbers(a_hex)
    b = to_numbers(b_hex)
    c = to_numbers(c_hex)

    # Step 5: AES decryption (assuming padding needs to be stripped)
    cipher = AES.new(bytes(a),        AES.MODE_CBC, bytes(b))
    decrypted = cipher.decrypt(bytes(c))

    # Strip any potential padding (PKCS7 padding method assumed)
    padding_length = decrypted[-1]
    if padding_length < 16:  # Valid padding range
        decrypted = decrypted[:-padding_length]

    # Convert decrypted bytes to hex
    decrypted_hex = to_hex(decrypted).strip()
    cookie = f"__test={decrypted_hex}"
    if valueonly:
        return decrypted_hex
    return cookie

# JSchallenge se bachne ke liye
def detect(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html,'html.parser')
    result = soup.find('noscript')
    return bool(result)

class Cookie:
                def __init__(self):
                    # Ensure the file exists at initialization
                    with open("cookie.txt", 'a'):
                        pass

                def get(self):
                    try:
                        with open("cookie.txt", 'r') as f:
                            return f.read()
                    except FileNotFoundError:
                        return ""

                def set(self, cookie):
                    with open("cookie.txt", 'w') as f:
                        f.write(cookie)
