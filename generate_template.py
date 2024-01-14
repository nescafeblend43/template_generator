import svgwrite
from specs import Specs


class SVGCreator:
    def __init__(self, stroke_width, stroke_color):
        """
        Initialize the SVGCreator with stroke properties.

        :param stroke_width: int, the thickness of the shapes' edges.
        :param stroke_color: str, the color of the shapes' edges.
        """
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color

    def create_svg_with_square(self, filename, canvas_size_mm, square_size_mm, square_position_mm):
        """
        Create an SVG file with a square drawn inside.

        :param filename: str, the name of the file to save the SVG.
        :param canvas_size: tuple, the size of the SVG canvas (width, height).
        :param square_size: int, the length of the side of the square.
        :param square_position: tuple, the top-left position of the square (x, y).
        """
        canvas_size = (f"{canvas_size_mm[0]}mm", f"{canvas_size_mm[1]}mm")
        square_size = f"{square_size_mm}mm"
        square_position = (f"{square_position_mm[0]}mm", f"{square_position_mm[1]}mm")

        # Create an SVG drawing instance with the specified canvas size
        dwg = svgwrite.Drawing(filename, size=canvas_size, profile='tiny')

        # Add a square to the drawing with no fill, using class attributes for stroke
        square = dwg.rect(
            insert=square_position, 
            size=(square_size, square_size), 
            fill='none',
            stroke=self.stroke_color,
            stroke_width=self.stroke_width
        )
        dwg.add(square)

        # Save the drawing as an SVG file
        dwg.save()

# Usage Example
svg_creator = SVGCreator(5, 'red')
svg_creator.create_svg_with_square('square4.svg', Specs.A1.value, 100, (200, 200))


# print(Specs.A4)  # (210, 297)

