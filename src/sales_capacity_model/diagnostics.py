"""Worksheet 4: why each quality lever is hard to pull, and the root cause.

'Add territories' is deliberately excluded, as in the original: the model
shows it is the weakest lever, and execution guidance would imply otherwise.
"""
from typing import Dict, List, Tuple

Obstacle = Tuple[str, str]  # (obstacle, root cause)

DIAGNOSTICS: Dict[str, List[Obstacle]] = {
    "close_rate": [
        ("Sales people unable to have relevant dialog with key stakeholders",
         "Lack of business context; product-centric rather than outcome-centric"),
        ("Client does not understand proposed value",
         "Feature-focused selling; value not translated into the client's context"),
        ("Product does not meet market needs",
         "Solution built for one context applied to different contexts"),
        ("Out-positioned by competitor",
         "Failure to influence requirements definition early in the cycle"),
        ("No defensible business case",
         "Economic justification not established; competing with other internal projects"),
    ],
    "cycle_time": [
        ("Lack of understanding of the customer's problem-solving lifecycle",
         "Salesperson's process misaligned with the buyer's process"),
        ("Solution complexity is overwhelming",
         "Client cannot see a clear path from current state to future state"),
        ("Sponsor has difficulty selling internally",
         "Champion not equipped with internal selling tools"),
        ("Client confusion about technology, approach or value",
         "Jargon-driven selling; lack of clarity"),
        ("Client lacks urgency",
         "No compelling event; unclear cost of inaction"),
    ],
    "deal_size": [
        ("Poor negotiation",
         "End-of-quarter desperation that professional buyers exploit"),
        ("Product features don't match perceived value",
         "Features optimized for a competitive checklist, not customer value"),
        ("Management desperation to close quarterly revenue",
         "Inadequate pipeline management; late visibility into shortfalls"),
        ("Economic ROI not established",
         "Failure to defend price with quantified value"),
        ("Pricing doesn't align to the value the customer receives",
         "Pricing model disconnected from how the customer realizes benefits"),
    ],
}

LEVER_NAMES = {"close_rate": "Raise close rate", "cycle_time": "Shorten sales cycle",
               "deal_size": "Raise deal size"}


def obstacles(lever: str) -> List[Obstacle]:
    if lever == "territories":
        raise ValueError("No diagnostics for 'territories' by design: it is the weakest lever.")
    if lever not in DIAGNOSTICS:
        raise ValueError(f"Unknown lever '{lever}'. Choose from: {', '.join(DIAGNOSTICS)}")
    return DIAGNOSTICS[lever]
