function navlinkVisibility() {
    var x = document.getElementById("navlinks");
    if (x.style.display === "block") {
        // "" == "none", but prevents the menu from staying hidden if the screen is then resized
        x.style.display = "";
    } else if (x.style.display === "") {
        x.style.display = "block";
    }
}

// daily readings
$(function() {
    $("#datepicker").datepicker({
        dateFormat: "yy-mm-dd",
        showOn: "both",
        buttonImageOnly: true,
        buttonImage: "calendar.svg",
        onSelect: function(date) {
            getLection(new Date(date));
        },
    }).datepicker("setDate", "0"); // initialize to today
});

var currDate;

function getLectionOffset(increment) {
    currDate.setDate(currDate.getDate() + increment);
    getLection(currDate);
}

function getLection(date) {
    currDate = date;
    dateStr = currDate.toISOString().slice(0, 10);
    fetch("/rest/daily/" + dateStr, {
            method: "GET",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json"
            }
        })
        .then(res => res.json())
        .then(data => {
            const day_json = data[0]
            document.getElementById("lection-date").innerHTML = day_json['date_str']
                // document.getElementById("lection-tone").innerHTML = day_json['tone']
                // document.getElementById("lection-desig-a").innerHTML = day_json['desig_a']
            document.getElementById("lection-general-commem").innerHTML = day_json['general_commem']
                // document.getElementById("lection-british-commem").innerHTML = day_json['british_commem']
                // ordering?
                // todo bold the readings for liturgy
            titles = [day_json['a_lect_1']]
            document.getElementById('lection-a1').innerHTML = day_json['a_text_1']

            if (day_json['a_lect_2']) {
                titles.push(day_json['a_lect_2'])
                document.getElementById('lection-a2').innerHTML = day_json['a_text_2']
            }
            titles.push(day_json['g_lect'])
            document.getElementById('lection-g').innerHTML = day_json['g_text']
            if (day_json['x_lect_1']) {
                titles.push(day_json['x_lect_1'])
            }
            if (day_json['x_lect_2']) {
                titles.push(day_json['x_lect_2'])
            }
            if (day_json['c_lect_1']) {
                titles.push(day_json['c_lect_1'])
            }
            if (day_json['c_lect_2']) {
                titles.push(day_json['c_lect_2'])
            }
            document.getElementById("lection-titles").innerHTML = titles.join("; ")
                // better?
                // document.querySelector(
                //     ".result"
                // ).innerText = `The sum is: ${result}`;
        })
        .catch(err => console.log(err));
}
