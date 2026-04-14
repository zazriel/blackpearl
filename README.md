# 💬 Python Real-Time Chatroom

A sleek, modern desktop chat application built with **Python**, powered by **PubNub's** global real-time network and styled with the **CustomTkinter** widget library. This project focuses on secure, real-time communication with a scalable architecture and a clean user experience.

---

## 🚀 Overview

This application is a **private, token-secured chatroom** that enables users to communicate instantly across multiple clients. It uses PubNub’s **Publish/Subscribe model** along with **Access Manager (PAM v3)** to ensure only authorized users can access the system.

The current implementation delivers a solid real-time messaging foundation, with a roadmap for advanced features and system enhancements.

---

## ✨ Features

* 🔑 **Token-Based Authentication (PAM v3)**
  Secure access using dynamically generated tokens tied to specific users.

* 💬 **Real-Time Messaging**
  Instant delivery and reception of messages using PubNub’s infrastructure.

* 🖥️ **Modern UI**
  Clean, contemporary interface with dark/light mode support via `CustomTkinter`.

* 👤 **User Identification**
  Each user is uniquely identified using a `uuid`.

* 🔄 **Auto-Scrolling Chat**
  Chat window automatically updates to display the latest messages.

* 🌍 **Multi-Client Support**
  Scalable backend allows multiple users to communicate globally.

* 🟢 **User Presence **
  Ability to track online/offline users in the chatroom.

---

## 🛠️ Built With

* **Python 3.x** – Core programming language
* **PubNub Python SDK** – Real-time messaging infrastructure
* **CustomTkinter** – Modern UI components and theming

---

## ⚙️ How It Works

1. A secure token is generated using a backend script .
2. The token is bound to a specific `uuid`.
3. The client application uses this token to:

   * Subscribe to a chat channel
   * Publish messages
4. PubNub enforces access control using PAM, ensuring only authorized users can interact.

---

## 🚀 Getting Started

### 📌 Prerequisites

1. **PubNub Keys**
   Get your `Publish Key` and `Subscribe Key` from the [PubNub Admin Portal](https://admin.pubnub.com/).

2. **Python**
   Ensure Python 3.8+ is installed.

---

### 📦 Installation

```bash
git clone https://github.com/zazriel/blackpearl.git
cd blackpearl
pip install -r requirements.txt
```

---

### ▶️ Run the Chat Client

```bash
python blackpearl_frontend.py
```

* Enter the `username`&`passwaord`

---

## ⚠️ Important Notes

* 🔒 Keep your PubNub keys and secret key secure.

---

## 🧠 Future Enhancements

This project is actively evolving. Planned features include:

* ⌨️ Typing indicators
* 📜 Message history & persistence
* 🔒 End-to-end encryption
* 📨 Private/direct messaging
* 📁 File and media sharing
* 🎨 Advanced UI/UX improvements

---

## 🤝 Contributing

This is currently a private project, but ideas, feedback, and collaboration are welcome for future development.

---

## 📄 License

This project is private and not licensed for public distribution at this time.

---

## 💡 Inspiration

Built as a practical exploration of **real-time systems**, **secure messaging**, and **modern Python GUI development**.

---
