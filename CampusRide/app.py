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
feedback_db = []

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
.notice{padding:15px;border-left:4px solid #1769aa;background:#eff6ff;border-radius:5px;margin-bottom:12px;line-height:1.6}
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
  <button data-page="routes" onclick="showPage('routes',this)">Route Management</button>
  <button data-page="schedule" onclick="showPage('schedule',this)">Bus Schedule</button>
  <button data-page="drivers" onclick="showPage('drivers',this)">Driver Management</button>
  <button data-page="buses" onclick="showPage('buses',this)">Bus Management</button>
  <button data-page="trips" onclick="showPage('trips',this)">Trip Scheduling</button>
  <button data-page="student" onclick="showPage('student',this)">Student Portal</button>
  <button data-page="reports" onclick="showPage('reports',this)">Reports & Feedback</button>
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
  <div class="panel"><h3>দ্রুত প্রবেশ</h3>
    <div class="schedule-buttons">
      <button onclick="showPage('routes')">রুট ম্যানেজমেন্ট দেখুন</button>
      <button onclick="openSchedule('regular')">অফিশিয়াল সময়সূচী</button>
      <button onclick="showPage('trips')">ট্রিপ শিডিউলিং</button>
    </div>
  </div>
  <div class="panel"><h3>📢 পরিবহন নোটিশ</h3><div class="notice">সমস্ত ম্যানেজমেন্ট সেকশনে এখন Delete-এর পাশাপাশি Edit অপশন যুক্ত করা হয়েছে।</div></div>
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
    <div class="small-note" style="margin-top:20px; border-top:1px solid #cbd5e1; padding-top:10px;">
      <p><strong>বিশেষ নির্দেশনা:</strong></p>
      <p>১. বিশেষ কারণে এবং কর্তৃপক্ষের নির্দেশক্রমে বিশ্ববিদ্যালয় বাসের সময়সূচী পরিবর্তন হতে পারে।</p>
      <p>২. হঠাৎ গাড়ী নষ্ট হলে অথবা রাস্তায় ট্রাফিক জ্যামের কারণে বিশ্ববিদ্যালয় বাস গন্তব্যে পৌঁছাতে নির্দিষ্ট সময়ে কিছু তারতম্য হতে পারে।</p>
    </div>
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
    <h3>ড্রাইভারের তালিকা</h3>
    <input id="driverSearch" placeholder="খুঁজুন..." oninput="renderDrivers()">
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
    <h3 id="busFormTitle">নতুন বাস যোগ করুন</h3>
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
      <button class="btn primary" type="submit" id="busSubmitBtn">সংরক্ষণ করুন</button>
      <button class="btn" type="button" onclick="resetBusForm()">রিসেট</button>
    </form>
  </div>
  <div class="panel">
    <h3>বাসের তালিকা</h3>
    <input id="busSearch" placeholder="খুঁজুন..." oninput="renderBuses()">
    <div class="table-wrap"><table>
      <thead><tr><th>বাস ID</th><th>মডেল</th><th>ধারণক্ষমতা</th><th>রুট</th><th>ড্রাইভার</th><th>স্ট্যাটাস</th><th>অ্যাকশন</th></tr></thead>
      <tbody id="busTable"><tr><td colspan="7">লোড হচ্ছে...</td></tr></tbody>
    </table></div>
  </div>
</section>

<!-- Trip Scheduling Section -->
<section id="trips" class="page">
  <div class="page-title"><h2>⏱️ Trip Scheduling & Overlap Detection</h2><p>ট্রিপ শিডিউল করুন এবং বাস বা ড্রাইভারের দ্বৈত এন্ট্রি এড়ান।</p></div>
  <div class="panel">
    <h3>নতুন ট্রিপ শিডিউল</h3>
    <form id="tripForm">
      <div class="form-grid">
        <div><label>Trip ID</label><input id="tId" placeholder="TR-101" required></div>
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
      <thead><tr><th>Trip ID</th><th>রুট</th><th>বাস</th><th>ড্রাইভার</th><th>সময়</th><th>অ্যাকশন</th></tr></thead>
      <tbody id="tripTable"><tr><td colspan="6">কোনো ট্রিপ নির্ধারিত নেই।</td></tr></tbody>
    </table></div>
  </div>
</section>

<!-- Student Portal Section -->
<section id="student" class="page">
  <div class="page-title"><h2>🎓 Student Travel Intentions</h2><p>শিক্ষার্থীদের যাতায়াতের চাহিদা এবং রুট সংরক্ষণ।</p></div>
  <div class="panel">
    <h3>চাহিদা জমা দিন</h3>
    <form id="intentionForm">
      <div class="form-grid">
        <div><label>শিক্ষার্থীর নাম ও আইডি</label><input id="sName" placeholder="রাফিউল ইসলাম" required></div>
        <div><label>পছন্দের রুট</label><input id="sRoute" placeholder="সাতমাথা থেকে ক্যাম্পাস" required></div>
        <div><label>যাত্রার সময়</label><input id="sTime" type="datetime-local" required></div>
      </div>
      <button class="btn primary" type="submit">জমা দিন</button>
    </form>
  </div>
  <div class="panel">
    <h3>রেকর্ডকৃত ট্রাভেল ডিমান্ড</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>শিক্ষার্থীর নাম</th><th>রুট</th><th>সময়</th><th>স্ট্যাটাস</th></tr></thead>
      <tbody id="intentionTable"><tr><td colspan="4">কোনো রেকর্ড নেই।</td></tr></tbody>
    </table></div>
  </div>
</section>

<!-- Reports & Feedback Section -->
<section id="reports" class="page">
  <div class="page-title"><h2>📋 Reports & Breakdown Feedback</h2><p>গাড়ী নষ্ট হওয়া, বিলম্ব বা যেকোনো অভিযোগ লগ করুন।</p></div>
  <div class="panel">
    <h3>রিপোর্ট জমা দিন</h3>
    <form id="feedbackForm">
      <div class="form-grid">
        <div><label>রিপোর্টার নাম</label><input id="fName" placeholder="নাম" required></div>
        <div><label>সমস্যার ধরন</label><select id="fType"><option>Bus Breakdown (গাড়ী নষ্ট)</option><option>Driver Absence (ড্রাইভার অনুপস্থিত)</option><option>Passenger Feedback (মতামত)</option></select></div>
        <div><label>বিস্তারিত</label><input id="fDetails" placeholder="বর্ণনা দিন..." required></div>
      </div>
      <button class="btn primary" type="submit">জমা দিন</button>
    </form>
  </div>
  <div class="panel">
    <h3>ইনসিডেন্ট লগ</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>রিপোর্টার</th><th>ধরন</th><th>বিস্তারিত</th><th>স্ট্যাটাস</th></tr></thead>
      <tbody id="feedbackTable"><tr><td colspan="4">কোনো রিপোর্ট নেই।</td></tr></tbody>
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
  if (pageId === 'student') fetchIntentions();
  if (pageId === 'reports') fetchFeedback();
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
    ['', 'বিকাল ৪:১৫ মিনিট', '—', '—', 'দুপুর ১:৫০ মিনিট', '—', '—', '—', 'সকাল ৯:২৫ মিনিট', '—', 0]
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

  const contactHTML = `
    <h3 style="margin-top:30px;">যোগাযোগ (চালক ও বাস তথ্য):</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>রুট</th><th>বাস নং</th><th>ড্রাইভারের নাম</th><th>মোবাইল নম্বর</th></tr></thead>
      <tbody>
        <tr><td>বি-ব্লক</td><td>২</td><td>মোঃ আলী আসলাম</td><td>০১৭২৩-০৮৩৯৪০</td></tr>
        <tr><td>গোবিন্দগঞ্জ</td><td>৩</td><td>মোঃ শহিদুল ইসলাম</td><td>০১৭০৩-১১৬৩২১</td></tr>
        <tr><td>বনানী</td><td>৮</td><td>মোঃ ডালিম</td><td>০১৭৩৪-৪৯১২৩৫</td></tr>
        <tr><td>গাবতলী</td><td>৫</td><td>মোঃ তোফাজ্জল</td><td>০১৯৩৪-৮৮৮৬৮৭</td></tr>
        <tr><td>তিনমাথা</td><td>৬</td><td>মোঃ সৈকত</td><td>০১৭৮৯-৮৮৫৯৮১</td></tr>
        <tr><td>শেরপুর</td><td>৭</td><td>মোঃ মুনছুর আলী</td><td>০১৭২২-৬৭০৫৮৩</td></tr>
        <tr><td>সাতমাথা</td><td>৮</td><td>মোঃ আবু তায়ের</td><td>০১৭২৫-৬৯৫৭৬৩</td></tr>
        <tr><td>দুপচাঁচিয়া</td><td>৯</td><td>মোঃ সাগর</td><td>০১৯১৬-৬৬৯৩১২</td></tr>
      </tbody>
    </table></div>
  `;

  content.innerHTML = tableHTML + contactHTML;
}
selectSchedule('regular');

