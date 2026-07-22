// ===============================
// DOM Elements
// ===============================

const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const uploadBtn = document.getElementById("uploadBtn");
const dropArea = document.getElementById("dropArea");

const progressSection = document.getElementById("progressSection");
const progressBar = document.getElementById("progressBar");

let selectedFile = null;

// ===============================
// Image Preview
// ===============================

imageInput.addEventListener("change", function () {

    if (!this.files.length) return;

    selectedFile = this.files[0];

    preview.src = URL.createObjectURL(selectedFile);

});

// ===============================
// Drag & Drop
// ===============================

dropArea.addEventListener("dragover", (e) => {

    e.preventDefault();

    dropArea.classList.add("dragover");

});

dropArea.addEventListener("dragleave", () => {

    dropArea.classList.remove("dragover");

});

dropArea.addEventListener("drop", (e) => {

    e.preventDefault();

    dropArea.classList.remove("dragover");

    if (!e.dataTransfer.files.length) return;

    selectedFile = e.dataTransfer.files[0];

    imageInput.files = e.dataTransfer.files;

    preview.src = URL.createObjectURL(selectedFile);

});

// ===============================
// Upload
// ===============================

uploadBtn.addEventListener("click", async () => {

    if (!selectedFile) {

        alert("Please choose an image.");
        return;

    }

    uploadBtn.disabled = true;

    uploadBtn.innerHTML =
        '<span class="spinner-border spinner-border-sm"></span> Uploading...';

    progressSection.style.display = "block";

    updateProgress(10);

    const formData = new FormData();

    formData.append("image", selectedFile);

    try {

        const response = await fetch("/api/upload", {

            method: "POST",
            body: formData

        });

        const data = await response.json();

        if (!data.success) {

            alert(data.error);

            resetButton();

            return;

        }

        updateProgress(25);

        pollStatus(data.processing_id);

    }
    catch (err) {

        console.error(err);

        alert("Upload failed.");

        resetButton();

    }

});

// ===============================
// Status Polling
// ===============================

function pollStatus(processingId) {

    uploadBtn.innerHTML =
        '<span class="spinner-border spinner-border-sm"></span> Processing...';

    const interval = setInterval(async () => {

        try {

            const response = await fetch(`/api/status/${processingId}`);

            const data = await response.json();

            if (!data.success) {

                clearInterval(interval);

                alert(data.error);

                resetButton();

                return;

            }

            switch (data.status) {

                case "Pending":

                    updateProgress(35);

                    break;

                case "Processing":

                    updateProgress(70);

                    break;

                case "Completed":

                    updateProgress(100);

                    clearInterval(interval);

                    loadResults(processingId);

                    break;

                case "Failed":

                    clearInterval(interval);

                    alert(data.failure_reason || "Processing Failed");

                    resetButton();

                    break;

            }

        }
        catch (err) {

            clearInterval(interval);

            console.error(err);

            resetButton();

        }

    }, 2000);

}

// ===============================
// Load Results
// ===============================

async function loadResults(processingId) {

    try {

        const response = await fetch(`/api/results/${processingId}`);

        const data = await response.json();

        if (!data.success) {

            alert(data.error);

            resetButton();

            return;

        }

        progressSection.style.display = "none";

        resetButton();

        renderResults(data.analysis);

    }
    catch (err) {

        console.error(err);

        resetButton();

    }

}

// ===============================
// Render Dashboard
// ===============================

function renderResults(report) {

    console.log("Analysis Report:", report);

    // OCR
    document.getElementById("ocrText").innerText =
        report.ocr_text ||
        report.extracted_text ||
        "-";

    // Vehicle Number
    document.getElementById("vehicleNumber").innerText =
        report.vehicle_number && report.vehicle_number !== ""
            ? report.vehicle_number
            : "Not Detected";

    // Blur
    document.getElementById("blurScore").innerText =
        report.blur_score ?? "-";

    // Brightness
    document.getElementById("brightness").innerText =
        report.brightness_score ??
        report.brightness ??
        "-";

    // Duplicate
    let duplicate = report.duplicate_image;

    if (typeof duplicate === "object" && duplicate !== null) {
        duplicate = duplicate.is_duplicate;
    }

    document.getElementById("duplicate").innerText =
        duplicate ? "Yes" : "No";

    // Screenshot
    let screenshot = report.screenshot_detected;

    if (typeof screenshot === "object" && screenshot !== null) {
        screenshot = screenshot.is_screenshot;
    }

    document.getElementById("screenshot").innerText =
        screenshot ? "Yes" : "No";

    // Metadata
    document.getElementById("metadata").innerText =
        report.metadata_available
            ? "Available"
            : "Not Available";

    // Confidence
    document.getElementById("confidence").innerText =
        (report.confidence_score ?? 0) + "%";

}

// ===============================
// Progress
// ===============================

function updateProgress(value) {

    progressBar.style.width = value + "%";

    progressBar.innerText = value + "%";

}

// ===============================
// Reset Button
// ===============================

function resetButton() {

    uploadBtn.disabled = false;

    uploadBtn.innerHTML = "Analyze Advertisement";

}