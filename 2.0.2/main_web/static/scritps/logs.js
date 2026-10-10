async function getLogs() {
  const url ="/get_logs";
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

async function post_command(){
    const command = document.getElementById("command");
    console.log(command.value);

    fetch("/postWrite", {
            method: "POST",
            body: command.value,
            headers: {"Content-type": "application/text; charset=UTF-8"}
        });
}

document.getElementById("send").addEventListener("click", async (event) => {
    await post_command();
});

document.addEventListener("DOMContentLoaded", async (event) => {
    setInterval(getLogs, 2000);
});