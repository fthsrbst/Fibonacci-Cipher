#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import tracemalloc
from tabulate import tabulate
import sys
import gc
import random
import string
import argparse
import os
import platform
from colorama import Fore, Back, Style, init
from pyfiglet import Figlet
from tqdm import tqdm
import math

# Colorama başlatma
init(autoreset=True)

# Ekranı temizleme işlevi
def clear_screen():
    """İşletim sistemine göre terminal ekranını temizler."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# Banner oluşturma
def print_banner(text, font="slant"):
    """Figlet kullanarak banner oluşturur."""
    f = Figlet(font=font)
    banner = f.renderText(text)
    print(Fore.CYAN + banner)
    print(Fore.YELLOW + "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
    print(Fore.YELLOW + "███ Fibonacci-Based Encryption and Password Generator ███")
    print(Fore.YELLOW + "▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
    print(Style.RESET_ALL)

# Renkli çıktı fonksiyonları
def print_info(text):
    """Bilgi mesajı yazdırır."""
    print(Fore.CYAN + Style.BRIGHT + "ℹ️  " + text + Style.RESET_ALL)

def print_success(text):
    """Başarı mesajı yazdırır."""
    print(Fore.GREEN + Style.BRIGHT + "✅ " + text + Style.RESET_ALL)

def print_warning(text):
    """Uyarı mesajı yazdırır."""
    print(Fore.YELLOW + Style.BRIGHT + "⚠️  " + text + Style.RESET_ALL)

def print_error(text):
    """Hata mesajı yazdırır."""
    print(Fore.RED + Style.BRIGHT + "❌ " + text + Style.RESET_ALL)

def print_header(text):
    """Başlık yazdırır."""
    separator = "=" * len(text)
    print("\n" + Fore.MAGENTA + Style.BRIGHT + separator)
    print(Fore.MAGENTA + Style.BRIGHT + text)
    print(Fore.MAGENTA + Style.BRIGHT + separator + Style.RESET_ALL + "\n")

def print_section(text):
    """Alt başlık yazdırır."""
    print("\n" + Fore.YELLOW + Style.BRIGHT + text)
    print(Fore.YELLOW + Style.BRIGHT + "-" * len(text) + Style.RESET_ALL + "\n")

# Fibonacci algoritmaları
class FibonacciMethods:
    def __init__(self):
        # Memoizasyon için kullanılacak
        self.memo = {}

    def naive_recursive(self, n):
        """Naif özyinelemeli Fibonacci."""
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.naive_recursive(n-1) + self.naive_recursive(n-2)

    def memoized_recursive(self, n):
        """Hafızalı özyinelemeli Fibonacci (top-down)."""
        if n in self.memo:
            return self.memo[n]
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            self.memo[n] = self.memoized_recursive(n-1) + self.memoized_recursive(n-2)
            return self.memo[n]

    def iterative(self, n):
        """Yinelemeli Fibonacci (bottom-up)."""
        if n <= 0:
            return 0
        elif n == 1:
            return 1
            
        a, b = 0, 1
        for _ in range(2, n+1):
            a, b = b, a + b
        return b

    def matrix_exponentiation(self, n):
        """Matris üs alma ile Fibonacci."""
        if n <= 0:
            return 0
        elif n == 1:
            return 1
            
        # Matris çarpımı: [[1, 1], [1, 0]]^n
        def matrix_multiply(A, B):
            C = [[0, 0], [0, 0]]
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        C[i][j] += A[i][k] * B[k][j]
            return C
        
        def matrix_power(A, n):
            if n == 1:
                return A
            if n % 2 == 0:
                return matrix_power(matrix_multiply(A, A), n // 2)
            else:
                return matrix_multiply(A, matrix_power(matrix_multiply(A, A), (n - 1) // 2))
        
        F = matrix_power([[1, 1], [1, 0]], n - 1)
        return F[0][0]

    def binet_formula(self, n):
        """Binet formülü ile Fibonacci."""
        if n <= 0:
            return 0
        elif n == 1:
            return 1
            
        import math
        phi = (1 + math.sqrt(5)) / 2
        psi = (1 - math.sqrt(5)) / 2
        return int((math.pow(phi, n) - math.pow(psi, n)) / math.sqrt(5))


# Şifreleme ve şifre çözme fonksiyonları
def encrypt(text, fib_method):
    """Metni Fibonacci kullanarak şifrele."""
    encrypted = []
    for i, char in enumerate(text):
        # Karakterin ASCII değeri + i. Fibonacci sayısı
        fib_val = fib_method(i)
        encrypted_val = ord(char) + fib_val
        encrypted.append(encrypted_val)
    return encrypted

def decrypt(encrypted_values, fib_method):
    """Şifrelenmiş metni Fibonacci kullanarak çöz."""
    decrypted = ""
    for i, val in enumerate(encrypted_values):
        # Şifrelenmiş değer - i. Fibonacci sayısı
        fib_val = fib_method(i)
        decrypted_val = val - fib_val
        decrypted += chr(decrypted_val)
    return decrypted

def measure_performance(message, method_name, method_func):
    """Belirli bir yöntemin performansını ölçer."""
    # Garbage collector'ı kapatarak daha doğru sonuçlar alalım
    gc.disable()
    
    # Hafıza kullanımını izlemeye başla
    tracemalloc.start()
    
    # Zamanı başlat
    start_time = time.time()
    
    # Şifrele
    encrypted = encrypt(message, method_func)
    
    # Şifreyi çöz
    decrypted = decrypt(encrypted, method_func)
    
    # Zamanı durdur
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Hafıza kullanımını ölç
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Garbage collector'ı yeniden etkinleştir
    gc.enable()
    
    # Şifre çözümünün doğruluğunu kontrol et
    is_correct = (decrypted == message)
    
    return {
        "method": method_name,
        "time": execution_time,
        "memory_current": current / 1024,  # KB
        "memory_peak": peak / 1024,  # KB
        "correct": is_correct
    }

# Şifre oluşturma (password generator) fonksiyonları
def generate_password_simple(length=12):
    """
    Basit şifre oluşturucu - karakter havuzundan rastgele seçim yapar.
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def generate_password_fibonacci(length=12, method='iterative'):
    """
    Fibonacci tabanlı şifre oluşturucu - karakter seçiminde Fibonacci sayılarını kullanır.
    """
    fib = FibonacciMethods()
    
    # Kullanılacak Fibonacci metodu
    method_func = {
        'naive': lambda n: fib.naive_recursive(min(n, 25)),
        'memoized': fib.memoized_recursive,
        'iterative': fib.iterative,
        'matrix': fib.matrix_exponentiation,
        'binet': fib.binet_formula
    }.get(method, fib.iterative)
    
    # Karakter havuzları
    chars = {
        'lowercase': string.ascii_lowercase,
        'uppercase': string.ascii_uppercase,
        'digits': string.digits,
        'special': string.punctuation
    }
    
    password = ""
    
    # Benzersiz şifre oluşturmak için farklı bir seed kullan
    current_time = time.time()
    random.seed(current_time + random.random())
    
    # Her bir karakter için, indekse göre bir Fibonacci sayısı hesapla
    # ve bu sayıyı karakter seçiminde kullan
    for i in range(length):
        # Fibonacci sayısını hesapla
        fib_val = method_func(i + 1)
        
        # Karakter tipini belirle (fib_val % 4)
        char_type = list(chars.keys())[fib_val % 4]
        
        # Karakter havuzundan rastgele bir karakter seç
        # Fibonacci sayısını ve pozisyonu kullanarak karakteri seç
        char_pool = chars[char_type]
        char_index = (fib_val + i + int(current_time * 1000) % 100) % len(char_pool)
        char = char_pool[char_index]
        
        # Şifreye karakteri ekle
        password += char
    
    # Şifrede en az bir rakam ve özel karakter olduğundan emin ol
    if not any(c in string.digits for c in password):
        # Rastgele bir pozisyona bir rakam ekle
        pos = random.randint(0, length - 1)
        password = password[:pos] + random.choice(string.digits) + password[pos+1:]
    
    if not any(c in string.punctuation for c in password):
        # Rastgele bir pozisyona bir özel karakter ekle
        pos = random.randint(0, length - 1)
        password = password[:pos] + random.choice(string.punctuation) + password[pos+1:]
    
    return password

