from pathlib import Path
import sys
import uuid

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image


# ============================================================
# PATH
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"
OUTPUT_DIR = Path("/tmp/secretpix_outputs")
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ============================================================
# IMPORT PROJECT
# ============================================================

from backend.steganography.lsb import (
    sisipkan_lsb,
    ekstrak_lsb
)

from backend.metrics.mse import (
    calculate_mse
)

from backend.metrics.psnr import (
    calculate_psnr
)

from backend.metrics.histogram import (
    generate_histogram_comparison
)

from backend.metrics.enhanced_lsb import (
    visualize_enhanced_lsb
)


# ============================================================
# FLASK
# ============================================================

app = Flask(__name__)

# Maksimal file upload 10 MB
app.config["MAX_CONTENT_LENGTH"] = (
    10 * 1024 * 1024
)

ALLOWED_EXTENSIONS = {
    "png",
    "bmp"
}


# ============================================================
# HELPER
# ============================================================

def allowed_file(filename):
    if "." not in filename:
        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in ALLOWED_EXTENSIONS


# ============================================================
# FRONTEND
# ============================================================

@app.get("/")
def index():
    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


@app.get("/js/<path:filename>")
def javascript_files(filename):
    return send_from_directory(
        FRONTEND_DIR / "js",
        filename
    )


@app.get("/css/<path:filename>")
def css_files(filename):
    return send_from_directory(
        FRONTEND_DIR / "css",
        filename
    )


# ============================================================
# EMBED
# ============================================================

@app.post("/api/embed")
def embed_message():

    input_path = None
    output_path = None
    histogram_path = None

    try:

        # ----------------------------------------------------
        # Ambil data
        # ----------------------------------------------------

        image = request.files.get("image")
        message = request.form.get(
            "message",
            ""
        ).strip()

        stego_key = request.form.get(
            "stego_key",
            ""
        ).strip()

        # ----------------------------------------------------
        # Validasi
        # ----------------------------------------------------

        if image is None:
            return jsonify({
                "success": False,
                "message": "Cover image belum dipilih."
            }), 400

        if not image.filename:
            return jsonify({
                "success": False,
                "message": "Nama file tidak valid."
            }), 400

        if not allowed_file(
            image.filename
        ):
            return jsonify({
                "success": False,
                "message": (
                    "Format gambar harus PNG atau BMP."
                )
            }), 400

        if not message:
            return jsonify({
                "success": False,
                "message": (
                    "Pesan rahasia belum diisi."
                )
            }), 400

        if not stego_key:
            return jsonify({
                "success": False,
                "message": (
                    "Stego-key belum diisi."
                )
            }), 400

        # ----------------------------------------------------
        # Nama file
        # ----------------------------------------------------

        original_name = secure_filename(
            image.filename
        )

        input_filename = (
            f"{uuid.uuid4().hex}_"
            f"{original_name}"
        )

        output_filename = (
            f"stego_"
            f"{uuid.uuid4().hex}.png"
        )

        histogram_filename = (
            f"histogram_"
            f"{uuid.uuid4().hex}.png"
        )

        input_path = (
            OUTPUT_DIR /
            input_filename
        )

        output_path = (
            OUTPUT_DIR /
            output_filename
        )

        histogram_path = (
            OUTPUT_DIR /
            histogram_filename
        )

        # ----------------------------------------------------
        # Simpan cover sementara
        # ----------------------------------------------------

        image.save(
            input_path
        )

        # ----------------------------------------------------
        # Embed
        # LSB + AES + PRNG
        # ----------------------------------------------------

        sisipkan_lsb(
            str(input_path),
            str(output_path),
            message,
            stego_key,
            encrypt=True,
            crypto_algo="aes"
        )

        # ----------------------------------------------------
        # MSE
        # ----------------------------------------------------

        mse_value = calculate_mse(
            str(input_path),
            str(output_path)
        )

        # ----------------------------------------------------
        # PSNR
        # ----------------------------------------------------

        psnr_value = calculate_psnr(
            str(input_path),
            str(output_path)
        )

        # ----------------------------------------------------
        # HISTOGRAM
        # Cover vs Stego
        # ----------------------------------------------------

        generate_histogram_comparison(
            str(input_path),
            str(output_path),
            str(histogram_path)
        )

        # ----------------------------------------------------
        # Hapus cover sementara
        # ----------------------------------------------------

        input_path.unlink(
            missing_ok=True
        )

        input_path = None

        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return jsonify({
            "success": True,
            "message": (
                "Pesan berhasil disisipkan."
            ),
            "stego_image": (
                f"/outputs/{output_filename}"
            ),
            "histogram_image": (
                f"/outputs/{histogram_filename}"
            ),
            "mse": round(
                mse_value,
                6
            ),
            "psnr": round(
                psnr_value,
                4
            )
        })

    except ValueError as error:

        if input_path is not None:
            input_path.unlink(
                missing_ok=True
            )

        if output_path is not None:
            output_path.unlink(
                missing_ok=True
            )

        if histogram_path is not None:
            histogram_path.unlink(
                missing_ok=True
            )

        return jsonify({
            "success": False,
            "message": str(error)
        }), 400

    except Exception as error:

        print(
            "Embed error:",
            error
        )

        if input_path is not None:
            input_path.unlink(
                missing_ok=True
            )

        if output_path is not None:
            output_path.unlink(
                missing_ok=True
            )

        if histogram_path is not None:
            histogram_path.unlink(
                missing_ok=True
            )

        return jsonify({
            "success": False,
            "message": (
                "Terjadi kesalahan saat "
                "proses embedding."
            )
        }), 500


