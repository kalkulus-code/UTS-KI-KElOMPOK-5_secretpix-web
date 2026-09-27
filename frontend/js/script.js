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

// Hasil embed
const embedResult = document.getElementById("embedResult");

const resultCoverImage = document.getElementById("resultCoverImage");
const resultStegoImage = document.getElementById("resultStegoImage");

const resultStegoPlaceholder =
    document.getElementById("resultStegoPlaceholder");

const resultStegoContainer =
    document.getElementById("resultStegoContainer");

    const downloadStegoButton =
    document.getElementById("downloadStegoButton");

const resultPsnr = document.getElementById("resultPsnr");
const resultMse = document.getElementById("resultMse");


// ==============================
// PREVIEW URL
// ==============================

let coverObjectUrl = null;
let stegoObjectUrl = null;


// ==============================
// TAB EMBED
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


// ==============================
// TAB EXTRACT
// ==============================

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

    downloadStegoButton.classList.add("hidden");
downloadStegoButton.href = "#";
}


// ==============================
// COVER IMAGE
// ==============================

coverImage.addEventListener("change", () => {
    const file = coverImage.files[0];

    if (coverObjectUrl) {
        URL.revokeObjectURL(coverObjectUrl);
        coverObjectUrl = null;
    }

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

    coverObjectUrl = URL.createObjectURL(file);

    // Preview pada area upload
    coverPreviewImage.src = coverObjectUrl;
    coverPreview.classList.remove("hidden");

    // Tampilkan area hasil
    embedResult.classList.remove("hidden");

    // Tampilkan cover pada area perbandingan
    resultCoverImage.src = coverObjectUrl;

    // Reset stego image
    resultStegoPlaceholder.classList.remove("hidden");
    resultStegoContainer.classList.add("hidden");
    resultStegoImage.src = "";

    // Reset metrik
    resultPsnr.textContent = "-";
    resultMse.textContent = "-";

    embedStatus.textContent = "";
});


// ==============================
// STEGO IMAGE
// ==============================

stegoImage.addEventListener("change", () => {
    const file = stegoImage.files[0];

    if (stegoObjectUrl) {
        URL.revokeObjectURL(stegoObjectUrl);
        stegoObjectUrl = null;
    }

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

    stegoObjectUrl = URL.createObjectURL(file);

    stegoPreviewImage.src = stegoObjectUrl;
    stegoPreview.classList.remove("hidden");

    extractStatus.textContent = "";
    recoveredMessage.textContent =
        "Pesan hasil ekstraksi akan muncul di sini.";
});


// ==============================
// MESSAGE COUNTER
// ==============================

message.addEventListener("input", () => {
    messageCounter.textContent =
        `${message.value.length} karakter`;
});


// ==============================
// EMBED
// ==============================

embedButton.addEventListener("click", async () => {
    embedStatus.className =
        "mt-3 min-h-5 text-sm";

    const image = coverImage.files[0];
    const text = message.value.trim();
    const key = stegoKey.value.trim();

    // Validasi image
    if (!image) {
        embedStatus.textContent =
            "Silakan pilih cover image.";

        embedStatus.classList.add("text-red-600");
        return;
    }

    // Validasi format
    if (!isSupportedImage(image)) {
        embedStatus.textContent =
            "Gunakan gambar PNG atau BMP.";

        embedStatus.classList.add("text-red-600");
        return;
    }

    // Validasi pesan
    if (!text) {
        embedStatus.textContent =
            "Pesan rahasia belum diisi.";

        embedStatus.classList.add("text-red-600");
        return;
    }

    // Validasi key
    if (!key) {
        embedStatus.textContent =
            "Stego-key belum diisi.";

        embedStatus.classList.add("text-red-600");
        return;
    }


    // Form data
    const formData = new FormData();

    formData.append("image", image);
    formData.append("message", text);
    formData.append("stego_key", key);


    // Disable tombol saat proses
    embedButton.disabled = true;
    embedButton.textContent = "Memproses...";

    embedStatus.textContent =
        "Sedang menyisipkan pesan...";

    embedStatus.classList.add("text-secret-600");


    try {
        const response = await fetch("/api/embed", {
            method: "POST",
            body: formData
        });

        const result = await response.json();


        if (!response.ok || !result.success) {
            throw new Error(
                result.message || "Proses embed gagal."
            );
        }


        // Status berhasil
        embedStatus.textContent =
            "Pesan berhasil disisipkan.";

        embedStatus.className =
            "mt-3 min-h-5 text-sm text-secret-600";


        // Tampilkan hasil
        embedResult.classList.remove("hidden");

        resultStegoPlaceholder.classList.add("hidden");
        resultStegoContainer.classList.remove("hidden");

        resultStegoImage.src = result.stego_image;

        downloadStegoButton.href = result.stego_image;
downloadStegoButton.classList.remove("hidden");


        // Metrik jika backend sudah mengirim
        resultPsnr.textContent =
            result.psnr !== undefined
                ? result.psnr
                : "-";

        resultMse.textContent =
            result.mse !== undefined
                ? result.mse
                : "-";


    } catch (error) {
        console.error("Embed error:", error);

        embedStatus.textContent =
            error.message || "Terjadi kesalahan saat embed.";

        embedStatus.className =
            "mt-3 min-h-5 text-sm text-red-600";
    } finally {
        embedButton.disabled = false;
        embedButton.textContent = "Sisipkan Pesan";
    }
});


// ==============================
// EXTRACT
// ==============================

extractButton.addEventListener("click", async () => {
    extractStatus.className =
        "mt-3 min-h-5 text-sm";

    const image = stegoImage.files[0];
    const key = extractKey.value.trim();


    // Validasi image
    if (!image) {
        extractStatus.textContent =
            "Silakan pilih stego image.";

        extractStatus.classList.add("text-red-600");
        return;
    }


    // Validasi format
    if (!isSupportedImage(image)) {
        extractStatus.textContent =
            "Gunakan gambar PNG atau BMP.";

        extractStatus.classList.add("text-red-600");
        return;
    }


    // Validasi key
    if (!key) {
        extractStatus.textContent =
            "Stego-key belum diisi.";

        extractStatus.classList.add("text-red-600");
        return;
    }


    // Form data
    const formData = new FormData();

    formData.append("image", image);
    formData.append("stego_key", key);


    // Disable tombol
    extractButton.disabled = true;
    extractButton.textContent = "Memproses...";

    extractStatus.textContent =
        "Sedang mengambil pesan...";

    extractStatus.classList.add("text-secret-600");


    try {
        const response = await fetch("/api/extract", {
            method: "POST",
            body: formData
        });

        const result = await response.json();


        if (!response.ok || !result.success) {
            throw new Error(
                result.message || "Proses extract gagal."
            );
        }


        // Tampilkan pesan
        recoveredMessage.textContent =
            result.data;


        extractStatus.textContent =
            "Pesan berhasil diekstraksi.";

        extractStatus.className =
            "mt-3 min-h-5 text-sm text-secret-600";


    } catch (error) {
        console.error("Extract error:", error);

        recoveredMessage.textContent =
            "Pesan tidak dapat diekstraksi.";

        extractStatus.textContent =
            error.message || "Terjadi kesalahan saat extract.";

        extractStatus.className =
            "mt-3 min-h-5 text-sm text-red-600";
    } finally {
        extractButton.disabled = false;
        extractButton.textContent = "Baca Pesan";
    }
});