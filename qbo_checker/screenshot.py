# qbo_checker/screenshot.py
"""Screenshot capture and annotation module"""

from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from .config import EVIDENCE_DIR, HIGHLIGHT_COLOR, ARROW_COLOR, SCREENSHOT_QUALITY


def generate_filename(ref: str, project: str, company: str, feature_name: str = None) -> str:
    """Generate screenshot filename following naming convention.

    Format: {YYYY-MM-DD}_{PROJECT}_{COMPANY}_{REF}_{FEATURE}.png

    Args:
        ref: Unique reference code (e.g., TCO_001) - PRIMARY KEY
        project: Project name (e.g., TCO)
        company: Company name (e.g., ApexTire)
        feature_name: Optional feature name for readability

    Returns:
        Filename string with date prefix and unique ref
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    # Sanitize company name
    safe_company = company.replace(" ", "").replace("&", "").replace(",", "")
    # Build filename with Ref as key component
    if feature_name:
        # Sanitize feature name (remove spaces, special chars) - shortened for readability
        safe_feature = (
            feature_name.replace(" ", "").replace("/", "_").replace(":", "").replace("(", "").replace(")", "")[:30]
        )
        return f"{date_str}_{project}_{safe_company}_{ref}_{safe_feature}.png"
    else:
        return f"{date_str}_{project}_{safe_company}_{ref}.png"


def capture_screenshot(page, filename: str) -> Path:
    """Capture screenshot from Playwright page and save to evidence folder.

    Args:
        page: Playwright page object
        filename: Target filename

    Returns:
        Path to saved screenshot
    """
    filepath = EVIDENCE_DIR / filename
    page.screenshot(path=str(filepath), full_page=False, timeout=60000, animations="disabled")
    return filepath


def add_box_highlight(image: Image.Image, bbox: tuple, color: tuple = HIGHLIGHT_COLOR, width: int = 3) -> Image.Image:
    """Add rectangular highlight box around an area.

    Args:
        image: PIL Image
        bbox: (x1, y1, x2, y2) bounding box
        color: RGB tuple for box color
        width: Line width

    Returns:
        Modified image
    """
    draw = ImageDraw.Draw(image)
    draw.rectangle(bbox, outline=color, width=width)
    return image


def add_arrow(
    image: Image.Image,
    start: tuple,
    end: tuple,
    color: tuple = ARROW_COLOR,
    width: int = 3,
) -> Image.Image:
    """Add arrow pointing to element.

    Args:
        image: PIL Image
        start: (x, y) arrow start point
        end: (x, y) arrow end point (tip)
        color: RGB tuple
        width: Line width

    Returns:
        Modified image
    """
    draw = ImageDraw.Draw(image)
    # Main line
    draw.line([start, end], fill=color, width=width)

    # Arrowhead (simple triangle)
    import math

    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    arrow_length = 15
    arrow_angle = math.pi / 6  # 30 degrees

    x1 = end[0] - arrow_length * math.cos(angle - arrow_angle)
    y1 = end[1] - arrow_length * math.sin(angle - arrow_angle)
    x2 = end[0] - arrow_length * math.cos(angle + arrow_angle)
    y2 = end[1] - arrow_length * math.sin(angle + arrow_angle)

    draw.polygon([end, (x1, y1), (x2, y2)], fill=color)
    return image


def add_label(image: Image.Image, position: tuple, text: str, color: tuple = HIGHLIGHT_COLOR) -> Image.Image:
    """Add text label to image.

    Args:
        image: PIL Image
        position: (x, y) position for text
        text: Label text
        color: RGB tuple

    Returns:
        Modified image
    """
    draw = ImageDraw.Draw(image)
    # Use default font (cross-platform)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except OSError:
        # Fonte Arial não disponível no sistema - usar fonte padrão
        font = ImageFont.load_default()

    # Add background for readability
    bbox = draw.textbbox(position, text, font=font)
    padding = 4
    draw.rectangle(
        [bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding],
        fill=(255, 255, 255, 200),
    )
    draw.text(position, text, fill=color, font=font)
    return image


def annotate_screenshot(filepath: Path, element_bbox: tuple, highlight_type: str = "box", label: str = None) -> Path:
    """Add annotations to existing screenshot.

    Args:
        filepath: Path to screenshot
        element_bbox: (x1, y1, x2, y2) of element to highlight
        highlight_type: "box" or "arrow"
        label: Optional text label

    Returns:
        Path to annotated screenshot (overwrites original)
    """
    image = Image.open(filepath)
    img_width, img_height = image.size

    # Validate bbox is within image bounds and reasonable size
    x1, y1, x2, y2 = element_bbox
    bbox_valid = (
        0 <= x1 < img_width
        and 0 <= y1 < img_height
        and x2 <= img_width
        and y2 <= img_height
        and (x2 - x1) > 20  # Min width
        and (y2 - y1) > 10  # Min height
        and (x2 - x1) < img_width * 0.8  # Max 80% of image width
        and (y2 - y1) < img_height * 0.8  # Max 80% of image height
    )

    # If bbox is invalid or highlight would be in wrong area, use arrow instead
    if not bbox_valid and highlight_type == "box":
        print("    [INFO] Box annotation out of bounds, switching to arrow")
        highlight_type = "arrow"

    if highlight_type == "box":
        image = add_box_highlight(image, element_bbox)
    elif highlight_type == "arrow":
        # Arrow from offset position pointing to element center
        center_x = (element_bbox[0] + element_bbox[2]) // 2
        center_y = (element_bbox[1] + element_bbox[3]) // 2
        # Position arrow start based on element position (avoid overlap)
        if center_y < img_height // 2:
            # Element in top half - arrow from bottom-left
            start = (max(50, center_x - 100), min(img_height - 50, center_y + 100))
        else:
            # Element in bottom half - arrow from top-left
            start = (max(50, center_x - 100), max(50, center_y - 100))
        image = add_arrow(image, start, (center_x, center_y))

    if label:
        # Position label above the element
        label_pos = (element_bbox[0], max(0, element_bbox[1] - 25))
        image = add_label(image, label_pos, label)

    image.save(filepath, quality=SCREENSHOT_QUALITY)
    return filepath


def get_element_bbox(
    page,
    selector: str = None,
    fallback_selector: str = None,
    text_target: str = None,
    fixed_bbox: tuple = None,
) -> tuple:
    """Get bounding box of element from Playwright page.

    Args:
        page: Playwright page
        selector: CSS/Playwright selector
        fallback_selector: Alternative selector if first fails
        text_target: Text to find and highlight (uses text= selector)
        fixed_bbox: Fixed (x1, y1, x2, y2) coordinates to use directly

    Returns:
        (x1, y1, x2, y2) tuple or None if not found
    """
    # If fixed coordinates provided, use them directly
    if fixed_bbox:
        return fixed_bbox

    selectors_to_try = []

    # If text_target provided, use it to find element
    if text_target:
        selectors_to_try.append(f"text={text_target}")

    if selector:
        selectors_to_try.append(selector)
    if fallback_selector:
        selectors_to_try.append(fallback_selector)

    for sel in selectors_to_try:
        try:
            element = page.locator(sel).first
            if element.is_visible(timeout=2000):
                box = element.bounding_box()
                if box and box["width"] > 20 and box["height"] > 10:
                    # Return bounding box with small padding
                    padding = 10
                    return (
                        max(0, int(box["x"]) - padding),
                        max(0, int(box["y"]) - padding),
                        int(box["x"] + box["width"]) + padding,
                        int(box["y"] + box["height"]) + padding,
                    )
        except Exception:
            # Elemento não encontrado ou timeout - tentar próximo seletor
            continue
    return None