def generate_passwords(count=5, length=12, method='iterative'):
    """
    Birden fazla şifre oluşturur.
    """
    passwords = []
    for _ in range(count):
        password = generate_password_fibonacci(length, method)
        passwords.append(password)
    return passwords

def analyze_password_strength(password):
    """
    Analyzes the strength of a password.
    Provides a more sophisticated and realistic evaluation.
    """
    score = 0
    feedback = []
    
    # Check length (0-4 points)
    if len(password) < 6:
        if 'benchmark_title' in LANG:  # Check if LANG is initialized
            feedback.append("Password is too short, not secure!")
            if LANG.get('benchmark_title') == "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI":
                feedback[-1] = "Şifre çok kısa, güvenli değil!"
        else:
            feedback.append("Password is too short, not secure!")
        length_score = 0
    elif len(password) < 8:
        if 'benchmark_title' in LANG:
            feedback.append("Password is short, should be at least 8 characters.")
            if LANG.get('benchmark_title') == "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI":
                feedback[-1] = "Şifre kısa, en az 8 karakter olmalı."
        else:
            feedback.append("Password is short, should be at least 8 characters.")
        length_score = 1
    elif len(password) < 10:
        if 'benchmark_title' in LANG:
            feedback.append("Password length is sufficient.")
            if LANG.get('benchmark_title') == "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI":
                feedback[-1] = "Şifre uzunluğu yeterli."
        else:
            feedback.append("Password length is sufficient.")
        length_score = 2
    elif len(password) < 12:
        length_score = 3
    else:
        length_score = 4
        
    score += length_score
    
    # Character diversity check (1 point each)
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_digit = any(c in string.digits for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    diversity_score = 0
    
    if has_lower:
        diversity_score += 1
    else:
        if 'benchmark_title' in LANG:
            feedback.append("Doesn't contain lowercase letters.")
            if LANG.get('benchmark_title') == "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI":
                feedback[-1] = "Küçük harf içermiyor."
        else:
            feedback.append("Doesn't contain lowercase letters.")
    
    if has_upper:
        diversity_score += 1
    else:
        if 'benchmark_title' in LANG:
            feedback.append("Doesn't contain uppercase letters.")
            if LANG.get('benchmark_title') == "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI":
                feedback[-1] = "Büyük harf içermiyor."
        else:
            feedback.append("Doesn't contain uppercase letters.")
    
    if has_digit:
        diversity_score += 1
    else:
        if 'benchmark_title' in LANG:
            feedback.append("Doesn't contain numbers.")
            if LANG.get('benchmark_title') == "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI":
                feedback[-1] = "Rakam içermiyor."
        else:
            feedback.append("Doesn't contain numbers.")
    
    if has_special:
        diversity_score += 1
    else:
        if 'benchmark_title' in LANG:
            feedback.append("Doesn't contain special characters.")
            if LANG.get('benchmark_title') == "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI":
                feedback[-1] = "Özel karakter içermiyor."
        else:
            feedback.append("Doesn't contain special characters.")
    
    score += diversity_score
    
    # Complexity analysis
    
    # Repeated character check
    unique_ratio = len(set(password)) / len(password)
    if unique_ratio < 0.6:
        if 'benchmark_title' in LANG:
            feedback.append("Contains too many repeated characters.")
            if LANG.get('benchmark_title') == "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI":
                feedback[-1] = "Çok fazla tekrarlayan karakter içeriyor."
        else:
            feedback.append("Contains too many repeated characters.")
        score -= 2
    elif unique_ratio < 0.7:
        if 'benchmark_title' in LANG:
            feedback.append("Some characters are repeated.")
            if LANG.get('benchmark_title') == "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI":
                feedback[-1] = "Bazı karakterler tekrarlanıyor."
        else:
            feedback.append("Some characters are repeated.")
        score -= 1
    
    # Sequential character check
    has_sequential = False
    for i in range(len(password) - 2):
        # Alphabetic sequence (abc, xyz)
        if (password[i].isalpha() and password[i+1].isalpha() and password[i+2].isalpha() and 
            ord(password[i+1].lower()) == ord(password[i].lower()) + 1 and 
            ord(password[i+2].lower()) == ord(password[i+1].lower()) + 1):
            has_sequential = True
            break
        # Numeric sequence (123, 789)
        if (password[i].isdigit() and password[i+1].isdigit() and password[i+2].isdigit() and 
            int(password[i+1]) == int(password[i]) + 1 and 
            int(password[i+2]) == int(password[i+1]) + 1):
            has_sequential = True
            break
            
    if has_sequential:
        if 'benchmark_title' in LANG:
            feedback.append("Contains sequential characters (e.g.: abc, 123).")
            if LANG.get('benchmark_title') == "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI":
                feedback[-1] = "Ardışık karakterler içeriyor (örnek: abc, 123)."
        else:
            feedback.append("Contains sequential characters (e.g.: abc, 123).")
        score -= 1
    
    # Common password pattern check (uppercase, lowercase, number, special character sequence)
    typical_pattern = True
    if len(password) >= 4:
        # Typical pattern: Start with uppercase, continue with lowercase, end with number (e.g.: Pass123!)
        if not (password[0].isupper() and password[1:3].islower() and password[-2].isdigit()):
            typical_pattern = False
    
    if not typical_pattern:
        score += 1  # Bonus point for non-typical pattern
    
    # Entropy (Shannon entropy calculation) - character distribution diversity
    char_freq = {}
    for char in password:
        if char in char_freq:
            char_freq[char] += 1
        else:
            char_freq[char] = 1
    
    entropy = 0
    for char, freq in char_freq.items():
        prob = freq / len(password)
        entropy -= prob * math.log2(prob)
    
    # Entropy scoring (0-2 points)
    if entropy > 3.5:
        score += 2
    elif entropy > 2.5:
        score += 1
    elif entropy < 2.0:
        if 'benchmark_title' in LANG:
            feedback.append("Character distribution is not diverse.")
            if LANG.get('benchmark_title') == "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI":
                feedback[-1] = "Karakter dağılımı çeşitli değil."
        else:
            feedback.append("Character distribution is not diverse.")
    
    # Total score evaluation (normalized)
    # Maximum score: 4 (length) + 4 (diversity) + 1 (atypical) + 2 (entropy) = 11
    # Minimum score: 0 (length) + 0 (diversity) - 2 (repetition) - 1 (sequential) = -3
    # Normalized score: scaled to 0-10
    normalized_score = max(0, min(10, int((score + 3) * 10 / 14)))
    
    # Strength evaluation
    if normalized_score <= 3:
        strength = LANG.get('weak', "Weak") if 'weak' in LANG else "Weak"
    elif normalized_score <= 5:
        strength = LANG.get('medium', "Medium") if 'medium' in LANG else "Medium"
    elif normalized_score <= 8:
        strength = LANG.get('strong', "Strong") if 'strong' in LANG else "Strong"
    else:
        strength = LANG.get('very_strong', "Very Strong") if 'very_strong' in LANG else "Very Strong"
    
    # Automatic suggestions
    if normalized_score < 7:
        if length_score < 3:
            if 'benchmark_title' in LANG:
                feedback.append("Increase password length (at least 12 characters).")
                if LANG.get('benchmark_title') == "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI":
                    feedback[-1] = "Şifre uzunluğunu artırın (en az 12 karakter)."
            else:
                feedback.append("Increase password length (at least 12 characters).")
        
        if diversity_score < 4:
            if 'benchmark_title' in LANG:
                feedback.append("Use lowercase, uppercase, numbers and special characters.")
                if LANG.get('benchmark_title') == "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI":
                    feedback[-1] = "Küçük harf, büyük harf, rakam ve özel karakter kullanın."
            else:
                feedback.append("Use lowercase, uppercase, numbers and special characters.")
            
        if unique_ratio < 0.7:
            if 'benchmark_title' in LANG:
                feedback.append("Use more diverse characters, avoid repetitions.")
                if LANG.get('benchmark_title') == "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI":
                    feedback[-1] = "Daha çeşitli karakterler kullanın, tekrarlardan kaçının."
            else:
                feedback.append("Use more diverse characters, avoid repetitions.")
            
        if has_sequential:
            if 'benchmark_title' in LANG:
                feedback.append("Use random characters instead of sequential ones.")
                if LANG.get('benchmark_title') == "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI":
                    feedback[-1] = "Ardışık karakterler yerine rastgele karakterler kullanın."
            else:
                feedback.append("Use random characters instead of sequential ones.")
    
    return {
        "strength": strength,
        "score": normalized_score,
        "feedback": feedback
    }

def performance_benchmark():
    """
    Compares the performance of different Fibonacci calculation algorithms.
    """
    clear_screen()
    print_banner("Fibonacci Performance")
    print_header(LANG['benchmark_title'])
    
    # Test message
    message = "Fibonacci sequence-based encryption and decryption mechanism."
    if 'tr' in sys.argv:
        message = "Fibonacci dizisine dayalı şifreleme ve şifre çözme mekanizması."
    
    # Fibonacci methods
    fib = FibonacciMethods()
    
    # Measurement results
    results = []
    
    # Limit n value for naive recursion to prevent stack overflow
    methods = [
        ("Naive Recursion", lambda n: fib.naive_recursive(min(n, 25)), "naive"),
        ("Memoized Recursion", fib.memoized_recursive, "memoized"),
        ("Iterative", fib.iterative, "iterative"),
        ("Matrix Exponentiation", fib.matrix_exponentiation, "matrix"),
        ("Binet's Formula", fib.binet_formula, "binet")
    ]
    
    # Progress bar
    print_info(LANG['testing_algorithms'])
    with tqdm(total=len(methods), desc="Algorithm Test", bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.BLUE, Fore.RESET)) as pbar:
        # Measure each method
        for method_name, method_func, method_key in methods:
            print(f"\n{Fore.CYAN}» {method_name}{Style.RESET_ALL} {LANG['method_measuring'].format(method_name)}...")
            result = measure_performance(message, method_name, method_func)
            result["key"] = method_key
            results.append(result)
            
            # Check accuracy
            if not result["correct"]:
                print_warning(LANG['method_incorrect'].format(method_name))
                
            pbar.update(1)
    
    # Display results as a table
    headers = [
        LANG['header_method'], 
        LANG['header_time'], 
        LANG['header_memory_current'], 
        LANG['header_memory_peak'], 
        LANG['header_accuracy']
    ]
    table_data = [[r["method"], r["time"], r["memory_current"], r["memory_peak"], r["correct"]] for r in results]
    
    print_header(LANG['comparison_title'])
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Find fastest and most memory-efficient methods
    fastest = min(results, key=lambda x: x["time"])
    most_memory_efficient = min(results, key=lambda x: x["memory_peak"])
    
    print_header(LANG['summary_title'])
    print_success(LANG['fastest_method'].format(fastest['method'], fastest['time']))
    print_success(LANG['memory_efficient'].format(most_memory_efficient['method'], most_memory_efficient['memory_peak']))
    
    # Show theoretical complexities
    print_section(LANG['theory_title'])
    
    complexity_data = [
        ["Naive Recursion", "O(2^n)", LANG['expo_slowest']],
        ["Memoized Recursion", "O(n)", LANG['linear_good']],
        ["Iterative", "O(n)", LANG['linear_good_const']],
        ["Matrix Exponentiation", "O(log n)", LANG['log_very_good']],
        ["Binet's Formula", "O(1)", LANG['const_best']]
    ]
    
    print(tabulate(complexity_data, headers=[
        LANG['header_algorithm'], 
        LANG['header_complexity'], 
        LANG['header_description']
    ], tablefmt="grid"))
    
    # Save results to Markdown file
    print_info(LANG['saving_results'])
    with open("fibonacci_performance.md", "w", encoding="utf-8") as f:
        f.write("# Fibonacci Algorithm Performance Results\n\n")
        f.write(tabulate(table_data, headers=headers, tablefmt="pipe"))
        f.write("\n\n## Summary\n\n")
        f.write(f"* {LANG['fastest_method'].format(fastest['method'], fastest['time'])}\n")
        f.write(f"* {LANG['memory_efficient'].format(most_memory_efficient['method'], most_memory_efficient['memory_peak'])}\n\n")
        
        f.write("## About the Methods\n\n")
        f.write("* **Naive Recursion**: Slowest method as it recalculates the same values repeatedly. Has O(2^n) time complexity.\n")
        f.write("* **Memoized Recursion**: Top-down dynamic programming approach. Values are stored and reused. Has O(n) time and O(n) space complexity.\n")
        f.write("* **Iterative**: Bottom-up dynamic programming approach. Uses less memory. Has O(n) time and O(1) space complexity.\n")
        f.write("* **Matrix Exponentiation**: Calculates in logarithmic time using matrix exponentiation. Has O(log n) time complexity.\n")
        f.write("* **Binet's Formula**: Closed-form solution. Theoretically has O(1) time complexity, but may have precision issues for large numbers in practice.\n")
    
    print_success(LANG['results_saved'].format('fibonacci_performance.md'))
    
    input(f"\n{LANG['continue']}")

