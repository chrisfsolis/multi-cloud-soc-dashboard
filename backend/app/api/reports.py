from fastapi import APIRouter
from app.demo_data import DEMO_DATA_NOTICE

router = APIRouter(tags=["reports"])


@router.get("/reports/executive-summary")
def executive_summary():
    return {
        "synthetic_data": True,
        "notice": DEMO_DATA_NOTICE,
        "title": "Executive SOC Summary",
        "summary": "The demo SOC is tracking credential misuse, storage exposure, and risky network changes across AWS, Azure, and GCP.",
        "business_risk": "Critical cloud identity activity is the top priority; public storage exposure is being remediated through a standard playbook.",
        "recommended_actions": [
            "Review privileged cloud identities and rotate demo access keys.",
            "Validate storage guardrails across all cloud providers.",
            "Use incident timelines as evidence for GRC and audit conversations.",
        ],
    }
