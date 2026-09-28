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

const coverPreviewImage =
    document.getElementById("coverPreviewImage");

const stegoPreviewImage =
    document.getElementById("stegoPreviewImage");

const message = document.getElementById("message");
const messageCounter = document.getElementById("messageCounter");

const embedButton = document.getElementById("embedButton");
const extractButton = document.getElementById("extractButton");

const embedStatus = document.getElementById("embedStatus");
const extractStatus = document.getElementById("extractStatus");

const recoveredMessage =
    document.getElementById("recoveredMessage");

const stegoKey = document.getElementById("stegoKey");
const extractKey = document.getElementById("extractKey");

const embedResult = document.getElementById("embedResult");

const resultCoverImage =
    document.getElementById("resultCoverImage");

const resultStegoImage =
    document.getElementById("resultStegoImage");

const resultStegoPlaceholder =
    document.getElementById("resultStegoPlaceholder");

const resultStegoContainer =
    document.getElementById("resultStegoContainer");

const downloadStegoButton =
    document.getElementById("downloadStegoButton");

const resultPsnr =
    document.getElementById("resultPsnr");

const resultMse =
    document.getElementById("resultMse");


// ==============================
// PREVIEW URL
// ==============================

let coverObjectUrl = null;
let stegoObjectUrl = null;


// ==============================
// TESTING STATE
// ==============================

let currentStegoUrl = null;
let currentOriginalMessage = "";
let currentStegoKey = "";

let testingPanel = null;
let histogramPreview = null;
let jpegPreview = null;
let jpegDownload = null;
let fragilityStatus = null;
let fragilityMessage = null;
let fragilityButton = null;


// ==============================
// TAB EMBED
// ==============================

function showEmbedTab() {
    embedSection.classList.remove("hidden");
    extractSection.classList.add("hidden");

    embedTab.classList.add(
        "bg-secret-600",
        "text-white"
    );

    embedTab.classList.remove("text-gray-600");

    extractTab.classList.remove(
        "bg-secret-600",
        "text-white"
    );

    extractTab.classList.add("text-gray-600");

    embedTab.setAttribute(
        "aria-selected",
        "true"
    );

    extractTab.setAttribute(
        "aria-selected",
        "false"
    );
}


// ==============================
// TAB EXTRACT
// ==============================

function showExtractTab() {
    embedSection.classList.add("hidden");
    extractSection.classList.remove("hidden");

    extractTab.classList.add(
        "bg-secret-600",
        "text-white"
    );

    extractTab.classList.remove("text-gray-600");

    embedTab.classList.remove(
        "bg-secret-600",
        "text-white"
    );

    embedTab.classList.add("text-gray-600");

    embedTab.setAttribute(
        "aria-selected",
        "false"
    );

    extractTab.setAttribute(
        "aria-selected",
        "true"
    );
}


embedTab.addEventListener(
    "click",
    showEmbedTab
);

extractTab.addEventListener(
    "click",
    showExtractTab
);


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
// TESTING PANEL
// ==============================

