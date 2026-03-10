# SecureDropVault

A secure password-based encrypted vault using AES-256 encryption with salted key derivation and tamper detection.

## Features

- **User Registration** — Accounts with randomly generated salts and selectable hash mode (MD5/SHA256)
- **Secure Note Storage** — AES-256-CBC encryption with password-based key derivation
- **Integrity Verification** — SHA-256 hashing to verify data hasn't been modified
- **Tamper Detection** — Detects any unauthorized changes to encrypted data

## Requirements

- Python 3.x
- pycryptodome (`pip install pycryptodome`)

## Usage

```bash
python Assignment1.py
```

Menu options:

```
1.Register  2.Store  3.Read  4.Tamper  5.DeleteUser  6.Exit
```

## Libraries Used

`os` · `json` · `base64` · `hashlib` · `Crypto.Cipher.AES` · `Crypto.Util.Padding`
