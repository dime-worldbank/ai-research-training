"""Generate QR codes for the links on the "Before the next session" slide.

Requires segno (pip install segno). The SVGs are committed, so ordinary Quarto
renders do not need segno; rerun this script only when a link changes.
"""

from pathlib import Path

import segno

LINKS = {
    "qr-baseline-survey.svg": "https://survey.wb.surveycto.com/collect/ai_bootcamp_pre_survey?caseid=",
    "qr-teams-channel.svg": "https://teams.microsoft.com/l/team/19%3AWSQWckjEYr1wdopHGzlta4n0OUhBgYgBkSPKvZAU2X81%40thread.tacv2/conversations?groupId=c5942f33-8b4c-4896-b91c-c4627e950b69&tenantId=31a2fec0-266b-4c67-b56e-2796d8f59c36",
    "qr-course-website.svg": "https://dime-worldbank.github.io/ai-research-training/bootcamp/",
    "qr-coding-agent-setup.svg": "https://dime-worldbank.github.io/ai-research-training/bootcamp/sessions/day-0/setup-coding-agent/",
}


def main():
    output_dir = Path(__file__).parent / "images"
    for filename, url in LINKS.items():
        qr = segno.make_qr(url, error="m")
        qr.save(output_dir / filename, kind="svg", scale=10, border=2, dark="#000000", light="#ffffff")
        print(f"{filename}: version {qr.version}")


if __name__ == "__main__":
    main()