function createTestingPanel() {

    if (testingPanel) {
        return;
    }

    testingPanel = document.createElement("div");

    testingPanel.className =
        "mt-8 border-t border-gray-200 pt-6";

    testingPanel.innerHTML = `
        <div class="mb-5">
            <h4 class="text-lg font-bold text-gray-900">
                Pengujian Wajib
            </h4>

            <p class="mt-1 text-sm text-gray-500">
                Analisis histogram dan uji kerapuhan
                setelah stego image disimpan ulang sebagai JPEG.
            </p>
        </div>

        <!-- HISTOGRAM -->
        <div class="rounded-lg border border-gray-200 bg-gray-50 p-4">

            <div class="mb-3">
                <h5 class="text-sm font-semibold text-gray-800">
                    Perbandingan Histogram
                </h5>

                <p class="mt-1 text-xs text-gray-500">
                    Distribusi nilai warna RGB pada cover
                    dan stego image.
                </p>
            </div>

            <div class="overflow-hidden rounded-lg bg-white p-2">
                <img
                    id="histogramPreview"
                    src=""
                    alt="Histogram Cover dan Stego"
                    class="mx-auto w-full"
                >
            </div>
        </div>


        <!-- JPEG FRAGILITY -->
        <div class="mt-5 rounded-lg border border-gray-200 bg-gray-50 p-4">

            <div class="mb-4">
            <!-- ENHANCED LSB -->
<div class="mt-5 rounded-lg border border-gray-200 bg-gray-50 p-4">

    <div class="mb-4">
        <h5 class="text-sm font-semibold text-gray-800">
            Enhanced LSB
        </h5>

        <p class="mt-1 text-xs leading-5 text-gray-500">
            Visualisasi bidang LSB pada stego image
            untuk melihat pola bit yang digunakan dalam
            proses steganografi.
        </p>
    </div>

    <button
        id="enhancedLsbButton"
        type="button"
        class="w-full rounded-lg border border-secret-600 bg-white px-4 py-3 text-sm font-semibold text-secret-700 transition hover:bg-secret-50"
    >
        Analisis Enhanced LSB
    </button>

    <p
        id="enhancedLsbStatus"
        class="mt-3 min-h-5 text-sm"
        role="status"
        aria-live="polite"
    ></p>

    <div
        id="enhancedLsbResult"
        class="mt-4 hidden"
    >

        <div class="overflow-hidden rounded-lg bg-white p-3">

            <img
                id="enhancedLsbPreview"
                src=""
                alt="Enhanced LSB"
                class="mx-auto w-full"
            >

        </div>

        <p class="mt-3 text-xs leading-5 text-gray-500">
            Hitam menunjukkan bit LSB bernilai 0,
            sedangkan putih menunjukkan bit LSB bernilai 1.
        </p>

    </div>

</div>
                <h5 class="text-sm font-semibold text-gray-800">
                    Uji Kerapuhan JPEG
                </h5>

                <p class="mt-1 text-xs leading-5 text-gray-500">
                    Stego image disimpan ulang sebagai JPEG
                    kualitas 90, kemudian dicoba diekstraksi
                    kembali menggunakan stego-key.
                </p>
            </div>

            <button
                id="fragilityButton"
                type="button"
                class="w-full rounded-lg border border-secret-600 bg-white px-4 py-3 text-sm font-semibold text-secret-700 transition hover:bg-secret-50"
            >
                Uji Simpan Ulang sebagai JPEG
            </button>

            <p
                id="fragilityStatus"
                class="mt-3 min-h-5 text-sm"
                role="status"
                aria-live="polite"
            ></p>

            <div
                id="fragilityResult"
                class="mt-4 hidden"
            >

                <div class="mb-2 flex items-center justify-between">
                    <p class="text-sm font-semibold text-gray-800">
                        Hasil JPEG
                    </p>

                    <a
                        id="jpegDownload"
                        href="#"
                        download
                        class="text-xs font-semibold text-secret-700 hover:text-secret-800"
                    >
                        Unduh JPEG
                    </a>
                </div>

                <div class="overflow-hidden rounded-lg bg-white p-3">
                    <img
                        id="jpegPreview"
                        src=""
                        alt="Stego JPEG"
                        class="mx-auto max-h-64 max-w-full object-contain"
                    >
                </div>

                <div
                    class="mt-4 rounded-lg border border-gray-200 bg-white p-4"
                >
                    <p class="text-xs text-gray-500">
                        Status Ekstraksi
                    </p>

                    <p
                        id="fragilityMessage"
                        class="mt-1 text-sm leading-6 text-gray-700"
                    >
                        Menunggu pengujian.
                    </p>
                </div>

            </div>
        </div>
    `;

    embedResult.appendChild(testingPanel);

    histogramPreview =
        document.getElementById(
            "histogramPreview"
        );

    jpegPreview =
        document.getElementById(
            "jpegPreview"
        );

    jpegDownload =
        document.getElementById(
            "jpegDownload"
        );

    fragilityStatus =
        document.getElementById(
            "fragilityStatus"
        );

    fragilityMessage =
        document.getElementById(
            "fragilityMessage"
        );

    fragilityButton =
        document.getElementById(
            "fragilityButton"
        );

const enhancedLsbButton =
    document.getElementById(
        "enhancedLsbButton"
    );

const enhancedLsbStatus =
    document.getElementById(
        "enhancedLsbStatus"
    );

const enhancedLsbResult =
    document.getElementById(
        "enhancedLsbResult"
    );

const enhancedLsbPreview =
    document.getElementById(
        "enhancedLsbPreview"
    );

enhancedLsbButton.addEventListener(
    "click",
    runEnhancedLsb
);

    fragilityButton.addEventListener(
        "click",
        runFragilityTest
    );
}


