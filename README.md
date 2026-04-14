# 🏴‍☠️ Black Pearl --- Real-Time Pirate Chat

![Black Pearl](icons/blackpearllogo.png)

A shadowed vessel drifting across the digital seas --- **Black Pearl**
is a real-time, token-secured chat system forged in Python. Built for
speed, secrecy, and control, it channels communication through a secure,
scalable network while maintaining a dark, minimal interface.

------------------------------------------------------------------------

## ⚓ Overview

**Black Pearl** is a **private communication channel** designed for
controlled access and real-time interaction. Each user is issued a
unique identity and token, ensuring only trusted entities may board the
ship.

Powered by PubNub's infrastructure and secured via **Access Manager (PAM
v3)**, the system enforces strict access boundaries while maintaining
low-latency message delivery across clients.

------------------------------------------------------------------------

## 🗝️ Core Capabilities

-   🔑 **Token-Gated Access** Entry is restricted. Each user operates
    under a dynamically issued token bound to their identity.

-   💬 **Live Message Flow** Messages travel instantly across the
    network---no delay, no drift.

-   🖤 **Dark Interface** A minimal, modern UI styled with
    `CustomTkinter`, aligned with the Black Pearl aesthetic.

-   🧭 **Unique Identity ** Every participant is distinctly
    tracked within the system.

-   🌊 **Seamless Chat Stream** Automatic scrolling ensures no message
    is lost to the depths.

-   🏴‍☠️ **Multi-Client Network** Multiple users can connect and
    communicate across regions in real time.

-   🟢 **Presence Tracking** Know who's aboard... and who's vanished
    into the void.

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   **Python 3.x**
-   **PubNub Python SDK**
-   **CustomTkinter**

------------------------------------------------------------------------

## ⚙️ System Flow

1.  A secure token is forged via backend logic\
2.  The token is bound to a user's `uuid`\
3.  The client uses this token to:
    -   Subscribe to a shared channel\
    -   Publish messages\
4.  PubNub enforces access control at every step

------------------------------------------------------------------------

## 🚀 Deployment

### 📌 Requirements

-   PubNub `Publish Key` & `Subscribe Key`
-   Python 3.8+

------------------------------------------------------------------------

### 📦 Setup

``` bash
git clone https://github.com/zazriel/blackpearl.git
cd blackpearl
pip install -r requirements.txt
```

------------------------------------------------------------------------

### ▶️ Launch

``` bash
python blackpearl_frontend.py
```

Enter your **username** and **password** to gain access.

------------------------------------------------------------------------

## ⚠️ Security Notes

-   Your keys are your lifeline --- do not expose them\
-   Tokens are ephemeral by design; treat them as such

------------------------------------------------------------------------

## 🧠 Roadmap

Planned evolutions of the vessel:

-   ⌨️ Typing indicators\
-   📜 Message persistence\
-   🔒 End-to-end encryption\
-   📨 Direct/private channels\
-   📁 File transfer\
-   🎨 UI refinement

------------------------------------------------------------------------

## ⚔️ Contribution

The project remains under controlled development. External input is
welcome---but access is earned, not given.

------------------------------------------------------------------------

## 📄 License

This project is private. Unauthorized distribution is prohibited.

------------------------------------------------------------------------

## 🌑 Closing Note

Not every system needs noise.\
Not every network needs exposure.

**Black Pearl sails quiet.**
