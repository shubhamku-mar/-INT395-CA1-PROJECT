from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from datetime import datetime, timezone
import hashlib
import hmac
import json
import math
import os
import re
import secrets
import time
import urllib.request
import urllib.error

import psycopg

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "10000"))

DATABASE_URL = os.environ.get("DATABASE_URL", "")
BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "")
BREVO_SENDER_EMAIL = os.environ.get("BREVO_SENDER_EMAIL", "")
BREVO_SENDER_NAME = os.environ.get("BREVO_SENDER_NAME", "SHUTTLELYZE")
DASHBOARD_READ_KEY = os.environ.get("DASHBOARD_READ_KEY", "")

OTP_SECONDS = 300
RESEND_SECONDS = 60
MAX_ATTEMPTS = 5
TOKEN_HOURS = 12


def check_config():
    missing = []
    for name, value in [
        ("DATABASE_URL", DATABASE_URL),
        ("BREVO_API_KEY", BREVO_API_KEY),
        ("BREVO_SENDER_EMAIL", BREVO_SENDER_EMAIL),
        ("DASHBOARD_READ_KEY", DASHBOARD_READ_KEY),
    ]:
        if not value:
            missing.append(name)

    if missing:
        raise RuntimeError("Missing environment variables: " + ", ".join(missing))


def db():
    return psycopg.connect(DATABASE_URL)


