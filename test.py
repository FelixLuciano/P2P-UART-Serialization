a = bytearray()

a.insert(0, b'\xFF\xFF')

a.insert(0, '\xAA\xBB')
a.insert(1, '\xCC\xDD')

print(a)
