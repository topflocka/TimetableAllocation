const course_names = [];

function closeModal() {
    const modal = document.getElementById("add-course-modal");
    modal.classList.add("hidden");
    const inputField = document.querySelector("#course-field");
    inputField.value = "";
}

const cancelButton = document.getElementsByClassName("cancel-btn")[0];
cancelButton.addEventListener("click", function () {
    closeModal();
});

const openModalBtn = document.getElementsByClassName("open-modal")[0];
openModalBtn.addEventListener("click", function () {
    const modal = document.getElementById("add-course-modal");
    modal.classList.remove("hidden");
});

const addCourseBtn = document.getElementsByClassName("add-course-btn")[0];
addCourseBtn.addEventListener("click", function () {
    const inputField = document.querySelector("#course-field");

    addCourse(inputField.value);
    closeModal();

});

const courseListButton = document.getElementById("courselist");
courseListButton.addEventListener("change", function (e) {
    // Get the selected file
    const file = event.target.files[0];

    // Create a new FileReader object
    const reader = new FileReader();

    // Define the onload event handler
    reader.onload = function (event) {
        // Parse the file contents as JSON
        try {
            const json = JSON.parse(event.target.result);
            console.log("Parsed JSON:", json);
            displayCourses(json);
            // Do something with the parsed JSON data
        } catch (error) {
            console.error("Error parsing JSON:", error);
        }
    };

    // Read the file as text
    reader.readAsText(file);
});

function addCourse(courseName) {
    const courses = document.getElementById("courses");
    const paragraph = document.createElement("p");
    paragraph.innerText = courseName;
    course_names.push(courseName);
    courses.appendChild(paragraph);
}

function displayCourses(courses) {
    for (const course of courses) {
        addCourse(course);   
    }
}

const nextPageButton = document.getElementById("next-page");
nextPageButton.addEventListener("click", function (e) {
    const encodedData = encodeURIComponent(JSON.stringify(course_names));
    console.log(course_names);
    console.log(encodedData)
    window.location.href = `timetable.html?data=${encodedData}`
})