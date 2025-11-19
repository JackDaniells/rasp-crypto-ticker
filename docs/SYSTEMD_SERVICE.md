# Systemd Service Setup Guide

Complete guide for setting up the crypto ticker to run automatically on boot using systemd.

---

## 🔄 Running on Boot (Autostart)

To have your crypto ticker start automatically when the Raspberry Pi boots up, use systemd services.

### Step 1: Create Launcher Script

Create a script file with all instructions to boot the app:

```bash
nano /path_to_project/launcher.sh
```

**Script content:**
```bash
#!/bin/bash
cd path_to_file
python main.py
```

Make it executable:
```bash
chmod +x /path_to_project/launcher.sh
```

---

### Step 2: Create Systemd Service File

Create a systemd service file to manage the crypto ticker:

```bash
sudo nano /etc/systemd/system/crypto_ticker.service
```

---

### Step 3: Add Service Configuration

Add the following content to the service file:

```ini
[Unit]
Description=Crypto Ticker Display Service
After=network.target

[Service]
Type=simple
ExecStart=/path_to_project/script.sh
User=pi
WorkingDirectory=/path_to_project
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Environment variables (if needed)
Environment="WEATHER_API_KEY=your_api_key_here"

[Install]
WantedBy=multi-user.target
```

**Configuration Explanation:**
- `Description`: Human-readable description of the service
- `After=network.target`: Wait for network to be available before starting
- `Type=simple`: The process starts and runs continuously
- `ExecStart`: Path to your launcher script
- `User`: Run as user 'pi' (change to your username)
- `WorkingDirectory`: Project directory
- `Restart=always`: Automatically restart if it crashes
- `RestartSec=10`: Wait 10 seconds before restarting
- `StandardOutput=journal`: Log output to systemd journal
- `Environment`: Set environment variables (optional)
- `WantedBy=multi-user.target`: Start in multi-user mode

---

### Step 4: Set Environment Variables (Optional)

If you need to set the weather API key:

```bash
# Create environment file
sudo nano .env

# Add your API key
WEATHER_API_KEY=your_actual_api_key

# Update service file to use it
[Service]
EnvironmentFile=path_to_file/.env
```

---

### Step 5: Enable and Start the Service

```bash
# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable crypto_ticker.service

# Start the service now
sudo systemctl start crypto_ticker.service
```

---

### Step 6: Verify Service Status

```bash
# Check if service is running
sudo systemctl status crypto_ticker.service

# Should show: "active (running)" in green
```

---

## 🔧 Managing the Systemd Service

### Check Service Status
```bash
sudo systemctl status crypto_ticker.service
```

### Start the Service
```bash
sudo systemctl start crypto_ticker.service
```

### Stop the Service
```bash
sudo systemctl stop crypto_ticker.service
```

### Restart the Service
```bash
sudo systemctl restart crypto_ticker.service
```

### Disable Autostart
```bash
sudo systemctl disable crypto_ticker.service
```

### View Service Logs
```bash
# View recent logs
sudo journalctl -u crypto_ticker.service

# View logs in real-time (follow)
sudo journalctl -u crypto_ticker.service -f

# View last 50 lines
sudo journalctl -u crypto_ticker.service -n 50

# View logs since last boot
sudo journalctl -u crypto_ticker.service -b
```

### Edit Service Configuration
```bash
# Edit the service file
sudo nano /etc/systemd/system/crypto_ticker.service

# After editing, reload and restart
sudo systemctl daemon-reload
sudo systemctl restart crypto_ticker.service
```

---

## 🐛 Troubleshooting Systemd Service

### Service won't start?

**Check the status for errors:**
```bash
sudo systemctl status crypto_ticker.service
```

**Check detailed logs:**
```bash
sudo journalctl -u crypto_ticker.service -n 100 --no-pager
```

**Common issues:**

1. **Permission denied on launcher script**
   ```bash
   chmod +x /path_to_project/launcher.sh
   ```

2. **Python module not found**
   - Make sure you're using the correct Python interpreter
   - Install packages: `pip install -r requirements.txt`

3. **Environment variables not set**
   - Add `Environment="WEATHER_API_KEY=..."` to service file
   - Or use `EnvironmentFile=/path/to/.env`

4. **LCD I2C not accessible**
   - Make sure user has I2C permissions:
     ```bash
     sudo usermod -a -G i2c pi
     sudo usermod -a -G gpio pi
     ```
   - Reboot after adding to groups

