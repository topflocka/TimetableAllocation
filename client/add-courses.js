let courseNames = [];

function closeModal() {
    const modal = document.getElementById("add-course-modal");
    modal.classList.add("hidden");
    const inputField = document.querySelector("#course-field");
    inputField.value = "";
}

const cancelButton = document.getElementsByClassName("cancel-btn")[0];
cancelButton.addEventListener("click", function () {
    const invalid = document.querySelector(".invalid");
    invalid.classList.add("hidden");
    closeModal();
});

const openModalBtn = document.getElementsByClassName("open-modal")[0];
openModalBtn.addEventListener("click", function () {
    const modal = document.getElementById("add-course-modal");
    modal.classList.remove("hidden");
    modal.getElementsByTagName("input")[0].focus()
});

const addCourseBtn = document.getElementsByClassName("add-course-btn")[0];
addCourseBtn.addEventListener("click", function () {
    const inputField = document.querySelector("#course-field");
    console.log(inputField.value);
    if (!inputField.value.match(/\w{3}\d{3}/i)) {
        const invalid = document.querySelector(".invalid");
        invalid.classList.remove("hidden");
    } else {
        const invalid = document.querySelector(".invalid");
        invalid.classList.add("hidden");
        addCourse(inputField.value.toUpperCase());
        closeModal();
    }
});

const courseListButton = document.getElementById("courselist");
courseListButton.addEventListener("change", function (e) {
    // Get the selected file
    const file = e.target.files[0];

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

const courses = document.getElementById("courses");
function addCourse(courseName) {
    const emptyPlaceholder = document.getElementById("empty-courses");
    emptyPlaceholder.classList.add("hidden");
    courseNames.push(courseName);
    // const paragraph = document.createElement("p");
    // paragraph.innerText = courseName;
    // const iconPath = document.createElementNS(
    //     'http://www.w3.org/2000/svg',
    //     './close-outline.svg'
    //   );

    // courses.appendChild(paragraph);
    courses.innerHTML += `
    <div class="course">
            <p>${courseName}</p>
            <svg xmlns="http://www.w3.org/2000/svg" class="delete" viewBox="0 0 512 512"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32" d="M368 368L144 144M368 144L144 368"/></svg>
    </div>`;
}

function displayCourses(courses) {
    const coursesNode = document.getElementById("courses");
    coursesNode.innerHTML = "";
    courseNames = [];

    for (const course of courses) {
        addCourse(course);
    }
}

courses.addEventListener("click", function (ev) {
    if (ev.target.classList.contains("delete")) {
        const courseName = ev.target.previousElementSibling.textContent;
        courseNames = courseNames.filter((item) => {
            console.log(item);
            return item != courseName;
        });
        ev.target.closest(".course").remove();
        if (!courseNames.length) {
            const emptyPlaceholder = document.getElementById("empty-courses");
            emptyPlaceholder.classList.remove("hidden");
        }
    }
});

const nextPageButton = document.getElementById("next-page");
nextPageButton.addEventListener("click", function (e) {
    const encodedData = encodeURIComponent(JSON.stringify(courseNames));
    console.log(courseNames);
    console.log(encodedData);
    window.location.href = `/client/timetable.html?data=${encodedData}`;
});
