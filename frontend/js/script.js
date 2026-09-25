// ==============================
// ELEMENT
// ==============================

const embedTab = document.getElementById("embedTab");
const extractTab = document.getElementById("extractTab");

const embedSection = document.getElementById("embedSection");
const extractSection = document.getElementById("extractSection");

const coverImage = document.getElementById("coverImage");
const stegoImage = document.getElementById("stegoImage");

const coverFileName = document.getElementById("coverFileName");
const stegoFileName = document.getElementById("stegoFileName");

const coverPreview = document.getElementById("coverPreview");
const stegoPreview = document.getElementById("stegoPreview");

const coverPreviewImage = document.getElementById("coverPreviewImage");
const stegoPreviewImage = document.getElementById("stegoPreviewImage");

const message = document.getElementById("message");
const messageCounter = document.getElementById("messageCounter");

const embedButton = document.getElementById("embedButton");
const extractButton = document.getElementById("extractButton");

const embedStatus = document.getElementById("embedStatus");
const extractStatus = document.getElementById("extractStatus");

const recoveredMessage = document.getElementById("recoveredMessage");

const stegoKey = document.getElementById("stegoKey");
const extractKey = document.getElementById("extractKey");

// Hasil steganografi
const embedResult = document.getElementById("embedResult");

const resultCoverImage = document.getElementById("resultCoverImage");
const resultStegoImage = document.getElementById("resultStegoImage");

const resultStegoPlaceholder =
    document.getElementById("resultStegoPlaceholder");

const resultStegoContainer =
    document.getElementById("resultStegoContainer");

const resultPsnr = document.getElementById("resultPsnr");
const resultMse = document.getElementById("resultMse");


// ==============================
// TAB
// ==============================

function showEmbedTab() {
    embedSection.classList.remove("hidden");
    extractSection.classList.add("hidden");

    embedTab.classList.add("bg-secret-600", "text-white");
    embedTab.classList.remove("text-gray-600");

    extractTab.classList.remove("bg-secret-600", "text-white");
    extractTab.classList.add("text-gray-600");

    embedTab.setAttribute("aria-selected", "true");
    extractTab.setAttribute("aria-selected", "false");
}

function showExtractTab() {
    embedSection.classList.add("hidden");
    extractSection.classList.remove("hidden");

    extractTab.classList.add("bg-secret-600", "text-white");
    extractTab.classList.remove("text-gray-600");

    embedTab.classList.remove("bg-secret-600", "text-white");
    embedTab.classList.add("text-gray-600");

    embedTab.setAttribute("aria-selected", "false");
    extractTab.setAttribute("aria-selected", "true");
}

embedTab.addEventListener("click", showEmbedTab);
extractTab.addEventListener("click", showExtractTab);


// ==============================
// VALIDASI GAMBAR
// ==============================

function isSupportedImage(file) {
    if (!file) {
        return false;
    }

    const allowedTypes = [
        "image/png",
        "image/bmp"
    ];

    return allowedTypes.includes(file.type);
}


// ==============================
// RESET HASIL EMBED
// ==============================

function resetEmbedResult() {
    embedResult.classList.add("hidden");

    resultCoverImage.src = "";

    resultStegoImage.src = "";

    resultPsnr.textContent = "-";
    resultMse.textContent = "-";

    resultStegoPlaceholder.classList.remove("hidden");
    resultStegoContainer.classList.add("hidden");
}


// ==============================
// COVER IMAGE
// ==============================

coverImage.addEventListener("change", () => {
    const file = coverImage.files[0];

    if (!file) {
        coverFileName.textContent = "Belum ada file dipilih.";

        coverPreview.classList.add("hidden");
        coverPreviewImage.src = "";

        resetEmbedResult();
        return;
    }

    if (!isSupportedImage(file)) {
        coverFileName.textContent =
            "Format file tidak didukung. Gunakan PNG atau BMP.";

        coverPreview.classList.add("hidden");
        coverPreviewImage.src = "";

        coverImage.value = "";

        resetEmbedResult();
        return;
    }

    coverFileName.textContent = file.name;

    const imageUrl = URL.createObjectURL(file);

    // Preview pada area upload
    coverPreviewImage.src = imageUrl;
    coverPreview.classList.remove("hidden");

    // Preview pada area hasil
    embedResult.classList.remove("hidden");
    resultCoverImage.src = imageUrl;

    // Stego belum tersedia karena backend belum terhubung
    resultStegoPlaceholder.classList.remove("hidden");
    resultStegoContainer.classList.add("hidden");

    resultStegoImage.src = "";

    // Reset nilai metrik
    resultPsnr.textContent = "-";
    resultMse.textContent = "-";

    coverPreviewImage.onload = () => {
        URL.revokeObjectURL(imageUrl);
    };
});


