import sys
import random
import string
from pyfiglet import Figlet 
import colorama
import time
import os
from corex import bin

def detect_os():
    if "win" in sys.platform:
        return "windows"
    else:
        return "linux"


rd = colorama.Fore.RED
cv = colorama.Fore.WHITE
mag = colorama.Fore.MAGENTA
bl = colorama.Fore.BLUE
gn = colorama.Fore.GREEN
yl = colorama.Fore.YELLOW
cy = colorama.Fore.CYAN
gg = colorama.Fore.LIGHTCYAN_EX

CARD_PREFIXES = {
    "VISA": ["4"],
    "MASTERCARD": ["51", "52", "53", "54", "55", "2221", "2720"],
    "AMEX": ["34", "37"],
    "DISCOVER": ["6011", "644", "645", "646", "647", "648", "649", "65"],
    "JCB": ["3528", "3529", "353", "354", "355", "356", "357", "358"],
}

CARD_LENGTHS = {
    "VISA": 16,
    "MASTERCARD": 16,
    "AMEX": 15,
    "DISCOVER": 16,
    "JCB": 16,
}

FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Daniel", "Nancy", "Matthew", "Lisa", "Anthony", "Betty", "Mark", "Margaret", "Donald", "Sandra"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris"]
STREETS = ["Main St", "Oak Ave", "Maple Dr", "Cedar Ln", "Pine Rd", "Elm St", "Park Ave", "Lake Dr", "Hill Rd", "River Ln", "Forest Ave", "Valley Rd", "Spring St", "Garden Way", "Sunset Blvd"]
CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte"]
STATES = ["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA", "TX", "CA", "TX", "FL", "TX", "OH", "NC"]
BANKS = ["Chase Bank", "Bank of America", "Wells Fargo", "Citibank", "US Bank", "Capital One", "PNC Bank", "TD Bank", "Truist Bank", "Fifth Third Bank"]
MONEY_RANGES = ["$100 - $500", "$500 - $1000", "$1000 - $5000", "$5000 - $10000"]

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

def generate_card_number(brand="VISA"):
    brand = brand.upper()
    if brand not in CARD_PREFIXES:
        brand = "VISA"
    
    prefix = random.choice(CARD_PREFIXES[brand])
    length = CARD_LENGTHS[brand]
    
    remaining_length = length - len(prefix) - 1
    card_body = prefix + ''.join([str(random.randint(0, 9)) for _ in range(remaining_length)])
    
    for check_digit in range(10):
        if luhn_checksum(card_body + str(check_digit)) == 0:
            return card_body + str(check_digit)
    
    return card_body + "0"

def generate_cvv(brand="VISA"):
    if brand.upper() == "AMEX":
        return ''.join([str(random.randint(0, 9)) for _ in range(4)])
    return ''.join([str(random.randint(0, 9)) for _ in range(3)])

def generate_expiry():
    month = random.randint(1, 12)
    year = random.randint(26, 32)
    return f"{month:02d}/{year}"

def generate_pin():
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])

def generate_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def generate_address():
    idx = random.randint(0, len(CITIES) - 1)
    return f"{random.randint(100, 9999)} {random.choice(STREETS)}, {CITIES[idx]}, {STATES[idx]} {random.randint(10000, 99999)}"

def generate_card_data(brand="VISA"):
    return {
        "IssuingNetwork": brand.upper(),
        "CardNumber": generate_card_number(brand),
        "Bank": random.choice(BANKS),
        "Name": generate_name(),
        "Address": generate_address(),
        "Country": "UNITED STATES",
        "MoneyRange": random.choice(MONEY_RANGES),
        "CVV": generate_cvv(brand),
        "Expiry": generate_expiry(),
        "Pin": generate_pin()
    }

def logo():
    figlet = Figlet(font="standard").renderText("Multi-CC")
    return (gn + figlet)
print (logo())
print (bl + "[-] Powered by Team HH [Hello Hackers] ")
print (gn + "[+] Made with 💖 By AnukarOP")
print (cy + "[=] Multi-CC Tool Version : 2.0")

opr = input (mag + "\n[x] 1) Generate single valid cc\n[x] 2) Generate multi valid cc (generate cc list)\n[x] 3) CC validator\n[x] 4) Generate Multi Bin Number \n\n[^] Please Enter an option :  ")

