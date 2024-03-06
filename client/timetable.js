const params = new URLSearchParams(window.location.search);
const encodedData = params.get("data");
const breakPeriod = 6;

const table = document.getElementById("table");
const baseTable = table.outerHTML;

function hideSpinner() {
    document
        .getElementsByClassName("spinner-backdrop")[0]
        .classList.add("hidden");
}

const regenerateButton = document.getElementById("regenerate");
regenerateButton.addEventListener("click", (ev) => {
    generateTimetable();
});

function resetTimetable() {
    const currentTable = document.getElementById("table");
    currentTable.outerHTML = baseTable;
}

function generateTimetable() {
    resetTimetable();

    fetch(`/api/get-timetable?data=${encodedData}`)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log(data);
            hideSpinner();
            document.getElementsByClassName("error")[0].classList.add("hidden");
            for (const [courseName, schedules] of Object.entries(data.data)) {
                for (const schedule of schedules) {
                    const dayRow =
                        document.getElementsByTagName("tbody")[0].children[
                            4 + schedule[0]
                        ];
                    const day =
                        dayRow.children[
                            1 +
                                (schedule[1] >= breakPeriod && schedule[0] != 0
                                    ? schedule[1] - 1
                                    : schedule[1])
                        ];
                    day.textContent = courseName;
                }
            }
        })
        .catch((error) => {
            console.log(error);
            hideSpinner();
            document.getElementsByClassName("error")[0].classList.remove("hidden");
        });
}

generateTimetable();