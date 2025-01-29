import hashlib

class BloomFilter:
    def __init__(self, size=1000, num_hashes=3):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [False] * self.size

    def add(self, password):
        password_str = str(password)
        for index in self._get_hash_indices(password_str):
            self.bit_array[index] = True

    def contains(self, password):
        password_str = str(password)
        for index in self._get_hash_indices(password_str):
            if not self.bit_array[index]:
                return False
        return True

    def _get_hash_indices(self, password_str):
        indices = []
        for i in range(self.num_hashes):
            h = hashlib.md5()
            h.update((password_str + str(i)).encode('utf-8'))
            hex_digest = h.hexdigest()
            hash_int = int(hex_digest, 16)
            index = hash_int % self.size
            indices.append(index)
        return indices

def check_password_uniqueness(bloom_filter, new_passwords):
    results = {}
    for password in new_passwords:
        password_str = str(password) if password is not None else ""
        if bloom_filter.contains(password_str):
            results[password] = "вже використаний."
        else:
            results[password] = "унікальний."
    return results

if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for pwd in existing_passwords:
        bloom.add(pwd)
    
    new_passwords = ["password123", "newpassword", "admin123", "guest", "", None, 12345]
    results = check_password_uniqueness(bloom, new_passwords)
    
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}")