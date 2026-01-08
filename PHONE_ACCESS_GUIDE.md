# 📱 Access Quantum Internet from Your Phone

## The Problem
Your Mac's firewall is blocking incoming connections from your phone.

## ✅ **EASIEST SOLUTION: Open Firewall for Python**

### Option 1: System Settings (GUI)
1. Open **System Settings** (or **System Preferences**)
2. Go to **Network** → **Firewall**
3. Click **Firewall Options**
4. Click the **+** button
5. Navigate to your Python:
   - Try: `/opt/homebrew/bin/python3`
   - Or: `/usr/local/bin/python3`
   - Or: `/usr/bin/python3`
6. Add it and set to **"Allow incoming connections"**
7. Click **OK**

### Option 2: Command Line (Fast)
```bash
# Add Python to firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /opt/homebrew/bin/python3
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /opt/homebrew/bin/python3

# Restart quantum server
pkill -f quantum_wifi_simple
python3 quantum_wifi_simple.py &
```

## 📱 Then Access from Phone

**Your WiFi IP:** `192.168.40.165`

Visit on your phone:
```
http://192.168.40.165:8765
```

Or try:
```
http://Nicholes-MacBook-Pro.local:8765
```

---

## 🌐 Alternative: Use Ngrok (Public URL)

If firewall doesn't work, use ngrok to create a public URL:

```bash
# Start ngrok (already installed)
ngrok http 8765
```

You'll see output like:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8765
```

Use that `https://abc123.ngrok.io` URL on **ANY device, anywhere**!

---

## ✅ **Verify It Works**

Test from your Mac first:
```bash
curl http://192.168.40.165:8765/status
```

If that works, your phone should too!

---

## 🔍 Troubleshooting

**Phone still can't connect?**
1. Make sure phone is on **same WiFi** network
2. Turn OFF **cellular data** on phone temporarily
3. Try the computer name URL instead
4. Use ngrok for guaranteed access

**Check what's blocking:**
```bash
./test_phone_connection.sh
```

This will tell you exactly what the problem is!
