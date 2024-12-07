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
        console.log(`Sending Function Call to - fetchVerse(${verseName}, introduction)`);
        fetchVerse(verseName, "introduction");
    });
});

chapterVerseRadioBtnList.forEach((node) => {
    node.addEventListener("click", () => {
        verseName = node.value;
        node.parentElement.className = "radio-selected";
        console.log(`Sending Function Call to - fetchVerse(${verseName}, chapters)`);
        fetchVerse(verseName, "chapters");
    });
});

concludingVerseRadioBtnList.forEach((node) => {
    node.addEventListener("click", () => {
        verseName = node.value;
        node.parentElement.className = "radio-selected";
        console.log(`Sending Function Call to - fetchVerse(${verseName}, conclusion)`);
        fetchVerse(verseName, "conclusion");
    });
});



async function fetchVerse(verseName, verseType) {
    console.info(`Call received for '${verseName}'`);
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

        jsonDataResponse.forEach((item) => {
            var pVerseSanskrit = document.createElement("p");
            var pVerseLatin = document.createElement("p");
            var pMeaning = document.createElement("p");

            if (item["id"] === "") {
                pVerseSanskrit.innerHTML = `<hindi>${item["devanagariShloka"]}</hindi>`;
            } else {
                pVerseSanskrit.innerHTML = `<hindi>${item["devanagariShloka"]} ${item["verseNo"]} ॥</hindi>`;
            }
            
            pVerseLatin.innerHTML = item["latinTranslation"];
            pMeaning.innerHTML = item["meanings"]["englishMeaning"];
            
            pVerseLatin.className = "latin-text";
            pMeaning.className = "english-text";
            
            divHindiShlokaContainer.append(pVerseSanskrit);
            divLatinShlokaContainer.append(pVerseLatin);
            divMeaningShlokaContainer.append(pMeaning);
        });

        divHindiShlokaContainer.id = "shloka-container-hindi";
        divLatinShlokaContainer.id = "shloka-container-latin";

        divHindiVerseContainer.append(divHindiShlokaContainer);
        divLatinVerseContainer.append(divLatinShlokaContainer);
        divMeaningMainContainer.append(divMeaningShlokaContainer);

        container.appendChild(divHindiVerseContainer);
        container.appendChild(divLatinVerseContainer);
        container.appendChild(divMeaningMainContainer);
    } catch (error) {
        console.error("Error fetching verse:", error);
    }
}