# ============================================================
# EXTRACT
# ============================================================

@app.post("/api/extract")
def extract_message():

    input_path = None

    try:

        # ----------------------------------------------------
        # Ambil data
        # ----------------------------------------------------

        image = request.files.get("image")

        stego_key = request.form.get(
            "stego_key",
            ""
        ).strip()

        # ----------------------------------------------------
        # Validasi
        # ----------------------------------------------------

        if image is None:
            return jsonify({
                "success": False,
                "message": (
                    "Stego image belum dipilih."
                )
            }), 400

        if not image.filename:
            return jsonify({
                "success": False,
                "message": (
                    "Nama file tidak valid."
                )
            }), 400

        if not allowed_file(
            image.filename
        ):
            return jsonify({
                "success": False,
                "message": (
                    "Format gambar harus PNG atau BMP."
                )
            }), 400

        if not stego_key:
            return jsonify({
                "success": False,
                "message": (
                    "Stego-key belum diisi."
                )
            }), 400

        # ----------------------------------------------------
        # Simpan sementara
        # ----------------------------------------------------

        original_name = secure_filename(
            image.filename
        )

        input_filename = (
            f"{uuid.uuid4().hex}_"
            f"{original_name}"
        )

        input_path = (
            OUTPUT_DIR /
            input_filename
        )

        image.save(
            input_path
        )

        # ----------------------------------------------------
        # Extract + decrypt
        # ----------------------------------------------------

        result = ekstrak_lsb(
            str(input_path),
            stego_key,
            decrypt=True
        )

        # ----------------------------------------------------
        # Hapus sementara
        # ----------------------------------------------------

        input_path.unlink(
            missing_ok=True
        )

        input_path = None

        # ----------------------------------------------------
        # Cek hasil
        # ----------------------------------------------------

        if (
            isinstance(result, str)
            and result.startswith("Error")
        ):
            return jsonify({
                "success": False,
                "message": result
            }), 400

        return jsonify({
            "success": True,
            "message": (
                "Pesan berhasil diekstraksi."
            ),
            "data": result
        })

    except Exception as error:

        print(
            "Extract error:",
            error
        )

        if input_path is not None:
            input_path.unlink(
                missing_ok=True
            )

        return jsonify({
            "success": False,
            "message": (
                "Terjadi kesalahan saat "
                "proses extraction."
            )
        }), 500


# ============================================================
# UJI KERAPUHAN JPEG
# ============================================================