def encrypt_file(input_file, output_file, fib_method_name='iterative'):
    """
    Dosyayı şifreler.
    """
    fib = FibonacciMethods()
    
    # Kullanılacak Fibonacci metodu
    method_func = {
        'naive': lambda n: fib.naive_recursive(min(n, 25)),
        'memoized': fib.memoized_recursive,
        'iterative': fib.iterative,
        'matrix': fib.matrix_exponentiation,
        'binet': fib.binet_formula
    }.get(fib_method_name, fib.iterative)
    
    try:
        # Dosyayı oku
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Şifrele
        encrypted = encrypt(text, method_func)
        
        # Şifrelenmiş veriyi kaydet
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(' '.join(map(str, encrypted)))
        
        print(f"Dosya başarıyla şifrelendi: {output_file}")
        return True
    except Exception as e:
        print(f"Dosya şifreleme hatası: {e}")
        return False

def decrypt_file(input_file, output_file, fib_method_name='iterative'):
    """
    Şifrelenmiş dosyayı çözer.
    """
    fib = FibonacciMethods()
    
    # Kullanılacak Fibonacci metodu
    method_func = {
        'naive': lambda n: fib.naive_recursive(min(n, 25)),
        'memoized': fib.memoized_recursive,
        'iterative': fib.iterative,
        'matrix': fib.matrix_exponentiation,
        'binet': fib.binet_formula
    }.get(fib_method_name, fib.iterative)
    
    try:
        # Şifrelenmiş veriyi oku
        with open(input_file, 'r', encoding='utf-8') as f:
            encrypted_text = f.read()
        
        # Sayılara dönüştür
        encrypted_values = list(map(int, encrypted_text.split()))
        
        # Şifreyi çöz
        decrypted = decrypt(encrypted_values, method_func)
        
        # Çözülmüş veriyi kaydet
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(decrypted)
        
        print(f"Dosya başarıyla çözüldü: {output_file}")
        return True
    except Exception as e:
        print(f"Dosya şifre çözme hatası: {e}")
        return False

