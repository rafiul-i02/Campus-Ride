from flask import Flask, jsonify, request

app = Flask(__name__)

drivers_db = [
    {"id": "DR-001", "name": "মোঃ আলী আসলাম", "phone": "01723-083940", "license": "LIC-9876", "bus": "২", "experience": 8, "status": "Available"},
    {"id": "DR-002", "name": "মোঃ শহিদুল ইসলাম", "phone": "01703-116321", "license": "LIC-9877", "bus": "৩", "experience": 7, "status": "Available"},
    {"id": "DR-003", "name": "মোঃ ডালিম", "phone": "01734-491235", "license": "LIC-9878", "bus": "৮", "experience": 6, "status": "Available"},
    {"id": "DR-004", "name": "মোঃ তোফাজ্জল", "phone": "01934-888687", "license": "LIC-9879", "bus": "৫", "experience": 9, "status": "Available"},
    {"id": "DR-005", "name": "মোঃ সৈকত", "phone": "01789-885981", "license": "LIC-9880", "bus": "৬", "experience": 5, "status": "Available"},
    {"id": "DR-006", "name": "মোঃ মুনছুর আলী", "phone": "01722-670583", "license": "LIC-9881", "bus": "৭", "experience": 10, "status": "Available"},
    {"id": "DR-007", "name": "মোঃ আবু তায়ের", "phone": "01725-695763", "license": "LIC-9882", "bus": "৮", "experience": 7, "status": "Available"},
    {"id": "DR-008", "name": "মোঃ সাগর", "phone": "01916-669312", "license": "LIC-9883", "bus": "৯", "experience": 6, "status": "Available"}
]

buses_db = [
    {"id": "BUS-02", "model": "Hino", "capacity": 40, "route": "বি-ব্লক", "driver": "মোঃ আলী আসলাম", "status": "Available"},
    {"id": "BUS-03", "model": "Hino", "capacity": 40, "route": "গোবিন্দগঞ্জ", "driver": "মোঃ শহিদুল ইসলাম", "status": "Available"},
    {"id": "BUS-08", "model": "Hino", "capacity": 40, "route": "বনানী / সাতমাথা", "driver": "মোঃ ডালিম", "status": "Available"},
    {"id": "BUS-05", "model": "Hino", "capacity": 40, "route": "গাবতলী", "driver": "মোঃ তোফাজ্জল", "status": "Available"},
    {"id": "BUS-06", "model": "Hino", "capacity": 40, "route": "তিনমাথা", "driver": "মোঃ সৈকত", "status": "Available"},
    {"id": "BUS-07", "model": "Hino", "capacity": 40, "route": "শেরপুর", "driver": "মোঃ মুনছুর আলী", "status": "Available"},
    {"id": "BUS-09", "model": "Hino", "capacity": 40, "route": "দুপচাঁচিয়া", "driver": "মোঃ সাগর", "status": "Available"}
]

routes_db = [
    {
        "routeId": "R-01", 
        "busNo": "৮",
        "departureTime": "সকাল ৮:৪০",
        "name": "সাতমাথা টু ক্যাম্পাস", 
        "stops": "সাতমাথা -> বনানী -> মোকামতলা -> ক্যাম্পাস", 
        "travelTime": "৩০ মিনিট", 
        "serviceDays": "রবিবার - বুধবার",
        "pickupInstruction": "নির্ধারিত সময়ের ৫ মিনিট আগে মূল রোডের পাশে দাঁড়াতে হবে।"
    }
]

