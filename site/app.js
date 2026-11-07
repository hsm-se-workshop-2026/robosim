const PYODIDE_VERSION = "0.29.3";
const PYTHON_MODULES = [
  "src/__init__.py",
  "src/browser_api.py",
  "src/adapters/__init__.py",
  "src/adapters/keyboard_control.py",
  "src/adapters/line_follower.py",
  "src/application/__init__.py",
  "src/application/ports.py",
  "src/application/simulation.py",
  "src/domain/__init__.py",
  "src/domain/robot.py",
  "src/domain/track.py",
];
const SVG_SCALE = 80;
const SVG_CENTER_X = 300;
const SVG_CENTER_Y = 150;
const MAX_TRAIL_POINTS = 2000;

const elements = Object.fromEntries(
  [
    "runtime-status",
    "run-status",
    "error-message",
    "track",
    "trail",
    "robot",
    "position",
    "heading",
    "distance",
    "width",
    "height",
    "curves",
    "width-value",
    "height-value",
    "curves-value",
    "apply-track",
    "manual-mode",
    "controller-mode",
    "start",
    "pause",
  ].map((id) => [id, document.getElementById(id)]),
);

let pyodide;
let api;
let apiQueue = Promise.resolve();
let running = false;
let timerId;
let manualMode = false;
let activeKey = null;
let trailPoints = [];

function serializePython(callback) {
  const result = apiQueue.then(callback);
  apiQueue = result.then(
    () => undefined,
    () => undefined,
  );
  return result;
}

function callApi(name, ...args) {
  return serializePython(() => api[name](...args));
}

function setRuntimeState(message) {
  elements["runtime-status"].textContent = message;
}

function setRunState(message) {
  elements["run-status"].textContent = message;
}

function showError(error) {
  running = false;
  window.clearInterval(timerId);
  elements["error-message"].hidden = false;
  elements["error-message"].textContent = `Fehler: ${error.message}`;
  setRunState("Die Simulation wurde angehalten.");
  setRuntimeState("Fehler beim Ausführen");
}

function setControlsEnabled(enabled) {
  for (const id of ["apply-track", "manual-mode", "controller-mode", "start", "pause"]) {
    elements[id].disabled = !enabled;
  }
}

function pointToSvg(point) {
  return `${(SVG_CENTER_X + point.x * SVG_SCALE).toFixed(2)},${(
    SVG_CENTER_Y - point.y * SVG_SCALE
  ).toFixed(2)}`;
}

function renderState(state) {
  const x = SVG_CENTER_X + state.x * SVG_SCALE;
  const y = SVG_CENTER_Y - state.y * SVG_SCALE;
  elements.robot.setAttribute(
    "transform",
    `translate(${x.toFixed(2)} ${y.toFixed(2)}) rotate(${(
      (-state.heading * 180) /
      Math.PI
    ).toFixed(2)})`,
  );
  trailPoints.push(`${x.toFixed(2)},${y.toFixed(2)}`);
  if (trailPoints.length > MAX_TRAIL_POINTS) {
    trailPoints.shift();
  }
  elements.trail.setAttribute("points", trailPoints.join(" "));
  elements.position.textContent = `x = ${state.x.toFixed(2)}, y = ${state.y.toFixed(2)}`;
  elements.heading.textContent = `Winkel = ${state.heading.toFixed(2)} rad`;
  elements.distance.textContent = `Abstand zur Linie: ${state.distance.toFixed(2)}`;
}

function renderReset(json) {
  const state = JSON.parse(json);
  elements.track.setAttribute(
    "points",
    `${state.track.map(pointToSvg).join(" ")} ${pointToSvg(state.track[0])}`,
  );
  trailPoints = [];
  renderState(state);
}

function setModeButtons(mode) {
  manualMode = mode === "manual";
  elements["manual-mode"].classList.toggle("selected", manualMode);
  elements["controller-mode"].classList.toggle("selected", !manualMode);
}