def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS gps_locations (
                id BIGSERIAL PRIMARY KEY,
                email TEXT NOT NULL,
                latitude DOUBLE PRECISION NOT NULL,
                longitude DOUBLE PRECISION NOT NULL,
                accuracy DOUBLE PRECISION,
                speed DOUBLE PRECISION,
                heading DOUBLE PRECISION,
                recorded_at TIMESTAMPTZ NOT NULL
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS gps_locations_email_id_idx
            ON gps_locations(email, id DESC)
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS gps_otp_challenges (
                email TEXT PRIMARY KEY,
                otp_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                expires_at DOUBLE PRECISION NOT NULL,
                sent_at DOUBLE PRECISION NOT NULL,
                attempts INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS gps_device_tokens (
                token_hash TEXT PRIMARY KEY,
                email TEXT NOT NULL,
                expires_at DOUBLE PRECISION NOT NULL,
                created_at DOUBLE PRECISION NOT NULL
            )
        """)


def send_otp(email, otp):
    payload = {
        "sender": {
            "name": BREVO_SENDER_NAME,
            "email": BREVO_SENDER_EMAIL
        },
        "to": [{"email": email}],
        "subject": "SHUTTLELYZE Email Verification",
        "textContent": (
            f"Your SHUTTLELYZE OTP is {otp}. "
            "It expires in five minutes. Do not share it."
        )
    }

    request = urllib.request.Request(
        "https://api.brevo.com/v3/smtp/email",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "api-key": BREVO_API_KEY,
            "accept": "application/json",
            "content-type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return 200 <= response.status < 300
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace").strip()
        try:
            parsed = json.loads(body)
            safe_details = {
                key: parsed[key]
                for key in ("code", "message", "error", "errorCode")
                if key in parsed
            }
            details = json.dumps(safe_details, ensure_ascii=False)
        except Exception:
            details = "(Brevo returned a non-JSON error response)"

        print(f"[OTP] Brevo HTTP {exc.code}; details: {details}")
        raise RuntimeError(
            f"Brevo rejected the request (HTTP {exc.code}). "
            "Check Render Logs for the Brevo error details."
        ) from None
    except Exception:
        raise RuntimeError("Could not connect to Brevo.") from None


PHONE_PAGE = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SHUTTLELYZE Driver GPS</title>
<style>
*{box-sizing:border-box}
body{font-family:Arial;background:#101827;color:white;padding:18px;
max-width:520px;margin:25px auto}
.card{background:#1e293b;padding:22px;border-radius:16px}
input,button{width:100%;padding:14px;margin:9px 0;border-radius:9px;
font-size:16px}
input{background:#0f172a;color:white;border:1px solid #64748b}
button{border:0;background:#f97316;color:#111827;font-weight:bold}
.stop{background:#dc2626;color:white}
.small{color:#cbd5e1;font-size:14px;line-height:1.5}
#status{padding:12px;background:#0f172a;border-radius:9px;margin-top:12px}
.hidden{display:none}
</style>
</head>
<body>
<div class="card">
<h2>SHUTTLELYZE</h2>
<h3>Driver GPS Tracker</h3>
<p class="small">Verify your email before starting GPS tracking.</p>
<label>Email address</label>
<input id="email" type="email" placeholder="Enter your email">
<button onclick="sendOTP()">SEND EMAIL OTP</button>
<div id="verify" class="hidden">
<label>Six-digit OTP</label>
<input id="otp" inputmode="numeric" maxlength="6" placeholder="Enter OTP">
<button onclick="verifyOTP()">VERIFY EMAIL</button>
</div>
<div id="tracking" class="hidden">
<p class="small">Email verified successfully.</p>
<button onclick="startTracking()">START GPS TRACKING</button>
<button class="stop" onclick="stopTracking()">STOP TRACKING</button>
</div>
<div id="status">Enter your email address to begin.</div>
<p id="details" class="small"></p>
</div>
<script>
let token=null,watchId=null,lastSent=0;
function status(message){
 document.getElementById("status").textContent=message;
}
async function api(path,data,auth=false){
 const headers={"Content-Type":"application/json"};
 if(auth)headers["Authorization"]="Bearer "+token;
 const response=await fetch(path,{
  method:"POST",headers:headers,body:JSON.stringify(data)
 });
 const result=await response.json();
 if(!response.ok)throw new Error(result.error||"Request failed");
 return result;
}
async function sendOTP(){
 const email=document.getElementById("email").value.trim();
 if(!email){status("Enter your email address.");return;}
 status("Sending OTP...");
 try{
  await api("/api/request-otp",{email:email});
  document.getElementById("verify").classList.remove("hidden");
  status("OTP sent. Check your inbox and spam folder.");
 }catch(e){status(e.message);}
}
async function verifyOTP(){
 const email=document.getElementById("email").value.trim();
 const otp=document.getElementById("otp").value.trim();
 if(!/^\d{6}$/.test(otp)){status("Enter the six-digit OTP.");return;}
 status("Verifying OTP...");
 try{
  const result=await api("/api/verify-otp",{email:email,otp:otp});
  token=result.token;
  document.getElementById("verify").classList.add("hidden");
  document.getElementById("tracking").classList.remove("hidden");
  status("Email verified. GPS tracking is ready.");
 }catch(e){status(e.message);}
}
function startTracking(){
 if(!token){status("Verify your email first.");return;}
 if(!navigator.geolocation){
  status("GPS is not supported by this browser.");return;
 }
 if(watchId!==null)navigator.geolocation.clearWatch(watchId);
 status("Waiting for GPS permission...");
 watchId=navigator.geolocation.watchPosition(async position=>{
  if(Date.now()-lastSent<2000)return;
  lastSent=Date.now();
  const c=position.coords;
  try{
   await api("/api/location",{
    latitude:c.latitude,longitude:c.longitude,accuracy:c.accuracy,
    speed:c.speed,heading:c.heading
   },true);
   status("GPS location sent successfully.");
   document.getElementById("details").textContent=
    "Latitude: "+c.latitude.toFixed(6)+" | Longitude: "+
    c.longitude.toFixed(6)+" | Accuracy: "+Math.round(c.accuracy)+" m"+
    (c.speed==null?"":" | Speed: "+(c.speed*3.6).toFixed(1)+" km/h");
  }catch(e){status(e.message);}
 },error=>{status("GPS error: "+error.message);},
 {enableHighAccuracy:true,maximumAge:1000,timeout:20000});
}
function stopTracking(){
 if(watchId!==null){
  navigator.geolocation.clearWatch(watchId);watchId=null;
 }
 status("GPS tracking stopped.");
}
</script>
</body>
</html>
"""


DASHBOARD_PAGE = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SHUTTLELYZE Live GPS Dashboard</title>
<link rel="stylesheet"
 href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>
*{box-sizing:border-box}
body{margin:0;background:#101827;color:white;font-family:Arial,sans-serif}
header{padding:18px 22px;background:#1e293b}
h2{margin:0;color:#fb923c}
main{padding:18px;max-width:1200px;margin:auto}
.panel{background:#1e293b;padding:18px;border-radius:14px;margin-bottom:15px}
input,button{padding:12px;border-radius:8px;font-size:15px}
input{background:#0f172a;color:white;border:1px solid #64748b;width:min(100%,420px)}
button{background:#f97316;border:0;font-weight:bold;cursor:pointer}
#map{height:65vh;min-height:380px;border-radius:12px}
.metrics{display:flex;gap:12px;flex-wrap:wrap}
.metric{background:#0f172a;padding:13px;border-radius:9px;min-width:145px}
.metric strong{display:block;color:#fb923c;font-size:20px;margin-top:7px}
.muted{color:#cbd5e1;font-size:14px}
#status{margin-top:10px;color:#cbd5e1}
</style>
</head>
<body>
<header><h2>SHUTTLELYZE — LIVE GPS</h2>
<div class="muted">Separate phone tracking dashboard</div></header>
<main>
<div class="panel">
<h3>Dashboard access</h3>
<input id="key" type="password" placeholder="Enter dashboard access key">
<button onclick="connect()">CONNECT</button>
<div id="status">Enter your dashboard key to view GPS data.</div>
</div>
<div class="panel">
<div class="metrics">
<div class="metric">Speed<strong id="speed">--</strong></div>
<div class="metric">Accuracy<strong id="accuracy">--</strong></div>
<div class="metric">Latitude<strong id="latitude">--</strong></div>
<div class="metric">Longitude<strong id="longitude">--</strong></div>
</div>
<p class="muted" id="updated">Waiting for GPS data.</p>
</div>
<div class="panel"><div id="map"></div></div>
</main>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
let dashboardKey="",marker=null,trail=null,accuracyCircle=null,map=null;
let timer=null;
function setStatus(text){
 document.getElementById("status").textContent=text;
}
function setupMap(){
 if(map)return;
 map=L.map("map").setView([31.255,75.705],15);
 L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{
  maxZoom:19,attribution:"&copy; OpenStreetMap contributors"
 }).addTo(map);
}
async function refresh(){
 try{
  const response=await fetch("/api/latest",{
   headers:{"X-Dashboard-Key":dashboardKey},
   cache:"no-store"
  });
  const result=await response.json();
  if(!response.ok)throw new Error(result.error||"Dashboard request failed");
  if(!result.latest){
   setStatus("Connected. No GPS data received yet. Start tracking on the phone.");
   return;
  }
  const p=result.latest;
  const point=[p.latitude,p.longitude];
  document.getElementById("speed").textContent=
   ((p.speed||0)*3.6).toFixed(1)+" km/h";
  document.getElementById("accuracy").textContent=
   (p.accuracy==null?"--":p.accuracy.toFixed(1)+" m");
  document.getElementById("latitude").textContent=p.latitude.toFixed(6);
  document.getElementById("longitude").textContent=p.longitude.toFixed(6);
  document.getElementById("updated").textContent=
   "Last GPS update: "+new Date(p.recorded_at).toLocaleString()+
   " | Email: "+p.email;
  if(!marker){
   marker=L.marker(point).addTo(map).bindPopup("SHUTTLELYZE LIVE SHUTTLE");
   map.setView(point,17);
  }else{
   marker.setLatLng(point);
  }
  if(trail)map.removeLayer(trail);
  if(accuracyCircle)map.removeLayer(accuracyCircle);
  const points=result.trail.map(x=>[x.latitude,x.longitude]);
  if(points.length>1){
   trail=L.polyline(points,{color:"#00bfff",weight:5,opacity:.85}).addTo(map);
  }
  accuracyCircle=L.circle(point,{
   radius:Math.max(p.accuracy||0,3),
   color:"#00bfff",fillOpacity:.12
  }).addTo(map);
  setStatus("Connected. Live GPS data is updating.");
 }catch(e){
  setStatus("Dashboard error: "+e.message);
 }
}
function connect(){
 dashboardKey=document.getElementById("key").value.trim();
 if(!dashboardKey){setStatus("Enter the dashboard access key.");return;}
 if(timer)clearInterval(timer);
 setupMap();
 refresh();
 timer=setInterval(refresh,2000);
}
</script>
</body>
</html>
"""


class GPSHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > 12000:
            raise ValueError("Invalid request size.")
        data = json.loads(self.rfile.read(length).decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Invalid request.")
        return data

    def authorized_device(self):
        header = self.headers.get("Authorization", "")
        token = header[7:].strip() if header.startswith("Bearer ") else ""
        if not token:
            return None
        digest = hashlib.sha256(token.encode()).hexdigest()
        with db() as conn:
            row = conn.execute("""
                SELECT email FROM gps_device_tokens
                WHERE token_hash=%s AND expires_at>%s
            """, (digest, time.time())).fetchone()
        return row[0] if row else None

    def authorized_dashboard(self):
        supplied = self.headers.get("X-Dashboard-Key", "")
        return bool(supplied) and hmac.compare_digest(
            supplied, DASHBOARD_READ_KEY
        )

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/phone":
            body = PHONE_PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/dashboard":
            body = DASHBOARD_PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/health":
            self.send_json(200, {"status": "SHUTTLELYZE cloud GPS online"})
            return

        if path == "/api/latest":
            if not self.authorized_dashboard():
                self.send_json(401, {"error": "Dashboard access key is invalid."})
                return

            try:
                with db() as conn:
                    latest = conn.execute("""
                        SELECT email,latitude,longitude,accuracy,speed,
                               heading,recorded_at
                        FROM gps_locations
                        ORDER BY id DESC LIMIT 1
                    """).fetchone()

                    trail = conn.execute("""
                        SELECT latitude,longitude
                        FROM (
                            SELECT id,latitude,longitude
                            FROM gps_locations
                            WHERE email=%s
                            ORDER BY id DESC LIMIT 100
                        ) recent
                        ORDER BY id ASC
                    """, (latest[0],)).fetchall() if latest else []

                if not latest:
                    self.send_json(200, {"latest": None, "trail": []})
                    return

                item = {
                    "email": latest[0],
                    "latitude": latest[1],
                    "longitude": latest[2],
                    "accuracy": latest[3],
                    "speed": latest[4],
                    "heading": latest[5],
                    "recorded_at": latest[6].isoformat()
                }
                points = [
                    {"latitude": row[0], "longitude": row[1]}
                    for row in trail
                ]
                self.send_json(200, {"latest": item, "trail": points})
            except Exception:
                print("[GPS] Could not read latest location.")
                self.send_json(500, {"error": "Could not read GPS data."})
            return

        self.send_json(404, {"error": "Not found."})

    def do_POST(self):
        path = urlparse(self.path).path

        try:
            if path == "/api/request-otp":
                data = self.read_json()
                email = str(data.get("email", "")).strip().lower()

                if len(email) > 254 or not re.fullmatch(
                    r"[^@\s]+@[^@\s]+\.[^@\s]+", email
                ):
                    self.send_json(400, {"error": "Enter a valid email address."})
                    return

                now = time.time()
                with db() as conn:
                    old = conn.execute("""
                        SELECT sent_at FROM gps_otp_challenges WHERE email=%s
                    """, (email,)).fetchone()

                if old and now - old[0] < RESEND_SECONDS:
                    self.send_json(429, {
                        "error": "Please wait before requesting another OTP."
                    })
                    return

                otp = f"{secrets.randbelow(1000000):06d}"
                salt = secrets.token_hex(16)
                digest = hashlib.sha256(
                    f"{email}:{otp}:{salt}".encode()
                ).hexdigest()

                send_otp(email, otp)

                with db() as conn:
                    conn.execute("""
                        INSERT INTO gps_otp_challenges
                        (email,otp_hash,salt,expires_at,sent_at,attempts)
                        VALUES(%s,%s,%s,%s,%s,0)
                        ON CONFLICT(email) DO UPDATE SET
                        otp_hash=EXCLUDED.otp_hash,
                        salt=EXCLUDED.salt,
                        expires_at=EXCLUDED.expires_at,
                        sent_at=EXCLUDED.sent_at,
                        attempts=0
                    """, (email, digest, salt, now + OTP_SECONDS, now))

                self.send_json(200, {"success": True})
                return

            if path == "/api/verify-otp":
                data = self.read_json()
                email = str(data.get("email", "")).strip().lower()
                otp = str(data.get("otp", "")).strip()

                if not email or not otp.isdigit() or len(otp) != 6:
                    self.send_json(400, {
                        "error": "Enter your email and six-digit OTP."
                    })
                    return

                now = time.time()
                with db() as conn:
                    row = conn.execute("""
                        SELECT otp_hash,salt,expires_at,attempts
                        FROM gps_otp_challenges WHERE email=%s
                    """, (email,)).fetchone()

                    if not row:
                        self.send_json(400, {
                            "error": "Request a new OTP first."
                        })
                        return

                    expected, salt, expires, attempts = row

                    if now > expires:
                        conn.execute("""
                            DELETE FROM gps_otp_challenges WHERE email=%s
                        """, (email,))
                        self.send_json(400, {
                            "error": "OTP expired. Request another."
                        })
                        return

                    if attempts >= MAX_ATTEMPTS:
                        conn.execute("""
                            DELETE FROM gps_otp_challenges WHERE email=%s
                        """, (email,))
                        self.send_json(429, {
                            "error": "Too many attempts. Request a new OTP."
                        })
                        return

                    supplied = hashlib.sha256(
                        f"{email}:{otp}:{salt}".encode()
                    ).hexdigest()

                    if not hmac.compare_digest(supplied, expected):
                        conn.execute("""
                            UPDATE gps_otp_challenges
                            SET attempts=attempts+1 WHERE email=%s
                        """, (email,))
                        self.send_json(400, {"error": "Incorrect OTP."})
                        return

                    conn.execute("""
                        DELETE FROM gps_otp_challenges WHERE email=%s
                    """, (email,))

                    token = secrets.token_urlsafe(32)
                    token_hash = hashlib.sha256(token.encode()).hexdigest()

                    conn.execute("""
                        INSERT INTO gps_device_tokens
                        (token_hash,email,expires_at,created_at)
                        VALUES(%s,%s,%s,%s)
                    """, (
                        token_hash, email,
                        now + TOKEN_HOURS * 3600, now
                    ))

                self.send_json(200, {
                    "success": True,
                    "token": token,
                    "expires_in_seconds": TOKEN_HOURS * 3600
                })
                return

            if path == "/api/location":
                email = self.authorized_device()
                if not email:
                    self.send_json(401, {
                        "error": "Verify your email again."
                    })
                    return

                data = self.read_json()
                lat = float(data["latitude"])
                lon = float(data["longitude"])

                if not (
                    math.isfinite(lat) and math.isfinite(lon)
                    and -90 <= lat <= 90 and -180 <= lon <= 180
                ):
                    raise ValueError("Invalid GPS coordinates.")

                def optional_number(key, minimum, maximum):
                    value = data.get(key)
                    if value is None:
                        return None
                    number = float(value)
                    if not math.isfinite(number) or not minimum <= number <= maximum:
                        raise ValueError("Invalid " + key)
                    return number

                accuracy = optional_number("accuracy", 0, 100000)
                speed = optional_number("speed", 0, 1000)
                heading = optional_number("heading", 0, 360)

                with db() as conn:
                    conn.execute("""
                        INSERT INTO gps_locations
                        (email,latitude,longitude,accuracy,speed,heading,recorded_at)
                        VALUES(%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        email, lat, lon, accuracy, speed, heading,
                        datetime.now(timezone.utc)
                    ))

                self.send_json(200, {"success": True})
                return

            self.send_json(404, {"error": "Not found."})

        except (ValueError, KeyError, json.JSONDecodeError,
                UnicodeDecodeError) as error:
            self.send_json(400, {"error": str(error) or "Invalid request data."})
        except RuntimeError as error:
            self.send_json(502, {"error": str(error)})
        except Exception:
            print("[GPS] Unexpected server error.")
            self.send_json(500, {"error": "Server error."})

    def log_message(self, fmt, *args):
        print("[GPS CLOUD] " + (fmt % args))


if __name__ == "__main__":
    check_config()
    init_db()
    print("SHUTTLELYZE cloud GPS server starting...")
    print(f"Listening on port {PORT}")
    server = ThreadingHTTPServer((HOST, PORT), GPSHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping SHUTTLELYZE cloud GPS server...")
    finally:
        server.server_close()
