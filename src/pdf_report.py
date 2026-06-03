from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_pdf(
    result,
    output_path
):

    doc = SimpleDocTemplate(
        output_path
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "INCIDENTGPT REPORT",
            styles['Title']
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Incident Type: {result['incident_type']}",
            styles['BodyText']
        )
    )

    story.append(
        Paragraph(
            f"Severity: {result['severity']}",
            styles['BodyText']
        )
    )

    story.append(
        Paragraph(
            f"Confidence Score: {result['confidence_score']}%",
            styles['BodyText']
        )
    )

    story.append(
        Paragraph(
            f"Summary: {result['summary']}",
            styles['BodyText']
        )
    )

    doc.build(story)