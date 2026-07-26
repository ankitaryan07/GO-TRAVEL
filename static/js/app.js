/* GO-TRAVEL — Frontend API helper */

const API = "/api";

function saveToken(t) { localStorage.setItem("gt_token", t); }
function getToken() { return localStorage.getItem("gt_token"); }
function clearToken() { localStorage.removeItem("gt_token"); localStorage.removeItem("gt_user"); }
function saveUser(u) { localStorage.setItem("gt_user", JSON.stringify(u)); }
function getUser() { try { const u = localStorage.getItem("gt_user"); return u ? JSON.parse(u) : null; } catch(e) { return null; } }
function isLoggedIn() { return !!getToken(); }

async function apiRequest(path, method = "GET", body = null, auth = true) {
  const headers = { "Content-Type": "application/json" };
  if (auth && getToken()) headers["Authorization"] = "Bearer " + getToken();
  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);
  
  let res, data;
  try {
    res = await fetch(API + path, opts);
    data = await res.json().catch(() => ({}));
  } catch(e) {
    throw new Error("Network error — is server running?");
  }
  
  // Token expired or invalid — auto logout
  if (res.status === 401) {
    clearToken();
    window.location.href = "/login";
    throw new Error("Session expired. Please login again.");
  }
  
  if (!res.ok) throw new Error(data.detail || "Something went wrong");
  return data;
}

async function loginRequest(email, password) {
  return apiRequest("/auth/login", "POST", { email, password }, false);
}

function logout() { clearToken(); window.location.href = "/login"; }
function requireAuth() { 
  if (!isLoggedIn()) { 
    window.location.href = "/login"; 
    return false;
  }
  return true;
}
