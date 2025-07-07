let currentValve = "";

function fetchData() {
    fetch("/data")
        .then(res => res.json())
        .then(data => {
            document.getElementById("input-hot").textContent = data.input_temp_hot;
            document.getElementById("input-cold").textContent = data.input_temp_cold;
            document.getElementById("output-temp").textContent = data.output_temp;
            document.getElementById("water-level").textContent = data.water_level;
            document.getElementById("valve-hot").textContent = data.valve_hot;
            document.getElementById("valve-cold").textContent = data.valve_cold;
            document.getElementById("valve-out").textContent = data.valve_out;
        });
}

function openValveModal(valveName) {
    currentValve = valveName;
    const modal = new bootstrap.Modal(document.getElementById("valveModal"));
    modal.show();
}

function saveValve() {
    const value = document.getElementById("valveRange").value;
    fetch("/set_valve", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: currentValve, value: value })
    }).then(() => {
        fetchData();
        bootstrap.Modal.getInstance(document.getElementById("valveModal")).hide();
    });
}

document.getElementById("valveRange").addEventListener("input", e => {
    document.getElementById("valveValue").textContent = e.target.value;
});

setInterval(fetchData, 2000);
fetchData();