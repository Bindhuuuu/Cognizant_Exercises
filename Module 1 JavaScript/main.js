
// Task 1 - JavaScript Basics
console.log("Welcome to the Community Portal");

window.onload = function () {

    alert("Welcome to the Community Portal");

    displayEventInfo();

    displayAvailableEvents();

};


// Task 2 - Syntax, Data Types


const eventName = "Yoga Camp";
const eventDate = "10 July 2026";

let availableSeats = 50;

function displayEventInfo() {

    document.getElementById("eventDetails").innerHTML =
        `Event : ${eventName}<br>Date : ${eventDate}`;

    document.getElementById("seatCount").innerHTML =
        `Available Seats : ${availableSeats}`;
}


document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("registerBtn").onclick = function () {

        try {

            if (availableSeats > 0) {

                availableSeats--;

                document.getElementById("seatCount").innerHTML =
                    `Available Seats : ${availableSeats}`;

                alert("Registration Successful!");

            } else {

                throw "No Seats Available!";

            }

        } catch (error) {

            alert(error);

        }

    };

});


// Task 3 - Conditionals, Loops


const eventList = [

    {
        name: "Yoga Camp",
        seats: 20,
        upcoming: true
    },

    {
        name: "Book Fair",
        seats: 0,
        upcoming: true
    },

    {
        name: "Food Festival",
        seats: 30,
        upcoming: true
    },

    {
        name: "Old Marathon",
        seats: 25,
        upcoming: false
    }

];


function displayAvailableEvents() {

    let output = "";

    eventList.forEach(function (event) {

        if (event.upcoming && event.seats > 0) {

            output += `
                <div class="eventCard">
                    <h3>${event.name}</h3>
                    <p>Seats Available : ${event.seats}</p>
                </div>
            `;

        }

    });

    document.getElementById("eventList").innerHTML = output;

}




// Task 4 - Functions, Scope & Closures


let communityEvents = [

    {
        name: "Yoga Camp",
        category: "Health"
    },

    {
        name: "Music Night",
        category: "Music"
    },

    {
        name: "Book Fair",
        category: "Education"
    }

];



function addEvent() {

    communityEvents.push({

        name: "Food Festival",

        category: "Food"

    });

    document.getElementById("task4Output").innerHTML =
        "Food Festival Added Successfully.";

}



function registrationCounter() {

    let total = 0;

    return function () {

        total++;

        return total;

    };

}

const yogaCounter = registrationCounter();



function registerUser(category) {

    let count = yogaCounter();

    document.getElementById("task4Output").innerHTML =

        "Registered for " + category +

        "<br>Total Registrations : " + count;

}



function filterEventsByCategory(category, callback) {

    let filtered = communityEvents.filter(function (event) {

        return event.category === category;

    });

    callback(filtered);

}



function displayFilteredEvents(filteredEvents) {

    let output = "";

    filteredEvents.forEach(function (event) {

        output += event.name + "<br>";

    });

    document.getElementById("task4Output").innerHTML = output;

}



function showMusicEvents() {

    filterEventsByCategory(

        "Music",

        displayFilteredEvents

    );

}

// Task 5 - Objects and Prototypes

function Event(name, date, seats) {

    this.name = name;
    this.date = date;
    this.seats = seats;

}



Event.prototype.checkAvailability = function () {

    if (this.seats > 0) {

        return "Seats Available";

    }

    return "Event Full";

};



const yogaEvent = new Event(

    "Yoga Camp",

    "10 July 2026",

    25

);



function showEventObject() {

    document.getElementById("task5Output").innerHTML =

        "<b>Event :</b> " + yogaEvent.name +

        "<br><b>Date :</b> " + yogaEvent.date +

        "<br><b>Seats :</b> " + yogaEvent.seats +

        "<br><b>Status :</b> " +

        yogaEvent.checkAvailability();

}



function showKeysValues() {

    let output = "";

    Object.entries(yogaEvent).forEach(function (item) {

        output += item[0] + " : " + item[1] + "<br>";

    });

    document.getElementById("task5Output").innerHTML = output;

}

