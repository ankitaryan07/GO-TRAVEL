/* GO-TRAVEL Chatbot — mood-based destination suggester */
(function() {

const DESTINATIONS = [
  { name:"Goa", emoji:"🏖️", mood:["beach","fun","party","relax","sea","chill","summer"],
    facts:["India's smallest state with 101 km coastline","Home to Basilica of Bom Jesus, a UNESCO site","Carnaval celebrated every February","Over 40 beaches from quiet Palolem to lively Baga"] },
  { name:"Manali", emoji:"🏔️", mood:["adventure","snow","cold","mountains","trekking","hiking","honeymoon"],
    facts:["Gateway to Rohtang Pass at 3,978m altitude","Apple orchards bloom every spring","Solang Valley offers skiing & paragliding","The Beas River flows through the valley"] },
  { name:"Kerala", emoji:"🌴", mood:["peace","nature","backwater","calm","ayurveda","relax","green","spa"],
    facts:["Over 900 km of backwater canals","First state to achieve 100% literacy in India","Munnar has 30,000 hectares of tea gardens","Kathakali dance art form originated here"] },
  { name:"Rajasthan", emoji:"🏰", mood:["culture","heritage","history","desert","royal","fort","camel"],
    facts:["Home to Thar Desert — largest in India","Jaipur's Hawa Mahal has 953 small windows","Udaipur called 'City of Lakes'","Pushkar has the world's only Brahma temple"] },
  { name:"Darjeeling", emoji:"☕", mood:["tea","peace","mist","mountains","cold","romantic","honeymoon","quiet"],
    facts:["Toy Train is a UNESCO World Heritage railway","Produces the world-famous 'champagne of teas'","Tiger Hill offers sunrise view of Kangchenjunga","Altitude 2,042m above sea level"] },
  { name:"Varanasi", emoji:"🪔", mood:["spiritual","religious","culture","ganga","temple","peaceful","heritage"],
    facts:["One of world's oldest continuously inhabited cities — 3,000+ years","Over 80 ghats along the Ganges","Ganga Aarti held every evening at Dasaswamedh Ghat","Silk weaving industry famous for Banarasi sarees"] },
  { name:"Andaman", emoji:"🐠", mood:["beach","diving","snorkeling","island","sea","blue","tropical","fun"],
    facts:["Radhanagar Beach voted Asia's best beach in 2004","Bioluminescent plankton glow at night","Cellular Jail housed freedom fighters","Over 572 islands, only 37 inhabited"] },
  { name:"Ladakh", emoji:"🏔️", mood:["adventure","extreme","cold","biking","mountains","solo","photography"],
    facts:["World's highest motorable road at Umling La — 19,300 ft","Pangong Lake changes colour throughout the day","Monasteries over 1,000 years old","Magnetic Hill appears to pull vehicles uphill"] },
  { name:"Rishikesh", emoji:"🧘", mood:["yoga","spiritual","adventure","rafting","peace","meditation","solo"],
    facts:["Yoga capital of the world","Beatles stayed at Maharishi Ashram in 1968","White-water rafting on Ganges starts here","Laxman Jhula bridge built in 1929"] },
  { name:"Munnar", emoji:"🌿", mood:["green","tea","nature","cool","romantic","misty","honeymoon","peace"],
    facts:["Neelakurinji flowers bloom only once every 12 years","Tea plantations at 1,600m elevation","Home to Nilgiri Tahr — endangered mountain goat","Eravikulam National Park is nearby"] },
];

const CHAT_STEPS = [
  { key:"greet", msg:"👋 Namaste! Main GO-TRAVEL ka AI assistant hun! 🌏<br><br>Aapka next trip plan karne mein help karunga. <b>Aap kaise feel kar rahe ho aaj?</b>", 
    options:["Excited & adventurous 🤩","Need to relax 😌","Romantic mood 💑","Spiritual journey 🙏","Just exploring 🤔"] },
  { key:"weather", msg:"Great! Aap kaisa <b>mausam</b> prefer karte ho?", 
    options:["Beach & sun ☀️","Mountains & snow ❄️","Greenery & rain 🌿","Desert & heat 🏜️","Any weather 🌤️"] },
  { key:"company", msg:"Aap <b>kiske saath</b> travel karna chahte ho?", 
    options:["Solo trip 🧍","With partner 💑","Family trip 👨‍👩‍👧","Friends group 👫","Honeymoon 🥂"] },
  { key:"done", msg:"", options:[] }
];

const MOOD_MAP = {
  "Excited & adventurous 🤩":["adventure","fun","biking"],
  "Need to relax 😌":["relax","calm","peace","spa"],
  "Romantic mood 💑":["romantic","honeymoon","quiet"],
  "Spiritual journey 🙏":["spiritual","religious","temple"],
  "Just exploring 🤔":["culture","heritage","history"],
  "Beach & sun ☀️":["beach","sea","tropical","diving"],
  "Mountains & snow ❄️":["mountains","snow","cold","trekking"],
  "Greenery & rain 🌿":["green","nature","tea","misty"],
  "Desert & heat 🏜️":["desert","royal","fort"],
  "Any weather 🌤️":["relax","fun","culture"],
  "Solo trip 🧍":["solo","adventure","photography"],
  "With partner 💑":["romantic","honeymoon","beach"],
  "Family trip 👨‍👩‍👧":["culture","heritage","relax"],
  "Friends group 👫":["fun","adventure","party"],
  "Honeymoon 🥂":["honeymoon","romantic","quiet"],
};

let step = 0, collectedMoods = [], chatOpen = false;

function createBot() {
  // Widget HTML
  const wrap = document.createElement('div');
  wrap.id = 'gtChatWrap';
  wrap.innerHTML = `
    <button id="gtChatBtn" onclick="toggleChat()">
      <span id="chatBtnIcon">💬</span>
      <span style="position:absolute;top:-4px;right:-4px;background:#ef4444;color:#fff;width:18px;height:18px;border-radius:50%;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;" id="chatDot">1</span>
    </button>
    <div id="gtChatBox">
      <div id="gtChatHead">
        <div style="display:flex;align-items:center;gap:10px;">
          <div style="width:36px;height:36px;border-radius:50%;background:#E8771E;display:flex;align-items:center;justify-content:center;font-size:18px;">🤖</div>
          <div>
            <div style="font-weight:700;font-size:14px;">GO-TRAVEL AI</div>
            <div style="font-size:11px;opacity:.7;display:flex;align-items:center;gap:4px;"><span style="width:6px;height:6px;border-radius:50%;background:#10b981;display:inline-block;"></span>Online</div>
          </div>
        </div>
        <button onclick="toggleChat()" style="background:rgba(255,255,255,.15);border:none;color:#fff;width:28px;height:28px;border-radius:50%;cursor:pointer;font-size:16px;">✕</button>
      </div>
      <div id="gtChatMessages"></div>
      <div id="gtChatOptions"></div>
    </div>`;
  document.body.appendChild(wrap);

  // CSS
  const style = document.createElement('style');
  style.textContent = `
    #gtChatWrap { position:fixed; bottom:24px; right:24px; z-index:8888; font-family:'Segoe UI',sans-serif; }
    #gtChatBtn { width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#E8771E,#f59e0b);border:none;cursor:pointer;box-shadow:0 4px 20px rgba(232,119,30,.5);font-size:24px;color:#fff;position:relative;transition:transform .2s; }
    #gtChatBtn:hover { transform:scale(1.1); }
    #gtChatBox { display:none;position:absolute;bottom:68px;right:0;width:320px;background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 12px 50px rgba(0,0,0,.2);animation:chatPop .3s cubic-bezier(.34,1.56,.64,1); }
    @keyframes chatPop { from{opacity:0;transform:scale(.85) translateY(20px)} to{opacity:1;transform:scale(1) translateY(0)} }
    #gtChatHead { background:linear-gradient(135deg,#0F1F47,#1a4480);padding:14px 16px;display:flex;justify-content:space-between;align-items:center;color:#fff; }
    #gtChatMessages { padding:12px;max-height:280px;overflow-y:auto;background:#f9fafb; }
    .chat-bubble { margin:8px 0;max-width:88%;animation:bubbleIn .25s ease; }
    @keyframes bubbleIn { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
    .bot-bubble { background:#fff;border:1px solid #e5e7eb;border-radius:0 14px 14px 14px;padding:10px 13px;font-size:13px;color:#1f2937;box-shadow:0 1px 4px rgba(0,0,0,.06);line-height:1.5; }
    .user-bubble { background:linear-gradient(135deg,#0F1F47,#1a4480);color:#fff;border-radius:14px 0 14px 14px;padding:10px 13px;font-size:13px;margin-left:auto;text-align:right; }
    #gtChatOptions { padding:8px 12px 12px;background:#fff;display:flex;flex-wrap:wrap;gap:6px; }
    .chat-opt { padding:7px 12px;border-radius:20px;border:1.5px solid #0F1F47;background:#fff;color:#0F1F47;font-size:12px;font-weight:600;cursor:pointer;transition:all .2s; }
    .chat-opt:hover { background:#0F1F47;color:#fff; }
    .dest-suggestion { background:linear-gradient(135deg,#0F1F47,#1a4480);border-radius:12px;padding:14px;margin:6px 0;color:#fff; }
    .dest-suggestion h4 { margin:0 0 6px;font-size:15px;color:#E8771E; }
    .dest-suggestion .fact { font-size:11px;opacity:.75;margin:2px 0;padding-left:10px;border-left:2px solid rgba(232,119,30,.5); }
    .dest-btn { margin-top:10px;padding:7px 14px;background:#E8771E;color:#fff;border:none;border-radius:8px;cursor:pointer;font-size:12px;font-weight:700; }`;
  document.head.appendChild(style);

  setTimeout(() => addBotMsg(CHAT_STEPS[0].msg, CHAT_STEPS[0].options), 800);
}

window.toggleChat = function() {
  chatOpen = !chatOpen;
  document.getElementById('gtChatBox').style.display = chatOpen ? 'block' : 'none';
  document.getElementById('chatDot').style.display = chatOpen ? 'none' : 'flex';
};

function addBotMsg(html, options=[]) {
  const msgs = document.getElementById('gtChatMessages');
  const d = document.createElement('div');
  d.className = 'chat-bubble';
  d.innerHTML = `<div class="bot-bubble">${html}</div>`;
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
  showOptions(options);
}

function addUserMsg(txt) {
  const msgs = document.getElementById('gtChatMessages');
  const d = document.createElement('div');
  d.className = 'chat-bubble';
  d.innerHTML = `<div class="user-bubble">${txt}</div>`;
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
  document.getElementById('gtChatOptions').innerHTML = '';
}

function showOptions(opts) {
  const box = document.getElementById('gtChatOptions');
  box.innerHTML = '';
  opts.forEach(o => {
    const b = document.createElement('button');
    b.className = 'chat-opt';
    b.textContent = o;
    b.onclick = () => handleOption(o);
    box.appendChild(b);
  });
}

function handleOption(choice) {
  addUserMsg(choice);
  const moods = MOOD_MAP[choice] || [];
  collectedMoods = collectedMoods.concat(moods);
  step++;
  if (step < CHAT_STEPS.length - 1) {
    setTimeout(() => addBotMsg(CHAT_STEPS[step].msg, CHAT_STEPS[step].options), 600);
  } else {
    setTimeout(showSuggestions, 700);
  }
}

function showSuggestions() {
  // Score destinations
  const scored = DESTINATIONS.map(d => ({
    ...d, score: d.mood.filter(m => collectedMoods.includes(m)).length
  })).sort((a,b) => b.score - a.score).slice(0,3);

  addBotMsg(`✨ <b>Perfect picks for you!</b> Yeh destinations aapke liye best hain:`);

  setTimeout(() => {
    const msgs = document.getElementById('gtChatMessages');
    scored.forEach((d, i) => {
      setTimeout(() => {
        const div = document.createElement('div');
        div.innerHTML = `<div class="dest-suggestion">
          <h4>${d.emoji} ${d.name}</h4>
          ${d.facts.slice(0,2).map(f => `<div class="fact">• ${f}</div>`).join('')}
          <button class="dest-btn" onclick="window.location.href='/dashboard?dest=${encodeURIComponent(d.name)}'">Plan Trip to ${d.name} →</button>
        </div>`;
        msgs.appendChild(div);
        msgs.scrollTop = msgs.scrollHeight;
      }, i * 400);
    });
    setTimeout(() => showOptions(["🔄 Start Over","🏠 Go to Dashboard"]), scored.length * 400 + 200);
  }, 500);
}

// Override option handler for final options
const origHandle = handleOption;
window._chatHandleOption = function(choice) {
  if (choice === "🔄 Start Over") {
    step = 0; collectedMoods = [];
    document.getElementById('gtChatMessages').innerHTML = '';
    addUserMsg(choice);
    setTimeout(() => addBotMsg(CHAT_STEPS[0].msg, CHAT_STEPS[0].options), 600);
  } else if (choice === "🏠 Go to Dashboard") {
    window.location.href = '/dashboard';
  } else {
    origHandle(choice);
  }
};

// Patch showOptions to use override
function showOptions(opts) {
  const box = document.getElementById('gtChatOptions');
  box.innerHTML = '';
  opts.forEach(o => {
    const b = document.createElement('button');
    b.className = 'chat-opt';
    b.textContent = o;
    b.onclick = () => {
      if (["🔄 Start Over","🏠 Go to Dashboard"].includes(o)) {
        addUserMsg(o);
        if (o === "🔄 Start Over") { step=0; collectedMoods=[]; document.getElementById('gtChatMessages').innerHTML=''; setTimeout(()=>addBotMsg(CHAT_STEPS[0].msg,CHAT_STEPS[0].options),600); }
        else window.location.href='/dashboard';
      } else { handleOption(o); }
    };
    box.appendChild(b);
  });
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', createBot);
else createBot();

})();
