"""
NutriVision — Flask API Server
Food calorie estimation via YOLOv4 deep learning pipeline
Auth · History · Analysis
"""

import cv2
import numpy as np
import os
import time
import uuid
import base64
import hashlib
import sqlite3
import json
from datetime import datetime
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory, g
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import timezone

# ── Paths ───────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_IMG_FOLDER_PATH = os.path.join(BASE_DIR, "test_images")
MODEL_PATH = os.path.join(BASE_DIR, "weights", "custom-yolov4-detector_3000(98.61).weights")
CFG_FILE_PATH = os.path.join(BASE_DIR, "custom-yolov4-detector.cfg")
OBJ_FILE_PATH = os.path.join(BASE_DIR, "darknet_yolov4_obj_names.names")
WRITE_CROPPED_IMG_PATH = os.path.join(BASE_DIR, "results", "cropped_img")
IMG_RESULT_PATH = os.path.join(BASE_DIR, "results", "final_result_img")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DB_PATH = os.path.join(BASE_DIR, "nutrivision.db")

for d in [UPLOAD_FOLDER, WRITE_CROPPED_IMG_PATH, IMG_RESULT_PATH, TEST_IMG_FOLDER_PATH]:
    os.makedirs(d, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# ── Nutrition constants ─────────────────────────────────────────────────
SKIN_MULTIPLIER = 5 * 2.3
PIXEL_TO_CM_MULTIPLIER_CONSTANT = 5.0

density_dict = {
    "Apple": 0.96, "Banana": 0.94, "Carrot": 0.641,
    "Onion": 0.513, "Orange": 0.482, "Tomato": 0.481, "Qiwi": 0.575,
}
calorie_dict = {
    "Apple": 52, "Banana": 89, "Carrot": 41,
    "Onion": 40, "Orange": 47, "Tomato": 18, "Qiwi": 44,
}

# ── Flask app ───────────────────────────────────────────────────────────
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "frontend", "dist"),
    static_url_path="",
)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "nutrivision-dev-secret-2026")
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# ═══════════════════════════════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════════════════════════════

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id          TEXT PRIMARY KEY,
            username    TEXT UNIQUE NOT NULL,
            email       TEXT UNIQUE NOT NULL,
            pw_hash     TEXT NOT NULL,
            created_at  TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS scan_history (
            id              TEXT PRIMARY KEY,
            user_id         TEXT NOT NULL,
            filename        TEXT,
            detections      TEXT,
            detection_time  REAL,
            thumb_found     INTEGER,
            total_calories  REAL,
            result_image    TEXT,
            scanned_at      TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE INDEX IF NOT EXISTS idx_history_user ON scan_history(user_id);
    """)
    db.close()


init_db()


# ── Auth helpers ────────────────────────────────────────────────────────

def hash_password(password, salt=None):
    if salt is None:
        salt = uuid.uuid4().hex
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120_000)
    return f"{salt}${hashed.hex()}"


def verify_password(password, stored):
    salt, _ = stored.split("$", 1)
    return hash_password(password, salt) == stored


def generate_token(user_id):
    payload = f"{user_id}|{app.config['SECRET_KEY']}"
    sig = hashlib.sha256(payload.encode()).hexdigest()[:32]
    return f"{user_id}.{sig}"


def verify_token(token):
    try:
        user_id, sig = token.rsplit(".", 1)
        expected = hashlib.sha256(f"{user_id}|{app.config['SECRET_KEY']}".encode()).hexdigest()[:32]
        if sig == expected:
            return user_id
    except Exception:
        pass
    return None


def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify(error="Authentication required"), 401
        token = auth_header[7:]
        user_id = verify_token(token)
        if not user_id:
            return jsonify(error="Invalid or expired token"), 401
        g.user_id = user_id
        return fn(*args, **kwargs)
    return wrapper


# ═══════════════════════════════════════════════════════════════════════
# YOLO MODEL (lazy)
# ═══════════════════════════════════════════════════════════════════════

_model_cache = {}

def get_model():
    if "net" not in _model_cache:
        print("[NutriVision] Loading YOLOv4 model …")
        t0 = time.time()
        net = cv2.dnn.readNet(MODEL_PATH, CFG_FILE_PATH)
        print(f"[NutriVision] Model loaded in {time.time()-t0:.2f}s")
        with open(OBJ_FILE_PATH) as f:
            classes = [l.strip() for l in f.readlines()]
        layer_names = net.getLayerNames()
        uncon = net.getUnconnectedOutLayers()
        if len(uncon.shape) == 2:
            out_layers = [layer_names[i[0] - 1] for i in uncon]
        else:
            out_layers = [layer_names[i - 1] for i in uncon]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        _model_cache.update(net=net, classes=classes, output_layers=out_layers,
                            layer_names=layer_names, colors=colors)
    return _model_cache


# ═══════════════════════════════════════════════════════════════════════
# IMAGE PROCESSING PIPELINE
# ═══════════════════════════════════════════════════════════════════════

def crop_img(input_img, img_name, bb, save_path=None, margin=5):
    dh, dw, _ = input_img.shape
    bb = [abs(c) for c in bb]
    xmin, ymin, w, h = bb
    p = margin
    x0, y0 = max(xmin - p, 0), max(ymin - p, 0)
    y1, x1 = min(ymin + h + p, dh), min(xmin + w + p, dw)
    cropped = input_img[y0:y1, x0:x1]
    if save_path:
        cv2.imwrite(os.path.join(save_path, img_name), cropped)
    return cropped


def segment_object(name, cropped):
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    th = cv2.adaptiveThreshold(gray, 100, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 15, 2)
    cnts, _ = cv2.findContours(th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea)
    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, [cnts[-1]], 0, 255, -1)
    masked = cv2.bitwise_or(cropped, cropped, mask=mask)
    hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)
    plate_m = cv2.inRange(hsv, np.array([0, 0, 50]), np.array([200, 90, 250]))
    fruit = cv2.bitwise_and(masked, masked, mask=cv2.bitwise_not(plate_m))
    g2 = cv2.cvtColor(fruit, cv2.COLOR_BGR2GRAY)
    _, t2 = cv2.threshold(g2, 10, 255, cv2.THRESH_BINARY)
    c2, _ = cv2.findContours(t2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c2 = sorted(c2, key=cv2.contourArea)

    if "thumb" in name.lower():
        rc = c2[-2] if len(c2) >= 2 else c2[-1]
        area = cv2.contourArea(rc)
        rect = cv2.minAreaRect(rc)
        dim = max(rect[1])
        pix_cm = PIXEL_TO_CM_MULTIPLIER_CONSTANT / dim if dim else 1.0
        return rc, area, pix_cm
    rc = c2[-1]
    return rc, cv2.contourArea(rc), None


def estimate_volume(label, box_w_cm, box_h_cm):
    """
    Estimate volume (cm³) from the physical dimensions of the YOLO bounding box.
    Using bbox dimensions is far more reliable than segmented contour areas,
    which can be near-zero or enormous depending on lighting / background.

    Sanity cap: 1500 cm³ (~1.5 litres) — no single hand-held food exceeds this.
    """
    MAX_VOL = 1500.0

    if label in ("Apple", "Orange", "Qiwi", "Tomato", "Onion"):
        # Model these as spheres; diameter ≈ average of bbox width & height
        d = (box_w_cm + box_h_cm) / 2.0
        r = d / 2.0
        return min((4.0 / 3.0) * np.pi * r ** 3, MAX_VOL)

    if label in ("Banana", "Carrot"):
        # Model as cylinder; length = long axis, radius ≈ short axis / 3
        length = max(box_w_cm, box_h_cm)
        r = min(box_w_cm, box_h_cm) / 3.0
        return min(np.pi * r ** 2 * length, MAX_VOL)

    # Generic fallback: rough ellipsoid
    depth_cm = (box_w_cm + box_h_cm) / 4.0
    return min((4.0 / 3.0) * np.pi * (box_w_cm / 2.0) * (box_h_cm / 2.0) * depth_cm, MAX_VOL)


def estimate_calories(label, volume):
    cal100 = calorie_dict.get(label, 50)
    dens = density_dict.get(label, 0.5)
    mass = volume * dens
    return mass, (cal100 / 100.0) * mass, cal100


def run_analysis(img):
    """Full pipeline: detect → segment → measure → estimate calories."""
    m = get_model()
    net, classes, out_layers, colors = m["net"], m["classes"], m["output_layers"], m["colors"]

    resized = cv2.resize(img, (608, 608))
    h, w, _ = resized.shape

    blob = cv2.dnn.blobFromImage(resized, 0.00392, (608, 608), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    t0 = time.time()
    outs = net.forward(out_layers)
    det_time = time.time() - t0

    cids, confs, boxes = [], [], []
    for out in outs:
        for det in out:
            scores = det[5:]
            cid = int(np.argmax(scores))
            conf = float(scores[cid])
            if conf > 0.5:
                cx, cy = int(det[0] * w), int(det[1] * h)
                bw, bh = int(det[2] * w), int(det[3] * h)
                boxes.append([cx - bw // 2, cy - bh // 2, bw, bh])
                confs.append(conf)
                cids.append(cid)

    idxs = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
    if len(idxs) == 0:
        return dict(detections=[], detection_time=round(det_time, 3),
                    result_image=None, thumb_found=False)

    # Segment each
    seg = {}
    for i in idxs.flatten():
        label = classes[cids[i]]
        c = confs[i]
        box = boxes[i]
        tag = f"{label}({round(c*100,2)})_{i}.jpg"
        cr = crop_img(resized, tag, box)
        try:
            cnt, area, pcm = segment_object(tag, cr)
            seg[tag] = dict(cnt=cnt, area=area, pcm=pcm, box=box,
                            label=label, conf=c, idx=i)
        except Exception:
            seg[tag] = dict(cnt=None, area=0, pcm=None, box=box,
                            label=label, conf=c, idx=i)

    # ── Thumb reference: derive pix_cm from YOLO bbox (reliable) ──────────
    # A human thumb is ~5 cm long. Use the larger bbox dimension as reference.
    # This avoids the segmented-contour approach which fails under poor lighting.
    pix_cm = None
    for v in seg.values():
        if v["label"] == "thumb":
            _, _, tbw, tbh = v["box"]
            thumb_dim = max(tbw, tbh, 1)
            pix_cm = PIXEL_TO_CM_MULTIPLIER_CONSTANT / thumb_dim
            # Sanity: clamp to [0.01, 0.5] cm/pixel
            pix_cm = max(0.01, min(pix_cm, 0.5))
            break

    # ── Shape-based Apple / Orange disambiguation ──────────────────────────
    # Both look round and orange-red; use hue of the bounding-box crop to
    # decide: oranges are distinctly orange (hue 10-25°), apples vary widely.
    def _disambiguate_apple_orange(det_label, crop_bgr):
        if det_label not in ("Apple", "Orange"):
            return det_label
        hsv = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2HSV)
        # Mask out near-white/grey background (low saturation)
        sat_mask = hsv[:, :, 1] > 60
        if sat_mask.sum() < 100:
            return det_label  # not enough colour info — keep model label
        mean_hue = float(np.median(hsv[:, :, 0][sat_mask]))
        # OpenCV hue: 0-180; orange ≈ 5-20, red/apple ≈ 0-5 or 160-180
        if 5 <= mean_hue <= 22:
            return "Orange"
        return "Apple"

    # Build result
    detections = []
    canvas = resized.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX

    for v in seg.values():
        label, conf, box = v["label"], v["conf"], v["box"]
        x, y, bw, bh = box

        # Refine Apple/Orange label via colour
        crop_bgr = resized[max(y, 0):min(y + bh, resized.shape[0]),
                           max(x, 0):min(x + bw, resized.shape[1])]
        if crop_bgr.size > 0:
            label = _disambiguate_apple_orange(label, crop_bgr)

        entry = dict(label=label, confidence=round(conf * 100, 2), box=box)

        if label != "thumb" and pix_cm:
            box_w_cm = bw * pix_cm
            box_h_cm = bh * pix_cm
            vol = estimate_volume(label, box_w_cm, box_h_cm)
            mass, cals, c100 = estimate_calories(label, vol)
            entry.update(volume_cm3=round(vol, 2), mass_g=round(mass, 2),
                         calories_kcal=round(cals, 1), cal_per_100g=c100)
            txt = f"{label}({round(conf*100,1)})_{round(cals)}kcal"
        else:
            txt = f"{label}({round(conf*100,1)})"

        color = tuple(int(c) for c in colors[cids[v["idx"]]])
        cv2.rectangle(canvas, (x, y), (x + bw, y + bh), color, 2)
        (tw, th_), _ = cv2.getTextSize(txt, font, 0.55, 2)
        cv2.rectangle(canvas, (x, y - th_ - 8), (x + tw, y), color, -1)
        cv2.putText(canvas, txt, (x, y - 4), font, 0.55, (255, 255, 255), 2)
        detections.append(entry)

    _, buf = cv2.imencode(".jpg", canvas, [cv2.IMWRITE_JPEG_QUALITY, 92])
    b64 = base64.b64encode(buf).decode()

    # Save annotated result to disk
    result_fname = f"scan_{uuid.uuid4().hex[:8]}.jpg"
    cv2.imwrite(os.path.join(IMG_RESULT_PATH, result_fname), canvas)

    return dict(detections=detections, detection_time=round(det_time, 3),
                result_image=b64, thumb_found=pix_cm is not None)


# ═══════════════════════════════════════════════════════════════════════
# AUTH ROUTES
# ═══════════════════════════════════════════════════════════════════════

@app.route("/api/auth/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not username or not email or not password:
        return jsonify(error="Username, email and password are required"), 400
    if len(username) < 3:
        return jsonify(error="Username must be at least 3 characters"), 400
    if "@" not in email:
        return jsonify(error="Invalid email address"), 400
    if len(password) < 6:
        return jsonify(error="Password must be at least 6 characters"), 400

    db = get_db()
    existing = db.execute(
        "SELECT id FROM users WHERE username=? OR email=?", (username, email)
    ).fetchone()
    if existing:
        return jsonify(error="Username or email already registered"), 409

    uid = uuid.uuid4().hex
    pw_hash = hash_password(password)
    now = datetime.now(timezone.utc).isoformat()
    db.execute("INSERT INTO users VALUES (?,?,?,?,?)",
               (uid, username, email, pw_hash, now))
    db.commit()

    token = generate_token(uid)
    return jsonify(token=token, user=dict(id=uid, username=username, email=email)), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    identifier = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not identifier or not password:
        return jsonify(error="Email and password are required"), 400

    db = get_db()
    row = db.execute(
        "SELECT * FROM users WHERE email=? OR username=?", (identifier, identifier)
    ).fetchone()

    if not row or not verify_password(password, row["pw_hash"]):
        return jsonify(error="Invalid credentials"), 401

    token = generate_token(row["id"])
    return jsonify(token=token, user=dict(id=row["id"], username=row["username"],
                                          email=row["email"]))


@app.route("/api/auth/me", methods=["GET"])
@auth_required
def get_me():
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE id=?", (g.user_id,)).fetchone()
    if not row:
        return jsonify(error="User not found"), 404
    return jsonify(user=dict(id=row["id"], username=row["username"], email=row["email"]))


# ═══════════════════════════════════════════════════════════════════════
# ANALYSIS ROUTES
# ═══════════════════════════════════════════════════════════════════════

@app.route("/api/analyze", methods=["POST"])
@auth_required
def analyze():
    if "image" not in request.files:
        return jsonify(error="No image file provided"), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify(error="Empty filename"), 400

    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify(error=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"), 400

    fname = f"{uuid.uuid4().hex}.{ext}"
    fpath = os.path.join(UPLOAD_FOLDER, fname)
    file.save(fpath)

    safe_name = secure_filename(file.filename)
    test_path = os.path.join(TEST_IMG_FOLDER_PATH, safe_name)
    img = cv2.imread(fpath)
    if img is not None:
        cv2.imwrite(test_path, img)

    if img is None:
        return jsonify(error="Failed to read the image"), 400

    try:
        result = run_analysis(img)
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        try:
            os.remove(fpath)
        except OSError:
            pass

    # Persist scan to history
    foods = [d for d in result["detections"] if d["label"] != "thumb"]
    total_cal = sum(d.get("calories_kcal", 0) for d in foods)
    scan_id = uuid.uuid4().hex
    db = get_db()
    db.execute(
        "INSERT INTO scan_history VALUES (?,?,?,?,?,?,?,?,?)",
        (scan_id, g.user_id, safe_name,
         json.dumps(result["detections"]),
         result["detection_time"],
         1 if result["thumb_found"] else 0,
         round(total_cal, 1),
         result["result_image"],
         datetime.now(timezone.utc).isoformat())
    )
    db.commit()

    result["scan_id"] = scan_id
    return jsonify(result)


# ═══════════════════════════════════════════════════════════════════════
# HISTORY ROUTES
# ═══════════════════════════════════════════════════════════════════════

@app.route("/api/history", methods=["GET"])
@auth_required
def get_history():
    db = get_db()
    rows = db.execute(
        "SELECT id, filename, detections, detection_time, thumb_found, "
        "total_calories, scanned_at FROM scan_history "
        "WHERE user_id=? ORDER BY scanned_at DESC LIMIT 50",
        (g.user_id,)
    ).fetchall()

    items = []
    for r in rows:
        items.append(dict(
            id=r["id"],
            filename=r["filename"],
            detections=json.loads(r["detections"]),
            detection_time=r["detection_time"],
            thumb_found=bool(r["thumb_found"]),
            total_calories=r["total_calories"],
            scanned_at=r["scanned_at"],
        ))
    return jsonify(history=items)


@app.route("/api/history/<scan_id>", methods=["GET"])
@auth_required
def get_scan_detail(scan_id):
    db = get_db()
    r = db.execute(
        "SELECT * FROM scan_history WHERE id=? AND user_id=?",
        (scan_id, g.user_id)
    ).fetchone()
    if not r:
        return jsonify(error="Scan not found"), 404
    return jsonify(
        id=r["id"], filename=r["filename"],
        detections=json.loads(r["detections"]),
        detection_time=r["detection_time"],
        thumb_found=bool(r["thumb_found"]),
        total_calories=r["total_calories"],
        result_image=r["result_image"],
        scanned_at=r["scanned_at"],
    )


@app.route("/api/history/<scan_id>", methods=["DELETE"])
@auth_required
def delete_scan(scan_id):
    db = get_db()
    db.execute("DELETE FROM scan_history WHERE id=? AND user_id=?",
               (scan_id, g.user_id))
    db.commit()
    return jsonify(ok=True)


# ═══════════════════════════════════════════════════════════════════════
# MISC
# ═══════════════════════════════════════════════════════════════════════

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify(status="ok", model_loaded="net" in _model_cache)


@app.route("/api/supported-foods", methods=["GET"])
def supported_foods():
    foods = [
        dict(name="Apple", emoji="🍎", cal_per_100g=52),
        dict(name="Banana", emoji="🍌", cal_per_100g=89),
        dict(name="Carrot", emoji="🥕", cal_per_100g=41),
        dict(name="Onion", emoji="🧅", cal_per_100g=40),
        dict(name="Orange", emoji="🍊", cal_per_100g=47),
        dict(name="Kiwi", emoji="🥝", cal_per_100g=44),
        dict(name="Tomato", emoji="🍅", cal_per_100g=18),
    ]
    return jsonify(foods=foods)


# ── Serve React SPA ────────────────────────────────────────────────────
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_spa(path):
    dist = os.path.join(BASE_DIR, "frontend", "dist")
    if path and os.path.exists(os.path.join(dist, path)):
        return send_from_directory(dist, path)
    return send_from_directory(dist, "index.html")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  NutriVision — AI Food Calorie Estimation Server")
    print("=" * 60)
    print(f"  Frontend : http://localhost:5000")
    print(f"  API      : http://localhost:5000/api/")
    print("=" * 60 + "\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
