from colorama import Fore, Style

def pretty_print_analysis(analysis: dict, severity: int):
    print("\n" + "-"*50)

    # --- Severity section ---
    severity_labels = {
        1: (Fore.GREEN, "🟢 Low"),
        2: (Fore.YELLOW, "🟡 Medium"),
        3: (Fore.RED, "🔴 High")
    }
    sev_color, sev_label = severity_labels.get(severity, (Fore.WHITE, "Unknown"))
    print(sev_color + f"🔎 Severity Level: {sev_label}" + Style.RESET_ALL)

    # --- Gemini Analysis ---
    if "error" in analysis:
        print(Fore.RED + "⚠️ Error parsing Gemini response" + Style.RESET_ALL)
        print("Raw output:", analysis.get("raw"))
        print("-"*50)
        return

    # Threat type
    print(Fore.RED + "⚠️  Threat Type:  " + Style.RESET_ALL + analysis.get("threat_type", "Unknown"))

    # Known attack
    known = analysis.get("known_attack", "Unknown")
    color = Fore.GREEN if known.lower() == "yes" else Fore.YELLOW
    print(color + "✅ Known Attack:  " + Style.RESET_ALL + known)

    # Recommended actions
    print("\n🔒 Recommended Actions:")
    actions = analysis.get("recommended_actions", [])
    for i, act in enumerate(actions, 1):
        print(f"   {i}. {act}")

    print("-"*50)