def password_generator_mode():
    """
    Password generator mode.
    """
    clear_screen()
    print_banner("Password Generator")
    print_header(LANG['pwd_gen_title'])
    
    try:
        count = int(input(f"{Fore.YELLOW}{LANG['pwd_count']}{Style.RESET_ALL} ").strip() or "5")
        count = max(1, min(count, 10))
        
        length = int(input(f"{Fore.YELLOW}{LANG['pwd_length']}{Style.RESET_ALL} ").strip() or "12")
        length = max(8, min(length, 32))
        
        print_header(LANG['method_select'])
        
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Naive Recursion")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Memoized Recursion")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Iterative {Fore.GREEN}{LANG['default']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} Matrix Exponentiation")
        print(f"{Fore.CYAN}5.{Style.RESET_ALL} Binet's Formula")
        
        method_choice = input(f"\n{Fore.YELLOW}{LANG['your_choice']}{Style.RESET_ALL} ").strip() or "3"
        method_map = {
            "1": "naive",
            "2": "memoized",
            "3": "iterative",
            "4": "matrix",
            "5": "binet"
        }
        method = method_map.get(method_choice, "iterative")
        
        print_info(LANG['generating_pwd'].format(method.capitalize(), count, length))
        
        # Progress bar
        with tqdm(total=count, desc="Password Generation", bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET)) as pbar:
            passwords = []
            for _ in range(count):
                password = generate_password_fibonacci(length, method)
                passwords.append(password)
                pbar.update(1)
                time.sleep(0.1)  # Brief pause for visual effect
        
        print_header(LANG['pwd_generated'])
        
        for i, password in enumerate(passwords, 1):
            strength = analyze_password_strength(password)
            strength_color = {
                LANG['weak']: Fore.RED,
                LANG['medium']: Fore.YELLOW,
                LANG['strong']: Fore.GREEN,
                LANG['very_strong']: Fore.CYAN
            }.get(strength['strength'], Fore.WHITE)
            
            print(f"{i}. {Fore.WHITE}{password}{Style.RESET_ALL} - {strength_color}{strength['strength']}{Style.RESET_ALL}")
        
        print_header(LANG['pwd_analysis'])
        
        for i, password in enumerate(passwords, 1):
            analysis = analyze_password_strength(password)
            strength_color = {
                LANG['weak']: Fore.RED,
                LANG['medium']: Fore.YELLOW,
                LANG['strong']: Fore.GREEN,
                LANG['very_strong']: Fore.CYAN
            }.get(analysis['strength'], Fore.WHITE)
            
            print(f"\n{LANG['pwd_number'].format(i, Fore.WHITE + password + Style.RESET_ALL)}")
            print(f"   {LANG['pwd_strength'].format(strength_color + analysis['strength'] + Style.RESET_ALL, analysis['score'])}")
            if analysis['feedback']:
                print(f"   {LANG['pwd_suggestions'].format(Fore.YELLOW + ', '.join(analysis['feedback']) + Style.RESET_ALL)}")
        
        save_prompt = LANG['save_option']
        save_option = input(f"\n{Fore.YELLOW}{save_prompt}{Style.RESET_ALL} ").strip().lower()
        if save_option in ('y', 'e', 'yes', 'evet'):
            filename = input(f"{Fore.YELLOW}{LANG['filename']}{Style.RESET_ALL} ").strip() or "passwords.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Fibonacci ({method.capitalize()}) Password Generator Results\n\n")
                for i, password in enumerate(passwords, 1):
                    analysis = analyze_password_strength(password)
                    f.write(f"{i}. {password} - {analysis['strength']}\n")
            print_success(LANG['pwd_saved'].format(filename))
    except ValueError:
        print_error(LANG['valid_numbers'])
    
    input(f"\n{LANG['return_menu']}")