// ==============================
// RESET TESTING
// ==============================

function resetTesting() {

    currentStegoUrl = null;
    currentOriginalMessage = "";
    currentStegoKey = "";

    if (!testingPanel) {
        return;
    }

    testingPanel.classList.add("hidden");

    histogramPreview.src = "";

    jpegPreview.src = "";

    jpegDownload.href = "#";

    fragilityStatus.textContent = "";

    fragilityMessage.textContent =
        "Menunggu pengujian.";

    fragilityButton.disabled = false;

    fragilityButton.textContent =
        "Uji Simpan Ulang sebagai JPEG";
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

    resultStegoPlaceholder.classList.remove(
        "hidden"
    );

    resultStegoContainer.classList.add(
        "hidden"
    );

    downloadStegoButton.classList.add(
        "hidden"
    );

    downloadStegoButton.href = "#";

    resetTesting();
}


// ==============================
// COVER IMAGE
// ==============================

coverImage.addEventListener("change", () => {

    const file = coverImage.files[0];

    if (coverObjectUrl) {
        URL.revokeObjectURL(
            coverObjectUrl
        );

        coverObjectUrl = null;
    }

    if (!file) {

        coverFileName.textContent =
            "Belum ada file dipilih.";

        coverPreview.classList.add(
            "hidden"
        );

        coverPreviewImage.src = "";

        resetEmbedResult();

        return;
    }

    if (!isSupportedImage(file)) {

        coverFileName.textContent =
            "Format file tidak didukung. Gunakan PNG atau BMP.";

        coverPreview.classList.add(
            "hidden"
        );

        coverPreviewImage.src = "";

        coverImage.value = "";

        resetEmbedResult();

        return;
    }

    coverFileName.textContent =
        file.name;

    coverObjectUrl =
        URL.createObjectURL(file);

    coverPreviewImage.src =
        coverObjectUrl;

    coverPreview.classList.remove(
        "hidden"
    );

    embedResult.classList.remove(
        "hidden"
    );

    resultCoverImage.src =
        coverObjectUrl;

    resultStegoPlaceholder.classList.remove(
        "hidden"
    );

    resultStegoContainer.classList.add(
        "hidden"
    );

    resultStegoImage.src = "";

    resultPsnr.textContent = "-";
    resultMse.textContent = "-";

    embedStatus.textContent = "";

    resetTesting();
});


// ==============================
// STEGO IMAGE
// ==============================