async function loadPythonSources() {
  pyodide.FS.mkdirTree("/src/adapters");
  pyodide.FS.mkdirTree("/src/application");
  pyodide.FS.mkdirTree("/src/domain");
  for (const path of PYTHON_MODULES) {
    const response = await fetch(`./python/${path}`);
    if (!response.ok) {
      throw new Error(`Python-Modul konnte nicht geladen werden: ${path} (${response.status})`);
    }
    pyodide.FS.writeFile(`/${path}`, await response.text());
  }
  await pyodide.runPythonAsync("import sys; sys.path.insert(0, '/')");
  api = pyodide.pyimport("src.browser_api");
}

async function startRuntime() {
  setRuntimeState("Pyodide wird geladen …");
  try {
    pyodide = await loadPyodide({
      indexURL: `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`,
    });
    await loadPythonSources();
    const resetResult = await callApi(
      "reset",
      Number(elements.width.value),
      Number(elements.height.value),
      Number(elements.curves.value),
    );
    renderReset(resetResult);
    setControlsEnabled(true);
    setRuntimeState("Python im Browser bereit");
    elements["error-message"].hidden = true;
  } catch (error) {
    showError(error);
    elements["runtime-status"].textContent = "Pyodide konnte nicht geladen werden";
  }
}

async function advance() {
  if (!running) return;
  try {
    const result = await callApi("step", 0.05);
    renderState(JSON.parse(result));
  } catch (error) {
    showError(error);
  }
}

function startSimulation() {
  if (running) return;
  running = true;
  setRunState("Simulation läuft");
  timerId = window.setInterval(advance, 50);
}

function releaseActiveKey() {
  if (activeKey === null) return;
  activeKey = null;
  callApi("release_key").catch(showError);
}

function pauseSimulation() {
  running = false;
  window.clearInterval(timerId);
  if (manualMode) releaseActiveKey();
  setRunState("Pausiert");
}

async function changeMode(mode) {
  releaseActiveKey();
  try {
    await callApi("set_mode", mode);
    setModeButtons(mode);
    setRunState(mode === "manual" ? "Manueller Modus – W/A/S/D verwenden" : "Linienfolger aktiv");
  } catch (error) {
    showError(error);
  }
}

async function resetTrack() {
  pauseSimulation();
  elements["error-message"].hidden = true;
  try {
    const result = await callApi(
      "reset",
      Number(elements.width.value),
      Number(elements.height.value),
      Number(elements.curves.value),
    );
    renderReset(result);
    setModeButtons("controller");
    setRunState("Kurs übernommen – Simulation ist bereit");
  } catch (error) {
    showError(error);
  }
}

function updateSliderValue(name, digits) {
  elements[`${name}-value`].textContent = Number(elements[name].value).toFixed(digits);
}

for (const [name, digits] of [["width", 1], ["height", 1], ["curves", 2]]) {
  elements[name].addEventListener("input", () => updateSliderValue(name, digits));
}

elements["apply-track"].addEventListener("click", resetTrack);
elements["manual-mode"].addEventListener("click", () => changeMode("manual"));
elements["controller-mode"].addEventListener("click", () => changeMode("controller"));
elements.start.addEventListener("click", startSimulation);
elements.pause.addEventListener("click", pauseSimulation);

window.addEventListener("keydown", (event) => {
  const key = event.key.toLowerCase();
  if (!manualMode || !running || !["w", "a", "s", "d"].includes(key)) return;
  event.preventDefault();
  if (event.repeat || activeKey === key) return;
  activeKey = key;
  callApi("press_key", key).catch(showError);
});

window.addEventListener("keyup", (event) => {
  if (event.key.toLowerCase() === activeKey) releaseActiveKey();
});

window.addEventListener("blur", releaseActiveKey);
document.addEventListener("visibilitychange", () => {
  if (document.hidden) releaseActiveKey();
});

startRuntime();
