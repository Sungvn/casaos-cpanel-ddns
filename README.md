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
- Docker / Docker Compose (included with CasaOS)
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

## Installation

### Method 1 — Manual Installation (Recommended / Current Working Method)

Some CasaOS versions do not support importing compose apps directly from URL. Manual installation via terminal is currently the most reliable method.

#### Step 1 — SSH into your CasaOS server

```bash
ssh username@your-server-ip
```

Example:

```bash
ssh root@192.168.1.xx
```

#### Step 2 — Clone repository

```bash
git clone https://github.com/Sungvn/casaos-cpanel-ddns.git
```

#### Step 3 — Enter application directory

```bash
cd casaos-cpanel-ddns/Apps/CpanelDynamicDNS
```

#### Step 4 — Start the application

```bash
docker compose up -d
```

Docker will:

- Build the application container
- Create persistent storage
- Start the web UI service

#### Step 5 — Open the web interface

Open your browser:

```
http://YOUR_SERVER_IP:7788
```

Example:

```
http://192.168.1.xx:7788
```

---

### Method 2 — CasaOS App Store Installation (Future Native Support)

When full native CasaOS support is available:

1. Open CasaOS App Store.
2. Add source:

```
https://github.com/Sungvn/casaos-cpanel-ddns/archive/refs/heads/main.zip
```

3. Install **cPanel Dynamic DNS (UI)**.
4. Click Open.

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

## Access CasaOS via DDNS Domain (Port Forwarding)

If you want to access CasaOS using your DDNS domain (for example: `http://homeserver.domain.ext`), you must configure port forwarding on your router.

### Example setup:

Forward the following ports from your router to your CasaOS server:

| External Port | Internal IP | Internal Port | Protocol |
|---------------|-------------|---------------|----------|
| 80            | 192.168.1.xx | 80            | TCP      |
| 443           | 192.168.1.xx | 443           | TCP      |

After port forwarding:

```
http://homeserver.vossen.network
```

will load your CasaOS dashboard instead of the local IP address.

You may also access the DDNS app UI externally:

```
http://homeserver.domain.ext:7788
```

⚠️ Security Note: Exposing services directly to the internet is not always recommended. Consider using a reverse proxy (Nginx Proxy Manager, Caddy, or Traefik) and HTTPS for better security.

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

Or via SSH:

```bash
docker logs cpanel-ddns-ui
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
- One-click native CasaOS installation

---

## License

MIT

---

## Author

Created by Sungvn  
Developer at VossenNetwork  
https://vossen.network
