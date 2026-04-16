from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


FINAL_PDF_PATH = "Jace_Romero_Platform_Cloud_Infra_Resume.pdf"


def horizontal_rule() -> Table:
    return Table(
        [[""]],
        colWidths=[7.2 * inch],
        style=TableStyle([("LINEBELOW", (0, 0), (-1, -1), 1, colors.black)]),
    )


def add_bullets(elements: list, bullets: list[str], style: ParagraphStyle) -> None:
    for bullet in bullets:
        elements.append(Paragraph(f"• {bullet}", style))


doc = SimpleDocTemplate(
    FINAL_PDF_PATH,
    pagesize=letter,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40,
)

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="Header",
        fontSize=14,
        leading=16,
        spaceAfter=10,
        spaceBefore=10,
        fontName="Helvetica-Bold",
    )
)
styles.add(
    ParagraphStyle(
        name="JobTitle",
        fontSize=11,
        leading=14,
        fontName="Helvetica-Bold",
    )
)
styles.add(
    ParagraphStyle(
        name="JobDetails",
        fontSize=9.5,
        leading=12.5,
        leftIndent=10,
        spaceAfter=1,
    )
)
styles.add(
    ParagraphStyle(
        name="Skills",
        fontSize=10,
        leading=13.5,
        spaceAfter=6,
    )
)

elements = []

elements.append(Paragraph("Jace Romero", styles["Title"]))
elements.append(
    Paragraph(
        "Brooklyn, NY 11215 | romero.jace@gmail.com | +1 956 346 4849",
        styles["Normal"],
    )
)
elements.append(
    Paragraph(
        "GitHub: https://github.com/Romero-jace | Projects: https://github.com/orgs/Black-And-White-Club/repositories",
        styles["Normal"],
    )
)
elements.append(Spacer(1, 10))
elements.append(horizontal_rule())
elements.append(Spacer(1, 6))

elements.append(Paragraph("Profile", styles["Header"]))
elements.append(
    Paragraph(
        "Engineer with senior QA automation experience and hands-on platform, cloud, and infrastructure project work. "
        "Built independent project experience across Kubernetes, ArgoCD, Terraform, Docker, Grafana, OpenTelemetry, PostgreSQL, and NATS, with a focus on delivery reliability, GitOps, observability, and automation.",
        styles["Normal"],
    )
)
elements.append(Spacer(1, 6))
elements.append(horizontal_rule())
elements.append(Spacer(1, 6))

elements.append(Paragraph("Independent Project", styles["Header"]))
elements.append(Paragraph("Independent Application Platform | 2025–Present", styles["JobTitle"]))
add_bullets(
    elements,
    [
        "Built and maintained a multi-service application stack using Go, Svelte, PostgreSQL, NATS, and containerized services deployed through GitOps workflows.",
        "Built and owned the infrastructure and delivery workflows across Kubernetes manifests, ArgoCD applications, Kustomize overlays, Helm values, image update automation, and deployment validation scripts.",
        "Added observability instrumentation and monitoring workflows using OpenTelemetry, Grafana, Prometheus/Mimir, Loki, and Tempo.",
        "Used strong QA automation and release engineering practices to improve deployment confidence, workflow resilience, and cross-service change safety.",
        "Structured implementation work to stay modular and repeatable, which made AI-assisted code generation, refactoring, and follow-on delivery work more effective.",
    ],
    styles["JobDetails"],
)
elements.append(Spacer(1, 6))
elements.append(horizontal_rule())
elements.append(Spacer(1, 6))

elements.append(Paragraph("Relevant Experience", styles["Header"]))

jobs = [
    (
        "Sr. QA Automation Engineer",
        "Bold Penguin, Inc | October 2023 – July 2024",
        [
            "Optimized GitHub Actions workflows and CI execution patterns to improve efficiency and release reliability.",
            "Collaborated on Kubernetes-based environments and infrastructure-adjacent developer workflows supporting dev/test delivery.",
            "Mentored engineers on automation, CI/CD, and maintainable delivery practices.",
        ],
    ),
    (
        "QA Engineer",
        "WorkStep | February 2022 – September 2022",
        [
            "Integrated automated quality gates into CircleCI workflows and supported environment configuration for reliable test execution.",
            "Expanded automated coverage to 100+ tests while helping teams adopt scalable quality and release practices.",
        ],
    ),
    (
        "Software QA Engineer",
        "CenterEdge | May 2021 – February 2022",
        [
            "Improved deployment readiness by integrating automated coverage into release workflows and pre-deployment checks.",
            "Assisted in CI and container-based workflow optimizations to improve build reuse and consistency.",
        ],
    ),
    (
        "QA Automation Engineer",
        "Edquity | June 2020 – February 2021",
        [
            "Used GitLab CI, Terraform, and basic Kubernetes tooling to support ephemeral test environments and automation workflows.",
        ],
    ),
    (
        "QA Automation Engineer",
        "EverlyWell | June 2018 – September 2019",
        [
            "Integrated automation into Jenkins, TravisCI, and AWS CodeBuild to improve release consistency and build confidence.",
        ],
    ),
]

for title, company, bullets in jobs:
    job_block = [
        Paragraph(title, styles["JobTitle"]),
        Paragraph(company, styles["Normal"]),
    ]
    for bullet in bullets:
        job_block.append(Paragraph(f"• {bullet}", styles["JobDetails"]))
    job_block.append(Spacer(1, 5))
    elements.append(KeepTogether(job_block))

elements.append(horizontal_rule())
elements.append(Spacer(1, 6))

elements.append(Paragraph("Skills", styles["Header"]))
skills_text = """
<b>Cloud & Platform:</b> GCP, OCI, Kubernetes, Docker, ArgoCD, Kustomize, Helm, Terraform, GitOps<br/>
<b>Observability:</b> Grafana, OpenTelemetry, Prometheus/Mimir, Loki, Tempo<br/>
<b>CI/CD & Automation:</b> GitHub Actions, GitLab CI, Jenkins, CircleCI, TravisCI, Spinnaker, AWS CodeBuild<br/>
<b>Programming:</b> Go, TypeScript, Python, JavaScript, Bash<br/>
<b>Systems:</b> PostgreSQL, NATS, event-driven systems, deployment validation, release safety automation<br/>
<b>Quality Engineering:</b> Test automation, quality gates, E2E/API testing, developer workflow improvements<br/>
<b>AI-Assisted Engineering:</b> Claude Code, Codex, Gemini for code generation, refactoring, debugging, test authoring, and documentation in modular, reusable workflows
"""
elements.append(Paragraph(skills_text, styles["Skills"]))

doc.build(elements)
print(f"Resume saved to {FINAL_PDF_PATH}")
