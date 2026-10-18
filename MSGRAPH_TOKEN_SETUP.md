# Konfiguracja tokena MS Graph w parsedmarc-dockerized

Ten dokument opisuje dwa niezależne, poprawne warianty konfiguracji odświeżania tokena OAuth2 dla Microsoft Graph:
1. `client secret` (sekret aplikacji)
2. `certificate` (certyfikat aplikacji)

W obu przypadkach token jest zapisywany przez `msgraph-token-refresh` do współdzielonego wolumenu Docker: `/tokens/.token.json`.

## Wymagania wspólne
1. Upewnij się, że działa zewnętrzny stack Elasticsearch i istnieje sieć `elasticsearch_elastic` (lub ustaw własną w `.env` jako `ELASTIC_NETWORK`).
2. Skopiuj plik środowiskowy:
```bash
cp .env.example .env
```
3. Ustaw co najmniej:
```env
TENANT_ID=<tenant-id-guid>
CLIENT_ID=<app-registration-client-id>
```
4. W Entra ID dodaj uprawnienia aplikacyjne do Microsoft Graph wymagane przez Twój scenariusz (np. `Mail.Read` / `Mail.ReadWrite`) i wykonaj `Grant admin consent`.

## Przypadek 1: Token po `client secret`

### 1) Utwórz sekret aplikacji w Entra ID
1. Wejdź w `App registrations` -> Twoja aplikacja -> `Certificates & secrets` -> `New client secret`.
2. Skopiuj wartość sekretu (tylko raz).

### 2) Zapisz sekret jako Docker secret (plik lokalny)
```bash
printf '%s' 'TU_WKLEJ_CLIENT_SECRET' > secrets/msgraph_client_secret.txt
chmod 600 secrets/msgraph_client_secret.txt
```

### 3) Uruchom odświeżanie tokena profilem `msgraph-secret`
```bash
sudo docker compose --profile msgraph-secret up -d --build msgraph-token-refresh-secret
```

### 4) Zweryfikuj wygenerowany token
```bash
sudo docker compose exec msgraph-token-refresh-secret sh -c 'ls -l /tokens/.token.json && tail -n +1 /tokens/.token.json'
```

## Przypadek 2: Token po `certificate`

### 1) Przygotuj certyfikat aplikacji
Wymagane są:
1. Klucz prywatny w PEM (`secrets/msgraph_client_certificate.pem`)
2. Certyfikat publiczny w PEM (`secrets/msgraph_client_certificate_public.pem`)
3. Thumbprint certyfikatu ustawiony w `.env` jako `MSGRAPH_CERT_THUMBPRINT`

Przykład ustawienia uprawnień plików:
```bash
chmod 600 secrets/msgraph_client_certificate.pem
chmod 644 secrets/msgraph_client_certificate_public.pem
```

### 2) Dodaj certyfikat publiczny do App Registration
1. Wejdź w `App registrations` -> Twoja aplikacja -> `Certificates & secrets` -> `Certificates`.
2. Dodaj certyfikat publiczny odpowiadający kluczowi prywatnemu.
3. Skopiuj thumbprint i ustaw w `.env`:
```env
MSGRAPH_CERT_THUMBPRINT=<thumbprint-bez-spacji>
```

### 3) Uruchom odświeżanie tokena profilem `msgraph-cert`
```bash
sudo docker compose --profile msgraph-cert up -d --build msgraph-token-refresh-cert
```

### 4) Zweryfikuj wygenerowany token
```bash
sudo docker compose exec msgraph-token-refresh-cert sh -c 'ls -l /tokens/.token.json && tail -n +1 /tokens/.token.json'
```

## Integracja z parsedmarc
`msgraph-token-refresh` generuje token typu bearer w pliku `/tokens/.token.json`.
To jest przydatne dla integracji, które potrafią czytać gotowy token z pliku.
W tym repo domyślna konfiguracja `parsedmarc/parsedmarc.ini` używa sekcji `[imap]` i nie korzysta bezpośrednio z tego pliku tokena.
Jeśli chcesz przejść na natywną konfigurację `[msgraph]` w parsedmarc, skonfiguruj ją osobno zgodnie z dokumentacją parsedmarc i uruchom:
```bash
sudo docker compose up -d parsedmarc
```

## Najczęstsze błędy
1. `Missing env var: TENANT_ID` lub `CLIENT_ID`: brak wartości w `.env`.
2. `invalid_client`: błędny sekret, niepasujący certyfikat albo zły `MSGRAPH_CERT_THUMBPRINT`.
3. Brak pliku `/tokens/.token.json`: nie uruchomiono profilu `msgraph-secret` / `msgraph-cert` albo odświeżacz nie ma poprawnych danych logowania.
4. `insufficient privileges`: brak wymaganych uprawnień aplikacyjnych w Microsoft Graph albo brak `admin consent`.
