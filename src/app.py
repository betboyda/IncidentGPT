from flask import (
    Flask,
    render_template,
    request,
    send_file
)

import os
import time

from preprocessing import (
    read_log_file,
    build_log_context_for_llm
)

from llm_module import (
    analyze_text_only,
    analyze_multimodal
)

from vision_module import (
    preprocess_image
)

from log_parser import (
    parse_log,
    detect_brute_force
)

from db_manager import (
    init_db,
    save_incident
)

from mitre_mapper import (
    map_to_mitre
)

from pdf_report import (
    generate_pdf
)

# ---------------------------------------------------
# FLASK
# ---------------------------------------------------

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# ---------------------------------------------------
# PDF CACHE
# ---------------------------------------------------

latest_result = {}

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

@app.route("/", methods=["GET"])
def upload_form():

    return render_template(
        "upload.html"
    )

# ---------------------------------------------------
# ANALYZE
# ---------------------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    global latest_result

    start_time = time.time()

    log_file = request.files.get(
        "log_file"
    )

    log_text_manual = request.form.get(
        "log_text",
        ""
    ).strip()

    image_file = request.files.get(
        "image_file"
    )

    log_text = ""

    image_ocr_text = ""

    is_multimodal = False

    # ---------------------------------------------------
    # LOG INPUT
    # ---------------------------------------------------

    if log_file and log_file.filename:

        upload_dir = os.path.join(
            "data",
            "uploads"
        )

        os.makedirs(
            upload_dir,
            exist_ok=True
        )

        temp_path = os.path.join(
            upload_dir,
            log_file.filename
        )

        log_file.save(temp_path)

        log_text = read_log_file(
            temp_path
        )

    elif log_text_manual:

        log_text = log_text_manual

    # ---------------------------------------------------
    # NO LOG
    # ---------------------------------------------------

    if not log_text:

        return render_template(

            "results.html",

            error="Herhangi bir log girişi yapılmadı.",

            result=None,

            raw_log=""
        )

    # ---------------------------------------------------
    # LOG CONTEXT
    # ---------------------------------------------------

    log_context = (
        build_log_context_for_llm(
            log_text
        )
    )

    # ---------------------------------------------------
    # STRUCTURED PARSING
    # ---------------------------------------------------

    parsed_logs = parse_log(
        log_context
    )

    brute_force = detect_brute_force(
        parsed_logs
    )

    # ---------------------------------------------------
    # MULTIMODAL
    # ---------------------------------------------------

    if image_file and image_file.filename:

        img_dir = os.path.join(
            "data",
            "uploads"
        )

        os.makedirs(
            img_dir,
            exist_ok=True
        )

        img_path = os.path.join(
            img_dir,
            image_file.filename
        )

        image_file.save(img_path)

        # OCR
        image_ocr_text = preprocess_image(
            img_path
        )

        # ANALYZE
        result = analyze_multimodal(
            log_context,
            image_ocr_text
        )

        is_multimodal = True

    # ---------------------------------------------------
    # TEXT ONLY
    # ---------------------------------------------------

    else:

        result = analyze_text_only(
            log_context
        )

    # ---------------------------------------------------
    # BRUTE FORCE OVERRIDE
    # ---------------------------------------------------

    if brute_force:

        result["incident_type"] = (
            "brute_force_attack"
        )

        result["severity"] = "high"

        result["summary"] = (
            "Çoklu başarısız giriş "
            "denemeleri nedeniyle "
            "brute force saldırısı "
            "tespit edildi."
        )

        result["confidence_score"] = 96

        result["mitre"] = {

            "id": "T1110",

            "name": "Brute Force"
        }

    # ---------------------------------------------------
    # EXTRA FINDINGS
    # ---------------------------------------------------

    extra_findings = []

    if brute_force:

        for attack in brute_force:

            extra_findings.append(

                f"Brute force şüphesi: "
                f"{attack['ip']} adresinden "
                f"{attack['attempts']} başarısız giriş denemesi tespit edildi."
            )

    # ---------------------------------------------------
    # MITRE
    # ---------------------------------------------------

    if "mitre" not in result:

        mitre = map_to_mitre(
            result.get(
                "incident_type",
                "unknown"
            )
        )

        result["mitre"] = mitre

    else:

        mitre = result["mitre"]

    # ---------------------------------------------------
    # TIME
    # ---------------------------------------------------

    inference_time = round(
        time.time() - start_time,
        2
    )

    # ---------------------------------------------------
    # RESULT TABLE
    # ---------------------------------------------------

    result_table = {

        "Model Used": result.get(
            "model_used",
            "Unknown"
        ),

        "Incident Type": result.get(
            "incident_type",
            "unknown"
        ),

        "Severity": result.get(
            "severity",
            "medium"
        ),

        "MITRE ATT&CK": (
            f"{mitre['id']} - {mitre['name']}"
        ),

        "Confidence Score": (
            f"{result.get('confidence_score', 0)}%"
        ),

        "Inference Time": (
            f"{inference_time} sec"
        ),

        "Parsed Logs": len(
            parsed_logs
        ),

        "Correlation Alerts": len(
            brute_force
        ),

        "Multimodal": (
            "Yes"
            if is_multimodal
            else "No"
        )
    }

    # ---------------------------------------------------
    # FINDINGS
    # ---------------------------------------------------

    if "diagram_observations" not in result:

        result["diagram_observations"] = []

    result["diagram_observations"].extend(
        extra_findings
    )

    # ---------------------------------------------------
    # PDF CACHE
    # ---------------------------------------------------

    latest_result = result

    # ---------------------------------------------------
    # DB SAVE
    # ---------------------------------------------------

    try:

        save_incident(

            incident_type=result.get(
                "incident_type",
                "unknown"
            ),

            severity=result.get(
                "severity",
                "medium"
            ),

            raw_log=log_context,

            is_multimodal=is_multimodal,

            inference_time=inference_time,

            diagram_observations=result.get(
                "diagram_observations",
                []
            ),

            actions=result.get(
                "actions",
                []
            ),

            confidence_score=result.get(
                "confidence_score",
                0
            ),

            mitre_id=mitre.get(
                "id",
                "Unknown"
            ),

            mitre_name=mitre.get(
                "name",
                "Unknown"
            )
        )

    except Exception as e:

        print(
            "[WARN] DB kayıt hatası:",
            e
        )

    # ---------------------------------------------------
    # RETURN
    # ---------------------------------------------------

    return render_template(

        "results.html",

        result=result,

        raw_log=log_context,

        result_table=result_table
    )

# ---------------------------------------------------
# PDF EXPORT
# ---------------------------------------------------

@app.route("/download-report")
def download_report():

    output_path = (
        "incident_report.pdf"
    )

    generate_pdf(
        latest_result,
        output_path
    )

    return send_file(
        output_path,
        as_attachment=True
    )

# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    init_db()

    app.run(debug=True)