import math
import string


def z1(podloga_dlugosc, podloga_szerokosc, panel_dl, panel_szer, ilosc_panel_w_opak):
    pole_podlogi = podloga_dlugosc * podloga_szerokosc
    pole_podlogi += pole_podlogi * 0.1
    pole_panelu = panel_dl * panel_szer
    pole_opakowania = pole_panelu * ilosc_panel_w_opak
    return pole_podlogi / pole_opakowania


def z2(*liczby):
    for liczba in liczby:
        is_prime = True
        for i in range(2, round(math.sqrt(liczba)) + 1):
            if liczba % i == 0:
                is_prime = False
                break
        if is_prime and liczba != 0 and liczba != 1:
            print(f"Liczba {liczba} jest pierwsza")
        else:
            print(f"Liczba {liczba} nie jest pierwsza")


def z3(data1, key, alphabet=list(string.ascii_lowercase)):
    data = list(data1.lower())
    for i in range(len(data)):
        if data[i] in alphabet:
            new_index = int(math.fabs((alphabet.index(data[i]) + key)%len(alphabet)))
            data[i] = alphabet[new_index]
    return ''.join(data)

print(round(z1(4, 4, 0.2, 1, 10)))  # zadanie 1
z2(0, 1, 2, 3, 4, 5)  # zadanie 2
print(z3("The Project Gutenberg eBook of Alice’s Adventures in Wonderland, by Lewis Carroll", 99, ["a","B"]))