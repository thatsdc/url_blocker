# 🚫 Local URL Blocker (Python)

This is a simple Python script that **blocks access to specific websites locally** on your computer.  
It works by editing the system’s **hosts file**, which controls how domain names are resolved.

This project is designed for **personal use**, **focus sessions**, or **parental control**, and does **not** affect other devices on the network.

---

## 🧠 What It Does

The script prevents your computer from loading certain websites by redirecting their URLs to your own machine (the local address `127.0.0.1`).  
For example, if you block `facebook.com`, every time you try to open Facebook, your computer will instead look for it on your local system — and the page won’t load.

In short:
- You choose which URLs to block.  
- The script adds them to your hosts file.  
- Those URLs become unreachable on your computer.  

---

## ⚙️ How It Works

1. The script opens your system’s **hosts file**:
   - On Windows: `C:\Windows\System32\drivers\etc\hosts`

2. It adds lines like:
127.0.0.1 facebook.com
127.0.0.1 www.facebook.com

3. Once saved, the operating system will redirect all requests for those websites to your local machine (which has no web server running), effectively **blocking access**.

4. To unblock, you can simply use the option 'Unblock all the URLs' or if you prefer edit directly the hosts files.

---

## ⚠️ Notes

- You need **administrator/root privileges** to modify the hosts file.  
- The script only affects **your local computer**, not your entire network.  
- It doesn’t collect or send any data — everything happens locally.

---

## 💡 Example

Before running the script:
ping facebook.com
Pinging facebook.com [31.13.71.36]...

After running the script:
ping facebook.com
Pinging facebook.com [127.0.0.1]...
