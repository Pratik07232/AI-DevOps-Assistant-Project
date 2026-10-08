async function analyzeProblem() {

    const input =
        document.getElementById("errorInput");

    const error = input.value.trim();

    if (!error) {

        alert("Please enter a DevOps problem.");

        return;
    }

    const result =
        document.getElementById("result");

    const resultContent =
        document.getElementById("resultContent");

    result.classList.remove("hidden");

    resultContent.innerHTML =
        "<p>🤖 Analyzing problem...</p>";


    try {

        const response = await fetch(
            "http://localhost:5000/analyze",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    error: error
                })
            }
        );


        const data = await response.json();


        let html = `

            <div class="result-section">

                <h3>🔴 Problem</h3>

                <p>
                    ${data.problem}
                </p>

            </div>

        `;


        html += `

            <div class="result-section">

                <h3>💡 Possible Causes</h3>

                <ul>
        `;


        data.causes.forEach(cause => {

            html += `<li>${cause}</li>`;

        });


        html += `
                </ul>

            </div>
        `;


        html += `

            <div class="result-section">

                <h3>💻 Recommended Commands</h3>
        `;


        data.commands.forEach(command => {

            html += `
                <div class="command">
                    ${command}
                </div>
            `;

        });


        html += `

            </div>

            <div class="result-section">

                <h3>🛠 Solution</h3>

                <div class="solution">
                    ${data.solution}
                </div>

            </div>
        `;


        resultContent.innerHTML = html;


    } catch (error) {

        resultContent.innerHTML = `
            <p>
                ❌ Backend service is unavailable.
            </p>
        `;
    }
}