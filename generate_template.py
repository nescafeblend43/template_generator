import svgwrite
from specs import Specs


class SVGCreator:
    def __init__(self, stroke_width, stroke_color, page_padding_mm, border_thk_mm, background_color='darkblue', divs_n = 3, divs_m = 5):
        """
        Initialize the SVGCreator with stroke properties and background color.

        :param stroke_width: int, the thickness of the shapes' edges.
        :param stroke_color: str, the color of the shapes' edges.
        :param background_color: str, the color of the background.
        """
        self.page_padding_mm = page_padding_mm
        self.border_thk_mm = border_thk_mm
        
        self.divs_n = divs_n
        self.divs_m = divs_m


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


        # Create outer rectangle
        rectangle_size_x_o = canvas_size_mm[0]-(2*self.page_padding_mm)
        rectangle_size_y_o = canvas_size_mm[1]-(2*self.page_padding_mm)
        rectangle_size_o = (f"{rectangle_size_x_o}mm", f"{rectangle_size_y_o}mm")

        x_position_o = (canvas_size_mm[0] - rectangle_size_x_o) / 2
        y_position_o = (canvas_size_mm[1] - rectangle_size_y_o) / 2
        rectangle_position_o = (f"{x_position_o}mm", f"{y_position_o}mm")
        
        # Create inner rectangle
        rectangle_size_x_i = canvas_size_mm[0]-2*(self.page_padding_mm+self.border_thk_mm)
        rectangle_size_y_i = canvas_size_mm[1]-2*(self.page_padding_mm+self.border_thk_mm)
        rectangle_size_i = (f"{rectangle_size_x_i}mm", f"{rectangle_size_y_i}mm")

        x_position_i = (canvas_size_mm[0] - rectangle_size_x_i) / 2
        y_position_i = (canvas_size_mm[1] - rectangle_size_y_i) / 2
        rectangle_position_i = (f"{x_position_i}mm", f"{y_position_i}mm")


        # Create an SVG drawing instance with the specified canvas size in mm
        dwg = svgwrite.Drawing(filename, size=canvas_size, profile='tiny')

        # Add a dark blue background
        background = dwg.rect(insert=(0, 0), size=canvas_size, fill=self.background_color)
        dwg.add(background)

        # Add a square to the drawing with no fill, using class attributes for stroke
        square = dwg.rect(
            insert=rectangle_position_o, 
            size=rectangle_size_o, 
            fill='none',
            stroke=self.stroke_color,
            stroke_width=self.stroke_width
        )
        dwg.add(square)
        
        inner_square = dwg.rect(
            insert=rectangle_position_i, 
            size=rectangle_size_i, 
            fill='none',
            stroke=self.stroke_color,
            stroke_width=self.stroke_width
        )
        dwg.add(inner_square)        


        # Convert start position and length to mm
        start_x, start_y = (self.page_padding_mm, canvas_size_mm[1]/2)
        start_position = (f"{start_x}mm", f"{start_y}mm")
        end_position = (f"{start_x + self.border_thk_mm}mm", f"{start_y}mm")


        # Create the line with the specified properties
        line = dwg.line(
            start=start_position,
            end=end_position,
            stroke=self.stroke_color,
            stroke_width=self.stroke_width
        )
        dwg.add(line)
        for i in range(self.divs_n-1):
            line = dwg.line(
                start=(f"{start_x}mm", f"{ start_y+(i+1)*((rectangle_size_y_i)/2)/(self.divs_n)}mm"),
                end=(f"{start_x + self.border_thk_mm}mm", f"{start_y+(i+1) * ((rectangle_size_y_i)/2)/(self.divs_n)}mm"),
                stroke=self.stroke_color,
                stroke_width=self.stroke_width
            )
            dwg.add(line)
            
            line = dwg.line(
                start=(f"{start_x}mm", f"{ start_y-(i+1) *((rectangle_size_y_i)/2)/(self.divs_n)}mm"),
                end=(f"{start_x + self.border_thk_mm}mm", f"{start_y-(i+1) * ((rectangle_size_y_i)/2)/(self.divs_n)}mm"),
                stroke=self.stroke_color,
                stroke_width=self.stroke_width
            )
            dwg.add(line)


        # Save the drawing as an SVG file
        dwg.save()

# Usage Example
svg_creator = SVGCreator(2, 'white', 50, 30)

svg_creator.create_svg_with_rectangle('square_with_background.svg', Specs.A1.value[::-1])

# print(Specs.A4)  # (210, 297)