@app.post("/api/fragility")
def fragility_test():

    input_path = None
    jpeg_path = None

    try:

        # ----------------------------------------------------
        # Ambil data
        # ----------------------------------------------------

        image = request.files.get("image")

        stego_key = request.form.get(
            "stego_key",
            ""
        ).strip()

        # ----------------------------------------------------
        # Validasi
        # ----------------------------------------------------

        if image is None:
            return jsonify({
                "success": False,
                "message": (
                    "Stego image belum dipilih."
                )
            }), 400

        if not image.filename:
            return jsonify({
                "success": False,
                "message": (
                    "Nama file tidak valid."
                )
            }), 400

        if not allowed_file(
            image.filename
        ):
            return jsonify({
                "success": False,
                "message": (
                    "Stego image harus PNG atau BMP."
                )
            }), 400

        if not stego_key:
            return jsonify({
                "success": False,
                "message": (
                    "Stego-key belum diisi."
                )
            }), 400

        # ----------------------------------------------------
        # Simpan stego sementara
        # ----------------------------------------------------

        original_name = secure_filename(
            image.filename
        )

        input_filename = (
            f"fragility_input_"
            f"{uuid.uuid4().hex}_"
            f"{original_name}"
        )

        jpeg_filename = (
            f"fragility_"
            f"{uuid.uuid4().hex}.jpg"
        )

        input_path = (
            OUTPUT_DIR /
            input_filename
        )

        jpeg_path = (
            OUTPUT_DIR /
            jpeg_filename
        )

        image.save(
            input_path
        )

        # ----------------------------------------------------
        # Simpan ulang sebagai JPEG
        # ----------------------------------------------------

        with Image.open(
            input_path
        ) as img:

            img.convert(
                "RGB"
            ).save(
                jpeg_path,
                format="JPEG",
                quality=90
            )

        # ----------------------------------------------------
        # Coba extract dari JPEG
        # ----------------------------------------------------

        extraction_success = False

        extracted_message = None

        extraction_error = None

        try:

            result = ekstrak_lsb(
                str(jpeg_path),
                stego_key,
                decrypt=True
            )

            if (
                isinstance(result, str)
                and result.startswith("Error")
            ):

                extraction_error = result

            else:

                extraction_success = True

                extracted_message = result

        except Exception as extract_error:

            extraction_error = str(
                extract_error
            )

        # ----------------------------------------------------
        # Hapus input sementara
        # ----------------------------------------------------

        input_path.unlink(
            missing_ok=True
        )

        input_path = None

        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return jsonify({
            "success": True,
            "message": (
                "Uji kerapuhan JPEG selesai."
            ),
            "jpeg_image": (
                f"/outputs/{jpeg_filename}"
            ),
            "extraction_success": (
                extraction_success
            ),
            "extracted_message": (
                extracted_message
            ),
            "extraction_error": (
                extraction_error
            )
        })

    except Exception as error:

        print(
            "Fragility error:",
            error
        )

        if input_path is not None:
            input_path.unlink(
                missing_ok=True
            )

        if jpeg_path is not None:
            jpeg_path.unlink(
                missing_ok=True
            )

        return jsonify({
            "success": False,
            "message": (
                "Terjadi kesalahan saat "
                "uji JPEG."
            )
        }), 500


# ============================================================
# ENHANCED LSB
# ============================================================

@app.post("/api/enhanced-lsb")
def enhanced_lsb_test():

    input_path = None
    output_path = None

    try:

        # ----------------------------------------------------
        # Ambil data
        # ----------------------------------------------------

        image = request.files.get(
            "image"
        )

        # ----------------------------------------------------
        # Validasi
        # ----------------------------------------------------

        if image is None:
            return jsonify({
                "success": False,
                "message": (
                    "Stego image belum dipilih."
                )
            }), 400

        if not image.filename:
            return jsonify({
                "success": False,
                "message": (
                    "Nama file tidak valid."
                )
            }), 400

        if not allowed_file(
            image.filename
        ):
            return jsonify({
                "success": False,
                "message": (
                    "Format gambar harus PNG atau BMP."
                )
            }), 400

        # ----------------------------------------------------
        # Nama file
        # ----------------------------------------------------

        original_name = secure_filename(
            image.filename
        )

        input_filename = (
            f"lsb_input_"
            f"{uuid.uuid4().hex}_"
            f"{original_name}"
        )

        output_filename = (
            f"enhanced_lsb_"
            f"{uuid.uuid4().hex}.png"
        )

        input_path = (
            OUTPUT_DIR /
            input_filename
        )

        output_path = (
            OUTPUT_DIR /
            output_filename
        )

        # ----------------------------------------------------
        # Simpan sementara
        # ----------------------------------------------------

        image.save(
            input_path
        )

        # ----------------------------------------------------
        # Generate Enhanced LSB
        # ----------------------------------------------------

        visualize_enhanced_lsb(
            str(input_path),
            str(output_path),
            bit_plane=0
        )

        # ----------------------------------------------------
        # Hapus input sementara
        # ----------------------------------------------------

        input_path.unlink(
            missing_ok=True
        )

        input_path = None

        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return jsonify({
            "success": True,
            "message": (
                "Analisis Enhanced LSB selesai."
            ),
            "enhanced_lsb_image": (
                f"/outputs/{output_filename}"
            )
        })

    except Exception as error:

        print(
            "Enhanced LSB error:",
            error
        )

        if input_path is not None:
            input_path.unlink(
                missing_ok=True
            )

        if output_path is not None:
            output_path.unlink(
                missing_ok=True
            )

        return jsonify({
            "success": False,
            "message": (
                "Terjadi kesalahan saat "
                "analisis Enhanced LSB."
            )
        }), 500


# ============================================================
# OUTPUT FILE
# ============================================================

@app.get("/outputs/<filename>")
def get_output(filename):

    return send_from_directory(
        OUTPUT_DIR,
        filename
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )