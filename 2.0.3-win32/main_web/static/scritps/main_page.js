async function post_power(){
    const status = document.getElementById("status");
    let data = "OFFLINE";

    if (status.textContent == "OFFLINE"){
        data = "ONLINE";
    }else if(status.textContent == "ONLINE"){
        data = "OFFLINE"
    }

    fetch("/postPower", {
            method: "POST",
            body: data,
            headers: {"Content-type": "application/text; charset=UTF-8"}
        });
    get_data();
}

async function get_data(){
    const response = await fetch("/get_data");

    const result = await response.json();

    const status = document.getElementById("status");
    status.textContent = result["status"];

    const ram = document.getElementById("ram");
    ram.textContent = result["ram"];

    const cpu = document.getElementById("cpu");
    cpu.textContent = result["cpu"];

}

document.addEventListener("DOMContentLoaded", async (event) => {
    setInterval(get_data, 2000);
});