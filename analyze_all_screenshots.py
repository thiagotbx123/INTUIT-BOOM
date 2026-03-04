# -*- coding: utf-8 -*-
"""
Deep Analysis of ALL Screenshots - TCO and Construction
"""

import os
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

TCO_DIR = "EvidencePack/WinterRelease/TCO"
CONSTRUCTION_DIR = "EvidencePack/WinterRelease/Construction"

# Error page size
ERROR_PAGE_SIZE = 142715


def analyze_directory(directory, env_name):
    """Analyze all screenshots in a directory"""
    results = []

    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return results

    files = [f for f in os.listdir(directory) if f.endswith(".png")]

    for filename in sorted(files):
        filepath = os.path.join(directory, filename)
        size = os.path.getsize(filepath)
        size_kb = size // 1024

        # Extract feature ref from filename
        ref = filename.split("_")[0] if "_" in filename else "UNKNOWN"

        # Quality assessment
        if size == ERROR_PAGE_SIZE:
            quality = "ERROR_PAGE"
            status = "FAIL"
        elif size < 100000:  # < 100KB
            quality = "WEAK"
            status = "REVIEW"
        elif size < 150000:  # 100-150KB
            quality = "ACCEPTABLE"
            status = "PASS"
        elif size < 250000:  # 150-250KB
            quality = "GOOD"
            status = "PASS"
        else:  # > 250KB
            quality = "EXCELLENT"
            status = "PASS"

        results.append(
            {
                "env": env_name,
                "ref": ref,
                "filename": filename,
                "size_bytes": size,
                "size_kb": size_kb,
                "quality": quality,
                "status": status,
            }
        )

    return results


def main():
    print("=" * 80)
    print("DEEP SCREENSHOT ANALYSIS - TCO & CONSTRUCTION")
    print("=" * 80)

    # Analyze TCO
    print("\n" + "=" * 40)
    print("TCO SCREENSHOTS")
    print("=" * 40)
    tco_results = analyze_directory(TCO_DIR, "TCO")

    if tco_results:
        tco_stats = {
            "EXCELLENT": 0,
            "GOOD": 0,
            "ACCEPTABLE": 0,
            "WEAK": 0,
            "ERROR_PAGE": 0,
        }
        for r in tco_results:
            tco_stats[r["quality"]] += 1
            indicator = "[OK]" if r["status"] == "PASS" else "[!!]" if r["status"] == "FAIL" else "[??]"
            print(f"{indicator} {r['ref']}: {r['size_kb']}KB - {r['quality']}")

        print(f"\nTCO Summary: {len(tco_results)} files")
        print(f"  EXCELLENT (>250KB): {tco_stats['EXCELLENT']}")
        print(f"  GOOD (150-250KB): {tco_stats['GOOD']}")
        print(f"  ACCEPTABLE (100-150KB): {tco_stats['ACCEPTABLE']}")
        print(f"  WEAK (<100KB): {tco_stats['WEAK']}")
        print(f"  ERROR_PAGE (404): {tco_stats['ERROR_PAGE']}")

    # Analyze Construction
    print("\n" + "=" * 40)
    print("CONSTRUCTION SCREENSHOTS")
    print("=" * 40)
    const_results = analyze_directory(CONSTRUCTION_DIR, "Construction")

    if const_results:
        const_stats = {
            "EXCELLENT": 0,
            "GOOD": 0,
            "ACCEPTABLE": 0,
            "WEAK": 0,
            "ERROR_PAGE": 0,
        }
        for r in const_results:
            const_stats[r["quality"]] += 1
            indicator = "[OK]" if r["status"] == "PASS" else "[!!]" if r["status"] == "FAIL" else "[??]"
            print(f"{indicator} {r['ref']}: {r['size_kb']}KB - {r['quality']}")

        print(f"\nConstruction Summary: {len(const_results)} files")
        print(f"  EXCELLENT (>250KB): {const_stats['EXCELLENT']}")
        print(f"  GOOD (150-250KB): {const_stats['GOOD']}")
        print(f"  ACCEPTABLE (100-150KB): {const_stats['ACCEPTABLE']}")
        print(f"  WEAK (<100KB): {const_stats['WEAK']}")
        print(f"  ERROR_PAGE (404): {const_stats['ERROR_PAGE']}")

    # Cross-reference with features
    print("\n" + "=" * 40)
    print("FEATURE COVERAGE ANALYSIS")
    print("=" * 40)

    # Load features
    with open("qbo_checker/features_winter.json", "r") as f:
        features = json.load(f)["features"]

    all_refs = {f["ref"] for f in features}
    tco_refs = {r["ref"] for r in tco_results}
    const_refs = {r["ref"] for r in const_results}

    print(f"\nTotal features defined: {len(all_refs)}")
    print(f"TCO screenshots: {len(tco_refs)} unique refs")
    print(f"Construction screenshots: {len(const_refs)} unique refs")

    # Missing in TCO
    tco_missing = all_refs - tco_refs
    if tco_missing:
        print(f"\nMissing in TCO: {sorted(tco_missing)}")

    # Identify duplicates (v2, v3 versions)
    print("\n" + "=" * 40)
    print("DUPLICATE/VERSION ANALYSIS")
    print("=" * 40)

    for r in const_results:
        if "_v2" in r["filename"] or "_v3" in r["filename"]:
            print(f"  {r['filename']} - {r['size_kb']}KB - {r['quality']}")

    # Identify error pages
    print("\n" + "=" * 40)
    print("ERROR PAGES DETECTED")
    print("=" * 40)

    error_pages = [r for r in tco_results + const_results if r["quality"] == "ERROR_PAGE"]
    if error_pages:
        for r in error_pages:
            print(f"  [{r['env']}] {r['filename']}")
    else:
        print("  No error pages detected")

    # Save full analysis
    all_results = {
        "tco": tco_results,
        "construction": const_results,
        "summary": {
            "tco_total": len(tco_results),
            "construction_total": len(const_results),
            "error_pages": len(error_pages),
        },
    }

    with open("docs/SCREENSHOT_ANALYSIS.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print("\n" + "=" * 80)
    print("Analysis saved to: docs/SCREENSHOT_ANALYSIS.json")
    print("=" * 80)


if __name__ == "__main__":
    main()
