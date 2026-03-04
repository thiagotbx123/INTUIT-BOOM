"""Screenshot capture and annotation utilities."""

from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from .config import get_config


class ScreenshotManager:
    """
    Manages screenshot capture and annotation.

    Features:
    - Capture full-page screenshots
    - Add annotations (boxes, arrows, text)
    - Consistent file naming
    """

    def __init__(self, output_dir: Path = None):
        """
        Initialize screenshot manager.

        Args:
            output_dir: Directory to save screenshots
        """
        config = get_config()
        self.output_dir = output_dir or config.evidence_dir
        self.quality = config.screenshot_quality

        # Annotation colors (RGB)
        self.highlight_color = (255, 0, 0)  # Red
        self.text_color = (255, 255, 255)  # White
        self.bg_color = (0, 0, 0)  # Black

    def generate_filename(
        self, product: str, project: str, feature: str, company: str = None
    ) -> str:
        """
        Generate consistent filename for screenshot.

        Format: {date}_{product}_{project}_{company}_{feature}.png

        Args:
            product: Product name (e.g., QBO)
            project: Project name (e.g., TCO)
            feature: Feature name
            company: Company name (optional)

        Returns:
            Filename string
        """
        date = datetime.now().strftime("%Y-%m-%d")

        # Clean names for filename
        def clean(s):
            return "".join(c if c.isalnum() else "_" for c in s).strip("_")[:30]

        parts = [date, clean(product), clean(project)]
        if company:
            parts.append(clean(company))
        parts.append(clean(feature))

        return "_".join(parts) + ".png"

    def save(self, image: Image.Image, filename: str) -> Path:
        """
        Save image to output directory.

        Args:
            image: PIL Image
            filename: Output filename

        Returns:
            Full path to saved file
        """
        filepath = self.output_dir / filename
        image.save(filepath, quality=self.quality)
        return filepath

    def annotate_box(
        self,
        image: Image.Image,
        bbox: Tuple[int, int, int, int],
        color: Tuple[int, int, int] = None,
        width: int = 3,
    ) -> Image.Image:
        """
        Draw a highlight box on image.

        Args:
            image: PIL Image
            bbox: Bounding box (x1, y1, x2, y2)
            color: RGB color tuple
            width: Line width

        Returns:
            Annotated image
        """
        draw = ImageDraw.Draw(image)
        color = color or self.highlight_color
        draw.rectangle(bbox, outline=color, width=width)
        return image

    def annotate_arrow(
        self,
        image: Image.Image,
        target: Tuple[int, int],
        color: Tuple[int, int, int] = None,
        size: int = 50,
    ) -> Image.Image:
        """
        Draw an arrow pointing to target.

        Args:
            image: PIL Image
            target: Target point (x, y)
            color: RGB color tuple
            size: Arrow size

        Returns:
            Annotated image
        """
        draw = ImageDraw.Draw(image)
        color = color or self.highlight_color

        x, y = target
        # Draw arrow pointing down-right to target
        points = [
            (x - size, y - size),  # Start
            (x - 5, y - 5),  # End (near target)
        ]
        draw.line(points, fill=color, width=4)

        # Arrow head
        draw.polygon(
            [
                (x - 5, y - 5),
                (x - 15, y - 20),
                (x - 20, y - 15),
            ],
            fill=color,
        )

        return image

    def annotate_text(
        self, image: Image.Image, text: str, position: Tuple[int, int], font_size: int = 20
    ) -> Image.Image:
        """
        Add text annotation to image.

        Args:
            image: PIL Image
            text: Text to add
            position: Position (x, y)
            font_size: Font size

        Returns:
            Annotated image
        """
        draw = ImageDraw.Draw(image)

        # Try to use a nice font, fall back to default
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

        # Draw background rectangle for readability
        bbox = draw.textbbox(position, text, font=font)
        padding = 5
        draw.rectangle(
            [bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding],
            fill=self.bg_color,
        )

        # Draw text
        draw.text(position, text, fill=self.text_color, font=font)

        return image

    def annotate(
        self,
        filepath: Path,
        bbox: Tuple[int, int, int, int] = None,
        annotation_type: str = "box",
        label: str = None,
    ) -> Path:
        """
        Add annotation to existing screenshot.

        Args:
            filepath: Path to screenshot
            bbox: Bounding box or target area
            annotation_type: Type of annotation (box, arrow)
            label: Optional text label

        Returns:
            Path to annotated file
        """
        image = Image.open(filepath)

        if bbox:
            if annotation_type == "box":
                image = self.annotate_box(image, bbox)
            elif annotation_type == "arrow":
                # Use center of bbox as target
                target = ((bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2)
                image = self.annotate_arrow(image, target)

        if label:
            # Position label above bbox or at top
            y_pos = bbox[1] - 30 if bbox else 10
            x_pos = bbox[0] if bbox else 10
            image = self.annotate_text(image, label, (x_pos, max(10, y_pos)))

        image.save(filepath)
        return filepath


def get_element_bbox(page, selector: str) -> Optional[Tuple[int, int, int, int]]:
    """
    Get bounding box of element on page.

    Args:
        page: Playwright page
        selector: CSS selector

    Returns:
        Bounding box tuple or None
    """
    try:
        element = page.query_selector(selector)
        if element:
            box = element.bounding_box()
            if box:
                return (
                    int(box["x"]),
                    int(box["y"]),
                    int(box["x"] + box["width"]),
                    int(box["y"] + box["height"]),
                )
    except Exception:
        pass
    return None
