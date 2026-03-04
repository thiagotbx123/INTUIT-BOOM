# qbo_checker/main.py
"""Main CLI orchestrator for QBO Feature Checker"""

import sys
import time

from .config import PROJECTS, EVIDENCE_DIR
from .login import ensure_logged_in
from .navigator import get_features_for_project, navigate_to_feature, reset_to_homepage
from .screenshot import (
    generate_filename,
    capture_screenshot,
    annotate_screenshot,
    get_element_bbox,
)
from .interpreter import interpret_screenshot
from .spreadsheet import (
    add_feature_result,
    find_existing_result,
    update_feature_result,
    get_summary,
)


def show_banner():
    """Display CLI banner."""
    print()
    print("\033[96m" + "=" * 60 + "\033[0m")
    print("\033[96m       QBO FEATURE CHECKER - INTUIT BOOM\033[0m")
    print("\033[96m" + "=" * 60 + "\033[0m")
    print()


def show_menu():
    """Display project selection menu."""
    print("\033[97mSelect Project:\033[0m")
    print("-" * 30)
    for i, (project, config) in enumerate(PROJECTS.items(), 1):
        companies = ", ".join(config["companies"])
        print(f"  [{i}] {project} ({companies})")
    print("-" * 30)
    print("  [Q] Quit")
    print()


def select_project() -> str:
    """Get project selection from user.

    Returns:
        Project name or None if quit
    """
    show_menu()
    choice = input("  > ").strip().upper()

    if choice == "Q":
        return None

    try:
        idx = int(choice) - 1
        project_names = list(PROJECTS.keys())
        if 0 <= idx < len(project_names):
            return project_names[idx]
    except ValueError:
        pass

    print("\033[91m  Invalid selection\033[0m")
    return select_project()


def check_feature(page, feature: dict, project: str) -> dict:
    """Check a single feature: navigate, screenshot, interpret, save.

    Args:
        page: Playwright page
        feature: Feature definition
        project: Project name

    Returns:
        Result dict with status and details
    """
    feature_name = feature["name"]
    companies = feature.get("companies", ["Default"])
    highlight_config = feature.get("highlight", {})

    results = []

    for company in companies:
        if company not in PROJECTS[project]["companies"]:
            continue

        print(f"\n  [{project}/{company}] Checking: {feature_name}")

        # Navigate
        success, nav_details = navigate_to_feature(page, feature)

        if not success:
            print(f"    \033[91m[FAIL] {nav_details}\033[0m")
            # Still take screenshot for evidence

        # Generate filename
        filename = generate_filename(project, company, feature_name)

        # Capture screenshot
        print("    Capturing screenshot...")
        filepath = capture_screenshot(page, filename)

        # Annotate if highlight config exists
        if highlight_config:
            selector = highlight_config.get("selector")
            fallback_selector = highlight_config.get("fallback_selector")
            text_target = highlight_config.get("text_target")
            fixed_bbox = highlight_config.get("fixed_bbox")
            highlight_type = highlight_config.get("type", "box")

            # Convert fixed_bbox list to tuple if provided
            if fixed_bbox and isinstance(fixed_bbox, list):
                fixed_bbox = tuple(fixed_bbox)

            bbox = get_element_bbox(page, selector, fallback_selector, text_target, fixed_bbox)
            if bbox:
                print(f"    Adding {highlight_type} annotation...")
                annotate_screenshot(filepath, bbox, highlight_type, feature_name)
            else:
                # If element not found, try arrow fallback if configured
                fallback_type = highlight_config.get("fallback_type", "arrow")
                print(f"    [93m[WARN]33[93m[WARN] Element not found, using {fallback_type} fallback[0m")
                # Use center of visible area as target
                from PIL import Image

                img = Image.open(filepath)
                center_bbox = (
                    img.width // 3,
                    img.height // 3,
                    img.width // 2,
                    img.height // 2,
                )
                annotate_screenshot(filepath, center_bbox, fallback_type, feature_name)

        # Generate notes based on navigation result
        print("    Generating notes...")
        try:
            interpretation = interpret_screenshot(
                filepath=filepath,
                feature_name=feature_name,
                feature_description=feature.get("description", ""),
                project=project,
                company=company,
            )
        except Exception as e:
            print(f"    \033[93m[WARN]33[93m[WARN] AI interpretation failed: {e}\033[0m")
            interpretation = {
                "status": "PARTIAL" if success else "NO",
                "intuit_notes": f"Feature {'accessible' if success else 'not accessible'} - manual review needed.",
                "internal_notes": f"Auto-check {'passed' if success else 'failed'}: {nav_details}",
            }

        status = interpretation["status"]
        status_color = {
            "YES": "\033[92m",
            "PARTIAL": "\033[93m",
            "NO": "\033[91m",
            "NA": "\033[90m",
        }.get(status, "")

        print(f"    Status: {status_color}{status}\033[0m")

        # Save to spreadsheet
        existing_row = find_existing_result(project, company, feature_name)

        if existing_row:
            update_feature_result(
                row=existing_row,
                status=status,
                intuit_notes=interpretation["intuit_notes"],
                internal_notes=interpretation["internal_notes"],
                evidence_file=filename,
            )
            print(f"    Updated row {existing_row} in control sheet")
        else:
            row = add_feature_result(
                project=project,
                company=company,
                ref=feature.get("ref", ""),
                feature=feature_name,
                status=status,
                intuit_notes=interpretation["intuit_notes"],
                internal_notes=interpretation["internal_notes"],
                evidence_file=filename,
            )
            print(f"    Added row {row} to control sheet")

        results.append({"company": company, "status": status, "file": filename})

    return results


