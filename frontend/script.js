const form = document.getElementById("complaintForm");

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    const complaint = {
        title: document.getElementById("title").value,
        description: document.getElementById("description").value,
        category: document.getElementById("category").value,
        location: document.getElementById("location").value
    };

    try {

        const response = await fetch("/api/complaints", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(complaint)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Submission failed");
        }

        const ai = result.ai_analysis;

        let duplicateMessage = ai.duplicate
            ? `Possible duplicate of complaint #${ai.duplicate.complaint_id} (${ai.duplicate.similarity}% similarity)`
            : "No likely duplicate detected.";

        alert(
            `Complaint submitted!\n\n` +
            `Complaint ID: ${result.complaint_id}\n\n` +
            `AI SUMMARY:\n${ai.summary}\n\n` +
            `PRIORITY: ${ai.priority}\n\n` +
            `REASON: ${ai.reason}\n\n` +
            `DUPLICATE CHECK:\n${duplicateMessage}`
        );

        form.reset();

    } catch (error) {

        alert("Error: " + error.message);

    }

});