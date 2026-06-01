import re
import hashlib
import random
import string
import os

PASSWORD_FILE = "password_history.txt"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def password_used_before(password):
    hashed = hash_password(password)

    if not os.path.exists(PASSWORD_FILE):
        return False

    with open(PASSWORD_FILE, "r") as file:
        old_passwords = file.read().splitlines()

    return hashed in old_passwords

def save_password(password):
    hashed = hash_password(password)

    with open(PASSWORD_FILE, "a") as file:
        file.write(hashed + "\n")

def generate_strong_password(length=14):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def analyze_password(password):
    score = 0
    suggestions = []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append("Increase length to at least 12 characters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("Add numbers.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        suggestions.append("Add special characters.")

    common_passwords = [
        "password", "123456", "123456789",
        "qwerty", "admin", "welcome"
    ]

    if password.lower() in common_passwords:
        score = 0
        suggestions.append("Avoid common passwords.")

    if len(set(password)) <= 3:
        suggestions.append("Avoid repeated characters.")

    if password_used_before(password):
        suggestions.append("This password was used before. Choose a new one.")

    if score <= 2:
        strength = "WEAK"
    elif score <= 5:
        strength = "MEDIUM"
    else:
        strength = "STRONG"

    return strength, suggestions

# Main Program
print("===== PASSWORD STRENGTH ANALYZER =====")

password = input("Enter Password: ")

strength, suggestions = analyze_password(password)

print("\nPassword Strength:", strength)

if suggestions:
    print("\nSuggestions:")
    for s in suggestions:
        print("-", s)

if strength != "STRONG":
    print("\nSuggested Strong Password:")
    print(generate_strong_password())

if not password_used_before(password):
    save_password(password)

print("\nAnalysis Complete.")