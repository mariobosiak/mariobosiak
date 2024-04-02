from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def pobierz_dane_ze_strony(nr_kw):
    # Ścieżka do sterownika przeglądarki - należy pobrać odpowiedni dla używanej przeglądarki
    driver_path = 'ścieżka_do_sterownika'
    driver = webdriver.Chrome(driver_path)  # Inicjalizacja przeglądarki (w tym przypadku Chrome)

    driver.get("https://przegladarka-ekw.ms.gov.pl/eukw_prz/KsiegiWieczyste/wyszukiwanieKW?komunikaty=true&kontakt=true&okienkoSerwisowe=false")
    time.sleep(5)  # Poczekaj 2 sekundy na załadowanie strony

    # Znajdź pole do wprowadzenia numeru KW i wprowadź numer KW
    input_field = driver.find_element_by_id("nrKw")
    input_field.send_keys(nr_kw)

    # Kliknij przycisk "Szukaj"
    search_button = driver.find_element_by_xpath("//button[contains(text(),'Wyszukaj KsięgęWR1O/00056058/2')]")
    search_button.click()

    time.sleep(5)  # Poczekaj 2 sekundy na załadowanie wyników

    # Pobierz dane z wyników
    dane = driver.find_element_by_class_name("dataTables_wrapper")
    # Tutaj możesz przetwarzać dane według potrzeb

    # Zamknij przeglądarkę
    driver.quit()

    return dane

# Podaj numer KW
nr_kw = input("Podaj numer KW: ")
dane = pobierz_dane_ze_strony(nr_kw)
print(dane)  # Wyświetl dane
