import random

def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10

def generate_card_from_bin(bin_prefix, card_length=16):
    bin_prefix = str(bin_prefix).replace(" ", "").replace("-", "")
    remaining_length = card_length - len(bin_prefix) - 1
    if remaining_length < 0:
        remaining_length = 0
    
    card_body = bin_prefix + ''.join([str(random.randint(0, 9)) for _ in range(remaining_length)])
    
    for check_digit in range(10):
        if luhn_checksum(card_body + str(check_digit)) == 0:
            return card_body + str(check_digit)
    
    return card_body + "0"

def generate_expiry():
    month = random.randint(1, 12)
    year = random.randint(26, 32)
    return f"{month:02d}/{year}"

def generate_cvv():
    return ''.join([str(random.randint(0, 9)) for _ in range(3)])

def bin_generator(bin_prefix, quantity):
    try:
        quantity = int(quantity)
    except:
        quantity = 10
    
    open("bin_generated.txt", "w").write("")
    
    print(f"[*] Generating {quantity} cards with BIN: {bin_prefix}")
    print("-" * 50)
    
    for i in range(quantity):
        card_number = generate_card_from_bin(bin_prefix)
        expiry = generate_expiry()
        cvv = generate_cvv()
        
        line = f"{card_number}|{expiry}|{cvv}"
        print(f"[{i+1}] {line}")
        
        with open("bin_generated.txt", "a") as f:
            f.write(line + "\n")
    
    print("-" * 50)
    print(f"[✓] Generated {quantity} cards successfully!")

