en_ch = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
ru_ch = [chr(i) for i in range(ord('А'), ord('Я') + 1)]
for ch in ['А', 'В', 'С', 'Е', 'К', 'Н', 'Р', 'О', 'Т', 'М', 'У', 'Х']:
            if ch in ru_ch:
                ru_ch.remove(ch)
cn_ch = [chr(i) for i in range(int('0x4E00', 16) + 500, int('0x9FFF', 16) + 1)]
free_chars = en_ch + ru_ch + cn_ch
free_chars = free_chars[:500]

print(free_chars)