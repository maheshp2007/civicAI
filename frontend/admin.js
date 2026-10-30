// LOAD COMPLAINTS
async function loadComplaints() {
    try {
        const response = await fetch("/api/complaints");
        const complaints = await response.json();

        const table = document.getElementById("complaintTable");
        table.innerHTML = "";

        // Dashboard statistics
        document.getElementById("total").textContent = complaints.length;

        document.getElementById("pending").textContent =
            complaints.filter(c => c.status === "Pending").length;

        document.getElementById("high").textContent =
            complaints.filter(c => c.priority === "High").length;

        document.getElementById("resolved").textContent =
            complaints.filter(c => c.status === "Resolved").length;

        complaints.forEach(complaint => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${complaint.id}</td>
                <td>${complaint.title}</td>
                <td>${complaint.category}</td>
                <td>${complaint.location}</td>
                <td>${complaint.priority}</td>
                <td>${complaint.recommendation || "No recommendation"}</td>
                <td>${complaint.status}</td>
                <td>
                    <select onchange="updateStatus(${complaint.id}, this.value)">
                        <option value="Pending" ${complaint.status === "Pending" ? "selected" : ""}>Pending</option>
                        <option value="In Progress" ${complaint.status === "In Progress" ? "selected" : ""}>In Progress</option>
                        <option value="Resolved" ${complaint.status === "Resolved" ? "selected" : ""}>Resolved</option>
                    </select>
                </td>
            `;

            table.appendChild(row);
        });

    } catch (error) {
        console.error("Error loading complaints:", error);
    }
}


// UPDATE COMPLAINT STATUS
async function updateStatus(id, status) {
    try {
        const response = await fetch(`/api/complaints/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ status: status })
        });

        if (!response.ok) {
            throw new Error("Status update failed");
        }

        alert("Complaint status updated!");
        loadComplaints();

    } catch (error) {
        alert("Unable to update status.");
        console.error(error);
    }
}


// LOAD HOTSPOTS
async function loadHotspots() {
    try {
        const response = await fetch("/api/hotspots");
        const hotspots = await response.json();

        const container = document.getElementById("hotspotList");
        container.innerHTML = "";

        if (hotspots.length === 0) {
            container.textContent = "No complaints reported yet.";
            return;
        }

        hotspots.forEach(item => {
            const card = document.createElement("div");
            card.className = "hotspot-card";

            const heading = document.createElement("h3");
            heading.textContent = "📍 " + item.location;

            const count = document.createElement("p");
            count.textContent = "Total complaints: " + item.complaint_count;

            card.appendChild(heading);
            card.appendChild(count);

            container.appendChild(card);
        });

    } catch (error) {
        console.error("Error loading hotspots:", error);
    }
}


// START DASHBOARD
loadComplaints();
loadHotspots();