def genscard():
    brand = input(yl + "[$] Select brand (VISA/MASTERCARD/AMEX/DISCOVER/JCB) [default: VISA]: ").strip().upper() or "VISA"
    card = generate_card_data(brand)
    return (gn + "[-] Brand : %s\n[-] Card Number : %s\n[-] Bank : %s\n[-] Name : %s\n[-] Address : %s\n[-] Country : %s\n[-] Money Range : %s\n[-] CVV : %s\n[-] Expiry : %s\n[-] Pin : %s\n============================\n[*] Script by @AnukarOP" % (card['IssuingNetwork'] , card['CardNumber'] , card['Bank'] , card['Name'] , card['Address'] , card['Country'] , card['MoneyRange'] , card['CVV'] , card['Expiry'] , card['Pin']) + cv)

def genmcard():
    brand = input(yl + "[$] Select brand (VISA/MASTERCARD/AMEX/DISCOVER/JCB) [default: VISA]: ").strip().upper() or "VISA"
    count = input(cy + "[+] How many cards to generate? [default: 10]: ").strip() or "10"
    try:
        count = int(count)
    except:
        count = 10
    
    open("generated_card.txt","w").write("")
    for i in range(count):
        card = generate_card_data(brand)
        f = open("generated_card.txt","a")
        f.write("[-] Brand : %s\n[-] Card Number : %s\n[-] Bank : %s\n[-] Name : %s\n[-] Address : %s\n[-] Country : %s\n[-] Money Range : %s\n[-] CVV : %s\n[-] Expiry : %s\n[-] Pin : %s\n===================================\n[*] Script by @AnukarOP\n\n" % (card['IssuingNetwork'] , card['CardNumber'] , card['Bank'] , card['Name'] , card['Address'] , card['Country'] , card['MoneyRange'] , card['CVV'] , card['Expiry'] , card['Pin']))
    return (gn + "[$] Generated %d cards successfully!\n[+] Saved File as generated_card.txt || Script by @AnukarOP" % count + cv)

def ccvalidator(number):
    number = number.replace(" ", "").replace("-", "")
    
    if not number.isdigit():
        return rd + "[!] Invalid: Card number must contain only digits" + cv
    
    if len(number) < 13 or len(number) > 19:
        return rd + "[!] Invalid: Card number length should be between 13-19 digits" + cv
    
    if luhn_checksum(number) == 0:
        card_type = "Unknown"
        if number[0] == "4":
            card_type = "VISA"
        elif number[:2] in ["51", "52", "53", "54", "55"] or (number[:4] >= "2221" and number[:4] <= "2720"):
            card_type = "MASTERCARD"
        elif number[:2] in ["34", "37"]:
            card_type = "AMERICAN EXPRESS"
        elif number[:4] == "6011" or number[:3] in ["644", "645", "646", "647", "648", "649"] or number[:2] == "65":
            card_type = "DISCOVER"
        elif number[:4] in ["3528", "3529"] or number[:3] in ["353", "354", "355", "356", "357", "358"]:
            card_type = "JCB"
        
        return gn + f"[✓] VALID CARD!\n[+] Card Type: {card_type}\n[+] Card Number: {number}\n[+] Luhn Check: PASSED" + cv
    else:
        return rd + "[✗] INVALID CARD!\n[-] Luhn Check: FAILED" + cv

if opr == "1":
    print (cy + "[&] You selected first option ! \n\n")
    time.sleep(1)
    print (genscard())
elif opr == "2":
    print (yl + "[&] You selected second option ! \n\n")
    print (genmcard())
elif opr == "3":
    print (mag + "[&] You selected third option !! \n\n")
    number = input(yl + "[$] Please Enter your card number : ")
    print(ccvalidator(number))
elif opr == "4":
    print (bl + "[&] You Selected Fourth Option !")
    time.sleep(0.3)
    number = input(gn + "[-] Please Enter Bin Number -  > ")
    round = input(cy + "[+] Please Enter Quantity ex : (10) - > ")
    print (rd)
    bin.bin_generator(number , round)
    print ("Saved File as bin_generated.txt !")
    print (mag + "[$] Script by AnukarOP" + cv)
else:
    print(rd + "[!] Invalid option selected!" + cv)