stegoImage.addEventListener("change", () => {

    const file = stegoImage.files[0];

    if (stegoObjectUrl) {

        URL.revokeObjectURL(
            stegoObjectUrl
        );

        stegoObjectUrl = null;
    }

    if (!file) {

        stegoFileName.textContent =
            "Belum ada file dipilih.";

        stegoPreview.classList.add(
            "hidden"
        );

        stegoPreviewImage.src = "";

        return;
    }

    if (!isSupportedImage(file)) {

        stegoFileName.textContent =
            "Format file tidak didukung. Gunakan PNG atau BMP.";

        stegoPreview.classList.add(
            "hidden"
        );

        stegoPreviewImage.src = "";

        stegoImage.value = "";

        return;
    }

    stegoFileName.textContent =
        file.name;

    stegoObjectUrl =
        URL.createObjectURL(file);

    stegoPreviewImage.src =
        stegoObjectUrl;

    stegoPreview.classList.remove(
        "hidden"
    );

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

embedButton.addEventListener(
    "click",
    async () => {

        embedStatus.className =
            "mt-3 min-h-5 text-sm";

        const image =
            coverImage.files[0];

        const text =
            message.value.trim();

        const key =
            stegoKey.value.trim();

        // Validasi image
        if (!image) {

            embedStatus.textContent =
                "Silakan pilih cover image.";

            embedStatus.classList.add(
                "text-red-600"
            );

            return;
        }

        // Validasi format
        if (!isSupportedImage(image)) {

            embedStatus.textContent =
                "Gunakan gambar PNG atau BMP.";

            embedStatus.classList.add(
                "text-red-600"
            );

            return;
        }

        // Validasi pesan
        if (!text) {

            embedStatus.textContent =
                "Pesan rahasia belum diisi.";

            embedStatus.classList.add(
                "text-red-600"
            );

            return;
        }

        // Validasi key
        if (!key) {

            embedStatus.textContent =
                "Stego-key belum diisi.";

            embedStatus.classList.add(
                "text-red-600"
            );

            return;
        }

        const formData =
            new FormData();

        formData.append(
            "image",
            image
        );

        formData.append(
            "message",
            text
        );

        formData.append(
            "stego_key",
            key
        );

        embedButton.disabled = true;

        embedButton.textContent =
            "Memproses...";

        embedStatus.textContent =
            "Sedang menyisipkan pesan...";

        embedStatus.classList.add(
            "text-secret-600"
        );

        try {

            const response =
                await fetch(
                    "/api/embed",
                    {
                        method: "POST",
                        body: formData
                    }
                );

            const result =
                await response.json();

            if (
                !response.ok ||
                !result.success
            ) {
                throw new Error(
                    result.message ||
                    "Proses embed gagal."
                );
            }

            embedStatus.textContent =
                "Pesan berhasil disisipkan.";

            embedStatus.className =
                "mt-3 min-h-5 text-sm text-secret-600";

            embedResult.classList.remove(
                "hidden"
            );

            resultStegoPlaceholder.classList.add(
                "hidden"
            );

            resultStegoContainer.classList.remove(
                "hidden"
            );

            resultStegoImage.src =
                result.stego_image;

            downloadStegoButton.href =
                result.stego_image;

            downloadStegoButton.classList.remove(
                "hidden"
            );

            resultPsnr.textContent =
                result.psnr !== undefined
                    ? result.psnr
                    : "-";

            resultMse.textContent =
                result.mse !== undefined
                    ? result.mse
                    : "-";

            // Simpan state testing
            currentStegoUrl =
                result.stego_image;

            currentOriginalMessage =
                text;

            currentStegoKey =
                key;

            // Tampilkan panel testing
            createTestingPanel();

            testingPanel.classList.remove(
                "hidden"
            );

            histogramPreview.src =
                result.histogram_image;

            jpegPreview.src = "";

            jpegDownload.href = "#";

            fragilityStatus.textContent = "";

            fragilityMessage.textContent =
                "Belum dilakukan uji JPEG.";

        } catch (error) {

            console.error(
                "Embed error:",
                error
            );

            embedStatus.textContent =
                error.message ||
                "Terjadi kesalahan saat embed.";

            embedStatus.className =
                "mt-3 min-h-5 text-sm text-red-600";

        } finally {

            embedButton.disabled = false;

            embedButton.textContent =
                "Sisipkan Pesan";
        }
    }
);


// ==============================
// JPEG FRAGILITY TEST
// ==============================

async function runEnhancedLsb() {

    if (!currentStegoUrl) {

        enhancedLsbStatus.className =
            "mt-3 min-h-5 text-sm text-red-600";

        enhancedLsbStatus.textContent =
            "Stego image belum tersedia.";

        return;
    }

    enhancedLsbButton.disabled = true;

    enhancedLsbButton.textContent =
        "Sedang menganalisis...";

    enhancedLsbStatus.className =
        "mt-3 min-h-5 text-sm text-secret-600";

    enhancedLsbStatus.textContent =
        "Membuat visualisasi bidang LSB...";

    try {

        // Ambil stego image
        const imageResponse =
            await fetch(currentStegoUrl);

        if (!imageResponse.ok) {
            throw new Error(
                "Stego image tidak dapat diambil."
            );
        }

        const blob =
            await imageResponse.blob();

        // Jadikan file
        const stegoFile =
            new File(
                [blob],
                "stego.png",
                {
                    type:
                        blob.type ||
                        "image/png"
                }
            );

        // FormData
        const formData =
            new FormData();

        formData.append(
            "image",
            stegoFile
        );

        // Kirim ke backend
        const response =
            await fetch(
                "/api/enhanced-lsb",
                {
                    method: "POST",
                    body: formData
                }
            );

        const result =
            await response.json();

        if (
            !response.ok ||
            !result.success
        ) {
            throw new Error(
                result.message ||
                "Analisis Enhanced LSB gagal."
            );
        }

        // Tampilkan hasil
        enhancedLsbPreview.src =
            result.enhanced_lsb_image;

        enhancedLsbResult.classList.remove(
            "hidden"
        );

        enhancedLsbStatus.className =
            "mt-3 min-h-5 text-sm text-secret-600";

        enhancedLsbStatus.textContent =
            "Analisis Enhanced LSB berhasil.";

    } catch (error) {

        console.error(
            "Enhanced LSB error:",
            error
        );

        enhancedLsbStatus.className =
            "mt-3 min-h-5 text-sm text-red-600";

        enhancedLsbStatus.textContent =
            error.message ||
            "Terjadi kesalahan saat analisis Enhanced LSB.";

    } finally {

        enhancedLsbButton.disabled = false;

        enhancedLsbButton.textContent =
            "Analisis Enhanced LSB";
    }
}

async function runFragilityTest() {

    if (
        !currentStegoUrl ||
        !currentStegoKey
    ) {
        fragilityStatus.textContent =
            "Stego image belum tersedia.";

        fragilityStatus.className =
            "mt-3 min-h-5 text-sm text-red-600";

        return;
    }

    fragilityButton.disabled = true;

    fragilityButton.textContent =
        "Sedang menguji...";

    fragilityStatus.className =
        "mt-3 min-h-5 text-sm text-secret-600";

    fragilityStatus.textContent =
        "Stego image sedang disimpan ulang sebagai JPEG...";

    fragilityMessage.textContent =
        "Menjalankan ekstraksi...";

    try {

        // Ambil stego image hasil embed
        const imageResponse =
            await fetch(
                currentStegoUrl
            );

        if (!imageResponse.ok) {
            throw new Error(
                "Stego image tidak dapat diambil."
            );
        }

        const blob =
            await imageResponse.blob();

        const jpegSourceFile =
            new File(
                [blob],
                "stego.png",
                {
                    type: blob.type ||
                        "image/png"
                }
            );

        // FormData
        const formData =
            new FormData();

        formData.append(
            "image",
            jpegSourceFile
        );

        formData.append(
            "stego_key",
            currentStegoKey
        );

        // Kirim ke backend
        const response =
            await fetch(
                "/api/fragility",
                {
                    method: "POST",
                    body: formData
                }
            );

        const result =
            await response.json();

        if (
            !response.ok ||
            !result.success
        ) {
            throw new Error(
                result.message ||
                "Uji JPEG gagal."
            );
        }

        // Tampilkan JPEG
        jpegPreview.src =
            result.jpeg_image;

        jpegDownload.href =
            result.jpeg_image;

        jpegDownload.download =
            "stego_reencoded.jpg";

        document
            .getElementById(
                "fragilityResult"
            )
            .classList.remove(
                "hidden"
            );

        // Analisis hasil ekstraksi
        if (
            result.extraction_success
        ) {

            const extracted =
                result.extracted_message;

            if (
                extracted ===
                currentOriginalMessage
            ) {

                fragilityStatus.className =
                    "mt-3 min-h-5 text-sm text-orange-600";

                fragilityStatus.textContent =
                    "Pesan masih dapat diekstraksi setelah disimpan sebagai JPEG.";

                fragilityMessage.textContent =
                    "Ekstraksi berhasil dan pesan masih sama dengan pesan asli.";

            } else {

                fragilityStatus.className =
                    "mt-3 min-h-5 text-sm text-orange-600";

                fragilityStatus.textContent =
                    "Ekstraksi berhasil, tetapi pesan mengalami perubahan.";

                fragilityMessage.textContent =
                    `Hasil ekstraksi: ${extracted}`;
            }

        } else {

            fragilityStatus.className =
                "mt-3 min-h-5 text-sm text-red-600";

            fragilityStatus.textContent =
                "Ekstraksi gagal setelah stego disimpan sebagai JPEG.";

            fragilityMessage.textContent =
                result.extraction_error ||
                "Data LSB tidak dapat dipulihkan.";
        }

    } catch (error) {

        console.error(
            "Fragility error:",
            error
        );

        fragilityStatus.className =
            "mt-3 min-h-5 text-sm text-red-600";

        fragilityStatus.textContent =
            error.message ||
            "Terjadi kesalahan saat uji JPEG.";

        fragilityMessage.textContent =
            "Pengujian tidak dapat diselesaikan.";

    } finally {

        fragilityButton.disabled =
            false;

        fragilityButton.textContent =
            "Uji Simpan Ulang sebagai JPEG";
    }
}


// ==============================
// EXTRACT
// ==============================

extractButton.addEventListener(
    "click",
    async () => {

        extractStatus.className =
            "mt-3 min-h-5 text-sm";

        const image =
            stegoImage.files[0];

        const key =
            extractKey.value.trim();

        // Validasi image
        if (!image) {

            extractStatus.textContent =
                "Silakan pilih stego image.";

            extractStatus.classList.add(
                "text-red-600"
            );

            return;
        }

        // Validasi format
        if (!isSupportedImage(image)) {

            extractStatus.textContent =
                "Gunakan gambar PNG atau BMP.";

            extractStatus.classList.add(
                "text-red-600"
            );

            return;
        }

        // Validasi key
        if (!key) {

            extractStatus.textContent =
                "Stego-key belum diisi.";

            extractStatus.classList.add(
                "text-red-600"
            );

            return;
        }

        const formData =
            new FormData();

        formData.append(
            "image",
            image
        );

        formData.append(
            "stego_key",
            key
        );

        extractButton.disabled =
            true;

        extractButton.textContent =
            "Memproses...";

        extractStatus.textContent =
            "Sedang mengambil pesan...";

        extractStatus.classList.add(
            "text-secret-600"
        );

        try {

            const response =
                await fetch(
                    "/api/extract",
                    {
                        method: "POST",
                        body: formData
                    }
                );

            const result =
                await response.json();

            if (
                !response.ok ||
                !result.success
            ) {
                throw new Error(
                    result.message ||
                    "Proses extract gagal."
                );
            }

            recoveredMessage.textContent =
                result.data;

            extractStatus.textContent =
                "Pesan berhasil diekstraksi.";

            extractStatus.className =
                "mt-3 min-h-5 text-sm text-secret-600";

        } catch (error) {

            console.error(
                "Extract error:",
                error
            );

            recoveredMessage.textContent =
                "Pesan tidak dapat diekstraksi.";

            extractStatus.textContent =
                error.message ||
                "Terjadi kesalahan saat extract.";

            extractStatus.className =
                "mt-3 min-h-5 text-sm text-red-600";

        } finally {

            extractButton.disabled =
                false;

            extractButton.textContent =
                "Baca Pesan";
        }
    }
);