def file_encryption_mode():
    """
    File encryption mode.
    """
    clear_screen()
    print_banner("File Encryption")
    print_header(LANG['file_enc_title'])
    
    # Add explanation
    print_info(LANG['file_enc_intro1'])
    print_info(LANG['file_enc_intro2'])
    print("")
    
    try:
        print_section(LANG['op_type'])
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} {LANG['op_encrypt']}")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} {LANG['op_decrypt']}")
        
        operation = input(f"\n{Fore.YELLOW}{LANG['your_choice'][:-3]}(1-2):{Style.RESET_ALL} ").strip() or "1"
        
        print_section(LANG['file_paths'])
        print_info(LANG['input_file_prompt'])
        input_file = input(f"\n{Fore.YELLOW}{LANG['input_file']}{Style.RESET_ALL} ").strip()
        if not input_file:
            print_error(LANG['input_file_error'])
            input(f"\n{LANG['return_menu']}")
            return
        
        # Check if file exists
        if not os.path.exists(input_file):
            print_error(LANG['file_not_found'].format(input_file))
            input(f"\n{LANG['return_menu']}")
            return
        
        print_info(LANG['output_file_prompt'])
        output_file = input(f"{Fore.YELLOW}{LANG['output_file']}{Style.RESET_ALL} ").strip()
        if not output_file:
            output_file = input_file + (".enc" if operation == "1" else ".dec")
            print_info(LANG['default_output'].format(output_file))
        
        print_header(LANG['method_select'])
        
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Naive Recursion")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Memoized Recursion")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Iterative {Fore.GREEN}{LANG['default']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} Matrix Exponentiation")
        print(f"{Fore.CYAN}5.{Style.RESET_ALL} Binet's Formula")
        
        method_choice = input(f"\n{Fore.YELLOW}{LANG['your_choice']}{Style.RESET_ALL} ").strip() or "3"
        method_map = {
            "1": "naive",
            "2": "memoized",
            "3": "iterative",
            "4": "matrix",
            "5": "binet"
        }
        method = method_map.get(method_choice, "iterative")
        
        if operation == "1":
            print_info(LANG['encrypting_file'].format(input_file, method.capitalize()))
            
            # Get file size
            file_size = os.path.getsize(input_file)
            print_info(LANG['file_size'].format(file_size))
            
            success = encrypt_file(input_file, output_file, method)
        else:
            print_info(LANG['decrypting_file'].format(input_file, method.capitalize()))
            success = decrypt_file(input_file, output_file, method)
        
        if success:
            print_success(LANG['success'])
            print_info(LANG['output_file_result'].format(output_file))
        else:
            print_error(LANG['failure'])
    except Exception as e:
        print_error(LANG['unexpected_error'].format(e))
    
    input(f"\n{LANG['return_menu']}")

