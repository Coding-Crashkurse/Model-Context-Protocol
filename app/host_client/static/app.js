const serverNameEl = document.getElementById("serverName");
const serverUrlEl = document.getElementById("serverUrl");
const btnAddServer = document.getElementById("btnAddServer");
const serverListEl = document.getElementById("serverList");

const questionEl = document.getElementById("question");
const btnAsk = document.getElementById("btnAsk");
const responseEl = document.getElementById("responseArea");

// Lädt aktuelle Server beim Start
async function fetchServers() {
  try {
    const res = await fetch("/api/servers");
    const data = await res.json();
    updateServerList(data);
  } catch (err) {
    console.error(err);
  }
}

function updateServerList(servers) {
  serverListEl.innerHTML = "";
  for (const [name, config] of Object.entries(servers)) {
    const li = document.createElement("li");
    li.textContent = `${name} -> ${config.url}`;
    serverListEl.appendChild(li);
  }
}

btnAddServer.addEventListener("click", async () => {
  const name = serverNameEl.value.trim();
  const url = serverUrlEl.value.trim();
  if (!name || !url) {
    alert("Bitte Name und URL angeben!");
    return;
  }
  try {
    await fetch("/api/servers", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, url }),
    });
    serverNameEl.value = "";
    serverUrlEl.value = "";
    await fetchServers();
  } catch (err) {
    console.error(err);
  }
});

btnAsk.addEventListener("click", async () => {
  const q = questionEl.value.trim();
  if (!q) {
    alert("Bitte eine Frage eingeben.");
    return;
  }
  responseEl.textContent = "Lade...";

  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q }),
    });
    const data = await res.json();
    if (data.answer) {
      responseEl.textContent = data.answer;
    } else {
      responseEl.textContent = "Fehler oder keine Antwort erhalten.";
    }
  } catch (err) {
    console.error(err);
    responseEl.textContent = "Fehler: " + err;
  }
});

window.addEventListener("DOMContentLoaded", fetchServers);
