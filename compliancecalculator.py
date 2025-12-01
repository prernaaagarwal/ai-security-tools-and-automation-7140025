# compliance_calculator.py

def cybersecurity_calculator():
    print("\n=== Cybersecurity Compliance Calculator ===")
    score = 0
    max_score = 5

    mfa = input("Do you use Multi-Factor Authentication (yes/no)? ").strip().lower()
    if mfa == "yes": score += 1

    encryption = input("Is sensitive data encrypted at rest and in transit (yes/no)? ").strip().lower()
    if encryption == "yes": score += 1

    ir_plan = input("Do you have a documented incident response plan (yes/no)? ").strip().lower()
    if ir_plan == "yes": score += 1

    monitoring = input("Do you have continuous monitoring for threats (yes/no)? ").strip().lower()
    if monitoring == "yes": score += 1

    backup = input("Do you regularly back up data and test recovery (yes/no)? ").strip().lower()
    if backup == "yes": score += 1

    compliance_percentage = (score / max_score) * 100
    print(f"\nYour Cybersecurity compliance score: {compliance_percentage:.0f}%")

    if compliance_percentage == 100:
        print("Excellent! You are fully compliant with these core controls.")
    else:
        print("Areas to improve:")
        if mfa != "yes": print("- Implement Multi-Factor Authentication")
        if encryption != "yes": print("- Encrypt sensitive data at rest and in transit")
        if ir_plan != "yes": print("- Create a documented incident response plan")
        if monitoring != "yes": print("- Set up continuous monitoring for threats")
        if backup != "yes": print("- Establish regular backups and test recovery")


def data_privacy_calculator():
    print("\n=== Data Privacy Compliance Calculator ===")
    score = 0
    max_score = 5

    consent = input("Do you obtain user consent before collecting personal data (yes/no)? ").strip().lower()
    if consent == "yes": score += 1

    retention = input("Do you have a clear data retention policy (yes/no)? ").strip().lower()
    if retention == "yes": score += 1

    access = input("Can users access and request deletion of their data (yes/no)? ").strip().lower()
    if access == "yes": score += 1

    breach = input("Do you notify users within 72 hours of a data breach (yes/no)? ").strip().lower()
    if breach == "yes": score += 1

    training = input("Do employees receive regular privacy training (yes/no)? ").strip().lower()
    if training == "yes": score += 1

    compliance_percentage = (score / max_score) * 100
    print(f"\nYour Data Privacy compliance score: {compliance_percentage:.0f}%")

    if compliance_percentage == 100:
        print("Excellent! You are fully compliant with these privacy controls.")
    else:
        print("Areas to improve:")
        if consent != "yes": print("- Obtain user consent before collecting personal data")
        if retention != "yes": print("- Establish a clear data retention policy")
        if access != "yes": print("- Allow users to access and delete their data")
        if breach != "yes": print("- Notify users within 72 hours of a data breach")
        if training != "yes": print("- Provide regular privacy training to employees")


def main():
    while True:
        print("\n=== Compliance Calculator Menu ===")
        print("1. Cybersecurity Compliance")
        print("2. Data Privacy Compliance")
        print("3. Exit")

        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            cybersecurity_calculator()
        elif choice == "2":
            data_privacy_calculator()
        elif choice == "3":
            print("Exiting Compliance Calculator. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