def generate_optimal_passwords(count=5, length=12):
    """
    Generates passwords using the optimal Fibonacci algorithm.
    """
    clear_screen()
    print_banner("Optimal Algorithm")
    print_header(LANG['opt_title'])
    
    try:
        # First get password count and length
        count = int(input(f"{Fore.YELLOW}{LANG['pwd_count']}{Style.RESET_ALL} ").strip() or "5")
        count = max(1, min(count, 10))
        
        length = int(input(f"{Fore.YELLOW}{LANG['pwd_length']}{Style.RESET_ALL} ").strip() or "12")
        length = max(8, min(length, 32))
        
        # Create text for the desired password
        password_text = f"Fibonacci password length {length}, password count {count}"
        
        print_section("ALGORITHM EVALUATION")
        print_info(LANG['opt_evaluating'])
        
        # Fibonacci methods
        fib = FibonacciMethods()
        
        # Measurement results
        results = []
        
        # Generate passwords for all algorithms and measure performance
        methods = [
            ("Naive Recursion", lambda n: fib.naive_recursive(min(n, 25)), "naive"),
            ("Memoized Recursion", fib.memoized_recursive, "memoized"),
            ("Iterative", fib.iterative, "iterative"),
            ("Matrix Exponentiation", fib.matrix_exponentiation, "matrix"),
            ("Binet's Formula", fib.binet_formula, "binet")
        ]
        
        all_passwords = {}
        
        # Progress bar
        with tqdm(total=len(methods), desc="Algorithm Test", bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.BLUE, Fore.RESET)) as pbar:
            # Measure each method and generate passwords
            for method_name, method_func, method_key in methods:
                print(f"{Fore.CYAN}» {method_name}{Style.RESET_ALL} {LANG['opt_generating'].format(method_name)}...")
                
                # Measure algorithm performance
                start_time = time.time()
                tracemalloc.start()
                
                # Generate passwords with this algorithm
                sub_pbar_desc = f"{method_name} passwords"
                with tqdm(total=count, desc=sub_pbar_desc, leave=False, bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET)) as sub_pbar:
                    passwords = []
                    for _ in range(count):
                        password = generate_password_fibonacci(length, method_key)
                        passwords.append(password)
                        sub_pbar.update(1)
                
                all_passwords[method_key] = passwords
                
                # Complete memory and time measurements
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                end_time = time.time()
                
                # Save results
                result = {
                    "method": method_name,
                    "key": method_key,
                    "time": end_time - start_time,
                    "memory_current": current / 1024,  # KB
                    "memory_peak": peak / 1024,  # KB
                }
                results.append(result)
                
                pbar.update(1)
        
        # Theoretical time complexity scores (0-10, higher is better)
        time_complexity_scores = {
            "naive": 1,       # O(2^n) - worst
            "memoized": 6,    # O(n) - medium
            "iterative": 7,   # O(n) - medium but constant space
            "matrix": 8,      # O(log n) - good
            "binet": 10       # O(1) - theoretically best
        }
        
        # Normalize practical test results (0-10, higher is better)
        # Time: Lower is better
        min_time = min(r["time"] for r in results)
        max_time = max(r["time"] for r in results)
        time_range = max_time - min_time if max_time > min_time else 1
        
        # Memory: Lower is better
        min_memory = min(r["memory_peak"] for r in results)
        max_memory = max(r["memory_peak"] for r in results)
        memory_range = max_memory - min_memory if max_memory > min_memory else 1
        
        # Calculate total score for each algorithm
        for result in results:
            # Normalized time score (0-10)
            if time_range > 0:
                time_score = 10 - ((result["time"] - min_time) / time_range) * 10
            else:
                time_score = 10
            
            # Normalized memory score (0-10)
            if memory_range > 0:
                memory_score = 10 - ((result["memory_peak"] - min_memory) / memory_range) * 10
            else:
                memory_score = 10
            
            # Theoretical complexity score
            complexity_score = time_complexity_scores[result["key"]]
            
            # Total score (weighted average)
            # Practical performance may be more important than theoretical
            # Time: 40%, Memory: 30%, Theoretical Complexity: 30%
            total_score = (time_score * 0.4) + (memory_score * 0.3) + (complexity_score * 0.3)
            
            result["time_score"] = time_score
            result["memory_score"] = memory_score
            result["complexity_score"] = complexity_score
            result["total_score"] = total_score
        
        # Sort results by score
        sorted_results = sorted(results, key=lambda x: x["total_score"], reverse=True)
        
        # Show results as a table
        headers = [LANG['header_method'], LANG['header_time'], LANG['header_memory_peak'], LANG['header_complexity'], "Total Score"]
        table_data = [
            [
                f"{r['method']}", 
                f"{r['time']:.6f}", 
                f"{r['memory_peak']:.2f}", 
                time_complexity_map(r["key"]), 
                f"{r['total_score']:.2f}"
            ]
            for r in sorted_results
        ]
        
        print_header(LANG['opt_comparison'])
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        # Highest scoring algorithm
        best_algorithm = sorted_results[0]
        optimal_method = best_algorithm["key"]
        
        print_header(LANG['opt_result'])
        print_success(LANG['opt_algorithm'].format(best_algorithm['method'], best_algorithm['total_score']))
        print_success(LANG['opt_complexity'].format(time_complexity_map(optimal_method)))
        print_success(LANG['opt_time'].format(best_algorithm['time']))
        print_success(LANG['opt_memory'].format(best_algorithm['memory_peak']))
        
        # Show passwords generated with the optimal algorithm
        optimal_passwords = all_passwords[optimal_method]
        
        print_header(LANG['opt_passwords'])
        
        for i, password in enumerate(optimal_passwords, 1):
            strength = analyze_password_strength(password)
            strength_color = {
                LANG['weak']: Fore.RED,
                LANG['medium']: Fore.YELLOW,
                LANG['strong']: Fore.GREEN,
                LANG['very_strong']: Fore.CYAN
            }.get(strength['strength'], Fore.WHITE)
            
            print(f"{i}. {Fore.WHITE}{password}{Style.RESET_ALL} - {strength_color}{strength['strength']}{Style.RESET_ALL}")
        
        print_header(LANG['pwd_analysis'])
        
        for i, password in enumerate(optimal_passwords, 1):
            analysis = analyze_password_strength(password)
            strength_color = {
                LANG['weak']: Fore.RED,
                LANG['medium']: Fore.YELLOW,
                LANG['strong']: Fore.GREEN,
                LANG['very_strong']: Fore.CYAN
            }.get(analysis['strength'], Fore.WHITE)
            
            print(f"\n{LANG['pwd_number'].format(i, Fore.WHITE + password + Style.RESET_ALL)}")
            print(f"   {LANG['pwd_strength'].format(strength_color + analysis['strength'] + Style.RESET_ALL, analysis['score'])}")
            if analysis['feedback']:
                print(f"   {LANG['pwd_suggestions'].format(Fore.YELLOW + ', '.join(analysis['feedback']) + Style.RESET_ALL)}")
        
        # Automatically save passwords
        filename = f"optimal_passwords_{optimal_method}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Optimal Fibonacci Algorithm ({best_algorithm['method']}) Generated Passwords\n\n")
            f.write(f"Theoretical Complexity: {time_complexity_map(optimal_method)}\n")
            f.write(f"Time: {best_algorithm['time']:.6f} seconds\n")
            f.write(f"Memory Usage: {best_algorithm['memory_peak']:.2f} KB\n\n")
            
            for i, password in enumerate(optimal_passwords, 1):
                analysis = analyze_password_strength(password)
                f.write(f"{i}. {password} - {analysis['strength']}\n")
        
        print_success(LANG['pwd_saved'].format(filename))
        
        # Optionally save passwords from all algorithms
        save_all = input(f"\n{Fore.YELLOW}{LANG['save_all']}{Style.RESET_ALL} ").strip().lower()
        if save_all in ('y', 'e', 'yes', 'evet'):
            for method_key, passwords in all_passwords.items():
                if method_key != optimal_method:  # Already saved the optimal method
                    filename = f"passwords_{method_key}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        method_name = next(m[0] for m in methods if m[2] == method_key)
                        f.write(f"# {method_name} Algorithm Generated Passwords\n\n")
                        for i, password in enumerate(passwords, 1):
                            analysis = analyze_password_strength(password)
                            f.write(f"{i}. {password} - {analysis['strength']}\n")
                    print_success(LANG['alg_passwords_saved'].format(method_name, filename))
                    
    except Exception as e:
        print_error(LANG['unexpected_error'].format(e))
        import traceback
        traceback.print_exc()
    
    input(f"\n{LANG['return_menu']}")
    
    return optimal_passwords, optimal_method

def time_complexity_map(method_key):
    """Algoritma anahtarına göre zaman karmaşıklığını döndürür."""
    complexity_map = {
        "naive": "O(2^n)",
        "memoized": "O(n)",
        "iterative": "O(n)",
        "matrix": "O(log n)",
        "binet": "O(1)"
    }
    return complexity_map.get(method_key, "Bilinmiyor")

