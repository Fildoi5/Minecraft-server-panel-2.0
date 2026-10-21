async function getLogs() {
  const url ="/getLogs";
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const result = await response.text();
    document.getElementById("logs").textContent = result;
  } catch (error) {
    console.error(error.message);
  }
}

document.addEventListener("DOMContentLoaded", async (event) => {
    setInterval(getLogs, 2000);
});