function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
}

// Route Management Logic (with Edit feature)
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

// Drivers API (with Edit feature)
let drivers = [];
async function fetchDrivers() {
  const res = await fetch('/api/drivers');
  drivers = await res.json();
  const tbody = document.getElementById('driverTable');
  tbody.innerHTML = drivers.length ? drivers.map(d => `
    <tr><td>${escapeHTML(d.id)}</td><td>${escapeHTML(d.name)}</td><td>${escapeHTML(d.phone)}</td>
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

// Buses API (with Edit feature)
let buses = [];
async function fetchBuses() {
  const res = await fetch('/api/buses');
  buses = await res.json();
  const tbody = document.getElementById('busTable');
  tbody.innerHTML = buses.length ? buses.map(b => `
    <tr><td>${escapeHTML(b.id)}</td><td>${escapeHTML(b.model)}</td><td>${escapeHTML(b.capacity)}</td>
    <td>${escapeHTML(b.route)}</td><td>${escapeHTML(b.driver || 'None')}</td>
    <td><span class="badge">${escapeHTML(b.status)}</span></td>
    <td>
      <button class="btn warning" onclick="editBus('${b.id}')">Edit</button>
      <button class="btn danger" onclick="deleteBus('${b.id}')">Delete</button>
    </td></tr>
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
  resetBusForm();
  fetchBuses();
  alert('বাসের তথ্য সংরক্ষিত হয়েছে!');
});