// Task 6 - Arrays and Methods


let allEvents = [

    {
        name: "Yoga Camp",
        category: "Health"
    },

    {
        name: "Music Night",
        category: "Music"
    },

    {
        name: "Book Fair",
        category: "Education"
    }

];


// push()

function addNewEvent() {

    allEvents.push({

        name: "Dance Workshop",

        category: "Music"

    });

    document.getElementById("task6Output").innerHTML =
        "Dance Workshop Added Successfully.";

}



// filter()

function showMusicOnly() {

    let musicEvents = allEvents.filter(function(event){

        return event.category === "Music";

    });

    let output = "";

    musicEvents.forEach(function(event){

        output += event.name + "<br>";

    });

    document.getElementById("task6Output").innerHTML = output;

}



// map()

function showFormattedEvents() {

    let formatted = allEvents.map(function(event){

        return "Workshop on " + event.name;

    });

    document.getElementById("task6Output").innerHTML =
        formatted.join("<br>");

}

// Task 7 - DOM Manipulation

let registered = false;

// Display Event Cards

function showEventCards() {

    const container = document.querySelector("#domEvents");

    container.innerHTML = "";

    let eventNames = [

        "Yoga Camp",

        "Food Festival",

        "Book Fair"

    ];

    eventNames.forEach(function(event) {

        let card = document.createElement("div");

        card.className = "eventCard";

        card.innerHTML =

            "<h3>" + event + "</h3>" +

            "<p>Seats Available</p>";

        container.appendChild(card);

    });

}

// Task 8 - Event Handling


const eventData = [

    {
        name: "Yoga Camp",
        category: "Health"
    },

    {
        name: "Music Night",
        category: "Music"
    },

    {
        name: "Book Fair",
        category: "Education"
    }

];


// onclick

function registerNow() {

    document.getElementById("task8Output").innerHTML =

        "<span style='color:green;'>Registration Successful!</span>";

}


// onchange

function filterCategory() {

    let category = document.getElementById("categorySelect").value;

    let output = "";

    eventData.forEach(function(event){

        if(category === "All" || event.category === category){

            output += event.name + "<br>";

        }

    });

    document.getElementById("task8Output").innerHTML = output;

}


// keydown

function searchEvent() {

    let search = document.getElementById("searchBox").value.toLowerCase();

    let output = "";

    eventData.forEach(function(event){

        if(event.name.toLowerCase().includes(search)){

            output += event.name + "<br>";

        }

    });

    document.getElementById("task8Output").innerHTML = output;

}


// Register

function registerEventDOM() {

    registered = true;

    document.querySelector("#domEvents").innerHTML +=

        "<p style='color:green;'><b>Registration Successful!</b></p>";

}


// Cancel

function cancelRegistration() {

    registered = false;

    document.querySelector("#domEvents").innerHTML +=

        "<p style='color:red;'><b>Registration Cancelled!</b></p>";

}

// Task 9 - Async JavaScript


// Mock API

const apiURL = "https://jsonplaceholder.typicode.com/users";


// Using .then() and .catch()

function loadEvents() {

    document.getElementById("loading").innerHTML = "Loading...";

    fetch(apiURL)

        .then(function(response){

            return response.json();

        })

        .then(function(data){

            let output = "";

            data.slice(0,5).forEach(function(event){

                output += event.name + "<br>";

            });

            document.getElementById("loading").innerHTML = "";

            document.getElementById("task9Output").innerHTML = output;

        })

        .catch(function(error){

            document.getElementById("loading").innerHTML =

                "Failed to load events.";

        });

}



// Using async / await

async function loadEventsAsync() {

    document.getElementById("loading").innerHTML = "Loading...";

    try{

        let response = await fetch(apiURL);

        let data = await response.json();

        let output = "";

        data.slice(0,5).forEach(function(event){

            output += event.name + "<br>";

        });

        document.getElementById("loading").innerHTML = "";

        document.getElementById("task9Output").innerHTML = output;

    }

    catch(error){

        document.getElementById("loading").innerHTML =

            "Failed to load events.";

    }

}

