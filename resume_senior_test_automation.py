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


FINAL_PDF_PATH = "Jace_Romero_Senior_Test_Automation_Engineer_Resume.pdf"


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
        "Senior QA Automation Engineer with deep experience in test automation, CI/CD, and release quality, plus hands-on project experience across platform and application infrastructure. "
        "Strongest in automation strategy, end-to-end testing, developer workflow improvements, and quality ownership across complex systems.",
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
        "Built and maintained a multi-service application spanning a Go backend, Svelte frontend, Discord bot, PostgreSQL, and NATS-based messaging.",
        "Drove quality and delivery improvements across frontend, backend, and bot workflows by tightening event contracts, admin tooling, and cross-service request flows.",
        "Built and owned the CI/CD, GitOps, and observability work needed to support the project using Kubernetes, ArgoCD, Grafana, OpenTelemetry, and deployment validation scripts.",
        "Structured implementation work to stay modular and repeatable, which made AI-assisted code generation, refactoring, and follow-on feature work more effective.",
    ],
    styles["JobDetails"],
)
elements.append(Spacer(1, 6))
elements.append(horizontal_rule())
elements.append(Spacer(1, 6))

elements.append(Paragraph("Work Experience", styles["Header"]))

jobs = [
    (
        "Sr. QA Automation Engineer",
        "Bold Penguin, Inc | October 2023 – July 2024",
        [
            "Implemented modular test architecture using the Page Object Model, improving maintainability and readability across automated coverage.",
            "Optimized GitHub Actions workflows with targeted execution patterns and CI improvements to reduce unnecessary test time and resource usage.",
            "Mentored engineers on automation design, CI/CD practices, and building quality into daily development workflows.",
        ],
    ),
    (
        "QA Engineer",
        "WorkStep | February 2022 – September 2022",
        [
            "Expanded a minimal automation suite into 100+ tests covering core application workflows.",
            "Served as the primary QA partner across teams, introducing scalable test practices and coaching engineers on testable design.",
            "Integrated automated quality gates into CircleCI to strengthen release confidence and reduce manual verification overhead.",
        ],
    ),
    (
        "Software QA Engineer",
        "CenterEdge | May 2021 – February 2022",
        [
            "Migrated front-end coverage from TestCafe to Cypress, improving suite reliability while expanding UI and API test coverage.",
            "Integrated automated checks into release workflows and pre-deployment gates to improve production readiness.",
        ],
    ),
    (
        "QA Automation Engineer",
        "Edquity | June 2020 – February 2021",
        [
            "Introduced parallel automated test execution in GitLab CI and helped improve team delivery processes.",
            "Balanced QA automation ownership with sprint facilitation, standups, and day-to-day process coordination.",
        ],
    ),
    (
        "QA Automation Engineer",
        "EverlyWell | June 2018 – September 2019",
        [
            "Built and scaled the team’s first automation suite using WATIR, later migrating to Cypress with Applitools.",
            "Integrated automated testing into Jenkins, TravisCI, and AWS CodeBuild workflows for repeatable release validation.",
            "Authored UI and API test coverage that contributed to a 40% reduction in post-deploy incidents.",
        ],
    ),
    (
        "Earlier Experience",
        "SpeakWrite and Trion Worlds | 2013 – 2018",
        [
            "Built foundational Selenium and Python-based automation, reduced manual regression effort, and supported release quality across internal and customer-facing systems.",
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
<b>Test Automation:</b> Cypress, Selenium, WATIR, Postman, REST Assured, UI/API/E2E testing, test strategy, quality gates<br/>
<b>CI/CD:</b> GitHub Actions, GitLab CI, Jenkins, CircleCI, TravisCI, Spinnaker, AWS CodeBuild<br/>
<b>Programming:</b> Python, JavaScript, TypeScript, Go, Bash<br/>
<b>Platform Exposure:</b> GCP, OCI, Kubernetes, Docker, ArgoCD, Helm, Terraform, GitOps<br/>
<b>Observability:</b> Grafana, OpenTelemetry, Prometheus/Mimir, Loki, Tempo<br/>
<b>Systems:</b> PostgreSQL, NATS, event-driven workflows<br/>
<b>AI-Assisted Engineering:</b> Claude Code, Codex, Gemini for code generation, refactoring, debugging, test authoring, and documentation in modular, reusable workflows
"""
elements.append(Paragraph(skills_text, styles["Skills"]))

doc.build(elements)
print(f"Resume saved to {FINAL_PDF_PATH}")