trips_db = []
intentions_db = []
saved_routes_db = []
feedback_db = [
    {"id": "FB-01", "name": "রাফিউল ইসলাম", "type": "Passenger Feedback", "details": "বাস সময়মতো ছেড়েছে, সেবা চমৎকার।", "status": "Resolved"}
]
dispatch_logs_db = []
breakdowns_db = []
notifications_db = []
maintenance_db = [
    {"id": "M-01", "type": "Maintenance Need", "target": "BUS-02", "details": "ইঞ্জিন ওভারহিট সমস্যা", "status": "Pending"}
]
urgent_notices_db = [
    {"id": "N-01", "title": "জরুরি বিজ্ঞপ্তি", "content": "বিশেষ পরিস্থিতির কারণে আগামীকাল সকালের সকল বাস যথাসময়ে ছেড়ে যাবে।", "time": "আজ, সকাল ১০:০০"}
]

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PUB CampusRide</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial,sans-serif}
body{background:#f3f6fb;color:#1e293b}
header{background:#123b70;color:#fff;padding:22px 6%}
header h1{font-size:27px;margin-bottom:7px}
header p{color:#dbeafe}
nav{background:#fff;padding:14px 6%;display:flex;flex-wrap:wrap;gap:10px;box-shadow:0 2px 8px #0000000d}
nav button,.btn{border:0;background:#e8eef8;color:#123b70;padding:11px 16px;border-radius:7px;cursor:pointer;font-weight:bold}
nav button:hover,nav button.active,.btn.primary{background:#123b70;color:#fff}
main{max-width:1150px;margin:30px auto;padding:0 20px}
.page{display:none}.page.active{display:block}
.page-title{margin-bottom:20px}.page-title h2{margin-bottom:8px}.page-title p,.muted{color:#64748b;line-height:1.6}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin-bottom:30px}
.card,.panel{background:#fff;padding:22px;border-radius:12px;box-shadow:0 3px 12px #00000008}
.card h3{font-size:15px;color:#64748b;margin-bottom:12px}.number{font-size:28px;color:#123b70;font-weight:bold}
.panel{margin-bottom:22px}.panel h3{margin-bottom:15px}
.schedule-buttons{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0}
.schedule-buttons button{background:#1769aa;color:#fff;border:0;padding:12px 18px;border-radius:7px;cursor:pointer}
.schedule-buttons button.selected{background:#123b70;outline:3px solid #bfdbfe}
input,select,textarea{width:100%;padding:12px;border:1px solid #cbd5e1;border-radius:7px;margin:8px 0 16px;font-size:15px}
label{font-weight:bold;font-size:14px;display:block}
.table-wrap{width:100%;overflow-x:auto}
table{border-collapse:collapse;width:100%;min-width:620px}
th,td{padding:12px;text-align:left;border:1px solid #cbd5e1}
th{background:#eaf1fb;color:#123b70}
.badge{display:inline-block;background:#fff3cd;color:#805b00;padding:6px 10px;border-radius:20px;font-size:12px}
.badge.danger{background:#fee2e2;color:#991b1b}
.badge.success{background:#d1fae5;color:#065f46}
.badge.warning{background:#fef3c7;color:#92400e}
.notice{padding:15px;border-left:4px solid #ef4444;background:#fef2f2;border-radius:5px;margin-bottom:12px;line-height:1.6;color:#991b1b}
.btn{margin:2px}.btn.danger{background:#fee2e2;color:#991b1b}
.btn.warning{background:#fef3c7;color:#92400e}
footer{margin-top:40px;padding:22px;text-align:center;background:#123b70;color:white}
.form-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:0 16px}
.small-note{font-size:13px;color:#64748b;line-height:1.6;margin-top:12px}
@media(max-width:600px){header h1{font-size:22px}main{margin-top:20px;padding:0 12px}.panel{padding:16px}}
</style>
</head>
<body>
<header>
  <h1>🚌 পুণ্ড্র ইউনিভার্সিটি অব সায়েন্স অ্যান্ড টেকনোলজি</h1>
  <p>CampusRide - বাসের সময়সূচী ও রুট ম্যানেজমেন্ট পোর্টাল</p>
</header>

<nav>
  <button class="active" data-page="dashboard" onclick="showPage('dashboard',this)">Dashboard</button>
  <button data-page="urgent-notices" onclick="showPage('urgent-notices',this)">📢 Urgent Notices</button>
  <button data-page="routes" onclick="showPage('routes',this)">Route Management</button>
  <button data-page="schedule" onclick="showPage('schedule',this)">Bus Schedule</button>
  <button data-page="drivers" onclick="showPage('drivers',this)">Driver Management</button>
  <button data-page="buses" onclick="showPage('buses',this)">Bus Management</button>
  <button data-page="trips" onclick="showPage('trips',this)">Trip Scheduling</button>
  <button data-page="dispatcher" onclick="showPage('dispatcher',this)">Dispatcher & ETA</button>
  <button data-page="breakdowns" onclick="showPage('breakdowns',this)">Breakdowns</button>
  <button data-page="reports-analytics" onclick="showPage('reports-analytics',this)">History & Reports</button>
  <button data-page="feedback" onclick="showPage('feedback',this)">Feedback</button>
  <button data-page="maintenance" onclick="showPage('maintenance',this)">Maintenance</button>
  <button data-page="student" onclick="showPage('student',this)">Student Portal</button>
  <button data-page="about" onclick="showPage('about',this)">About</button>
</nav>

<main>
<section id="dashboard" class="page active">
  <div class="page-title"><h2>স্বাগতম CampusRide-এ 👋</h2><p>অফিশিয়াল রুট, বাসের সময়সূচী ও পরিবহন ব্যবস্থাপনা এক পোর্টালে।</p></div>
  <div class="cards">
    <div class="card"><h3>মোট রুট</h3><div class="number" id="routeCount">0</div><p class="muted">সক্রিয় রুট</p></div>
    <div class="card"><h3>ড্রাইভার রেকর্ড</h3><div class="number" id="driverCount">0</div><p class="muted">সক্রিয় ড্রাইভার</p></div>
    <div class="card"><h3>বাস রেকর্ড</h3><div class="number" id="busCount">0</div><p class="muted">সক্রিয় বাস</p></div>
    <div class="card"><h3>নির্ধারিত ট্রিপ</h3><div class="number" id="tripCount">0</div><p class="muted">সিস্টেমে ট্রিপ</p></div>
  </div>
  <div class="panel"><h3>🚨 জরুরি পরিবহন নোটিশ বোর্ড (Live Notice)</h3><div id="homeNoticeContainer">লোড হচ্ছে...</div></div>
  <div class="panel"><h3>দ্রুত প্রবেশ</h3>
    <div class="schedule-buttons">
      <button onclick="showPage('urgent-notices')">জরুরি নোটিশ প্রকাশ করুন</button>
      <button onclick="showPage('dispatcher')">ডিসপ্যাচার ও ETA পোর্টাল</button>
      <button onclick="showPage('student')">স্টুডেন্ট পোর্টাল</button>
    </div>
  </div>
</section>

<!-- Urgent Notices Management Section (Newly Added) -->
<section id="urgent-notices" class="page">
  <div class="page-title"><h2>📢 Urgent Notice Management</h2><p>Publish critical transport announcements to display instantly on the website front page.</p></div>
  <div class="panel">
    <h3>নতুন জরুরি নোটিশ প্রকাশ করুন</h3>
    <form id="noticeForm">
      <div class="form-grid">
        <div><label>নোটিশের শিরোনাম (Title)</label><input id="nTitle" placeholder="যেমন: জরুরি বিজ্ঞপ্তি" required></div>
        <div><label>প্রকাশের সময় (Time)</label><input id="nTime" placeholder="যেমন: আজ, দুপুর ২:০০" required></div>
      </div>
      <div><label>নোটিশের বিস্তারিত বিবরণ (Content)</label><textarea id="nContent" rows="3" placeholder="নোটিশের বিস্তারিত বার্তা এখানে লিখুন..." required></textarea></div>
      <button class="btn primary" type="submit">নোটিশ পাবলিশ করুন</button>
    </form>
  </div>
  <div class="panel">
    <h3>প্রকাশিত নোটিশসমূহ</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>শিরোনাম</th><th>বিস্তারিত</th><th>সময়</th><th>অ্যাকশন</th></tr></thead>
      <tbody id="noticeTable"><tr><td colspan="4">কোনো নোটিশ নেই।</td></tr></tbody>
    </table></div>
  </div>
</section>

<!-- Route Management Section -->
<section id="routes" class="page">
  <div class="page-title"><h2>📍 Route & Stop Management</h2><p>Manage ordered stops, service days, travel times and pickup instructions.</p></div>
  <div class="panel">
    <h3 id="routeFormTitle">নতুন রুট ও স্টপ যুক্ত করুন</h3>
    <form id="routeForm">
      <div class="form-grid">
        <div><label>Route ID</label><input id="rId" placeholder="R-02" required></div>
        <div><label>বাস নম্বর (Bus No)</label><input id="rBusNo" placeholder="যেমন: ৮" required></div>
        <div><label>বাস ছাড়ার সময় (Departure Time)</label><input id="rDepTime" placeholder="সকাল ৮:৪০" required></div>
        <div><label>রুটের নাম</label><input id="rName" placeholder="শেরপুর থেকে ক্যাম্পাস" required></div>
        <div><label>ক্রমানুযায়ী স্টপ (Ordered Stops)</label><input id="rStops" placeholder="শেরপুর -> গাবতলী -> ক্যাম্পাস" required></div>
        <div><label>ভ্রমণের সময় (Travel Time)</label><input id="rTime" placeholder="৪৫ মিনিট" required></div>
        <div><label>সারভিস ডে (Service Days)</label><input id="rDays" placeholder="শনিবার - বৃহস্পতিবার" required></div>
      </div>
      <div><label>পিকআপ নির্দেশনা (Pickup Instructions)</label><textarea id="rInst" rows="2" placeholder="যেমন: মূল গেটের সামনে নির্ধারিত সময়ে দাঁড়াতে হবে" required></textarea></div>
      <button class="btn primary" type="submit" id="routeSubmitBtn">রুট সংরক্ষণ করুন</button>
      <button class="btn" type="button" onclick="resetRouteForm()">রিসেট</button>
    </form>
  </div>
  <div class="panel">
    <h3>সক্রিয় রুটসমূহের তালিকা</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>Route ID</th><th>বাস নম্বর</th><th>বাস ছাড়ার সময়</th><th>রুটের নাম</th><th>ক্রমানুযায়ী স্টপ</th><th>ভ্রমণের সময়</th><th>সারভিস ডে</th><th>পিকআপ নির্দেশনা</th><th>অ্যাকশন</th></tr></thead>
      <tbody id="routeTable"><tr><td colspan="9">লোড হচ্ছে...</td></tr></tbody>
    </table></div>
  </div>
</section>

<!-- Bus Schedule Section -->
<section id="schedule" class="page">
  <div class="page-title"><h2>🚌 বাসের সময়সূচী (শিক্ষার্থী)</h2><p>তারিখ: ০৩/০৭/২০২৬</p></div>
  <div class="panel">
    <div class="schedule-buttons">
      <button id="regularBtn" class="selected" onclick="selectSchedule('regular')">মূল সময়সূচী (রুটিন)</button>
    </div>
    <h3 id="scheduleHeading">পাবলিক বাস রুটিন ও সময়</h3>
    <div id="scheduleContent"></div>
  </div>
</section>

<!-- Driver Management Section -->
<section id="drivers" class="page">
  <div class="page-title"><h2>👨‍✈️ Driver Management</h2><p>বাস চালকদের তথ্য সংযোজন, সম্পাদনা ও ব্যবস্থাপনা।</p></div>
  <div class="panel">
    <h3 id="driverFormTitle">নতুন ড্রাইভার যোগ করুন</h3>
    <form id="driverForm">
      <div class="form-grid">
        <div><label>Driver ID</label><input id="driverId" placeholder="DR-001" required></div>
        <div><label>ড্রাইভারের নাম</label><input id="driverName" placeholder="নাম দিন" required></div>
        <div><label>মোবাইল নম্বর</label><input id="driverPhone" placeholder="০১৭..." required></div>
        <div><label>লাইসেন্স নম্বর</label><input id="driverLicense" placeholder="লাইসেন্স" required></div>
        <div><label>বাস নম্বর</label><input id="driverBus" placeholder="২, ৩ ইত্যাদি" required></div>
        <div><label>অভিজ্ঞতা (বছর)</label><input id="driverExperience" type="number" min="0" required></div>
        <div><label>উপস্থিতি / স্ট্যাটাস (Availability)</label><select id="driverStatus"><option value="Available">Available (সক্রিয়)</option><option value="On Trip">On Trip (ব্যস্ত)</option><option value="Unavailable">Unavailable (অনুপস্থিত)</option></select></div>
      </div>
      <button class="btn primary" type="submit" id="driverSubmitBtn">সংরক্ষণ করুন</button>
      <button class="btn" type="button" onclick="resetDriverForm()">রিসেট</button>
    </form>
  </div>
  <div class="panel">
    <h3>ড্রাইভারের তালিকা (গোপনীয় নম্বরসহ)</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>ID</th><th>নাম</th><th>মোবাইল</th><th>লাইসেন্স</th><th>বাস</th><th>অভিজ্ঞতা</th><th>স্ট্যাটাস</th><th>অ্যাকশন</th></tr></thead>
      <tbody id="driverTable"><tr><td colspan="8">লোড হচ্ছে...</td></tr></tbody>
    </table></div>
  </div>
</section>

<!-- Bus Management Section -->
<section id="buses" class="page">
  <div class="page-title"><h2>🚌 Bus Management</h2><p>বিশ্ববিদ্যালয়ের বাস বহর ব্যবস্থাপনা।</p></div>
  <div class="panel">
    <h3>নতুন বাস যোগ করুন</h3>
    <form id="busForm">
      <div class="form-grid">
        <div><label>বাস নম্বর / ID</label><input id="busId" placeholder="BUS-01" required></div>
        <div><label>মডেল / নাম</label><input id="busModel" placeholder="Hino" required></div>
        <div><label>ধারণক্ষমতা (Capacity)</label><input id="busCapacity" type="number" min="1" required></div>
        <div><label>রুট</label><input id="busRoute" placeholder="রুট" required></div>
        <div><label>ড্রাইভারের নাম</label><input id="busDriver" placeholder="ড্রাইভার"></div>
        <div><label>যানের স্ট্যাটাস (Vehicle Status)</label>
          <select id="busStatus">
            <option value="Available">Available</option>
            <option value="Under Maintenance">Under Maintenance</option>
            <option value="Temporarily Unavailable">Temporarily Unavailable</option>
          </select>
        </div>
      </div>
      <button class="btn primary" type="submit">সংরক্ষণ করুন</button>
    </form>
  </div>
  <div class="panel">
    <h3>বাসের তালিকা</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>বাস ID</th><th>মডেল</th><th>ধারণক্ষমতা</th><th>রুট</th><th>ড্রাইভার</th><th>স্ট্যাটাস</th><th>অ্যাকশন</th></tr></thead>
      <tbody id="busTable"><tr><td colspan="7">লোড হচ্ছে...</td></tr></tbody>
    </table></div>
  </div>
</section>

<!-- Trip Scheduling Section -->
<section id="trips" class="page">
  <div class="page-title"><h2>⏱️ Trip Scheduling & Overlap Detection</h2><p>রিকারিং ও ওয়ান-অফ ট্রিপ শিডিউল করুন এবং সময় সংঘাত (Overlap) এড়ান।</p></div>
  <div class="panel">
    <h3>নতুন ট্রিপ শিডিউল</h3>
    <form id="tripForm">
      <div class="form-grid">
        <div><label>Trip ID</label><input id="tId" placeholder="TR-101" required></div>
        <div><label>ট্রিপ টাইপ (Trip Type)</label>
          <select id="tType" onchange="toggleTripDate()">
            <option value="Recurring">Recurring (নিয়মিত/দৈনিক)</option>
            <option value="One-off">One-off (এককালীন)</option>
          </select>
        </div>
        <div id="dateDiv" style="display:none;"><label>নির্দিষ্ট তারিখ (Date)</label><input id="tDate" type="date"></div>
        <div><label>রুট</label><input id="tRoute" placeholder="সাতমাথা - ক্যাম্পাস" required></div>
        <div><label>বাস নম্বর</label><input id="tBus" placeholder="BUS-01" required></div>
        <div><label>ড্রাইভার ID</label><input id="tDriver" placeholder="DR-001" required></div>
        <div><label>সময় (Departure Time)</label><input id="tTime" type="time" required></div>
      </div>
      <button class="btn primary" type="submit">শিডিউল করুন</button>
    </form>
    <div id="tripAlert" style="margin-top:10px;"></div>
  </div>
  <div class="panel">
    <h3>নির্ধারিত ট্রিপসমূহ</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>Trip ID</th><th>ধরন (Type)</th><th>তারিখ / বিবরণ</th><th>রুট</th><th>বাস</th><th>ড্রাইভার</th><th>সময়</th><th>অ্যাকশন</th></tr></thead>
      <tbody id="tripTable"><tr><td colspan="8">কোনো ট্রিপ নির্ধারিত নেই।</td></tr></tbody>
    </table></div>
  </div>
</section>

<!-- Driver / Dispatcher Portal Section -->
<section id="dispatcher" class="page">
  <div class="page-title"><h2>🚦 Driver / Dispatcher Portal & ETA</h2><p>Record departures, stop arrivals, delays, trip completions, cancellations and Estimated Time of Arrival (ETA).</p></div>
  <div class="panel">
    <h3>ট্রিপ স্ট্যাটাস ও ETA আপডেট করুন</h3>
    <form id="dispatchForm">
      <div class="form-grid">
        <div><label>Trip ID</label><input id="disTripId" placeholder="TR-101" required></div>
        <div><label>অ্যাকশন / স্ট্যাটাস (Action Status)</label>
          <select id="disStatus">
            <option value="Departed">Departed (ছেড়ে গেছে)</option>
            <option value="Stop Arrived">Stop Arrived (স্টপে পৌঁছেছে)</option>
            <option value="Delayed">Delayed (বিলম্ব হয়েছে)</option>
            <option value="Completed">Completed (সম্পন্ন হয়েছে)</option>
            <option value="Cancelled">Cancelled (বাতিল করা হয়েছে)</option>
          </select>
        </div>
        <div><label>আগমনের সম্ভাব্য সময় (ETA)</label><input id="disEta" placeholder="যেমন: সকাল ৯:১০ মিনিট" required></div>
        <div><label>মন্তব্য / বিবরণ</label><input id="disRemarks" placeholder="যেমন: ট্রাফিক জ্যামের কারণে ১০ মিনিট দেরি" required></div>
      </div>
      <button class="btn primary" type="submit">স্ট্যাটাস ও ETA আপডেট করুন</button>
    </form>
  </div>
  <div class="panel">
    <h3>লাইভ ট্রিপ প্রোগ্রেস ও ETA লগ</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>Trip ID</th><th>স্ট্যাটাস</th><th>ETA (সম্ভাব্য সময়)</th><th>বিবরণ / মন্তব্য</th><th>আপডেটের সময়</th><th>অ্যাকশন</th></tr></thead>
      <tbody id="dispatchTable"><tr><td colspan="6">কোনো লগ পাওয়া যায়নি।</td></tr></tbody>
    </table></div>
  </div>
</section>

<!-- Breakdown & Replacement Handling Section -->
<section id="breakdowns" class="page">
  <div class="page-title"><h2>🛠️ Breakdown & Replacement Handling</h2><p>Find available replacements for broken buses or absent drivers, or flag capacity shortages.</p></div>
  <div class="panel">
    <h3>ব্রেকডাউন বা অনুপস্থিতি রিপোর্ট ও রিপ্লেসমেন্ট ফাইন্ডার</h3>
    <form id="breakdownForm">
      <div class="form-grid">
        <div><label>সমস্যার ধরন (Issue Type)</label>
          <select id="bType">
            <option value="Bus Breakdown">Bus Breakdown (বাস নষ্ট)</option>
            <option value="Driver Absence">Driver Absence (ড্রাইভার অনুপস্থিত)</option>
          </select>
        </div>
        <div><label>অফেক্টেড আইডি (Bus ID or Driver ID)</label><input id="bTargetId" placeholder="যেমন: BUS-02 বা DR-001" required></div>
        <div><label>বিবরণ</label><input id="bDetails" placeholder="ইঞ্জিন সমস্যা বা অসুস্থতা" required></div>
      </div>
      <button class="btn primary" type="submit">বিকল্প খুঁজুন (Find Replacement)</button>
    </form>
  </div>
  <div class="panel">
    <h3>ব্রেকডাউন ও রিপ্লেসমেন্ট লগ</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>ধরন</th><th>টার্গেট আইডি</th><th>বিস্তারিত</th><th>রিপ্লেসমেন্ট স্ট্যাটাস</th><th>অ্যাকশন</th></tr></thead>
      <tbody id="breakdownTable"><tr><td colspan="5">কোনো রেকর্ড নেই।</td></tr></tbody>
    </table></div>
  </div>
</section>

<!-- Trip History & Analytics Reports Section -->
<section id="reports-analytics" class="page">
  <div class="page-title"><h2>📈 Trip History & Analytics Reports</h2><p>Comprehensive reports on trip history, delays, cancellations, passenger demand, and vehicle usage.</p></div>
  <div class="cards">
    <div class="card"><h3>মোট ট্রিপ হিস্ট্রি</h3><div class="number" id="repTripCount">0</div><p class="muted">লগকৃত ট্রিপ</p></div>
    <div class="card"><h3>বিলম্ব ও ক্যান্সেলেশন</h3><div class="number" id="repDelayCount">0</div><p class="muted">ইনসিডেন্ট ঘটনা</p></div>
    <div class="card"><h3>মোট প্যাসেঞ্জার ডিমান্ড</h3><div class="number" id="repDemandCount">0</div><p class="muted">ইন্টেনশন সাবমিট</p></div>
    <div class="card"><h3>ভেহিক্যাল ইউজেজ রেট</h3><div class="number" id="repUsageRate">100%</div><p class="muted">বাস ব্যবহার হার</p></div>
  </div>
  <div class="panel">
    <h3>📊 বিলম্ব ও ক্যান্সেলেশন রিপোর্ট</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>Trip ID / Route</th><th>ইভেন্ট টাইপ</th><th>কারণ / বিবরণ</th><th>সময়</th></tr></thead>
      <tbody id="repDelayTable"><tr><td colspan="4">কোনো বিলম্ব বা ক্যান্সেলেশন রেকর্ড নেই।</td></tr></tbody>
    </table></div>
  </div>
  <div class="panel">
    <h3>🚍 ভেহিক্যাল ইউজেজ ও রুট ডিমান্ড অ্যানালিসিস</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>রুট</th><th>অ্যাসাইনড বাস</th><th>ধারণক্ষমতা</th><th>প্রত্যাশিত যাত্রী চাহিদা</th><th>ইউজেজ স্ট্যাটাস</th></tr></thead>
      <tbody id="repUsageTable"><tr><td colspan="5">লোড হচ্ছে...</td></tr></tbody>
    </table></div>
  </div>
</section>

<!-- Passenger Feedback & Reports Section -->
<section id="feedback" class="page">
  <div class="page-title"><h2>💬 Passenger Feedback & Incident Reports</h2><p>Record passenger feedback, complaints and operational incidents with resolution tracking.</p></div>
  <div class="panel">
    <h3>নতুন ফিডব্যাক বা অভিযোগ জমা দিন</h3>
    <form id="feedbackPortalForm">
      <div class="form-grid">
        <div><label>যাত্রীর নাম</label><input id="fbName" placeholder="আপনার নাম" required></div>
        <div><label>ফিডব্যাকের ধরন (Type)</label>
          <select id="fbType">
            <option value="Passenger Feedback">Passenger Feedback (মতামত ও পরামর্শ)</option>
            <option value="Complaint">Complaint (অভিযোগ)</option>
            <option value="Incident Report">Incident Report (দুর্ঘটনা বা সমস্যা)</option>
          </select>
        </div>
        <div><label>বিস্তারিত বিবরণ</label><input id="fbDetails" placeholder="আপনার মন্তব্য বা সমস্যা বিস্তারিত লিখুন..." required></div>
      </div>
      <button class="btn primary" type="submit">ফিডব্যাক জমা দিন</button>
    </form>
  </div>
  <div class="panel">
    <h3>জমা হওয়া ফিডব্যাক ও রিপোর্টের তালিকা</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>ID</th><th>নাম</th><th>ধরন</th><th>বিস্তারিত</th><th>স্ট্যাটাস</th><th>অ্যাকশন</th></tr></thead>
      <tbody id="feedbackPortalTable"><tr><td colspan="6">কোনো ফিডব্যাক নেই।</td></tr></tbody>
    </table></div>
  </div>
</section>

<!-- Maintenance & Resolution Tracking Section -->
<section id="maintenance" class="page">
  <div class="page-title"><h2>🔧 Maintenance & Resolution Tracking</h2><p>Record maintenance needs, incidents, and track follow-up actions to resolution.</p></div>
  <div class="panel">
    <h3>নতুন মেইনটেন্যান্স রেকর্ড করুন</h3>
    <form id="maintForm">
      <div class="form-grid">
        <div><label>রেকর্ডের ধরন (Type)</label>
          <select id="mType">
            <option value="Maintenance Need">Maintenance Need (মেইনটেন্যান্স প্রয়োজন)</option>
            <option value="Incident Log">Incident Log (অনাকাঙ্ক্ষিত ঘটনা)</option>
          </select>
        </div>
        <div><label>টার্গেট / বাস আইডি</label><input id="mTarget" placeholder="যেমন: BUS-02" required></div>
        <div><label>বিস্তারিত বিবরণ (Details)</label><input id="mDetails" placeholder="বর্ণনা দিন..." required></div>
        <div><label>রেজোলিউশন স্ট্যাটাস (Status)</label>
          <select id="mStatus">
            <option value="Pending">Pending (অপেক্ষমাণ)</option>
            <option value="In Progress">In Progress (চলমান)</option>
            <option value="Resolved">Resolved (সমাধানকৃত)</option>
          </select>
        </div>
      </div>
      <button class="btn primary" type="submit">রেকর্ড সংরক্ষণ করুন</button>
    </form>
  </div>
  <div class="panel">
    <h3>মেইনটেন্যান্স ও রিজোলিউশন ট্র্যাকিং তালিকা</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>ID</th><th>ধরণ</th><th>টার্গেট</th><th>বিস্তারিত বিবরণ</th><th>রিজোলিউশন স্ট্যাটাস</th><th>অ্যাকশন</th></tr></thead>
      <tbody id="maintenanceTable"><tr><td colspan="6">কোনো রেকর্ড নেই।</td></tr></tbody>
    </table></div>
  </div>
</section>

<!-- Student Portal Section -->
<section id="student" class="page">
  <div class="page-title"><h2>🎓 Student Portal & Demand Analysis</h2><p>শিডিউল দেখুন, পছন্দের রুট সেভ করুন, ট্রাভেল ইন্টেনশন দিন এবং বাসের ধারণক্ষমতার সাথে ডিমান্ড তুলনা করুন।</p></div>
  
  <div class="panel">
    <h3>⭐ পছন্দের রুট সেভ করুন (Save Preferred Routes)</h3>
    <form id="savedRouteForm">
      <div class="form-grid">
        <div><label>শিক্ষার্থীর নাম</label><input id="srName" placeholder="রাফিউল ইসলাম" required></div>
        <div><label>পছন্দের রুট নির্বাচন করুন</label>
          <select id="srRoute">
            <option value="সাতমাথা টু ক্যাম্পাস">সাতমাথা টু ক্যাম্পাস</option>
            <option value="বি-ব্লক টু ক্যাম্পাস">বি-ব্লক টু ক্যাম্পাস</option>
            <option value="গোবিন্দগঞ্জ টু ক্যাম্পাস">গোবিন্দগঞ্জ টু ক্যাম্পাস</option>
            <option value="শেরপুর টু ক্যাম্পাস">শেরপুর টু ক্যাম্পাস</option>
            <option value="গাবতলী টু ক্যাম্পাস">গাবতলী টু ক্যাম্পাস</option>
          </select>
        </div>
      </div>
      <button class="btn primary" type="submit">রুট সেভ করুন</button>
    </form>
    <div style="margin-top:15px;">
      <h4>আপনার সেভ করা রুটসমূহ:</h4>
      <div id="savedRoutesList" class="muted" style="margin-top:5px;">কোনো রুট সেভ করা হয়নি।</div>
    </div>
  </div>

  <div class="panel">
    <h3>🎫 ট্রাভেল ইন্টেনশন রেকর্ড করুন (Travel Intention)</h3>
    <form id="intentionForm">
      <div class="form-grid">
        <div><label>শিক্ষার্থীর নাম ও আইডি</label><input id="sName" placeholder="রাফিউল ইসলাম" required></div>
        <div><label>রুট</label>
          <select id="sRoute">
            <option value="সাতমাথা টু ক্যাম্পাস">সাতমাথা টু ক্যাম্পাস</option>
            <option value="বি-ব্লক টু ক্যাম্পাস">বি-ব্লক টু ক্যাম্পাস</option>
            <option value="গোবিন্দগঞ্জ টু ক্যাম্পাস">গোবিন্দগঞ্জ টু ক্যাম্পাস</option>
            <option value="শেরপুর টু ক্যাম্পাস">শেরপুর টু ক্যাম্পাস</option>
            <option value="গাবতলী টু ক্যাম্পাস">গাবতলী টু ক্যাম্পাস</option>
          </select>
        </div>
        <div><label>যাত্রার সময়</label><input id="sTime" type="datetime-local" required></div>
      </div>
      <button class="btn primary" type="submit">ইন্টেনশন জমা দিন</button>
    </form>
  </div>

  <div class="panel">
    <h3>📊 Expected Demand vs Bus Capacity (তুলনামূলক বিশ্লেষণ)</h3>
    <p class="muted">প্রতিটি রুটে শিক্ষার্থীদের প্রত্যাশিত চাহিদা এবং বাসের ধারণক্ষমতার রিয়েল-টাইম তুলনা:</p><br>
    <div class="table-wrap"><table>
      <thead><tr><th>রুট</th><th>প্রত্যাশিত যাত্রী (Expected Demand)</th><th>বাস ক্যাপাসিটি (Capacity)</th><th>স্ট্যাটাস (Status)</th></tr></thead>
      <tbody id="demandComparisonTable"><tr><td colspan="4">তথ্য বিশ্লেষণ করা হচ্ছে...</td></tr></tbody>
    </table></div>
  </div>
</section>

<section id="about" class="page">
  <div class="page-title"><h2>About CampusRide</h2><p>University Transport Portal</p></div>
  <div class="panel"><h3>আমাদের লক্ষ্য</h3><p class="muted">পুণ্ড্র ইউনিভার্সিটি অব সায়েন্স অ্যান্ড টেকনোলজির শিক্ষার্থীদের যাতায়াত সহজ ও সুশৃঙ্খল করা।</p></div>
</section>
</main>
<footer><p>© 2026 PUB CampusRide | Pundra University of Science & Technology</p></footer>

<script>
function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
}

function maskPhone(phone) {
  if (!phone || phone.length < 6) return phone;
  const start = phone.slice(0, 5);
  const end = phone.slice(-1);
  return start + '*****' + end;
}

function showPage(pageId, button) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById(pageId).classList.add('active');
  document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
  const targetButton = button || document.querySelector('nav button[data-page="' + pageId + '"]');
  if (targetButton) targetButton.classList.add('active');
  if (pageId === 'routes') fetchRoutes();
  if (pageId === 'drivers') fetchDrivers();
  if (pageId === 'buses') fetchBuses();
  if (pageId === 'trips') fetchTrips();
  if (pageId === 'dispatcher') fetchDispatches();
  if (pageId === 'breakdowns') fetchBreakdowns();
  if (pageId === 'urgent-notices') fetchNotices();
  if (pageId === 'reports-analytics') fetchAnalyticsReports();
  if (pageId === 'feedback') fetchFeedbackPortal();
  if (pageId === 'maintenance') fetchMaintenance();
  if (pageId === 'student') { fetchIntentions(); fetchSavedRoutes(); fetchDemandComparison(); }
}

function openSchedule(type) { showPage('schedule'); selectSchedule(type); }

function selectSchedule(type) {
  const content = document.getElementById('scheduleContent');
  const headers = ['বার', 'ক্যাম্পাস থেকে ছাড়ার সময়', 'শেরপুর থেকে', 'বি-ব্লক থেকে', 'বনানী থেকে', 'গোবিন্দগঞ্জ থেকে', 'মোকামতলা থেকে', 'গাবতলী থেকে', 'সাতমাথা থেকে', 'দুপচাঁচিয়া থেকে'];
  
  const rows = [
    ['শুক্রবার', 'দুপুর ০১:০৫ মিনিট', '—', '—', 'সকাল ৮:৩০ মিনিট', 'সকাল ৮:২৫ মিনিট', 'সকাল ৮:৪০ মিনিট', '—', 'সকাল ৮:৪০ মিনিট', '—', 3],
    ['', '—', '—', '—', 'দুপুর ১:৫৫ মিনিট', '—', '—', '—', 'সকাল ১০:০৫ মিনিট', '—', 0],
    ['', 'বিকাল ৪:১৫ মিনিট', 'গোবিন্দগঞ্জ বাস যাবে', '—', '—', '—', '—', '—', 'দুপুর ২:০৫ মিনিট', '—', 0],
    ['শনিবার', 'দুপুর ১:২০ মিনিট', 'সকাল ৮:০০ মিনিট', 'সকাল ৮:২৫ মিনিট', 'সকাল ৮:৩০ মিনিট', 'সকাল ৮:২৫ মিনিট', 'সকাল ৮:৪০ মিনিট', 'সকাল ৮:২০ মিনিট', 'সকাল ৮:৪০ মিনিট', 'সকাল ৮:১৫ মিনিট', 4],
    ['', 'বিকাল ৪:১৫ মিনিট', 'গোবিন্দগঞ্জ বাস যাবে', '—', 'দুপুর ১২:১০ মিনিট', '—', '—', '—', 'সকাল ৯:২৫ মিনিট', '—', 0],
    ['', 'বিকাল ৫:১৫ মিনিট', '—', '—', 'দুপুর ১:৫০ মিনিট', '—', '—', '—', 'দুপুর ১২:২০ মিনিট', '—', 0],
    ['', '—', '—', '—', '—', '—', '—', '—', 'দুপুর ১:৪০ মিনিট', '—', 0],
    ['রবিবার থেকে মঙ্গলবার', 'দুপুর ১:২০ মিনিট', 'সকাল ৮:০০ মিনিট', 'সকাল ৮:২৫ মিনিট', 'সকাল ৮:৩০ মিনিট', 'সকাল ৮:২৫ মিনিট', 'সকাল ৮:৪০ মিনিট', 'সকাল ৮:২০ মিনিট', 'সকাল ৮:৪০ মিনিট', 'সকাল ৮:১৫ মিনিট', 2],
    ['', 'বিকাল ৪:১৫ মিনিট', '—', '—', '—', '—', '—', '—', 'সকাল ৯:২৫ মিনিট', '—', 0]
  ];

  let tableHTML = '<div class="table-wrap"><table><thead><tr>' + headers.map(h => '<th>' + h + '</th>').join('') + '</tr></thead><tbody>';
  rows.forEach(r => {
    tableHTML += '<tr>';
    let span = r[10];
    if (span > 0) {
      tableHTML += `<td rowspan="${span}" style="font-weight:bold; background:#f8fafc; vertical-align:middle;">${r[0]}</td>`;
    }
    for (let i = 1; i < 10; i++) {
      tableHTML += `<td>${r[i]}</td>`;
    }
    tableHTML += '</tr>';
  });
  tableHTML += '</tbody></table></div>';

  content.innerHTML = tableHTML;
}
selectSchedule('regular');

function toggleTripDate() {
  const type = document.getElementById('tType').value;
  const dateDiv = document.getElementById('dateDiv');
  dateDiv.style.display = (type === 'One-off') ? 'block' : 'none';
}

// Urgent Notice Logic
async function fetchNotices() {
  const res = await fetch('/api/urgent-notices');
  const data = await res.json();
  
  // Render Home Dashboard Notice
  const homeBox = document.getElementById('homeNoticeContainer');
  if (data.length > 0) {
    homeBox.innerHTML = data.map(n => `
      <div class="notice">
        <strong>📢 ${escapeHTML(n.title)}</strong> (${escapeHTML(n.time)})<br>
        ${escapeHTML(n.content)}
      </div>
    `).join('');
  } else {
    homeBox.innerHTML = '<p class="muted">বর্তমানে কোনো জরুরি নোটিশ নেই।</p>';
  }

  // Render Notices Table
  const tbody = document.getElementById('noticeTable');
  tbody.innerHTML = data.length ? data.map(n => `
    <tr><td>${escapeHTML(n.title)}</td><td>${escapeHTML(n.content)}</td><td>${escapeHTML(n.time)}</td>
    <td><button class="btn danger" onclick="deleteNotice('${n.id}')">Delete</button></td></tr>
  `).join('') : '<tr><td colspan="4">কোনো নোটিশ নেই।</td></tr>';
}

document.getElementById('noticeForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    id: 'NOTIC-' + Date.now().toString().slice(-4),
    title: document.getElementById('nTitle').value.trim(),
    content: document.getElementById('nContent').value.trim(),
    time: document.getElementById('nTime').value.trim()
  };
  await fetch('/api/urgent-notices', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  document.getElementById('noticeForm').reset();
  fetchNotices();
  alert('জরুরি নোটিশ সফলভাবে পাবলিশ করা হয়েছে!');
});

async function deleteNotice(id) {
  if(!confirm('নোটিশ ডিলিট করতে চান?')) return;
  await fetch('/api/urgent-notices/' + id, { method: 'DELETE' });
  fetchNotices();
}

// Route Management Logic
let routes = [];
async function fetchRoutes() {
  const res = await fetch('/api/routes');
  routes = await res.json();
  const tbody = document.getElementById('routeTable');
  tbody.innerHTML = routes.length ? routes.map(r => `
    <tr><td>${escapeHTML(r.routeId)}</td><td>${escapeHTML(r.busNo)}</td><td>${escapeHTML(r.departureTime)}</td>
    <td>${escapeHTML(r.name)}</td><td>${escapeHTML(r.stops)}</td><td>${escapeHTML(r.travelTime)}</td>
    <td>${escapeHTML(r.serviceDays)}</td><td>${escapeHTML(r.pickupInstruction)}</td>
    <td>
      <button class="btn warning" onclick="editRoute('${r.routeId}')">Edit</button>
      <button class="btn danger" onclick="deleteRoute('${r.routeId}')">Delete</button>
    </td></tr>
  `).join('') : '<tr><td colspan="9">কোনো রুট পাওয়া যায়নি।</td></tr>';
  document.getElementById('routeCount').textContent = routes.length;
}

document.getElementById('routeForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    routeId: document.getElementById('rId').value.trim(),
    busNo: document.getElementById('rBusNo').value.trim(),
    departureTime: document.getElementById('rDepTime').value.trim(),
    name: document.getElementById('rName').value.trim(),
    stops: document.getElementById('rStops').value.trim(),
    travelTime: document.getElementById('rTime').value.trim(),
    serviceDays: document.getElementById('rDays').value.trim(),
    pickupInstruction: document.getElementById('rInst').value.trim()
  };
  await fetch('/api/routes', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  resetRouteForm();
  fetchRoutes();
  alert('রুট সফলভাবে সংরক্ষিত হয়েছে!');
});

function editRoute(id) {
  const r = routes.find(item => item.routeId === id);
  if (!r) return;
  document.getElementById('rId').value = r.routeId;
  document.getElementById('rId').readOnly = true;
  document.getElementById('rBusNo').value = r.busNo;
  document.getElementById('rDepTime').value = r.departureTime;
  document.getElementById('rName').value = r.name;
  document.getElementById('rStops').value = r.stops;
  document.getElementById('rTime').value = r.travelTime;
  document.getElementById('rDays').value = r.serviceDays;
  document.getElementById('rInst').value = r.pickupInstruction;
  document.getElementById('routeFormTitle').textContent = 'রুট সম্পাদনা করুন (Edit Route)';
  document.getElementById('routeSubmitBtn').textContent = 'আপডেট করুন';
  document.getElementById('routeForm').scrollIntoView({behavior:'smooth'});
}

function resetRouteForm() {
  document.getElementById('routeForm').reset();
  document.getElementById('rId').readOnly = false;
  document.getElementById('routeFormTitle').textContent = 'নতুন রুট ও স্টপ যুক্ত করুন';
  document.getElementById('routeSubmitBtn').textContent = 'রুট সংরক্ষণ করুন';
}

async function deleteRoute(id) {
  if(!confirm('রুট ডিলিট করতে চান?')) return;
  await fetch('/api/routes/' + id, { method: 'DELETE' });
  fetchRoutes();
}

// Drivers API
let drivers = [];
async function fetchDrivers() {
  const res = await fetch('/api/drivers');
  drivers = await res.json();
  const tbody = document.getElementById('driverTable');
  tbody.innerHTML = drivers.length ? drivers.map(d => `
    <tr><td>${escapeHTML(d.id)}</td><td>${escapeHTML(d.name)}</td><td>${maskPhone(escapeHTML(d.phone))}</td>
    <td>${escapeHTML(d.license)}</td><td>${escapeHTML(d.bus)}</td><td>${escapeHTML(d.experience)} yrs</td>
    <td><span class="badge">${escapeHTML(d.status)}</span></td>
    <td>
      <button class="btn warning" onclick="editDriver('${d.id}')">Edit</button>
      <button class="btn danger" onclick="deleteDriver('${d.id}')">Delete</button>
    </td></tr>
  `).join('') : '<tr><td colspan="8">কোনো ড্রাইভার পাওয়া যায়নি।</td></tr>';
  document.getElementById('driverCount').textContent = drivers.length;
}

document.getElementById('driverForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    id: document.getElementById('driverId').value.trim(),
    name: document.getElementById('driverName').value.trim(),
    phone: document.getElementById('driverPhone').value.trim(),
    license: document.getElementById('driverLicense').value.trim(),
    bus: document.getElementById('driverBus').value.trim(),
    experience: document.getElementById('driverExperience').value,
    status: document.getElementById('driverStatus').value
  };
  await fetch('/api/drivers', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  resetDriverForm();
  fetchDrivers();
  alert('ড্রাইভারের তথ্য সংরক্ষিত হয়েছে!');
});

function editDriver(id) {
  const d = drivers.find(item => item.id === id);
  if (!d) return;
  document.getElementById('driverId').value = d.id;
  document.getElementById('driverId').readOnly = true;
  document.getElementById('driverName').value = d.name;
  document.getElementById('driverPhone').value = d.phone;
  document.getElementById('driverLicense').value = d.license;
  document.getElementById('driverBus').value = d.bus;
  document.getElementById('driverExperience').value = d.experience;
  document.getElementById('driverStatus').value = d.status;
  document.getElementById('driverFormTitle').textContent = 'ড্রাইভার সম্পাদনা করুন (Edit Driver)';
  document.getElementById('driverSubmitBtn').textContent = 'আপডেট করুন';
  document.getElementById('driverForm').scrollIntoView({behavior:'smooth'});
}

function resetDriverForm() {
  document.getElementById('driverForm').reset();
  document.getElementById('driverId').readOnly = false;
  document.getElementById('driverFormTitle').textContent = 'নতুন ড্রাইভার যোগ করুন';
  document.getElementById('driverSubmitBtn').textContent = 'সংরক্ষণ করুন';
}

async function deleteDriver(id) {
  if(!confirm('ড্রাইভার ডিলিট করতে চান?')) return;
  await fetch('/api/drivers/' + id, { method: 'DELETE' });
  fetchDrivers();
}

// Buses API
let buses = [];
async function fetchBuses() {
  const res = await fetch('/api/buses');
  buses = await res.json();
  const tbody = document.getElementById('busTable');
  tbody.innerHTML = buses.length ? buses.map(b => `
    <tr><td>${escapeHTML(b.id)}</td><td>${escapeHTML(b.model)}</td><td>${escapeHTML(b.capacity)}</td>
    <td>${escapeHTML(b.route)}</td><td>${escapeHTML(b.driver || 'None')}</td>
    <td><span class="badge">${escapeHTML(b.status)}</span></td>
    <td><button class="btn danger" onclick="deleteBus('${b.id}')">Delete</button></td></tr>
  `).join('') : '<tr><td colspan="7">কোনো বাস পাওয়া যায়নি।</td></tr>';
  document.getElementById('busCount').textContent = buses.length;
}

document.getElementById('busForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    id: document.getElementById('busId').value.trim(),
    model: document.getElementById('busModel').value.trim(),
    capacity: document.getElementById('busCapacity').value,
    route: document.getElementById('busRoute').value.trim(),
    driver: document.getElementById('busDriver').value.trim(),
    status: document.getElementById('busStatus').value
  };
  await fetch('/api/buses', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  document.getElementById('busForm').reset();
  fetchBuses();
  alert('বাসের তথ্য সংরক্ষিত হয়েছে!');
});

async function deleteBus(id) {
  if(!confirm('বাস ডিলিট করতে চান?')) return;
  await fetch('/api/buses/' + id, { method: 'DELETE' });
  fetchBuses();
}

// Trips API
async function fetchTrips() {
  const res = await fetch('/api/trips');
  const trips = await res.json();
  document.getElementById('tripTable').innerHTML = trips.length ? trips.map(t => `
    <tr><td>${escapeHTML(t.tripId)}</td><td><span class="badge">${escapeHTML(t.tripType)}</span></td>
    <td>${escapeHTML(t.tripDate || 'প্রতিদিন (Recurring)')}</td>
    <td>${escapeHTML(t.route)}</td><td>${escapeHTML(t.busId)}</td>
    <td>${escapeHTML(t.driverId)}</td><td>${escapeHTML(t.departureTime)}</td>
    <td><button class="btn danger" onclick="deleteTrip('${t.tripId}')">Delete</button></td></tr>
  `).join('') : '<tr><td colspan="8">কোনো ট্রিপ নির্ধারিত নেই।</td></tr>';
  document.getElementById('tripCount').textContent = trips.length;
}

document.getElementById('tripForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const tripType = document.getElementById('tType').value;
  const data = {
    tripId: document.getElementById('tId').value.trim(),
    tripType: tripType,
    tripDate: tripType === 'One-off' ? document.getElementById('tDate').value : 'Recurring',
    route: document.getElementById('tRoute').value.trim(),
    busId: document.getElementById('tBus').value.trim(),
    driverId: document.getElementById('tDriver').value.trim(),
    departureTime: document.getElementById('tTime').value.trim()
  };
  const res = await fetch('/api/trips', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  const result = await res.json();
  const alertBox = document.getElementById('tripAlert');
  if(result.overlap) {
    alertBox.innerHTML = `<div class="notice" style="border-color:#ef4444;background:#fee2e2;color:#991b1b;">⚠️ Overlap Detected! এই বাস বা ড্রাইভার এই সময়ে ইতিমধ্যে নির্ধারিত আছে।</div>`;
  } else {
    alertBox.innerHTML = `<div class="notice" style="border-color:#10b981;background:#d1fae5;color:#065f46;">✅ সফলভাবে ট্রিপ শিডিউল করা হয়েছে!</div>`;
    document.getElementById('tripForm').reset();
    document.getElementById('dateDiv').style.display = 'none';
    fetchTrips();
  }
});

async function deleteTrip(id) {
  if(!confirm('ট্রিপ ডিলিট করতে চান?')) return;
  await fetch('/api/trips/' + id, { method: 'DELETE' });
  fetchTrips();
}

// Dispatcher Portal Logic
async function fetchDispatches() {
  const res = await fetch('/api/dispatches');
  const data = await res.json();
  const tbody = document.getElementById('dispatchTable');
  tbody.innerHTML = data.length ? data.map(d => `
    <tr><td>${escapeHTML(d.tripId)}</td><td><span class="badge info">${escapeHTML(d.status)}</span></td>
    <td><strong>${escapeHTML(d.eta || 'N/A')}</strong></td>
    <td>${escapeHTML(d.remarks)}</td><td>${escapeHTML(d.timestamp)}</td>
    <td><button class="btn danger" onclick="deleteDispatch('${d.tripId}')">Delete</button></td></tr>
  `).join('') : '<tr><td colspan="6">কোনো লগ পাওয়া যায়নি।</td></tr>';
}

document.getElementById('dispatchForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    tripId: document.getElementById('disTripId').value.trim(),
    status: document.getElementById('disStatus').value,
    eta: document.getElementById('disEta').value.trim(),
    remarks: document.getElementById('disRemarks').value.trim(),
    timestamp: new Date().toLocaleTimeString()
  };
  await fetch('/api/dispatches', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  document.getElementById('dispatchForm').reset();
  fetchDispatches();
  alert('স্ট্যাটাস ও ETA সফলভাবে আপডেট করা হয়েছে!');
});

async function deleteDispatch(tripId) {
  if(!confirm('লগ ডিলিট করতে চান?')) return;
  await fetch('/api/dispatches/' + tripId, { method: 'DELETE' });
  fetchDispatches();
}

// Breakdown & Replacement Logic
async function fetchBreakdowns() {
  const res = await fetch('/api/breakdowns');
  const data = await res.json();
  const tbody = document.getElementById('breakdownTable');
  tbody.innerHTML = data.length ? data.map(b => `
    <tr><td>${escapeHTML(b.type)}</td><td>${escapeHTML(b.targetId)}</td><td>${escapeHTML(b.details)}</td>
    <td><span class="badge ${b.replacement.includes('Shortage') ? 'danger' : 'success'}">${escapeHTML(b.replacement)}</span></td>
    <td><button class="btn danger" onclick="deleteBreakdown('${b.targetId}')">Delete</button></td></tr>
  `).join('') : '<tr><td colspan="5">কোনো রেকর্ড নেই।</td></tr>';
}

document.getElementById('breakdownForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    type: document.getElementById('bType').value,
    targetId: document.getElementById('bTargetId').value.trim(),
    details: document.getElementById('bDetails').value.trim()
  };
  const res = await fetch('/api/breakdowns', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  const result = await res.json();
  document.getElementById('breakdownForm').reset();
  fetchBreakdowns();
  alert('স্ট্যাটাস প্রসেস করা হয়েছে: ' + result.replacement);
});

async function deleteBreakdown(targetId) {
  if(!confirm('ডিলিট করতে চান?')) return;
  await fetch('/api/breakdowns/' + targetId, { method: 'DELETE' });
  fetchBreakdowns();
}

// Trip History & Analytics Reports Logic
async function fetchAnalyticsReports() {
  const [tRes, dRes, iRes, bRes] = await Promise.all([
    fetch('/api/trips').then(r => r.json()),
    fetch('/api/dispatches').then(r => r.json()),
    fetch('/api/intentions').then(r => r.json()),
    fetch('/api/buses').then(r => r.json())
  ]);

  document.getElementById('repTripCount').textContent = tRes.length;
  const delayedCancelled = dRes.filter(d => d.status === 'Delayed' || d.status === 'Cancelled');
  document.getElementById('repDelayCount').textContent = delayedCancelled.length;
  document.getElementById('repDemandCount').textContent = iRes.length;

  const delayTbody = document.getElementById('repDelayTable');
  delayTbody.innerHTML = delayedCancelled.length ? delayedCancelled.map(dc => `
    <tr><td>${escapeHTML(dc.tripId)}</td><td><span class="badge danger">${escapeHTML(dc.status)}</span></td>
    <td>${escapeHTML(dc.remarks)} (ETA: ${escapeHTML(dc.eta || 'N/A')})</td><td>${escapeHTML(dc.timestamp)}</td></tr>
  `).join('') : '<tr><td colspan="4">কোনো বিলম্ব বা ক্যান্সেলেশন রেকর্ড নেই।</td></tr>';

  const usageTbody = document.getElementById('repUsageTable');
  const routesList = ["সাতমাথা টু ক্যাম্পাস", "বি-ব্লক টু ক্যাম্পাস", "গোবিন্দগঞ্জ টু ক্যাম্পাস", "শেরপুর টু ক্যাম্পাস", "গাবতলী টু ক্যাম্পাস"];
  
  let usageHtml = '';
  routesList.forEach(rt => {
    const matchedBus = bRes.find(b => b.route.includes(rt.split(' ')[0]));
    const busId = matchedBus ? matchedBus.id : 'BUS-General';
    const capacity = matchedBus ? matchedBus.capacity : 40;
    const demand = iRes.filter(i => i.route === rt).length;

    let usageBadge = '<span class="badge success">Optimum</span>';
    if (demand > capacity) usageBadge = '<span class="badge danger">Overloaded</span>';
    else if (demand === 0) usageBadge = '<span class="badge warning">Low Usage</span>';

    usageHtml += `<tr><td>${rt}</td><td>${busId}</td><td>${capacity} জন</td><td>${demand} জন</td><td>${usageBadge}</td></tr>`;
  });
  usageTbody.innerHTML = usageHtml;
}

// Passenger Feedback Portal Logic
async function fetchFeedbackPortal() {
  const res = await fetch('/api/feedback-portal');
  const data = await res.json();
  const tbody = document.getElementById('feedbackPortalTable');
  tbody.innerHTML = data.length ? data.map(f => `
    <tr><td>${escapeHTML(f.id)}</td><td>${escapeHTML(f.name)}</td><td>${escapeHTML(f.type)}</td>
    <td>${escapeHTML(f.details)}</td>
    <td><span class="badge ${f.status === 'Resolved' ? 'success' : 'warning'}">${escapeHTML(f.status)}</span></td>
    <td>
      <button class="btn warning" onclick="updateFeedbackStatus('${f.id}', 'Resolved')">Resolve</button>
      <button class="btn danger" onclick="deleteFeedbackPortal('${f.id}')">Delete</button>
    </td></tr>
  `).join('') : '<tr><td colspan="6">কোনো ফিডব্যাক নেই।</td></tr>';
}

document.getElementById('feedbackPortalForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    id: 'FB-' + Date.now().toString().slice(-4),
    name: document.getElementById('fbName').value.trim(),
    type: document.getElementById('fbType').value,
    details: document.getElementById('fbDetails').value.trim(),
    status: 'Pending'
  };
  await fetch('/api/feedback-portal', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  document.getElementById('feedbackPortalForm').reset();
  fetchFeedbackPortal();
  alert('আপনার ফিডব্যাক সফলভাবে জমা হয়েছে!');
});

async function updateFeedbackStatus(id, newStatus) {
  await fetch('/api/feedback-portal/' + id, { method: 'PUT', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({status: newStatus}) });
  fetchFeedbackPortal();
}

async function deleteFeedbackPortal(id) {
  if(!confirm('ডিলিট করতে চান?')) return;
  await fetch('/api/feedback-portal/' + id, { method: 'DELETE' });
  fetchFeedbackPortal();
}

// Maintenance & Resolution Tracking Logic
async function fetchMaintenance() {
  const res = await fetch('/api/maintenance');
  const data = await res.json();
  const tbody = document.getElementById('maintenanceTable');
  tbody.innerHTML = data.length ? data.map(m => {
    let badgeCls = 'warning';
    if(m.status === 'Resolved') badgeCls = 'success';
    if(m.status === 'Pending') badgeCls = 'danger';
    return `
      <tr><td>${escapeHTML(m.id)}</td><td>${escapeHTML(m.type)}</td><td>${escapeHTML(m.target)}</td>
      <td>${escapeHTML(m.details)}</td>
      <td><span class="badge ${badgeCls}">${escapeHTML(m.status)}</span></td>
      <td>
        <button class="btn warning" onclick="updateMaintenanceStatus('${m.id}', 'Resolved')">Resolve</button>
        <button class="btn danger" onclick="deleteMaintenance('${m.id}')">Delete</button>
      </td></tr>
    `;
  }).join('') : '<tr><td colspan="6">কোনো রেকর্ড নেই।</td></tr>';
}

document.getElementById('maintForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    id: 'MNT-' + Date.now().toString().slice(-4),
    type: document.getElementById('mType').value,
    target: document.getElementById('mTarget').value.trim(),
    details: document.getElementById('mDetails').value.trim(),
    status: document.getElementById('mStatus').value
  };
  await fetch('/api/maintenance', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  document.getElementById('maintForm').reset();
  fetchMaintenance();
  alert('মেইনটেন্যান্স রেকর্ড সফলভাবে সংরক্ষিত হয়েছে!');
});

async function updateMaintenanceStatus(id, newStatus) {
  await fetch('/api/maintenance/' + id, { method: 'PUT', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({status: newStatus}) });
  fetchMaintenance();
}

async function deleteMaintenance(id) {
  if(!confirm('রেকর্ড ডিলিট করতে চান?')) return;
  await fetch('/api/maintenance/' + id, { method: 'DELETE' });
  fetchMaintenance();
}

// Student Portal Logic
async function fetchSavedRoutes() {
  const res = await fetch('/api/saved-routes');
  const data = await res.json();
  const list = document.getElementById('savedRoutesList');
  list.innerHTML = data.length ? data.map(sr => `<span class="badge" style="margin-right:5px;background:#e2e8f0;color:#1e293b;">📌 ${escapeHTML(sr.name)}: ${escapeHTML(sr.route)}</span>`).join('') : 'কোনো রুট সেভ করা হয়নি।';
}

document.getElementById('savedRouteForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    name: document.getElementById('srName').value.trim(),
    route: document.getElementById('srRoute').value
  };
  await fetch('/api/saved-routes', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  fetchSavedRoutes();
  alert('পছন্দের রুট সফলভাবে সেভ করা হয়েছে!');
});

async function fetchIntentions() {
  const res = await fetch('/api/intentions');
  const data = await res.json();
  fetchDemandComparison();
}

document.getElementById('intentionForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    name: document.getElementById('sName').value.trim(),
    route: document.getElementById('sRoute').value,
    time: document.getElementById('sTime').value.trim()
  };
  await fetch('/api/intentions', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  document.getElementById('intentionForm').reset();
  fetchIntentions();
  alert('ইন্টেনশন জমা হয়েছে!');
});

async function fetchDemandComparison() {
  const [iRes, bRes] = await Promise.all([
    fetch('/api/intentions').then(r => r.json()),
    fetch('/api/buses').then(r => r.json())
  ]);

  const demandMap = {};
  iRes.forEach(i => {
    demandMap[i.route] = (demandMap[i.route] || 0) + 1;
  });

  const routesList = ["সাতমাথা টু ক্যাম্পাস", "বি-ব্লক টু ক্যাম্পাস", "গোবিন্দগঞ্জ টু ক্যাম্পাস", "শেরপুর টু ক্যাম্পাস", "গাবতলী টু ক্যাম্পাস"];
  const tbody = document.getElementById('demandComparisonTable');
  
  let html = '';
  routesList.forEach(rt => {
    const demand = demandMap[rt] || 0;
    const matchedBus = bRes.find(b => b.route.includes(rt.split(' ')[0]));
    const capacity = matchedBus ? parseInt(matchedBus.capacity) : 40;
    
    let badgeClass = 'success';
    let statusText = 'Normal (স্বাভাবিক)';
    if (demand > capacity) {
      badgeClass = 'danger';
      statusText = 'Overloaded (অতিরিক্ত চাপ)';
    }

    html += `<tr><td>${rt}</td><td>${demand} জন</td><td>${capacity} জন</td><td><span class="badge ${badgeClass}">${statusText}</span></td></tr>`;
  });
  tbody.innerHTML = html;
}

fetchRoutes();
fetchDrivers();
fetchBuses();
fetchTrips();
fetchDispatches();
fetchBreakdowns();
fetchNotices();
fetchAnalyticsReports();
fetchFeedbackPortal();
fetchMaintenance();
fetchIntentions();
</script>
</body>
</html>
    """

# --- API Endpoints ---
@app.route("/api/routes", methods=["GET", "POST"])
def handle_routes():
    global routes_db
    if request.method == "POST":
        data = request.json
        routes_db = [r for r in routes_db if r["routeId"] != data["routeId"]]
        routes_db.append(data)
        return jsonify({"success": True})
    return jsonify(routes_db)

@app.route("/api/routes/<route_id>", methods=["DELETE"])
def delete_route(route_id):
    global routes_db
    routes_db = [r for r in routes_db if r["routeId"] != route_id]
    return jsonify({"success": True})

@app.route("/api/drivers", methods=["GET", "POST"])
def handle_drivers():
    global drivers_db
    if request.method == "POST":
        data = request.json
        drivers_db = [d for d in drivers_db if d["id"] != data["id"]]
        drivers_db.append(data)
        return jsonify({"success": True})
    return jsonify(drivers_db)

@app.route("/api/drivers/<driver_id>", methods=["DELETE"])
def delete_driver(driver_id):
    global drivers_db
    drivers_db = [d for d in drivers_db if d["id"] != driver_id]
    return jsonify({"success": True})

@app.route("/api/buses", methods=["GET", "POST"])
def handle_buses():
    global buses_db
    if request.method == "POST":
        data = request.json
        buses_db = [b for b in buses_db if b["id"] != data["id"]]
        buses_db.append(data)
        return jsonify({"success": True})
    return jsonify(buses_db)

@app.route("/api/buses/<bus_id>", methods=["DELETE"])
def delete_bus(bus_id):
    global buses_db
    buses_db = [b for b in buses_db if b["id"] != bus_id]
    return jsonify({"success": True})

@app.route("/api/trips", methods=["GET", "POST"])
def handle_trips():
    global trips_db
    if request.method == "POST":
        data = request.json
        overlap = any(
            (t["busId"] == data["busId"] or t["driverId"] == data["driverId"]) and 
            t["departureTime"] == data["departureTime"] and
            (t.get("tripDate") == data.get("tripDate") or t["tripType"] == "Recurring" or data["tripType"] == "Recurring")
            for t in trips_db
        )
        if overlap:
            return jsonify({"success": False, "overlap": True})
        trips_db = [t for t in trips_db if t["tripId"] != data["tripId"]]
        trips_db.append(data)
        return jsonify({"success": True, "overlap": False})
    return jsonify(trips_db)

@app.route("/api/trips/<trip_id>", methods=["DELETE"])
def delete_trip(trip_id):
    global trips_db
    trips_db = [t for t in trips_db if t["tripId"] != trip_id]
    return jsonify({"success": True})

@app.route("/api/dispatches", methods=["GET", "POST"])
def handle_dispatches():
    global dispatch_logs_db
    if request.method == "POST":
        data = request.json
        dispatch_logs_db = [d for d in dispatch_logs_db if d["tripId"] != data["tripId"]]
        dispatch_logs_db.append(data)
        return jsonify({"success": True})
    return jsonify(dispatch_logs_db)

@app.route("/api/dispatches/<trip_id>", methods=["DELETE"])
def delete_dispatch(trip_id):
    global dispatch_logs_db
    dispatch_logs_db = [d for d in dispatch_logs_db if d["tripId"] != trip_id]
    return jsonify({"success": True})

@app.route("/api/breakdowns", methods=["GET", "POST"])
def handle_breakdowns():
    global breakdowns_db, buses_db, drivers_db
    if request.method == "POST":
        data = request.json
        target = data["targetId"]
        issue_type = data["type"]
        
        replacement_msg = ""
        if "Bus" in issue_type:
            free_bus = next((b for b in buses_db if b["status"] == "Available" and b["id"] != target), None)
            if free_bus:
                replacement_msg = f"Assigned Replacement Bus: {free_bus['id']} ({free_bus['route']})"
            else:
                replacement_msg = "⚠️ Capacity Shortage Flagged! No replacement bus available."
        else:
            free_driver = next((d for d in drivers_db if d["status"] == "Available" and d["id"] != target), None)
            if free_driver:
                start = free_driver['phone'][:5] if len(free_driver['phone']) >= 6 else free_driver['phone']
                end = free_driver['phone'][-1:] if len(free_driver['phone']) >= 1 else ''
                masked_p = start + '*****' + end
                replacement_msg = f"Assigned Replacement Driver: {free_driver['name']} ({masked_p})"
            else:
                replacement_msg = "⚠️ Capacity Shortage Flagged! No replacement driver available."
        
        data["replacement"] = replacement_msg
        breakdowns_db = [b for b in breakdowns_db if b["targetId"] != target]
        breakdowns_db.append(data)
        return jsonify({"success": True, "replacement": replacement_msg})
    return jsonify(breakdowns_db)

@app.route("/api/breakdowns/<target_id>", methods=["DELETE"])
def delete_breakdown(target_id):
    global breakdowns_db
    breakdowns_db = [b for b in breakdowns_db if b["targetId"] != target_id]
    return jsonify({"success": True})

@app.route("/api/urgent-notices", methods=["GET", "POST"])
def handle_urgent_notices():
    global urgent_notices_db
    if request.method == "POST":
        urgent_notices_db.insert(0, request.json)
        return jsonify({"success": True})
    return jsonify(urgent_notices_db)

@app.route("/api/urgent-notices/<notice_id>", methods=["DELETE"])
def delete_urgent_notice(notice_id):
    global urgent_notices_db
    urgent_notices_db = [n for n in urgent_notices_db if n["id"] != notice_id]
    return jsonify({"success": True})

@app.route("/api/feedback-portal", methods=["GET", "POST"])
def handle_feedback_portal():
    global feedback_db
    if request.method == "POST":
        feedback_db.append(request.json)
        return jsonify({"success": True})
    return jsonify(feedback_db)

@app.route("/api/feedback-portal/<fb_id>", methods=["PUT", "DELETE"])
def update_delete_feedback(fb_id):
    global feedback_db
    if request.method == "PUT":
        data = request.json
        for f in feedback_db:
            if f["id"] == fb_id:
                f["status"] = data.get("status", f["status"])
        return jsonify({"success": True})
    elif request.method == "DELETE":
        feedback_db = [f for f in feedback_db if f["id"] != fb_id]
        return jsonify({"success": True})

@app.route("/api/maintenance", methods=["GET", "POST"])
def handle_maintenance():
    global maintenance_db
    if request.method == "POST":
        maintenance_db.append(request.json)
        return jsonify({"success": True})
    return jsonify(maintenance_db)

@app.route("/api/maintenance/<m_id>", methods=["PUT", "DELETE"])
def update_delete_maintenance(m_id):
    global maintenance_db
    if request.method == "PUT":
        data = request.json
        for m in maintenance_db:
            if m["id"] == m_id:
                m["status"] = data.get("status", m["status"])
        return jsonify({"success": True})
    elif request.method == "DELETE":
        maintenance_db = [m for m in maintenance_db if m["id"] != m_id]
        return jsonify({"success": True})

@app.route("/api/saved-routes", methods=["GET", "POST"])
def handle_saved_routes():
    global saved_routes_db
    if request.method == "POST":
        saved_routes_db.append(request.json)
        return jsonify({"success": True})
    return jsonify(saved_routes_db)

@app.route("/api/intentions", methods=["GET", "POST"])
def handle_intentions():
    global intentions_db
    if request.method == "POST":
        intentions_db.append(request.json)
        return jsonify({"success": True})
    return jsonify(intentions_db)

if __name__ == "__main__":
    app.run(debug=True)