5. **Service starts but displays nothing**
   - Check logs: `sudo journalctl -u crypto_ticker.service -f`
   - Verify LCD is connected: `i2cdetect -y 1`
   - Test manually: `python main.py`

---

### Test manually before enabling service

Before setting up the systemd service, make sure everything works manually:

```bash
# Navigate to project directory
cd /path_to_project

# Set environment variable
export WEATHER_API_KEY="your_api_key"

# Run manually
python main.py

# If it works, then set up the service
```

---

## 🔄 Alternative Autostart Methods

### Method 1: Using cron @reboot (Simple)

If you don't need logging or automatic restarts:

```bash
# Edit crontab
crontab -e

# Add this line
@reboot sleep 30 && /path_to_project/launcher.sh
```

**Pros:** Simple, easy to set up  
**Cons:** No automatic restart, limited logging

---

### Method 2: Using /etc/rc.local (Legacy)

```bash
sudo nano /etc/rc.local

# Add before "exit 0"
/path_to_project/launcher.sh &

exit 0
```

**Pros:** Simple, works on older systems  
**Cons:** Deprecated, no service management

---

### Method 3: Using systemd (Recommended) ✅

Already described above - best option for:
- Automatic restart on failure
- Proper logging
- Service management
- Dependency handling
- Environment variables

---

## 📋 Service File Examples

### Minimal Service (No Virtual Environment)

```ini
[Unit]
Description=Crypto Ticker
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/main.py
WorkingDirectory=/path/to/project
User=pi
Restart=always

[Install]
WantedBy=multi-user.target
```

---

### With Virtual Environment

```ini
[Unit]
Description=Crypto Ticker
After=network.target

[Service]
ExecStart=/path/to/project/venv/bin/python /path/to/project/main.py
WorkingDirectory=/path/to/project
User=pi
Environment="WEATHER_API_KEY=your_key"
Restart=always

[Install]
WantedBy=multi-user.target
```

---

### With Launcher Script

```ini
[Unit]
Description=Crypto Ticker
After=network.target

[Service]
ExecStart=/path/to/project/launcher.sh
WorkingDirectory=/path/to/project
User=pi
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## 🎯 Best Practices

1. **Test manually first** - Always verify the app works before creating the service
2. **Use absolute paths** - Avoid relative paths in service files
3. **Set proper user** - Don't run as root unless necessary
4. **Enable logging** - Use `StandardOutput=journal` for debugging
5. **Add restart policy** - `Restart=always` ensures reliability
6. **Wait for network** - `After=network.target` for API-dependent apps
7. **Use environment files** - Keep sensitive data in separate files
8. **Check permissions** - Ensure user has access to I2C, GPIO, etc.

---

## 📝 Quick Command Reference

```bash
# Service Management
sudo systemctl start crypto_ticker.service      # Start
sudo systemctl stop crypto_ticker.service       # Stop
sudo systemctl restart crypto_ticker.service    # Restart
sudo systemctl status crypto_ticker.service     # Status
sudo systemctl enable crypto_ticker.service     # Enable on boot
sudo systemctl disable crypto_ticker.service    # Disable on boot

# View Logs
sudo journalctl -u crypto_ticker.service        # All logs
sudo journalctl -u crypto_ticker.service -f     # Follow logs
sudo journalctl -u crypto_ticker.service -n 50  # Last 50 lines
sudo journalctl -u crypto_ticker.service -b     # Since boot

# Service File Management
sudo systemctl daemon-reload                    # Reload after changes
sudo systemctl edit crypto_ticker.service       # Edit with override
sudo nano /etc/systemd/system/crypto_ticker.service  # Direct edit
```

---

## 💡 Tips

- **Check service status regularly** during initial setup
- **Use `journalctl -f`** to watch logs in real-time while testing
- **Set RestartSec** to avoid rapid restart loops on persistent errors
- **Document your configuration** for future reference
- **Test after reboot** to ensure autostart works correctly

---

**For more information:**
- Systemd documentation: https://www.freedesktop.org/software/systemd/man/systemd.service.html
- Raspberry Pi systemd guide: https://www.raspberrypi.org/documentation/linux/usage/systemd.md

---

**Back to main README**: See [README.md](../README.md) for project overview and basic setup.