def run_project_check(project: str):
    """Run all feature checks for a project.

    Args:
        project: Project name
    """
    print(f"\n\033[97mStarting checks for: {project}\033[0m")
    print(f"Evidence folder: {EVIDENCE_DIR}")
    print("-" * 50)

    # Get features for project
    features = get_features_for_project(project)
    print(f"Found {len(features)} features to check")

    if not features:
        print("\033[93mNo features defined for this project\033[0m")
        return

    # Login and connect to Chrome
    print("\nLogging in...")
    try:
        pw, browser, page = ensure_logged_in(project)
    except Exception as e:
        print(f"\033[91mLogin failed: {e}\033[0m")
        return

    print("\033[92mReady!\033[0m")

    # Process each feature
    all_results = []
    try:
        for i, feature in enumerate(features, 1):
            print(f"\n[{i}/{len(features)}] {feature['name']}")

            # Reset to homepage before each feature (clean state)
            if i > 1:
                print("  Resetting to homepage...")
                reset_to_homepage(page)

            results = check_feature(page, feature, project)
            all_results.extend(results)

            # Brief pause between features
            time.sleep(1)
    finally:
        # Disconnect (don't close browser)
        pw.stop()

    # Summary
    print("\n" + "=" * 50)
    print("\033[97mSUMMARY\033[0m")
    print("=" * 50)

    summary = get_summary()
    print(f"  Total checked: {summary['total']}")
    print(f"  \033[92mYES: {summary['YES']}\033[0m")
    print(f"  \033[93mPARTIAL: {summary['PARTIAL']}\033[0m")
    print(f"  \033[91mNO: {summary['NO']}\033[0m")
    print(f"  \033[90mNA: {summary['NA']}\033[0m")
    print()
    print(f"Control sheet: {EVIDENCE_DIR / 'fall_release_control.xlsx'}")
    print()


def main():
    """Main entry point."""
    show_banner()

    # Check for command-line arguments
    if len(sys.argv) > 1:
        project_arg = sys.argv[1].upper()
        # Find matching project
        project_names = list(PROJECTS.keys())
        matched = None
        for p in project_names:
            if p.upper() == project_arg or p.upper().startswith(project_arg):
                matched = p
                break

        if matched:
            run_project_check(matched)
        else:
            print(f"\033[91mProject '{project_arg}' not found. Available: {', '.join(project_names)}\033[0m")
        return

    # Interactive mode
    while True:
        project = select_project()

        if project is None:
            print("\n\033[90mGoodbye!\033[0m\n")
            break

        run_project_check(project)

        print("\n" + "-" * 50)
        input("Press ENTER to continue...")
        show_banner()


if __name__ == "__main__":
    main()
