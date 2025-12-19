// This gets replaced by GitHub Actions
const BACKEND_URL = "";

const btn = document.getElementById("btn");
const output = document.getElementById("output");

btn.onclick = async () => {
  try {
    const res = await fetch(`${BACKEND_URL}/api/hello`);
    const data = await res.json();
    output.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    output.textContent = "Error: " + err;
  }
};