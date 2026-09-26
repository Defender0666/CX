import json
from urllib.parse import urlparse

import flet as ft


APP_NAME = "Career OS Ultimate by Maccy Creations"
DEVELOPER = "SAKET YADAV"
COMPANY = "MACCY CREATIONS"
STORAGE_KEY = "maccy.careeros.applications.v1"
STAGES = ["Saved / Wishlist", "Applied", "Interview Scheduled", "Offer Received", "Rejected"]

CAREER_PATHS = [
    {
        "title": "Identity & Access Management",
        "summary": "Design and operate identity lifecycle, authentication, authorization, and access-governance processes.",
        "skills": "RBAC · SSO · MFA · Entra ID · IAM governance",
    },
    {
        "title": "Active Directory Administration",
        "summary": "Maintain directory services, users and groups, Group Policy, authentication, and hybrid identity.",
        "skills": "AD DS · DNS · Group Policy · PowerShell · Entra ID",
    },
    {
        "title": "System Administration",
        "summary": "Operate server and endpoint environments, patching, backups, monitoring, and incident response.",
        "skills": "Windows Server · Linux · Monitoring · Automation",
    },
    {
        "title": "IT Help Desk & Service Desk",
        "summary": "Resolve user incidents and service requests, document solutions, and meet support service levels.",
        "skills": "ITIL · Ticketing · Troubleshooting · Documentation",
    },
    {
        "title": "IT Infrastructure Support",
        "summary": "Support enterprise networks, endpoints, servers, and access services with reliable escalation.",
        "skills": "Networking · Endpoint support · Identity · Incident management",
    },
]


def _load_applications(page: ft.Page) -> list[dict[str, str]]:
    stored = page.client_storage.get(STORAGE_KEY)
    if not stored:
        return []
    try:
        records = json.loads(stored)
    except (TypeError, json.JSONDecodeError):
        return []
    if not isinstance(records, list):
        return []
    return [
        record
        for record in records
        if isinstance(record, dict)
        and all(isinstance(record.get(key), str) for key in ("title", "company", "stage"))
    ]


