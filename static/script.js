const inputText = document.getElementById("inputText");
const outputText = document.getElementById("outputText");

const humanizeBtn = document.getElementById("humanizeBtn");
const clearBtn = document.getElementById("clearBtn");
const copyBtn = document.getElementById("copyBtn");
const checkBtn = document.getElementById("checkBtn");

const tone = document.getElementById("tone");

const wordCount = document.getElementById("wordCount");
const charCount = document.getElementById("charCount");
const outputWordCount = document.getElementById("outputWordCount");
const status = document.getElementById("status");

const MAX_WORDS = 1000;


/* =========================
   WORD COUNTER
========================= */

function countWords(text) {

    const cleaned = text.trim();

    if (!cleaned) {
        return 0;
    }

    return cleaned.split(/\s+/).length;
}


/* =========================
   INPUT STATISTICS
========================= */

function updateInputStats() {

    const words = countWords(inputText.value);

    wordCount.textContent =
        `${words} / ${MAX_WORDS} words`;

    charCount.textContent =
        `${inputText.value.length} characters`;


    if (words > MAX_WORDS) {

        wordCount.style.color = "#d93025";

        humanizeBtn.disabled = true;

        if (checkBtn) {
            checkBtn.disabled = true;
        }

        status.textContent =
            "Text is too long";

    } else {

        wordCount.style.color = "";

        humanizeBtn.disabled = false;

        if (checkBtn) {
            checkBtn.disabled = false;
        }

        if (
            !humanizeBtn.textContent.includes("Humanizing") &&
            !checkBtn?.textContent.includes("Checking")
        ) {
            status.textContent = "Ready";
        }
    }
}


/* =========================
   OUTPUT STATISTICS
========================= */

function updateOutputStats() {

    const words = countWords(outputText.value);

    outputWordCount.textContent =
        `${words} words`;
}


/* =========================
   INPUT LISTENER
========================= */

inputText.addEventListener(
    "input",
    updateInputStats
);


/* =========================
   HUMANIZE
========================= */

humanizeBtn.addEventListener(
    "click",
    async function () {

        const text =
            inputText.value.trim();

        const words =
            countWords(text);


        if (!text) {

            alert(
                "Please paste some text first."
            );

            return;
        }


        if (words > MAX_WORDS) {

            alert(
                `Your text contains ${words} words. ` +
                `The maximum allowed is ${MAX_WORDS} words.`
            );

            return;
        }


        humanizeBtn.disabled = true;

        if (checkBtn) {
            checkBtn.disabled = true;
        }

        humanizeBtn.textContent =
            "Humanizing...";

        status.textContent =
            "AI is processing your text...";


        try {

            const response =
                await fetch(
                    "/humanize",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            text: text,
                            tone: tone.value
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                throw new Error(
                    data.message ||
                    "Humanization failed."
                );
            }


            outputText.value =
                data.result.trim();

            updateOutputStats();

            status.textContent =
                "Completed";


        } catch (error) {

            console.error(
                "Humanization error:",
                error
            );

            status.textContent =
                "Error";

            alert(
                error.message ||
                "Something went wrong."
            );

        } finally {

            humanizeBtn.textContent =
                "Humanize Text";

            updateInputStats();
        }

    }
);


/* =========================
   AI CHECK
========================= */

if (checkBtn) {

    checkBtn.addEventListener(
        "click",
        async function () {

            const text =
                inputText.value.trim();

            const words =
                countWords(text);


            if (!text) {

                alert(
                    "Please enter some text first."
                );

                return;
            }


            if (words > MAX_WORDS) {

                alert(
                    `Your text contains ${words} words. ` +
                    `The maximum allowed is ${MAX_WORDS} words.`
                );

                return;
            }


            checkBtn.disabled = true;

            humanizeBtn.disabled = true;

            checkBtn.textContent =
                "Checking...";

            status.textContent =
                "Analyzing text...";


            try {

                const response =
                    await fetch(
                        "/check",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                text: text
                            })
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok || !data.success) {

                    throw new Error(
                        data.message ||
                        "AI Check failed."
                    );
                }


                /* =========================
                   UPDATE AI CHECK UI
                ========================= */

                const analysisSection =
                    document.getElementById(
                        "analysisSection"
                    );

                const aiScore =
                    document.getElementById(
                        "aiScore"
                    );

                const humanScore =
                    document.getElementById(
                        "humanScore"
                    );

                const aiAnalysis =
                    document.getElementById(
                        "aiAnalysis"
                    );


                if (aiScore) {

                    aiScore.textContent =
                        `${data.ai_score}%`;
                }


                if (humanScore) {

                    humanScore.textContent =
                        `${data.human_score}%`;
                }


                if (aiAnalysis) {

                    aiAnalysis.textContent =
                        data.analysis;
                }


                /* =========================
                   SHOW ANALYSIS
                ========================= */

                if (analysisSection) {

                    analysisSection.classList.remove(
                        "hidden"
                    );

                    analysisSection.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                }


                status.textContent =
                    "Check completed";


            } catch (error) {

                console.error(
                    "AI Check error:",
                    error
                );

                status.textContent =
                    "Error";

                alert(
                    error.message ||
                    "AI Check failed."
                );

            } finally {

                checkBtn.disabled = false;

                checkBtn.textContent =
                    "Check AI";

                updateInputStats();
            }

        }
    );

}


/* =========================
   CLEAR
========================= */

clearBtn.addEventListener(
    "click",
    function () {

        inputText.value = "";

        outputText.value = "";

        updateInputStats();

        updateOutputStats();

        status.textContent =
            "Ready";


        /* Hide old AI result */

        const analysisSection =
            document.getElementById(
                "analysisSection"
            );

        if (analysisSection) {

            analysisSection.classList.add(
                "hidden"
            );
        }

    }
);


/* =========================
   COPY
========================= */

copyBtn.addEventListener(
    "click",
    async function () {

        const text =
            outputText.value.trim();


        if (!text) {

            alert(
                "There is no humanized text to copy."
            );

            return;
        }


        try {

            await navigator.clipboard.writeText(
                text
            );

            copyBtn.textContent =
                "Copied!";


            setTimeout(
                function () {

                    copyBtn.textContent =
                        "Copy";

                },
                1500
            );


        } catch (error) {

            console.error(
                "Copy error:",
                error
            );

            alert(
                "Could not copy the text."
            );
        }

    }
);


/* =========================
   INITIALIZE
========================= */

updateInputStats();

updateOutputStats();