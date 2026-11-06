markdown
<div align="center">

# 🚀 AGS COMMUNITY · Friend Request Sender API

### ⚡ Fast · Reliable · 24/7 Online · Render-Ready

[![Credit](https://img.shields.io/badge/Credit-AGS__COMMUNITY-red?style=for-the-badge)](https://t.me/ags_community)
[![Developer](https://img.shields.io/badge/Developer-@ags__atif-blue?style=for-the-badge)](https://t.me/ags_atif)
[![Telegram](https://img.shields.io/badge/Telegram-AGS__COMMUNITY-2CA5E0?style=for-the-badge&logo=telegram)](https://t.me/ags_community)
[![Python](https://img.shields.io/badge/Python-3.11-yellow?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)

</div>

---

## 🌟 About This Project

**AGS Community Friend Request Sender API** is a lightweight, high-performance Flask API that lets you send Free Fire friend requests programmatically — either via **GET** or **POST** request.

Built by the **AGS COMMUNITY** team, this API handles:
- ✅ Guest account login (Garena)
- ✅ Auto token generation
- ✅ AES-encrypted friend request payloads
- ✅ Clean JSON responses with credit info
- ✅ Render / Heroku ready with one-click deploy

---

## 👑 Credit & Credits

<div align="center">

### 🏆 **Full Credit Goes To**

| Role | Name | Contact |
|------|------|---------|
| 🎯 **Credit** | **AGS COMMUNITY** | [@ags_community](https://t.me/ags_community) |
| 👨‍💻 **Developer** | **AGS ATIF** | [@ags_atif](https://t.me/ags_atif) |
| 🌐 **Telegram** | **AGS Community Group** | [t.me/ags_community](https://t.me/ags_community) |

</div>

> ⚠️ **Please keep original credits if you fork/redistribute.**  
> Removing credit is strictly prohibited. 🙏

---

## 📁 Folder Structure
friend_request_api/
│
├── app.py # Main Flask API
├── login_engine.py # Garena login engine
├── byte.py # Encrypt_ID helper
├── requirements.txt # Python dependencies
├── render.yaml # One-click Render deploy
├── Procfile # Heroku / fallback
├── runtime.txt # Python version
├── README.md # This file
│
└── Pb2/ # Protobuf modules
├── init.py
├── MajoRLoGinrEs_pb2.py
├── MajoRLoGinrEq_pb2.py
└── PorTs_pb2.py

text

---

## ⚡ API Endpoint

### `GET /send`

Send a friend request from your bot account to a target UID.

```http
GET /send?uid=YOUR_UID&password=YOUR_PW&target=TARGET_UID
Parameter	Type	Required	Description
uid	string	✅	Your bot account UID
password	string	✅	Your bot account password (hex hash)
target	string	✅	Target player UID (numeric)
POST /send
Same as above, but with JSON body.

http
POST /send
Content-Type: application/json

{
  "uid": "8121114283",
  "password": "D9BA0974A2AF7EF43DA0B509...",
  "target": "1234567890"
}
🧪 Example Requests
cURL (GET)
bash
curl "https://your-app.onrender.com/send?uid=8121114283&password=YOUR_PW&target=1234567890"
cURL (POST)
bash
curl -X POST https://your-app.onrender.com/send \
  -H "Content-Type: application/json" \
  -d '{"uid":"8121114283","password":"YOUR_PW","target":"1234567890"}'
Python
python
import requests

r = requests.get(
    "https://your-app.onrender.com/send",
    params={
        "uid": "8121114283",
        "password": "YOUR_PW",
        "target": "1234567890",
    },
)
print(r.json())
✅ Success Response
json
{
  "success": true,
  "message": "Friend request sent successfully",
  "credit": "ags_community",
  "developer": "ags_atif",
  "version": "1.0.0",
  "timestamp": 1730000000,
  "bot_uid": "8121114283",
  "bot_name": "MyBot",
  "region": "BD",
  "target_uid": "1234567890",
  "status_code": 200,
  "elapsed_ms": 1842
}
❌ Error Response
json
{
  "success": false,
  "error": "Login failed — check UID / password",
  "credit": "ags_community",
  "developer": "ags_atif",
  "version": "1.0.0",
  "timestamp": 1730000000,
  "elapsed_ms": 913
}
Possible errors:

Error	Meaning
Missing parameter(s)	uid / password / target missing
target must be numeric	target is not a valid UID
Login failed	Wrong UID or password
Unauthorized (401)	Token invalid / expired
Rate limited (429)	Too many requests — slow down
Bad request (400)	Garena rejected the request
🚀 Deploy on Render (One-Click)
Step 1 — Push to GitHub
bash
git init
git add .
git commit -m "AGS Friend Request API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/friend-request-api.git
git push -u origin main
Step 2 — Open Render
Go to render.com → New + → Web Service

Connect your GitHub repo

Render reads render.yaml automatically → click Deploy

Wait ~2 minutes → your API is live 🎉

Your URL will look like:

text
https://ags-friend-api.onrender.com
🤖 Keep Alive with UptimeRobot (Recommended)
Render free tier sleeps after 15 min of inactivity. Use UptimeRobot to keep it alive 24/7.

Setup:
Go to uptimerobot.com → Sign up free

Click Add New Monitor

Fill in:

Field	Value
Monitor Type	HTTP(s)
Friendly Name	AGS Friend API
URL	https://your-app.onrender.com/healthz
Monitoring Interval	5 minutes
Click Create Monitor

✅ Result: Your bot will stay online 24/7 — no more cold starts! 🚀

🔧 Environment Variables
Variable	Default	Description
PORT	10000	Server port (auto on Render)
REGION	BD	Garena region (BD, IND, PK, ME, SG, ID)
🛡️ Security Recommendations
For production use, add an API key:

python
# In app.py
API_KEY = os.environ.get("API_KEY")

if API_KEY and request.args.get("key") != API_KEY:
    return jsonify({"success": False, "error": "Unauthorized"}), 401
Then add API_KEY in Render → Environment and call:

bash
curl ".../send?uid=...&password=...&target=...&key=YOUR_SECRET"
⚠️ Disclaimer
This project is for educational purposes only.

Do NOT use for spamming or abusing Garena servers.

Rate limits apply — overuse may result in temporary or permanent account bans.

The developer and AGS Community are not responsible for any account bans or misuse.

Use at your own risk. 🙏

📞 Contact & Support
<div align="center">
💬 Need Help?
https://img.shields.io/badge/Telegram-@ags__community-2CA5E0?style=for-the-badge&logo=telegram
https://img.shields.io/badge/Developer-@ags__atif-blue?style=for-the-badge&logo=telegram

Join AGS COMMUNITY for updates, new tools & support!

</div>
📜 License
This project is free to use with credit to:

🎯 Credit: AGS COMMUNITY

👨‍💻 Developer: AGS ATIF

Redistribution must include original credit.
Commercial use without permission is prohibited.

<div align="center">
⚡ Powered By AGS COMMUNITY ⚡
Made with ❤️ by @ags_atif

⭐ Star this repo if it helped you! ⭐

</div> ```