function editBus(id) {
  const b = buses.find(item => item.id === id);
  if (!b) return;
  document.getElementById('busId').value = b.id;
  document.getElementById('busId').readOnly = true;
  document.getElementById('busModel').value = b.model;
  document.getElementById('busCapacity').value = b.capacity;
  document.getElementById('busRoute').value = b.route;
  document.getElementById('busDriver').value = b.driver;
  document.getElementById('busStatus').value = b.status;
  document.getElementById('busFormTitle').textContent = 'বাস সম্পাদনা করুন (Edit Bus)';
  document.getElementById('busSubmitBtn').textContent = 'আপডেট করুন';
  document.getElementById('busForm').scrollIntoView({behavior:'smooth'});
}

function resetBusForm() {
  document.getElementById('busForm').reset();
  document.getElementById('busId').readOnly = false;
  document.getElementById('busFormTitle').textContent = 'নতুন বাস যোগ করুন';
  document.getElementById('busSubmitBtn').textContent = 'সংরক্ষণ করুন';
}

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
    <tr><td>${escapeHTML(t.tripId)}</td><td>${escapeHTML(t.route)}</td><td>${escapeHTML(t.busId)}</td>
    <td>${escapeHTML(t.driverId)}</td><td>${escapeHTML(t.departureTime)}</td>
    <td><button class="btn danger" onclick="deleteTrip('${t.tripId}')">Delete</button></td></tr>
  `).join('') : '<tr><td colspan="6">কোনো ট্রিপ নির্ধারিত নেই।</td></tr>';
  document.getElementById('tripCount').textContent = trips.length;
}

document.getElementById('tripForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    tripId: document.getElementById('tId').value.trim(),
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
    fetchTrips();
  }
});

async function deleteTrip(id) {
  if(!confirm('ট্রিপ ডিলিট করতে চান?')) return;
  await fetch('/api/trips/' + id, { method: 'DELETE' });
  fetchTrips();
}

async function fetchIntentions() {
  const res = await fetch('/api/intentions');
  const data = await res.json();
  document.getElementById('intentionTable').innerHTML = data.length ? data.map(i => `
    <tr><td>${escapeHTML(i.name)}</td><td>${escapeHTML(i.route)}</td><td>${escapeHTML(i.time)}</td>
    <td><span class="badge">Recorded</span></td></tr>
  `).join('') : '<tr><td colspan="4">কোনো রেকর্ড নেই।</td></tr>';
}

document.getElementById('intentionForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    name: document.getElementById('sName').value.trim(),
    route: document.getElementById('sRoute').value.trim(),
    time: document.getElementById('sTime').value.trim()
  };
  await fetch('/api/intentions', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  document.getElementById('intentionForm').reset();
  fetchIntentions();
  alert('চাহিদা সংরক্ষিত হয়েছে!');
});

async function fetchFeedback() {
  const res = await fetch('/api/feedback');
  const data = await res.json();
  document.getElementById('feedbackTable').innerHTML = data.length ? data.map(f => `
    <tr><td>${escapeHTML(f.name)}</td><td>${escapeHTML(f.type)}</td><td>${escapeHTML(f.details)}</td>
    <td><span class="badge">Logged</span></td></tr>
  `).join('') : '<tr><td colspan="4">কোনো রিপোর্ট নেই।</td></tr>';
}

document.getElementById('feedbackForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    name: document.getElementById('fName').value.trim(),
    type: document.getElementById('fType').value.trim(),
    details: document.getElementById('fDetails').value.trim()
  };
  await fetch('/api/feedback', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  document.getElementById('feedbackForm').reset();
  fetchFeedback();
  alert('রিপোর্ট জমা হয়েছে!');
});

fetchRoutes();
fetchDrivers();
fetchBuses();
fetchTrips();
fetchIntentions();
fetchFeedback();
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
        overlap = any(t["busId"] == data["busId"] or t["driverId"] == data["driverId"] for t in trips_db if t["departureTime"] == data["departureTime"])
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

@app.route("/api/intentions", methods=["GET", "POST"])
def handle_intentions():
    global intentions_db
    if request.method == "POST":
        intentions_db.append(request.json)
        return jsonify({"success": True})
    return jsonify(intentions_db)

@app.route("/api/feedback", methods=["GET", "POST"])
def handle_feedback():
    global feedback_db
    if request.method == "POST":
        feedback_db.append(request.json)
        return jsonify({"success": True})
    return jsonify(feedback_db)

if __name__ == "__main__":
    app.run(debug=True)
