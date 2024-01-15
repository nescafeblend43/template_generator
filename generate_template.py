import svgwrite
from specs import Specs


class SVGCreator:
    def __init__(self, stroke_width, stroke_color, page_padding, border_thk, background_color='darkblue'):
        """
        Initialize the SVGCreator with stroke properties and background color.

        :param stroke_width: int, the thickness of the shapes' edges.
        :param stroke_color: str, the color of the shapes' edges.
        :param background_color: str, the color of the background.
        """
        self.page_padding = page_padding
        self.border_thk = border_thk

        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.background_color = background_color

    def create_svg_with_rectangle(self, filename, canvas_size_mm):
        """
        Create an SVG file with a square drawn inside.

        :param filename: str, the name of the file to save the SVG.
        :param canvas_size_mm: tuple, the size of the SVG canvas in millimeters (width, height).
        :param square_size_mm: int, the length of the side of the square in millimeters.
        :param square_position_mm: tuple, the top-left position of the square in millimeters (x, y).
        """
        # Convert sizes and position to mm
        canvas_size = (f"{canvas_size_mm[0]}mm", f"{canvas_size_mm[1]}mm")
        # rectangle_size = (f"{rectangle_size_mm[0]}mm", f"{rectangle_size_mm[1]}mm")
        rectangle_size_x = canvas_size_mm[0]-self.page_padding
        rectangle_size_y = canvas_size_mm[1]-self.page_padding
        rectangle_size = (f"{rectangle_size_x}mm", f"{rectangle_size_y}mm")

        # rectangle_size = (f"{rectangle_size_mm[0]}mm", f"{rectangle_size_mm[1]}mm")

        x_position = (canvas_size_mm[0] - rectangle_size_x) / 2
        y_position = (canvas_size_mm[1] - rectangle_size_y) / 2
        rectangle_position = (f"{x_position}mm", f"{y_position}mm")
        
        # Create an SVG drawing instance with the specified canvas size in mm
        dwg = svgwrite.Drawing(filename, size=canvas_size, profile='tiny')

        # Add a dark blue background
        background = dwg.rect(insert=(0, 0), size=canvas_size, fill=self.background_color)
        dwg.add(background)

        # Add a square to the drawing with no fill, using class attributes for stroke
        square = dwg.rect(
            insert=rectangle_position, 
            size=rectangle_size, 
            fill='none',
            stroke=self.stroke_color,
            stroke_width=self.stroke_width
        )
        dwg.add(square)

        # Save the drawing as an SVG file
        dwg.save()

# Usage Example
svg_creator = SVGCreator(2, 'white', 50, 2)

svg_creator.create_svg_with_rectangle('square_with_background.svg', Specs.A1.value[::-1])

# print(Specs.A4)  # (210, 297)

