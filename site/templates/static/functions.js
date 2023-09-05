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

function setInnerHtmlIfExists(id, content) {
    var element = document.getElementById(id);
    if (element) {
        element.innerHTML = content;
    }
}


// dynamic content
document.addEventListener("DOMContentLoaded", function () {
    var is_debug = window.location.host.startsWith("localhost") || window.location.host.startsWith("127.0.0.1");
    is_debug = false;
    var rest_host = is_debug ? "http://localhost:5000" : "https://yorkorthodox-rest.onrender.com";

    var formattedDate = getTodaysDate();

    // Lectionary
    getData(`${rest_host}/lectionary?date=${formattedDate}`,
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
            setInnerHtmlIfExists("major-commem", data.major_commem);
            setInnerHtmlIfExists("daily-lect", references);
            setInnerHtmlIfExists("daily-commem-general", data.general_commem);
            setInnerHtmlIfExists("daily-commem-british", data.british_commem);

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
    getData(`${rest_host}/services?date=${formattedDate}&num_services=5`,
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
});

// $(function() {
//     $("#datepicker").datepicker({
//         dateFormat: "yy-mm-dd",
//         showOn: "both",
//         buttonImageOnly: true,
//         buttonImage: "calendar.svg",
//         onSelect: function(date) {
//             getLection(new Date(date));
//         },
//     }).datepicker("setDate", "0"); // initialize to today
// });

// var currDate;

// function getLectionOffset(increment) {
//     currDate.setDate(currDate.getDate() + increment);
//     getLection(currDate);
// }

// function getLection(date) {
//     currDate = date;
//     dateStr = currDate.toISOString().slice(0, 10);
//     fetch("/rest/daily/" + dateStr, {
//             method: "GET",
//             headers: {
//                 Accept: "application/json",
//                 "Content-Type": "application/json"
//             }
//         })
//         .then(res => res.json())
//         .then(data => {
//             const day_json = data[0]
//             document.getElementById("lection-date").innerHTML = day_json['date_str']
//                 // document.getElementById("lection-tone").innerHTML = day_json['tone']
//                 // document.getElementById("lection-desig-a").innerHTML = day_json['desig_a']
//             document.getElementById("lection-general-commem").innerHTML = day_json['general_commem']
//                 // document.getElementById("lection-british-commem").innerHTML = day_json['british_commem']
//                 // ordering?
//                 // todo bold the readings for liturgy
//             titles = [day_json['a_lect_1']]
//             document.getElementById('lection-a1').innerHTML = day_json['a_text_1']

//             if (day_json['a_lect_2']) {
//                 titles.push(day_json['a_lect_2'])
//                 document.getElementById('lection-a2').innerHTML = day_json['a_text_2']
//             }
//             titles.push(day_json['g_lect'])
//             document.getElementById('lection-g').innerHTML = day_json['g_text']
//             if (day_json['x_lect_1']) {
//                 titles.push(day_json['x_lect_1'])
//             }
//             if (day_json['x_lect_2']) {
//                 titles.push(day_json['x_lect_2'])
//             }
//             if (day_json['c_lect_1']) {
//                 titles.push(day_json['c_lect_1'])
//             }
//             if (day_json['c_lect_2']) {
//                 titles.push(day_json['c_lect_2'])
//             }
//             document.getElementById("lection-titles").innerHTML = titles.join("; ")
//                 // better?
//                 // document.querySelector(
//                 //     ".result"
//                 // ).innerText = `The sum is: ${result}`;
//         })
//         .catch(err => console.log(err));
// }
