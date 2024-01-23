import svgwrite
from specs import Specs
import string
import random

class SVGCreator:
    def __init__(self, stroke_width, stroke_color, page_padding_mm, border_thk_mm, background_color='darkblue'):
        """
        Initialize the SVGCreator with stroke properties and background color.

        :param stroke_width: int, the thickness of the shapes' edges.
        :param stroke_color: str, the color of the shapes' edges.
        :param background_color: str, the color of the background.
        """
        self.page_padding_mm = page_padding_mm
        self.border_thk_mm = border_thk_mm
        self.divs_n = 3
        self.divs_m = 4
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.background_color = background_color
        self.font_size_mm=4
        self.font_family="Arial"


    def get_random_color(self):
        """
        Generate a random color in hexadecimal format.
        :return: str, the random color in hexadecimal format.
        """
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f'#{r:02x}{g:02x}{b:02x}'


    def offset_y(self, original_coords, offset):
        """
        Adjust the Y-coordinate of a point by a given offset.
        """
        adjusted_y_position =float(self.font_size_mm-1)  / 2
        x, y = original_coords
        return (x, y - offset+adjusted_y_position)
    
    def offset_x(self, original_coords, offset):
        """
        Adjust the Y-coordinate of a point by a given offset.
        """
        adjusted_y_position =float(self.font_size_mm-1) / 2
        x, y = original_coords
        return (x- offset, y +adjusted_y_position)

    def from_mm(self, input_tuple):
            x, y = input_tuple
            return (f"{x:.5f}mm", f"{y:.5f}mm")
    

    def center(self, point1, point2):
           x_center = round((point1[0] + point2[0]) / 2, 5)
           y_center = round((point1[1] + point2[1]) / 2, 5)
           return (x_center, y_center)

    def add_text(self, dwg, text, position_mm):
        """
        Add text to the SVG drawing.
        """
        dwg.add(dwg.text(
            text, 
            insert=self.from_mm(position_mm),
            fill=self.stroke_color,
            font_size=str(self.font_size_mm)+'mm',
            font_family=self.font_family,
            text_anchor="middle"  
        ))


    def add_box(self, dwg, position_mm, size_mm):
        """
        Add box to the SVG drawing.
        """
        dwg.add(dwg.rect(
            insert=self.from_mm(position_mm), 
            size=self.from_mm(size_mm), 
            fill='none',
            stroke=self.stroke_color,
            stroke_width=self.stroke_width
        ))


    def add_line(self, dwg, start, end):
        """
        Add line to the SVG drawing.
        """
        dwg.add(dwg.line(
            start=self.from_mm(start),
            end=self.from_mm(end),
            stroke=self.stroke_color, 
            stroke_width=self.stroke_width
        ))


    def create_svg_with_rectangle(self, filename, canvas_size_mm, divs_n = 3, divs_m = 5):
        """
        Create an SVG file with a square drawn inside.

        :param filename: str, the name of the file to save the SVG.
        :param canvas_size_mm: tuple, the size of the SVG canvas in millimeters (width, height).
        :param square_size_mm: int, the length of the side of the square in millimeters.
        :param square_position_mm: tuple, the top-left position of the square in millimeters (x, y).
        """
        self.divs_n = divs_n
        self.divs_m = divs_m

        # Convert sizes and position to mm
        canvas_size = self.from_mm(canvas_size_mm)
        # Create an SVG drawing instance with the specified canvas size in mm
        dwg = svgwrite.Drawing(filename, size=canvas_size, profile='tiny')
       
        # Add a dark blue background
        background = dwg.rect(insert=(0, 0), size=canvas_size, fill=self.get_random_color())
        dwg.add(background)

        # Create outer rectangle
        outer_rec_size_mm = tuple(x-(2*self.page_padding_mm) for x in canvas_size_mm)
        outer_rec_pos_mm = tuple(((a - b)/2.0) for a, b in zip(canvas_size_mm, outer_rec_size_mm))
        inner_rec_size_mm =tuple(x-2*(self.page_padding_mm+self.border_thk_mm) for x in canvas_size_mm)
        inner_rec_pos_mm = tuple(((a - b)/2.0) for a, b in zip(canvas_size_mm, inner_rec_size_mm))
        self.add_box(dwg, outer_rec_pos_mm, outer_rec_size_mm)
        self.add_box(dwg, inner_rec_pos_mm, inner_rec_size_mm)

        # X grid
        start_x, start_y = (outer_rec_pos_mm[0], canvas_size_mm[1]/2)
        start_position = self.from_mm((start_x,start_y)) 
        start_position_opp = self.from_mm((canvas_size_mm[0]-start_x,start_y)) 
        end_position = self.from_mm((start_x+ self.border_thk_mm,start_y)) 
        end_position_opp = self.from_mm((canvas_size_mm[0]-(start_x+ self.border_thk_mm),start_y)) 

        # Create the line with the specified properties
        dwg.add(dwg.line(start=start_position,end=end_position,stroke=self.stroke_color,stroke_width=self.stroke_width*2))
        dwg.add(dwg.line(start=start_position_opp,end=end_position_opp,stroke=self.stroke_color,stroke_width=self.stroke_width*2))

        # text=string.ascii_uppercase[self.divs_n]
        # text_position_mm = (20, 50)
        # self.add_text(dwg, "fghj", text_position_mm)

        for i in range(self.divs_n-1):
            ptc=((inner_rec_size_mm[1])/2)/(self.divs_n)
            pitch_y = (i+1)*ptc

            start_u =(start_x, start_y+pitch_y)
            end_u  = (start_x+self.border_thk_mm, start_y+pitch_y)
            self.add_line(dwg, start_u, end_u)
            letter = string.ascii_uppercase[self.divs_n-1+(i+1)]
            self.add_text(dwg, letter, self.center(self.offset_y(start_u, ptc/2), self.offset_y(end_u, ptc/2)))

            start_l =(start_x, start_y-pitch_y)
            end_l = (start_x + self.border_thk_mm, start_y-pitch_y)
            self.add_line(dwg, start_l, end_l)      
            letter = string.ascii_uppercase[self.divs_n-(i+1)]
            self.add_text(dwg, letter, self.center(self.offset_y(start_l, -ptc/2), self.offset_y(end_l, -ptc/2)))

            start_u_r =(canvas_size_mm[0]-(start_x + self.border_thk_mm), start_y+pitch_y)
            end_u_r = (canvas_size_mm[0]-(start_x), start_y+pitch_y)
            self.add_line(dwg, start_u_r, end_u_r)
            letter = string.ascii_uppercase[self.divs_n-1+(i+1)]
            self.add_text(dwg, letter, self.center(self.offset_y(start_u_r, ptc/2), self.offset_y(end_u_r, ptc/2)))

            start_l_r =(canvas_size_mm[0]-(start_x + self.border_thk_mm), start_y-pitch_y)
            end_l_r = (canvas_size_mm[0]-(start_x), start_y-pitch_y)
            self.add_line(dwg, start_l_r, end_l_r)
            letter = string.ascii_uppercase[self.divs_n-(i+1)]
            self.add_text(dwg, letter, self.center(self.offset_y(start_l_r, -ptc/2), self.offset_y(end_l_r, -ptc/2)))


        letter = string.ascii_uppercase[self.divs_n-1+(i+2)]
        self.add_text(dwg, letter, self.center(self.offset_y(start_u, -(ptc/2)), self.offset_y(end_u, -(ptc/2))))            
        self.add_text(dwg, letter, self.center(self.offset_y(start_u_r, -(ptc/2)), self.offset_y(end_u_r, -(ptc/2))))            

        letter = string.ascii_uppercase[self.divs_n-(i+2)]
        self.add_text(dwg, letter, self.center(self.offset_y(start_l, +(ptc/2)), self.offset_y(end_l, +(ptc/2))))
        self.add_text(dwg, letter, self.center(self.offset_y(start_l_r, +(ptc/2)), self.offset_y(end_l_r, +(ptc/2))))


        # Y grid
        start_x, start_y = (canvas_size_mm[0]/2, outer_rec_pos_mm[1])
        start_position = self.from_mm((start_x,start_y)) 
        start_position_opp = self.from_mm((start_x,canvas_size_mm[1]-start_y)) 

        end_position = self.from_mm((start_x,start_y+ self.border_thk_mm)) 
        end_position_opp = self.from_mm((start_x,canvas_size_mm[1]-(start_y+ self.border_thk_mm))) 

        # Create the line with the specified properties
        dwg.add(dwg.line(start=start_position,end=end_position,stroke=self.stroke_color,stroke_width=self.stroke_width*2))
        dwg.add(dwg.line(start=start_position_opp,end=end_position_opp,stroke=self.stroke_color,stroke_width=self.stroke_width*2))     

        for i in range(self.divs_m-1):
            ptc=((inner_rec_size_mm[0])/2)/(self.divs_m)
            pitch_x = (i+1)*ptc

            start_r =(start_x+pitch_x, start_y)
            end_r = (start_x+pitch_x, start_y+self.border_thk_mm)
            self.add_line(dwg, start_r, end_r)                 
            letter = str(self.divs_m+(i+1))
            self.add_text(dwg, letter, self.center(self.offset_x(start_r, ptc/2), self.offset_x(end_r, ptc/2)))

            start_l =(start_x-pitch_x, start_y)
            end_l = (start_x-pitch_x, start_y+self.border_thk_mm)
            self.add_line(dwg, start_l, end_l)     
            letter = str(self.divs_m-(i))
            self.add_text(dwg, letter, self.center(self.offset_x(start_l, -ptc/2), self.offset_x(end_l, -ptc/2)))

            start_r_l =(start_x + pitch_x, canvas_size_mm[1]-(start_y+self.border_thk_mm))
            end_r_l = (start_x + pitch_x, canvas_size_mm[1]-start_y)
            self.add_line(dwg, start_r_l, end_r_l)     
            letter = str(self.divs_m+(i+1))
            self.add_text(dwg, letter, self.center(self.offset_x(start_r_l, ptc/2), self.offset_x(end_r_l, ptc/2)))

            start_l_l =(start_x - pitch_x, canvas_size_mm[1]-(start_y+self.border_thk_mm))
            end_l_l = (start_x - pitch_x, canvas_size_mm[1]-start_y)
            self.add_line(dwg, start_l_l, end_l_l)  
            letter = str(self.divs_m-(i))
            self.add_text(dwg, letter, self.center(self.offset_x(start_l_l, -ptc/2), self.offset_x(end_l_l, -ptc/2)))

        letter = str(self.divs_m+(i+2))
        self.add_text(dwg, letter, self.center(self.offset_x(start_r, -(ptc/2)), self.offset_x(end_r, -(ptc/2))))      #OK       
        self.add_text(dwg, letter, self.center(self.offset_x(start_r_l, -(ptc/2)), self.offset_x(end_r_l, -(ptc/2))))

        letter = str(self.divs_m-(i+1))
        self.add_text(dwg, letter, self.center(self.offset_x(start_l_l, (ptc/2)), self.offset_x(end_l_l, (ptc/2))))
        self.add_text(dwg, letter, self.center(self.offset_x(start_l, (ptc/2)), self.offset_x(end_l, (ptc/2))))            

        # Save the drawing as awr   n SVG file
        dwg.save()


svg_creator = SVGCreator(stroke_width=2, stroke_color='white', page_padding_mm=15, border_thk_mm=5, background_color='red')

svg_creator.create_svg_with_rectangle('a0.svg', Specs.A1.value[::-1], divs_n = 8, divs_m = 12)
svg_creator.create_svg_with_rectangle('a1.svg', Specs.A1.value[::-1], divs_n = 6, divs_m = 8)
svg_creator.create_svg_with_rectangle('a2.svg', Specs.A1.value[::-1], divs_n = 4, divs_m = 6)
svg_creator.create_svg_with_rectangle('a3.svg', Specs.A1.value[::-1], divs_n = 3, divs_m = 4)
svg_creator.create_svg_with_rectangle('a4.svg', Specs.A1.value[::-1], divs_n = 2, divs_m = 3)


