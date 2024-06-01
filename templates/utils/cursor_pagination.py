from base64 import b64encode, b64decode

def encode_cursor(uuid_value: str) -> str:
  return b64encode(f"cursor:{uuid_value}".encode("ascii")).decode("ascii")


def decode_cursor(cursor: str) -> str:
  cursor_data = b64decode(cursor.encode("ascii")).decode("ascii")
  return cursor_data.split(":")[1]