def main():
    clear_screen()
    print_banner("Fibonacci Cipher")
    
    parser = argparse.ArgumentParser(description="Fibonacci Encryption and Password Generator")
    parser.add_argument('--benchmark', action='store_true', help='Run performance benchmark')
    parser.add_argument('--generate', action='store_true', help='Start password generator mode')
    parser.add_argument('--encrypt', action='store_true', help='Start file encryption mode')
    parser.add_argument('--optimal', action='store_true', help='Find optimal algorithm and generate passwords')
    parser.add_argument('--language', '-l', choices=['en', 'tr'], default='en', 
                      help='Select language (en: English, tr: Turkish)')
    
    args = parser.parse_args()
    
    # Set language
    language = args.language
    set_language(language)
    
    if args.benchmark:
        performance_benchmark()
    elif args.generate:
        password_generator_mode()
    elif args.encrypt:
        file_encryption_mode()
    elif args.optimal:
        generate_optimal_passwords()
    else:
        while True:
            clear_screen()
            print_banner("Fibonacci Cipher")
            
            if language == 'tr':
                print_header("FİBONACCİ ŞİFRELEME ARACI")
                print(f"{Fore.CYAN}1.{Style.RESET_ALL} Performans Karşılaştırması")
                print(f"{Fore.CYAN}2.{Style.RESET_ALL} Şifre Üreteci")
                print(f"{Fore.CYAN}3.{Style.RESET_ALL} Dosya Şifreleme")
                print(f"{Fore.CYAN}4.{Style.RESET_ALL} Optimum Algoritma ile Şifre Üretimi")
                print(f"{Fore.CYAN}5.{Style.RESET_ALL} Dil Değiştir (Türkçe → English)")
                print(f"{Fore.CYAN}0.{Style.RESET_ALL} Çıkış")
                
                prompt = f"\n{Fore.YELLOW}Seçiminiz (0-5):{Style.RESET_ALL} "
            else:
                print_header("FIBONACCI CIPHER TOOL")
                print(f"{Fore.CYAN}1.{Style.RESET_ALL} Performance Benchmark")
                print(f"{Fore.CYAN}2.{Style.RESET_ALL} Password Generator")
                print(f"{Fore.CYAN}3.{Style.RESET_ALL} File Encryption")
                print(f"{Fore.CYAN}4.{Style.RESET_ALL} Optimal Algorithm Password Generation")
                print(f"{Fore.CYAN}5.{Style.RESET_ALL} Change Language (English → Türkçe)")
                print(f"{Fore.CYAN}0.{Style.RESET_ALL} Exit")
                
                prompt = f"\n{Fore.YELLOW}Your choice (0-5):{Style.RESET_ALL} "
            
            try:
                mode = input(prompt).strip()
                
                if mode == "1":
                    performance_benchmark()
                elif mode == "2":
                    password_generator_mode()
                elif mode == "3":
                    file_encryption_mode()
                elif mode == "4":
                    generate_optimal_passwords()
                elif mode == "5":
                    # Toggle language
                    language = 'en' if language == 'tr' else 'tr'
                    set_language(language)
                elif mode == "0":
                    clear_screen()
                    print_banner("Fibonacci Cipher")
                    
                    if language == 'tr':
                        print_success("Program sonlandırıldı. Güle güle!")
                    else:
                        print_success("Program terminated. Goodbye!")
                        
                    sys.exit(0)
                else:
                    if language == 'tr':
                        print_error("Geçersiz seçim!")
                    else:
                        print_error("Invalid choice!")
                    time.sleep(1)
            except ValueError:
                if language == 'tr':
                    print_error("Lütfen geçerli bir sayı girin!")
                else:
                    print_error("Please enter a valid number!")
                time.sleep(1)

# Global variables for language strings
LANG = {}

