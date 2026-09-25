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


// ==============================
// TAB EMBED
// ==============================

embedTab.addEventListener("click", () => {
    embedSection.classList.remove("hidden");
    extractSection.classList.add("hidden");

    embedTab.classList.add("bg-secret-600", "text-white");
    embedTab.classList.remove("text-gray-600");

    extractTab.classList.remove("bg-secret-600", "text-white");
    extractTab.classList.add("text-gray-600");

    embedTab.setAttribute("aria-selected", "true");
    extractTab.setAttribute("aria-selected", "false");
});


// ==============================
// TAB EXTRACT
// ==============================

extractTab.addEventListener("click", () => {
    embedSection.classList.add("hidden");
    extractSection.classList.remove("hidden");

    extractTab.classList.add("bg-secret-600", "text-white");
    extractTab.classList.remove("text-gray-600");

    embedTab.classList.remove("bg-secret-600", "text-white");
    embedTab.classList.add("text-gray-600");

    embedTab.setAttribute("aria-selected", "false");
    extractTab.setAttribute("aria-selected", "true");
});


// ==============================
// VALIDASI EXTENSION
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
// COVER IMAGE
// ==============================

coverImage.addEventListener("change", () => {
    const file = coverImage.files[0];

    if (!file) {
        coverFileName.textContent = "Belum ada file dipilih.";
        coverPreview.classList.add("hidden");
        coverPreviewImage.src = "";
        return;
    }

    if (!isSupportedImage(file)) {
        coverFileName.textContent = "Format file tidak didukung.";
        coverPreview.classList.add("hidden");
        coverPreviewImage.src = "";
        coverImage.value = "";
        return;
    }

    coverFileName.textContent = file.name;

    const imageUrl = URL.createObjectURL(file);

    coverPreviewImage.src = imageUrl;
    coverPreview.classList.remove("hidden");

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
        stegoFileName.textContent = "Format file tidak didukung.";
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
    messageCounter.textContent = `${message.value.length} karakter`;
});


// ==============================
// EMBED BUTTON
// ==============================

embedButton.addEventListener("click", () => {

    embedStatus.className = "mt-3 min-h-5 text-sm";

    const image = coverImage.files[0];
    const text = message.value.trim();
    const key = stegoKey.value.trim();

    if (!image) {
        embedStatus.textContent = "Silakan pilih cover image.";
        embedStatus.classList.add("text-red-600");
        return;
    }

    if (!isSupportedImage(image)) {
        embedStatus.textContent = "Gunakan gambar PNG atau BMP.";
        embedStatus.classList.add("text-red-600");
        return;
    }

    if (!text) {
        embedStatus.textContent = "Pesan rahasia belum diisi.";
        embedStatus.classList.add("text-red-600");
        return;
    }

    if (!key) {
        embedStatus.textContent = "Stego-key belum diisi.";
        embedStatus.classList.add("text-red-600");
        return;
    }

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

    if (!image) {
        extractStatus.textContent = "Silakan pilih stego image.";
        extractStatus.classList.add("text-red-600");
        return;
    }

    if (!isSupportedImage(image)) {
        extractStatus.textContent = "Gunakan gambar PNG atau BMP.";
        extractStatus.classList.add("text-red-600");
        return;
    }

    if (!key) {
        extractStatus.textContent = "Stego-key belum diisi.";
        extractStatus.classList.add("text-red-600");
        return;
    }

    extractStatus.textContent =
        "Input valid. Proses extract akan dihubungkan ke backend.";
    extractStatus.classList.add("text-secret-600");

    recoveredMessage.textContent =
        "Backend belum terhubung.";
});