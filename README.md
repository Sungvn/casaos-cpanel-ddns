# cPanel Dynamic DNS for CasaOS (UI)

A CasaOS app that provides a **web dashboard** to configure and run **cPanel Dynamic DNS (DDNS)** updates.

It monitors your public IP address and automatically updates your cPanel Dynamic DNS record when your IP changes. The built-in web UI allows easy configuration, status monitoring, and manual updates directly from CasaOS.

---

## Features

- Web UI dashboard inside CasaOS
- Automatic Dynamic DNS updates
- Manual **Test Update Now** button
- Status panel (Current IP, Last update, Last result)
- Persistent configuration storage
- Lightweight and efficient
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

3. Create a new Dynamic DNS entry.
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

1. Find **cPanel Dynamic DNS (UI)** in the App Store.
2. Click Install.
3. After installation, click **Open** to launch the web interface.

---

## Configuration

Inside the web UI:

1. Paste your cPanel Dynamic DNS **Webcall URL**
2. Set check interval (recommended: 300 seconds)
3. Save settings
4. Click **Test Update Now** to verify functionality

---

## How It Works

The app:

1. Checks your public IP address periodically.
2. Detects changes automatically.
3. Calls the cPanel Dynamic DNS webcall URL.
4. Updates DNS only when required.

---

## Status Dashboard

The UI displays:

- Current detected IP address
- Last updated IP
- Last update time
- HTTP response from cPanel
- Error messages (if any)

---

## Logs

Logs can be viewed from inside CasaOS:

```
App → Terminal / Logs
```

---

## Data Storage

Settings and runtime state are stored inside the container volume:

```
/config/settings.json
/config/state.json
```

---

## Security

- No credentials stored.
- Uses secure cPanel webcall URL.
- Webcall URL is masked inside UI.
- Only updates DNS when IP changes.

---

## Roadmap

- Enhanced dashboard styling
- Optional notification support
- Advanced logging view
- CasaOS native theme integration

---

## License

MIT

---

## Author

Created by Sungvn  
Developer at VossenNetwork  
https://vossen.network