def set_language(lang_code):
    """Set the application language"""
    global LANG
    
    if lang_code == 'tr':
        LANG = {
            # Common
            'continue': "Devam etmek için Enter tuşuna basın...",
            'return_menu': "Ana menüye dönmek için Enter tuşuna basın...",
            'valid_numbers': "Lütfen geçerli sayılar girin!",
            'unexpected_error': "Beklenmeyen hata: {}",
            
            # Benchmark
            'benchmark_title': "ALGORİTMA PERFORMANS KARŞILAŞTIRMASI",
            'testing_algorithms': "Her algoritma sırayla test ediliyor...",
            'method_measuring': "{} yöntemi ile ölçüm yapılıyor...",
            'method_incorrect': "{} doğru sonuç vermedi!",
            'comparison_title': "PERFORMANS KARŞILAŞTIRMASI",
            'summary_title': "ÖZET",
            'fastest_method': "En hızlı yöntem: {} ({:.6f} saniye)",
            'memory_efficient': "En bellek-verimli yöntem: {} ({:.2f} KB)",
            'theory_title': "Teorik Karmaşıklıklar",
            'saving_results': "Sonuçlar dosyaya kaydediliyor...",
            'results_saved': "Sonuçlar '{}' dosyasına kaydedildi.",
            
            # Table headers
            'header_method': "Metot",
            'header_time': "Süre (saniye)",
            'header_memory_current': "Anlık Bellek (KB)",
            'header_memory_peak': "Tepe Bellek (KB)",
            'header_accuracy': "Doğruluk",
            'header_algorithm': "Algoritma",
            'header_complexity': "Zaman Karmaşıklığı",
            'header_description': "Açıklama",
            
            # Complexity descriptions
            'expo_slowest': "Üstel - En Yavaş",
            'linear_good': "Doğrusal - İyi",
            'linear_good_const': "Doğrusal - İyi (Sabit Alan)",
            'log_very_good': "Logaritmik - Çok İyi",
            'const_best': "Sabit - En İyi",
            
            # Password generator
            'pwd_gen_title': "FİBONACCİ ŞİFRE ÜRETECİ",
            'pwd_count': "Kaç şifre üretilsin? (1-10):",
            'pwd_length': "Şifre uzunluğu kaç karakter olsun? (8-32):",
            'method_select': "FİBONACCİ METODU SEÇİMİ",
            'default': "(Varsayılan)",
            'your_choice': "Seçiminiz (1-5):",
            'generating_pwd': "{} metodu kullanılarak {} adet {} karakterlik şifre üretiliyor...",
            'pwd_generated': "ÜRETİLEN ŞİFRELER",
            'pwd_analysis': "ŞİFRE ANALİZİ",
            'pwd_number': "{}. Şifre: {}",
            'pwd_strength': "Güç: {} ({}/10)",
            'pwd_suggestions': "Öneriler: {}",
            'save_option': "Şifreleri bir dosyaya kaydetmek ister misiniz? (E/H):",
            'filename': "Dosya adı (passwords.txt):",
            'pwd_saved': "Şifreler {} dosyasına kaydedildi.",
            
            # File encryption
            'file_enc_title': "FİBONACCİ DOSYA ŞİFRELEME",
            'file_enc_intro1': "Bu ekranda dosyalarınızı Fibonacci tabanlı algoritma ile şifreleyebilir veya şifrelerini çözebilirsiniz.",
            'file_enc_intro2': "Lütfen önce işlem türünü, sonra giriş ve çıkış dosyalarını, son olarak da kullanılacak algoritmayı seçin.",
            'op_type': "İŞLEM TÜRÜ",
            'op_encrypt': "Şifrele",
            'op_decrypt': "Şifre Çöz",
            'file_paths': "DOSYA YOLLARI",
            'input_file_prompt': "Lütfen şifrelenecek/çözülecek dosyanın tam yolunu girin.",
            'input_file': "Giriş dosyası:",
            'input_file_error': "Hata: Giriş dosyası belirtilmedi!",
            'file_not_found': "Hata: '{}' dosyası bulunamadı!",
            'output_file_prompt': "Lütfen çıktı dosyasının tam yolunu girin veya varsayılan için boş bırakın.",
            'output_file': "Çıkış dosyası:",
            'default_output': "Varsayılan çıkış dosyası kullanılıyor: {}",
            'encrypting_file': "{} dosyası şifreleniyor... {} metodu kullanılıyor.",
            'file_size': "Dosya boyutu: {} byte",
            'decrypting_file': "{} dosyasının şifresi çözülüyor... {} metodu kullanılıyor.",
            'success': "İşlem başarıyla tamamlandı!",
            'output_file_result': "Çıkış dosyası: {}",
            'failure': "İşlem başarısız oldu!",
            
            # Password strength
            'weak': "Zayıf",
            'medium': "Orta",
            'strong': "Güçlü",
            'very_strong': "Çok Güçlü",
            
            # Optimal algorithm
            'opt_title': "OPTİMUM FİBONACCİ ŞİFRE ÜRETECİ",
            'opt_evaluating': "En optimum algoritma değerlendiriliyor...",
            'opt_generating': "{} ile şifreler üretiliyor...",
            'opt_comparison': "ALGORİTMA KARŞILAŞTIRMASI",
            'opt_result': "SONUÇ",
            'opt_algorithm': "En optimum algoritma: {} (Skor: {:.2f})",
            'opt_complexity': "Teorik Karmaşıklık: {}",
            'opt_time': "Süre: {:.6f} saniye",
            'opt_memory': "Bellek Kullanımı: {:.2f} KB",
            'opt_passwords': "PASSWORDS GENERATED WITH OPTIMAL ALGORITHM",
            'save_all': "Tüm algoritmaların ürettiği şifreleri de kaydetmek ister misiniz? (E/H):",
            'alg_passwords_saved': "{} algoritmasının şifreleri {} dosyasına kaydedildi."
        }
    else:  # Default to English
        LANG = {
            # Common
            'continue': "Press Enter to continue...",
            'return_menu': "Press Enter to return to the main menu...",
            'valid_numbers': "Please enter valid numbers!",
            'unexpected_error': "Unexpected error: {}",
            
            # Benchmark
            'benchmark_title': "ALGORITHM PERFORMANCE COMPARISON",
            'testing_algorithms': "Testing each algorithm in sequence...",
            'method_measuring': "Measuring with {} method...",
            'method_incorrect': "{} did not produce correct results!",
            'comparison_title': "PERFORMANCE COMPARISON",
            'summary_title': "SUMMARY",
            'fastest_method': "Fastest method: {} ({:.6f} seconds)",
            'memory_efficient': "Most memory-efficient method: {} ({:.2f} KB)",
            'theory_title': "Theoretical Complexity",
            'saving_results': "Saving results to file...",
            'results_saved': "Results saved to '{}' file.",
            
            # Table headers
            'header_method': "Method",
            'header_time': "Time (seconds)",
            'header_memory_current': "Current Memory (KB)",
            'header_memory_peak': "Peak Memory (KB)",
            'header_accuracy': "Accuracy",
            'header_algorithm': "Algorithm",
            'header_complexity': "Time Complexity",
            'header_description': "Description",
            
            # Complexity descriptions
            'expo_slowest': "Exponential - Slowest",
            'linear_good': "Linear - Good",
            'linear_good_const': "Linear - Good (Constant Space)",
            'log_very_good': "Logarithmic - Very Good",
            'const_best': "Constant - Best",
            
            # Password generator
            'pwd_gen_title': "FIBONACCI PASSWORD GENERATOR",
            'pwd_count': "How many passwords to generate? (1-10):",
            'pwd_length': "Password length (characters)? (8-32):",
            'method_select': "FIBONACCI METHOD SELECTION",
            'default': "(Default)",
            'your_choice': "Your choice (1-5):",
            'generating_pwd': "Generating {} passwords of {} characters using {} method...",
            'pwd_generated': "GENERATED PASSWORDS",
            'pwd_analysis': "PASSWORD ANALYSIS",
            'pwd_number': "{}. Password: {}",
            'pwd_strength': "Strength: {} ({}/10)",
            'pwd_suggestions': "Suggestions: {}",
            'save_option': "Would you like to save the passwords to a file? (Y/N):",
            'filename': "Filename (passwords.txt):",
            'pwd_saved': "Passwords saved to {} file.",
            
            # File encryption
            'file_enc_title': "FIBONACCI FILE ENCRYPTION",
            'file_enc_intro1': "On this screen, you can encrypt or decrypt files using Fibonacci-based algorithm.",
            'file_enc_intro2': "Please select the operation type, then input and output files, and finally the algorithm to use.",
            'op_type': "OPERATION TYPE",
            'op_encrypt': "Encrypt",
            'op_decrypt': "Decrypt",
            'file_paths': "FILE PATHS",
            'input_file_prompt': "Please enter the full path of the file to encrypt/decrypt.",
            'input_file': "Input file:",
            'input_file_error': "Error: Input file not specified!",
            'file_not_found': "Error: File '{}' not found!",
            'output_file_prompt': "Please enter the full path for the output file or leave blank for default.",
            'output_file': "Output file:",
            'default_output': "Using default output file: {}",
            'encrypting_file': "Encrypting file {}... Using {} method.",
            'file_size': "File size: {} bytes",
            'decrypting_file': "Decrypting file {}... Using {} method.",
            'success': "Operation completed successfully!",
            'output_file_result': "Output file: {}",
            'failure': "Operation failed!",
            
            # Password strength
            'weak': "Weak",
            'medium': "Medium", 
            'strong': "Strong",
            'very_strong': "Very Strong",
            
            # Optimal algorithm
            'opt_title': "OPTIMAL FIBONACCI PASSWORD GENERATOR",
            'opt_evaluating': "Evaluating the optimal algorithm...",
            'opt_generating': "Generating passwords with {}...",
            'opt_comparison': "ALGORITHM COMPARISON",
            'opt_result': "RESULT",
            'opt_algorithm': "Optimal algorithm: {} (Score: {:.2f})",
            'opt_complexity': "Theoretical Complexity: {}",
            'opt_time': "Time: {:.6f} seconds",
            'opt_memory': "Memory Usage: {:.2f} KB",
            'opt_passwords': "PASSWORDS GENERATED WITH OPTIMAL ALGORITHM",
            'save_all': "Would you like to save passwords generated by all algorithms? (Y/N):",
            'alg_passwords_saved': "Passwords from {} algorithm saved to {} file."
        }

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"Hata: {e}") 