// Task 10 - Modern JavaScript Features


// Event List

const modernEvents = [

    {
        name: "Yoga Camp",
        category: "Health",
        seats: 20
    },

    {
        name: "Music Night",
        category: "Music",
        seats: 30
    },

    {
        name: "Book Fair",
        category: "Education",
        seats: 15
    }

];

// Default Parameter

function welcomeUser(user = "Guest") {

    return "Welcome " + user;

}

// Show Event Details

function showEventDetails() {

    const { name, category, seats } = modernEvents[0];

    document.getElementById("task10Output").innerHTML =

        welcomeUser() +

        "<br><br><b>Event :</b> " + name +

        "<br><b>Category :</b> " + category +

        "<br><b>Seats :</b> " + seats;

}

// Clone Event List

function cloneEventList() {

    const copiedEvents = [...modernEvents];

    let output = "<b>Cloned Events</b><br><br>";

    copiedEvents.forEach(function(event){

        output += event.name + "<br>";

    });

    document.getElementById("task10Output").innerHTML = output;

}

// Task 11 - Working with Forms


document
.getElementById("registrationForm")
.addEventListener("submit", registerForm);

function registerForm(event){

    event.preventDefault();

    // Clear old messages

    document.getElementById("nameError").innerHTML = "";

    document.getElementById("emailError").innerHTML = "";

    document.getElementById("eventError").innerHTML = "";

    document.getElementById("task11Output").innerHTML = "";

    const form = event.target;

    const username = form.elements["username"].value.trim();

    const email = form.elements["email"].value.trim();

    const eventName = form.elements["eventName"].value;

    let valid = true;

    // Name Validation

    if(username === ""){

        document.getElementById("nameError").innerHTML =
        "Name is required";

        valid = false;

    }

    // Email Validation

    if(email === ""){

        document.getElementById("emailError").innerHTML =
        "Email is required";

        valid = false;

    }

    // Event Validation

    if(eventName === ""){

        document.getElementById("eventError").innerHTML =
        "Please select an event";

        valid = false;

    }

    if(valid){

        document.getElementById("task11Output").innerHTML =

        "<span style='color:green;'>Registration Successful!</span><br><br>" +

        "<b>Name :</b> " + username +

        "<br><b>Email :</b> " + email +

        "<br><b>Event :</b> " + eventName;

    }

}

// Task 12 - AJAX & Fetch API


function submitRegistration() {

    document.getElementById("task12Output").innerHTML =
        "Submitting Registration...";

    // Simulate delay

    setTimeout(function () {

        fetch("https://jsonplaceholder.typicode.com/posts", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                name: "Rahul",

                email: "rahul@gmail.com",

                event: "Yoga Camp"

            })

        })

        .then(function(response){

            return response.json();

        })

        .then(function(data){

            document.getElementById("task12Output").innerHTML =

                "<span style='color:green;'>Registration Submitted Successfully!</span><br><br>" +

                "Registration ID : " + data.id;

        })

        .catch(function(){

            document.getElementById("task12Output").innerHTML =

                "<span style='color:red;'>Submission Failed!</span>";

        });

    }, 2000);

}

// Task 13 - Debugging and Testing


function debugRegistration() {

    console.log("Registration Started");

    let userName = "Rahul";
    let eventName = "Yoga Camp";

    console.log("User Name:", userName);
    console.log("Event:", eventName);

    // Pause execution here
    debugger;

    console.log("Registration Successful");

    document.getElementById("task13Output").innerHTML =

        "<span style='color:green;'>Check the Console for Debug Messages.</span>";

}
// Task 14 - jQuery


$(document).ready(function () {

    // Register Button

    $("#registerBtnJQ").click(function () {

        alert("Registered Successfully using jQuery!");

    });

    // Fade Out

    $("#hideCard").click(function () {

        $("#jqCard").fadeOut();

    });

    // Fade In

    $("#showCard").click(function () {

        $("#jqCard").fadeIn();

    });

});