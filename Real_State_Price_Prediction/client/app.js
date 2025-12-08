function getBHKValue() {
    let options = document.getElementsByName("uiBHK");
    for (let i = 0; i < options.length; i++) {
        if (options[i].checked) return parseInt(options[i].value);
    }
    return -1;
}

function getBathValue() {
    let options = document.getElementsByName("uiBathrooms");
    for (let i = 0; i < options.length; i++) {
        if (options[i].checked) return parseInt(options[i].value);
    }
    return -1;
}

function showSpinner(show) {
    const spinner = document.getElementById("loadingSpinner");
    spinner.style.display = show ? "block" : "none";
}

function onClickedEstimatePrice() {
    const sqft = document.getElementById("uiSqft").value;
    const bhk = getBHKValue();
    const bath = getBathValue();
    const location = document.getElementById("uiLocations").value;
    const resultBox = document.getElementById("uiEstimatedPrice");

    if (!sqft || isNaN(sqft)) {
        alert("Please enter valid square feet.");
        return;
    }
    if (!location) {
        alert("Please select a location!");
        return;
    }

    showSpinner(true);
    resultBox.style.display = "none";

    $.post(
        "http://127.0.0.1:5000/predict_home_price",
        {
            total_sqft: parseFloat(sqft),
            bhk: bhk,
            bath: bath,
            location: location,
        },
        function (data) {
            showSpinner(false);
            resultBox.innerHTML = `<h2>${data.estimated_price} Lakh</h2>`;
            resultBox.style.display = "block";
        }
    ).fail(function () {
        showSpinner(false);
        alert("❌ API Error: Flask server not running?");
    });
}

function onPageLoad() {
    $.get("http://127.0.0.1:5000/get_location_names", function (data) {
        let locations = data.locations;
        let uiLocations = document.getElementById("uiLocations");

        uiLocations.innerHTML = "";

        locations.forEach(loc => {
            let option = new Option(loc, loc);
            uiLocations.appendChild(option);
        });

    }).fail(function () {
        alert("❌ Cannot fetch locations. Start Flask server!");
    });
}

window.onload = onPageLoad;
