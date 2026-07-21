# V4.0 Validation Copy

Validate in order:

```bash
python3 scripts/check_scope_intake.py /path/to/case
python3 scripts/check_business_blueprint.py /path/to/case
python3 scripts/check_page_state_contract.py /path/to/case
python3 scripts/check_blueprint_implementation.py /path/to/case
python3 scripts/check_design_intake.py /path/to/case
python3 scripts/check_design_foundation_implementation.py /path/to/case
python3 scripts/check_component_usage.py /path/to/case
python3 scripts/check_representative_layout_review.py /path/to/case
python3 scripts/check_design_acceptance.py /path/to/case
python3 scripts/check_prototype_delivery_bundle.py /path/to/case
```

The final delivery includes the exact confirmed scope, business blueprint, page-state contract, separate design intake, component-usage manifest, pre-acceptance Chrome layout report, user acceptance of representative screens, protected runtime, branded prototype, visual token, and final visible-Chrome acceptance bound to the HTML hash.
