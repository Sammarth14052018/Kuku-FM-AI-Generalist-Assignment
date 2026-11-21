"""Shared vocabulary and evidence checks for pitch annotations."""
LABELS = {
    "twist_type": "hidden_identity imposter_takes_place secret_baby contract_marriage revenge_return fake_death inheritance_secret mistaken_identity betrayal_by_ally supernatural_reveal other".split(),
    "hero_role_group": "corporate_executive corporate_staff founder_ceo heir_family service_worker student creative_artist supernatural_being legal_medical other".split(),
    "setting_group": "us_city_named small_town corporate_office mansion_estate fantasy_world other".split(),
    "cliffhanger_type": "reveal confrontation_slap threat arrival betrayal choice_ultimatum other".split(),
}
FIELDS = (*LABELS, "city")
SHORT = ("city", "hero_job", "villain", "secret")
COLUMNS = ("number", "logline", *LABELS, *SHORT, "evidence")


def check(condition, message):
    if not condition:
        raise ValueError(message)


def validate(row):
    for key, allowed in LABELS.items():
        check(row[key] in [*allowed, "unknown"], f"Invalid {key}")
    for key in SHORT:
        check(isinstance(row[key], str) and 1 <= len(row[key].split()) <= 6, f"Invalid {key}")
    quote = row["evidence"]
    check(quote and (quote in row["logline"] or
          (quote == "unknown" and row["twist_type"] == "unknown")), "Unsupported twist evidence")
