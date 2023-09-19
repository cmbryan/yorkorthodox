function navlinkVisibility() {
    var x = document.getElementById("navlinks");
    if (x.style.display === "block") {
        // "" == "none", but prevents the menu from staying hidden if the screen is then resized
        x.style.display = "";
    } else if (x.style.display === "") {
        x.style.display = "block";
    }
}

function getTodaysDate() {
    var currentDate = new Date();

    // Extract the year, month, and day
    var year = currentDate.getFullYear();
    var month = String(currentDate.getMonth() + 1).padStart(2, '0'); // Months are zero-indexed
    var day = String(currentDate.getDate()).padStart(2, '0');

    // Format the date as "YYYY-MM-DD"
    return `${year}-${month}-${day}`;
}

function getData(url, mode, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open(mode, url, true);
    xhr.onload = callback;
    xhr.onload = function () {
        if (xhr.status === 200) {
            var responseData = JSON.parse(xhr.responseText);
            callback(responseData);
        }
    };
    xhr.send();
}

function getRestHost() {
    var is_debug = window.location.host.startsWith("localhost") || window.location.host.startsWith("127.0.0.1");
    var rest_host = is_debug ? "http://localhost:5000" : "https://yorkorthodox-rest-2.onrender.com";
    return rest_host;
}

function setInnerHtmlIfExists(id, content) {
    var element = document.getElementById(id);
    if (element && content !== undefined) {
        element.innerHTML = content;
    }
}

function setLectionary(formattedDate) {
    // Lectionary
    getData(`${getRestHost()}/lectionary?date=${formattedDate}`,
        'GET',
        function (data) {
            var references = data.a_lect_1;
            references += data.a_lect_2 ? `; ${data.a_lect_2}` : "";
            references += data.g_lect ? `; ${data.g_lect}` : "";
            references += data.c_lect_1 ? `<br/><i>For the commemoration:</i> ${data.c_lect_1}` : "";
            references += data.c_lect_2 ? `; ${data.c_lect_2}` : "";
            references += data.x_lect_1 ? `<br/>${data.x_lect_1}` : "";
            references += data.x_lect_2 ? `; ${data.x_lect_2}` : "";

            setInnerHtmlIfExists("daily-date", data.date_str);
            setInnerHtmlIfExists("major-commem", data.desig);
            setInnerHtmlIfExists("daily-lect", references);
            setInnerHtmlIfExists("daily-commem-general", data.general_saints);
            setInnerHtmlIfExists("daily-commem-british", data.british_saints);

            setInnerHtmlIfExists("a_text_1", data.a_text_1);
            setInnerHtmlIfExists("a_text_2", data.a_text_2);
            setInnerHtmlIfExists("g_text", data.g_text);
            setInnerHtmlIfExists("c_text_1", data.c_text_1);
            setInnerHtmlIfExists("c_text_2", data.c_text_2);
            setInnerHtmlIfExists("x_text_1", data.x_text_1);
            setInnerHtmlIfExists("x_text_2", data.x_text_2);
        }
    );

    // Services
    getData(`${getRestHost()}/services?date=${formattedDate}&num_services=5`,
        'GET',
        function (data) {
            content = "";
            for (const service of data) {
                content += "<p>";
                content += `<b>${service.date}</b><br/>`;
                if (service.commemoration) {
                    content += `<i>${service.commemoration}</i><br/>`;
                }
                content += service.description;
                content += "</p>";
            }
            setInnerHtmlIfExists("services", content);
        }
    );
}

// dynamic content
document.addEventListener("DOMContentLoaded", function () {
    // Date Selector
    const dateControl = document.querySelector('input[type="date"]');
    if (dateControl) {
        dateControl.value = getTodaysDate();
    }

    setLectionary(getTodaysDate());
});

function dateSelector(event) {
    setLectionary(event.target.value);
}
