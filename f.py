from bs4 import BeautifulSoup
from Crypto.Cipher import AES
import re

def jschallenge(html, valueonly=False):
    # Step 1: Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Attempt to find the script tag containing 'toNumbers'
    script = None
    for s in soup.find_all('script'):
        if 'toNumbers' in s.string if s.string else '':
            script = s.string
            break

    if not script:
        raise ValueError("No script containing 'toNumbers' found on the page.")

    # Step 3: Extract the hex values using regex
    matches = re.findall(r'toNumbers\("([0-9a-f]+)"\)', script)
    if len(matches) < 3:
        raise ValueError("Could not extract the required number of hex values (a, b, c).")

    a_hex, b_hex, c_hex = matches[0], matches[1], matches[2]

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
    try:
        cipher = AES.new(bytes(a), AES.MODE_CBC, bytes(b))
        decrypted = cipher.decrypt(bytes(c))

        # Strip padding (assuming PKCS7 padding)
        padding_length = decrypted[-1]
        if padding_length < 16:
            decrypted = decrypted[:-padding_length]

        # Convert decrypted bytes to hex
        decrypted_hex = to_hex(decrypted).strip()
        cookie = f"__test={decrypted_hex}"
        if valueonly:
            return decrypted_hex
        return cookie
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")


def detect(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find('noscript')
    return bool(result)


class Cookie:
    def __init__(self):
        # Ensure the file exists at initialization
        try:
            with open("cookie.txt", 'a'):
                pass
            print("Initialized Cookie class, cookie.txt file ready.")
        except Exception as e:
            print(f"Error initializing cookie file: {e}")

    def get(self):
        try:
            with open("cookie.txt", 'r') as f:
                cookie = f.read().strip()  # Remove any trailing newlines
                print(f"Retrieved cookie: {cookie}")
                return cookie
        except FileNotFoundError:
            print("cookie.txt not found, returning empty cookie.")
            return ""
        except Exception as e:
            print(f"Error reading cookie.txt: {e}")
            return ""

    def set(self, cookie):
        try:
            with open("cookie.txt", 'w') as f:
                f.write(cookie)
            print(f"Cookie successfully written: {cookie}")
        except Exception as e:
            print(f"Failed to write cookie to file: {e}")
