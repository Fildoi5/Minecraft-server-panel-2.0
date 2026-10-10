
let data = null;

function changeVersion(event){
    document.getElementById("version").innerHTML = "";
    data["modloader"][document.getElementById("modloader").value].forEach((data2) => {
        console.log(data2["version"]);
        let option = document.createElement("option"); 
        option.textContent = data2["version"];
        option.value = data2["version"];
        document.getElementById("version").appendChild(option);
    });
}

async function getData() {
  const url ="/getData";
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error(error.message);
  }
}



document.addEventListener("DOMContentLoaded", async (event) => {
    data = JSON.parse(await getData());
    data["java"].forEach((data2) => {
        console.log(data2["version"]);
        let option = document.createElement("option"); 
        option.textContent = data2["version"];
        option.value = data2["version"];
        document.getElementById("java").appendChild(option);
    });
    changeVersion();
});

document.getElementById("modloader").addEventListener("change", changeVersion);

async function submit(){
    
    let data = {
        "modloader": document.getElementById("modloader").value,
        "version": document.getElementById("version").value,
        "ram": document.getElementById("ram").value,
        "java": document.getElementById("java").value,
        "name": document.getElementById("name").value,
        "motd": document.getElementById("motd").value,
        "onlinemod": document.getElementById("onlinemod").value,
        "ip": document.getElementById("ip").value

    };

    if ((data["name"] != "") && (data["motd"] != "") && (data["ip"] != "")){
        fetch("/postData", {
            method: "POST",
            body: JSON.stringify(data),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });
        if (document.getElementById("file").files[0] != null){
            fetch("/postIcon", {
                method: "POST",
                body: document.getElementById("file").files[0],
                headers: {"Content-type":document.getElementById("file").files[0].type}
            });
        }
        window.location.replace("/install");
        
    }else{
        alert("Everything must be filled in.");
    }
    
}