// ==============================
// STEGO IMAGE
// ==============================

stegoImage.addEventListener("change", () => {
    const file = stegoImage.files[0];

    if (!file) {
        stegoFileName.textContent = "Belum ada file dipilih.";

        stegoPreview.classList.add("hidden");
        stegoPreviewImage.src = "";

        return;
    }

    if (!isSupportedImage(file)) {
        stegoFileName.textContent =
            "Format file tidak didukung. Gunakan PNG atau BMP.";

        stegoPreview.classList.add("hidden");
        stegoPreviewImage.src = "";

        stegoImage.value = "";

        return;
    }

    stegoFileName.textContent = file.name;

    const imageUrl = URL.createObjectURL(file);

    stegoPreviewImage.src = imageUrl;
    stegoPreview.classList.remove("hidden");

    stegoPreviewImage.onload = () => {
        URL.revokeObjectURL(imageUrl);
    };
});


// ==============================
// MESSAGE COUNTER
// ==============================

message.addEventListener("input", () => {
    messageCounter.textContent =
        `${message.value.length} karakter`;
});


// ==============================
// EMBED BUTTON
// ==============================

embedButton.addEventListener("click", () => {
    embedStatus.className = "mt-3 min-h-5 text-sm";

    const image = coverImage.files[0];
    const text = message.value.trim();
    const key = stegoKey.value.trim();

    // Belum pilih gambar
    if (!image) {
        embedStatus.textContent =
            "Silakan pilih cover image.";

        embedStatus.classList.add("text-red-600");
        return;
    }

    // Format gambar
    if (!isSupportedImage(image)) {
        embedStatus.textContent =
            "Gunakan gambar PNG atau BMP.";

        embedStatus.classList.add("text-red-600");
        return;
    }

    // Pesan kosong
    if (!text) {
        embedStatus.textContent =
            "Pesan rahasia belum diisi.";

        embedStatus.classList.add("text-red-600");
        return;
    }

    // Key kosong
    if (!key) {
        embedStatus.textContent =
            "Stego-key belum diisi.";

        embedStatus.classList.add("text-red-600");
        return;
    }

    // Backend belum tersambung
    embedStatus.textContent =
        "Input valid. Proses embed akan dihubungkan ke backend.";

    embedStatus.classList.add("text-secret-600");
});


// ==============================
// EXTRACT BUTTON
// ==============================

extractButton.addEventListener("click", () => {
    extractStatus.className = "mt-3 min-h-5 text-sm";

    const image = stegoImage.files[0];
    const key = extractKey.value.trim();

    // Belum pilih gambar
    if (!image) {
        extractStatus.textContent =
            "Silakan pilih stego image.";

        extractStatus.classList.add("text-red-600");
        return;
    }

    // Format gambar
    if (!isSupportedImage(image)) {
        extractStatus.textContent =
            "Gunakan gambar PNG atau BMP.";

        extractStatus.classList.add("text-red-600");
        return;
    }

    // Key kosong
    if (!key) {
        extractStatus.textContent =
            "Stego-key belum diisi.";

        extractStatus.classList.add("text-red-600");
        return;
    }

    // Backend belum tersambung
    extractStatus.textContent =
        "Input valid. Proses extract akan dihubungkan ke backend.";

    extractStatus.classList.add("text-secret-600");

    recoveredMessage.textContent =
        "Backend belum terhubung.";
});


// ==============================
// FUNGSI UNTUK HASIL BACKEND
// ==============================
// Fungsi ini belum dipanggil sekarang.
// Nanti akan digunakan saat T12,
// ketika frontend sudah terhubung ke backend.

function showEmbedResult(stegoImageUrl, psnr, mse) {
    embedResult.classList.remove("hidden");

    resultStegoPlaceholder.classList.add("hidden");
    resultStegoContainer.classList.remove("hidden");

    resultStegoImage.src = stegoImageUrl;

    resultPsnr.textContent =
        psnr !== undefined ? psnr : "-";

    resultMse.textContent =
        mse !== undefined ? mse : "-";
}