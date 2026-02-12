# cPanel Dynamic DNS for CasaOS

Automatically update your **cPanel Dynamic DNS (DDNS)** record directly from CasaOS.

This lightweight CasaOS app monitors your public IP address and updates your cPanel Dynamic DNS entry whenever your IP changes.

---

## Features

- Automatic Dynamic DNS updates for cPanel
- Works with CasaOS custom app stores
- Lightweight and reliable background service
- No API keys or login required (uses secure cPanel webcall URL)
- Supports AMD64, ARM64, and ARM devices

---

## Requirements

- CasaOS installed
- cPanel hosting account with Dynamic DNS enabled

---

## Setup (cPanel)

1. Login to your cPanel account.
2. Navigate to:

```
Domains → Dynamic DNS
```

3. Create a new Dynamic DNS domain.
4. Copy the generated **webcall URL**.

Example:

```
https://example.com/cpanelwebcall/xxxxxxxxxxxxxxxx
```

⚠️ Treat this URL like a password — anyone with it can update your DNS.

---

## Installation (CasaOS)

### Add App Store Source

Open CasaOS:

```
App Store → Add Source
```

Paste:

```
https://github.com/Sungvn/casaos-cpanel-ddns/archive/refs/heads/main.zip
```

---

### Install App

1. Find **cPanel Dynamic DNS** in the App Store.
2. Click Install.
3. Configure:

```
WEBCALL_URL    = your cPanel webcall URL
CHECK_INTERVAL = 300 (recommended default)
IP_CHECK_URL   = https://api.ipify.org
```

---

## How It Works

The container:

1. Checks your public IP address.
2. Detects changes.
3. Calls your cPanel DDNS webcall automatically.
4. Updates DNS only when needed.

---

## Logs

View logs inside CasaOS:

```
App → Terminal / Logs
```

---

## Security

- No credentials stored.
- Uses cPanel's secure webcall mechanism.
- Only updates when IP changes.

---

## Roadmap

- Built-in UI dashboard
- Status panel (current IP / last update)
- Manual update button
- Enhanced logging

---

## License

MIT

---

## Author

Created by Sungvn  
Developer at VossenNetwork  
https://vossen.network