def main(page: ft.Page) -> None:
    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.padding = 18
    applications = _load_applications(page)
    current_view = "Home"

    def persist_applications() -> None:
        page.client_storage.set(STORAGE_KEY, json.dumps(applications))

    def card(title: str, content: ft.Control) -> ft.Control:
        return ft.Container(
            content=ft.Column(
                [ft.Text(title, size=18, weight=ft.FontWeight.BOLD), content],
                spacing=10,
            ),
            padding=16,
            border_radius=14,
            bgcolor=ft.Colors.BLUE_GREY_800,
        )

    def show_view(view: str) -> None:
        nonlocal current_view
        current_view = view
        render()

    def advance_stage(index: int) -> None:
        record = applications[index]
        stage_index = STAGES.index(record["stage"]) if record["stage"] in STAGES else 0
        record["stage"] = STAGES[(stage_index + 1) % len(STAGES)]
        persist_applications()
        render()

    def render_home() -> ft.Control:
        interview_count = sum(record["stage"] == "Interview Scheduled" for record in applications)
        offers_count = sum(record["stage"] == "Offer Received" for record in applications)
        return ft.Column(
            [
                ft.Text("Your career workspace", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Explore technical career paths and track opportunities you have verified yourself.",
                    color=ft.Colors.BLUE_GREY_100,
                ),
                card(
                    "Applications",
                    ft.Text(str(len(applications)), size=30, weight=ft.FontWeight.BOLD),
                ),
                card(
                    "Interviews scheduled",
                    ft.Text(str(interview_count), size=30, weight=ft.FontWeight.BOLD),
                ),
                card(
                    "Offers received",
                    ft.Text(str(offers_count), size=30, weight=ft.FontWeight.BOLD),
                ),
                card(
                    "Resume drafts",
                    ft.Text("0", size=30, weight=ft.FontWeight.BOLD),
                ),
                ft.Text(
                    "Offline-first: tracker records are stored on this device. "
                    "No cloud account or API key is required.",
                    size=12,
                    color=ft.Colors.BLUE_GREY_200,
                ),
            ],
            spacing=14,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def render_careers() -> ft.Control:
        return ft.Column(
            [
                ft.Text("Career paths", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Role and skill guidance only—not live vacancies or salary claims.",
                    color=ft.Colors.BLUE_GREY_100,
                ),
                *[
                    card(
                        role["title"],
                        ft.Column(
                            [
                                ft.Text(role["summary"]),
                                ft.Text(role["skills"], color=ft.Colors.CYAN_200),
                            ],
                            spacing=8,
                        ),
                    )
                    for role in CAREER_PATHS
                ],
            ],
            spacing=14,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def render_jobs() -> ft.Control:
        return ft.Column(
            [
                ft.Text("Live jobs", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Text(
                        "No verified live job listings are available in this offline-first build.",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=24,
                    border_radius=14,
                    bgcolor=ft.Colors.BLUE_GREY_800,
                ),
                ft.Text(
                    "Only verified job listings should be added. This build does not "
                    "invent vacancies, compensation, or employer requirements.",
                    size=12,
                    color=ft.Colors.BLUE_GREY_200,
                ),
            ],
            spacing=14,
            expand=True,
        )

    def render_tracker() -> ft.Control:
        title_input = ft.TextField(label="Verified job title")
        company_input = ft.TextField(label="Company")
        url_input = ft.TextField(label="Official application URL (optional)")
        feedback = ft.Text("", color=ft.Colors.AMBER_200)

        def add_application(_: ft.ControlEvent) -> None:
            title = (title_input.value or "").strip()
            company = (company_input.value or "").strip()
            url = (url_input.value or "").strip()
            if not title or not company:
                feedback.value = "Enter both the verified job title and company."
                page.update()
                return
            if url:
                parsed = urlparse(url)
                if parsed.scheme != "https" or not parsed.netloc:
                    feedback.value = "Use a complete official HTTPS application URL."
                    page.update()
                    return
            applications.insert(
                0,
                {
                    "title": title,
                    "company": company,
                    "url": url,
                    "stage": "Saved / Wishlist",
                },
            )
            persist_applications()
            render()

        records: list[ft.Control] = []
        if not applications:
            records.append(
                ft.Text("No applications saved yet.", color=ft.Colors.BLUE_GREY_200)
            )
        for index, record in enumerate(applications):
            records.append(
                card(
                    record["title"],
                    ft.Column(
                        [
                            ft.Text(record["company"]),
                            ft.Text(f"Stage: {record['stage']}", color=ft.Colors.CYAN_200),
                            ft.OutlinedButton(
                                "Advance stage",
                                on_click=lambda _, item_index=index: advance_stage(item_index),
                            ),
                        ],
                        spacing=8,
                    ),
                )
            )
        return ft.Column(
            [
                ft.Text("Application tracker", size=24, weight=ft.FontWeight.BOLD),
                title_input,
                company_input,
                url_input,
                ft.FilledButton("Save verified application", on_click=add_application),
                feedback,
                *records,
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def render() -> None:
        page.controls.clear()
        page.add(
            ft.Column(
                [
                    ft.Text(APP_NAME, size=22, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        f"{DEVELOPER} · {COMPANY}",
                        size=12,
                        color=ft.Colors.CYAN_200,
                    ),
                    ft.Row(
                        [
                            ft.TextButton("Home", on_click=lambda _: show_view("Home")),
                            ft.TextButton("Careers", on_click=lambda _: show_view("Careers")),
                            ft.TextButton("Live Jobs", on_click=lambda _: show_view("Live Jobs")),
                            ft.TextButton("Tracker", on_click=lambda _: show_view("Tracker")),
                        ],
                        wrap=True,
                    ),
                    ft.Divider(),
                    render_home()
                    if current_view == "Home"
                    else render_careers()
                    if current_view == "Careers"
                    else render_jobs()
                    if current_view == "Live Jobs"
                    else render_tracker(),
                ],
                spacing=12,
                expand=True,
            )
        )
        page.update()

    render()


ft.run(main)
