let initVerseRadioBtn = document.querySelectorAll("[id^='verse-']");
let chapterVerseRadioBtn = document.querySelectorAll("[id^='chapter-']");
let concludingVerseRadioBtn = document.querySelectorAll("[id^='exit-']");

let initVerseRadioBtnList = [...initVerseRadioBtn];
let chapterVerseRadioBtnList = [...chapterVerseRadioBtn];
let concludingVerseRadioBtnList = [...concludingVerseRadioBtn];
let verseName;

initVerseRadioBtnList.forEach(node => {
    node.addEventListener('click', () => {
        verseName = node.value;
        node.parentElement.className = "radio-selected";
        console.log(
            `${generateDateTime(new Date())} Sending Function Call to - fetchVerse(${verseName}, introduction)`
        );
        fetchVerse(verseName, "introduction");
    });
});

chapterVerseRadioBtnList.forEach((node) => {
    node.addEventListener("click", () => {
        verseName = node.value;
        node.parentElement.className = "radio-selected";
        console.log(
            `${generateDateTime(new Date())} Sending Function Call to - fetchVerse(${verseName}, chapters)`
        );
        fetchVerse(verseName, "chapters");
    });
});

concludingVerseRadioBtnList.forEach((node) => {
    node.addEventListener("click", () => {
        verseName = node.value;
        node.parentElement.className = "radio-selected";
        console.log(
            `${generateDateTime(new Date())} Sending Function Call to - fetchVerse(${verseName}, conclusion)`
        );
        fetchVerse(verseName, "conclusion");
    });
});



async function fetchVerse(verseName, verseType) {
    
    console.info(`${generateDateTime(new Date())} Call received for '${verseName}'`);
    
    var divHindiVerseContainer = document.getElementById(
        "hindi-text-container"
    );
    var divLatinVerseContainer = document.getElementById(
        "latin-text-container"
    );
    var divMeaningMainContainer = document.getElementById(
        "meaning-text-container"
    );

    Array.from(divHindiVerseContainer.children).forEach((child) => {
        if (!child.classList.contains("verse-title")) {
            divHindiVerseContainer.removeChild(child);
        }
    });

    Array.from(divLatinVerseContainer.children).forEach((child) => {
        if (!child.classList.contains("verse-title")) {
            divLatinVerseContainer.removeChild(child);
        }
    });

    try {
        console.log(`${generateDateTime(new Date())} API call send to Application`);
        const response = await fetch("/fetchVerse", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                verseName: verseName,
                verseType: verseType,
            }),
        });

        var jsonDataResponse = await response.json();
        var container = document.getElementById("verses-container");
        var divHindiShlokaContainer = document.createElement("div");
        var divLatinShlokaContainer = document.createElement("div");
        var divMeaningShlokaContainer = document.createElement("div");

        console.log(`${generateDateTime(new Date())} API response received from Application`);

        jsonDataResponse["dataExtract"].forEach((item) => {
            var pVerseSanskrit = document.createElement("p");
            var pVerseLatin = document.createElement("p");
            // var pMeaning = document.createElement("p");

            if (item["id"] === "") {
                pVerseSanskrit.innerHTML = `<hindi>${item["verseDetails"]["devanagariShloka"]}</hindi>`;
            } else {
                pVerseSanskrit.innerHTML = `<hindi>${item["verseDetails"]["devanagariShloka"]} ${item["verseNo"]} ॥</hindi>`;
            }

            pVerseLatin.innerHTML = item["verseDetails"]["translationIAST"];
            // pMeaning.innerHTML = item["meanings"]["englishMeaning"];

            pVerseLatin.className = "latin-text";
            // pMeaning.className = "english-text";

            divHindiShlokaContainer.append(pVerseSanskrit);
            divLatinShlokaContainer.append(pVerseLatin);
            // divMeaningShlokaContainer.append(pMeaning);
        });

        divHindiShlokaContainer.id = "shloka-container-hindi";
        divLatinShlokaContainer.id = "shloka-container-latin";

        divHindiVerseContainer.append(divHindiShlokaContainer);
        divLatinVerseContainer.append(divLatinShlokaContainer);
        // divMeaningMainContainer.append(divMeaningShlokaContainer);

        container.appendChild(divHindiVerseContainer);
        container.appendChild(divLatinVerseContainer);
        // container.appendChild(divMeaningMainContainer);
        console.log(`${generateDateTime(new Date())} Populating HTML page`);
    } catch (error) {
        console.error("Error fetching verse:", error);
    }
}


function generateDateTime(date) {
    // return date.toISOString().replace("T", " ").substring(0, 19);
    const p = new Intl.DateTimeFormat("en", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false,
    })
        .formatToParts(date)
        .reduce((acc, part) => {
            acc[part.type] = part.value;
            return acc;
        }, {});

    return `${p.year}-${p.month}-${p.day} ${p.hour}:${p.minute}:${p.second}`;
}

