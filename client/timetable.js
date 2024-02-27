const params = new URLSearchParams(window.location.search);
const encodedData = params.get("data");
const breakPeriod = 6;

function hideSpinner() {
    document.getElementsByClassName("spinner-backdrop")[0].classList.add("hidden")
}

fetch(`http://127.0.0.1:5000/get-timetable?data=${encodedData}`)
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log(data);
        hideSpinner();
        for (const [courseName, schedules] of Object.entries(data.data)) {
            for (const schedule of schedules) {
                const dayRow =
                    document.getElementsByTagName("tbody")[0].children[
                        4 + schedule[0]
                    ];
                const day = dayRow.children[1 + ((schedule[1] >= breakPeriod && schedule[0] != 0) ? schedule[1] - 1 : schedule[1])];
                day.textContent = courseName;

            }
        }
    }).catch((error) => {
		// console.log(error)
        hideSpinner();
        document.getElementsByClassName("error")[0].classList.remove("hidden");
	});
