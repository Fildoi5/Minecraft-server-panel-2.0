document.addEventListener("DOMContentLoaded",  async (event) => {
    const request = await fetch("/get_time");
    let j = await request.json();

    document.getElementById("start-monday").value = j["startup"]["Monday"];
    document.getElementById("start-tuesday").value = j["startup"]["Tuesday"];
    document.getElementById("start-wednesday").value = j["startup"]["Wednesday"];
    document.getElementById("start-thursday").value = j["startup"]["Thursday"];
    document.getElementById("start-friday").value = j["startup"]["Friday"];
    document.getElementById("start-saturday").value = j["startup"]["Saturday"];
    document.getElementById("start-sunday").value = j["startup"]["Sunday"];

    document.getElementById("stop-monday").value = j["shutdown"]["Monday"];
    document.getElementById("stop-tuesday").value = j["shutdown"]["Tuesday"];
    document.getElementById("stop-wednesday").value = j["shutdown"]["Wednesday"];
    document.getElementById("stop-thursday").value = j["shutdown"]["Thursday"];
    document.getElementById("stop-friday").value = j["shutdown"]["Friday"];
    document.getElementById("stop-saturday").value = j["shutdown"]["Saturday"];
    document.getElementById("stop-sunday").value = j["shutdown"]["Sunday"];

});

function send(){
    const dic = {
                "startup": {
                    "Monday": document.getElementById("start-monday").value ,
                    "Tuesday": document.getElementById("start-tuesday").value ,
                    "Wednesday": document.getElementById("start-wednesday").value ,
                    "Thursday": document.getElementById("start-thursday").value ,
                    "Friday": document.getElementById("start-friday").value ,
                    "Saturday": document.getElementById("start-saturday").value ,
                    "Sunday": document.getElementById("start-sunday").value},

                "shutdown": {
                    "Monday": document.getElementById("stop-monday").value ,
                    "Tuesday": document.getElementById("stop-tuesday").value ,
                    "Wednesday": document.getElementById("stop-wednesday").value ,
                    "Thursday": document.getElementById("stop-thursday").value ,
                    "Friday": document.getElementById("stop-friday").value ,
                    "Saturday": document.getElementById("stop-saturday").value ,
                    "Sunday": document.getElementById("stop-sunday").value}
            };
    console.log(dic);
    fetch("/postTime", {
            method: "POST",
            body: JSON.stringify(dic),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });
}