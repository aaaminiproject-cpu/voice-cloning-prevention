LABEL_MAP = {
    "bonafide": 0,
    "spoof": 1
}

LABEL_NAMES = {
    0: "Genuine",
    1: "AI Generated"
}


def get_label(label):
    label = str(label).lower().strip()

    if label not in LABEL_MAP:
        raise ValueError(
            f"Unknown audio label: {label}"
        )

    return LABEL_MAP[label]


def get_label_name(label_id):
    return LABEL_NAMES[int(label_id)]
