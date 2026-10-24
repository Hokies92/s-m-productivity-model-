"""Command line interface: `scm` (or `python -m sales_capacity_model`)."""
from __future__ import annotations

import argparse
import json
import sys

from . import __about__
from .diagnostics import DIAGNOSTICS, LEVER_NAMES, obstacles
from .engine import run_scenarios
from .inputs import RAMP_RULES, Adjustments, ModelInputs, ModelOptions
from .report import json_report, text_report
from .verify import verify


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="scm", description=__about__.__summary__)
    p.add_argument("--version", action="version", version=f"%(prog)s {__about__.__version__}")
    sub = p.add_subparsers(dest="command")

    sub.add_parser("about", help="What this project is and where it came from")
    sub.add_parser("overview", help="Product overview: who it's for, inputs, outputs, usage")
    sub.add_parser("template", help="Print default inputs as JSON to edit")
    sub.add_parser("verify", help="Check the engine against the original workbook")

    d = sub.add_parser("diagnose", help="Obstacles and root causes for a quality lever")
    d.add_argument("lever", choices=list(DIAGNOSTICS))

    r = sub.add_parser("run", help="Run all scenarios")
    r.add_argument("--inputs", help="JSON file of inputs (any subset of `scm template`)")
    r.add_argument("--set", action="append", default=[], metavar="FIELD=VALUE",
                   help="Override one input, e.g. --set close_rate=0.3 (repeatable)")
    r.add_argument("--adjust", type=float, help="Same change for every lever, e.g. 0.15")
    for lever in ("territories", "close_rate", "cycle_time", "deal_size"):
        r.add_argument(f"--adjust-{lever.replace('_', '-')}", type=float, dest=f"adj_{lever}")
    r.add_argument("--ramp-rule", choices=RAMP_RULES, default="workbook")
    r.add_argument("--use-entered-salary", action="store_true",
                   help="Use base salary x (1 + load rate) instead of the workbook's 87,750")
    r.add_argument("--json", action="store_true", help="Output JSON")
    return p


def _load_inputs(args) -> ModelInputs:
    data = {}
    if args.inputs:
        with open(args.inputs) as f:
            data.update(json.load(f))
    for item in args.set:
        key, _, val = item.partition("=")
        data[key.strip()] = None if val.strip().lower() in ("none", "null", "") else float(val)
    return ModelInputs.from_dict(data)


def _build_options(args) -> ModelOptions:
    adj = Adjustments.uniform(args.adjust) if args.adjust is not None else Adjustments()
    for lever in ("territories", "close_rate", "cycle_time", "deal_size"):
        v = getattr(args, f"adj_{lever}")
        if v is not None:
            setattr(adj, lever, v)
    return ModelOptions(use_entered_salary=args.use_entered_salary,
                        ramp_rule=args.ramp_rule, adjustments=adj)


def main(argv=None) -> int:
    args = _build_parser().parse_args(argv)
    cmd = args.command or "about"
    try:
        if cmd == "about":
            print(__about__.ABOUT)
        elif cmd == "overview":
            print(__about__.OVERVIEW)
        elif cmd == "template":
            print(json.dumps(ModelInputs().to_dict(), indent=2))
        elif cmd == "diagnose":
            print(f"{LEVER_NAMES[args.lever]}: common obstacles\n")
            for n, (obs, cause) in enumerate(obstacles(args.lever), 1):
                print(f"  {n}. {obs}\n     Root cause: {cause}")
        elif cmd == "verify":
            checks = verify()
            for c in checks:
                print(f"  {'OK ' if c.ok else 'BAD'} {c.scenario:17}{c.metric:18}"
                      f"workbook={c.workbook:>18,.4f}  engine={c.engine:>18,.4f}")
            passed = sum(c.ok for c in checks)
            print(f"\n{passed}/{len(checks)} workbook outputs reproduced")
            return 0 if passed == len(checks) else 1
        elif cmd == "run":
            inputs, options = _load_inputs(args), _build_options(args)
            results = run_scenarios(inputs, options)
            print(json_report(results, inputs, options) if args.json
                  else text_report(results, inputs, options))
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
