const form = document.getElementById("complaintForm");

form.addEventListener("submit", async function(event) {

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

        alert(
            result.message +
            "\nComplaint ID: " + result.complaint_id
        );

        form.reset();

    } catch (error) {

        alert("Error: " + error.message);

    }

});