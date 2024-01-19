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

    def from_mm(self, input_tuple):
        return (f"{input_tuple[0]}mm", f"{input_tuple[1]}mm")
    
    


    def create_svg_with_rectangle(self, filename, canvas_size_mm):
        """
        Create an SVG file with a square drawn inside.

        :param filename: str, the name of the file to save the SVG.
        :param canvas_size_mm: tuple, the size of the SVG canvas in millimeters (width, height).
        :param square_size_mm: int, the length of the side of the square in millimeters.
        :param square_position_mm: tuple, the top-left position of the square in millimeters (x, y).
        """
        # Convert sizes and position to mm
        canvas_size = self.from_mm(canvas_size_mm)

        # Create outer rectangle
        outer_rec_size_mm = tuple(x-(2*self.page_padding_mm) for x in canvas_size_mm)
        outer_rec_pos_mm = tuple(((a - b)/2.0) for a, b in zip(canvas_size_mm, outer_rec_size_mm))
        
        # Create inner rectangle
        inner_rec_size_mm =tuple(x-2*(self.page_padding_mm+self.border_thk_mm) for x in canvas_size_mm)
        inner_rec_pos_mm = tuple(((a - b)/2.0) for a, b in zip(canvas_size_mm, inner_rec_size_mm))

        # Create an SVG drawing instance with the specified canvas size in mm
        dwg = svgwrite.Drawing(filename, size=canvas_size, profile='tiny')

        # Add a dark blue background
        background = dwg.rect(insert=(0, 0), size=canvas_size, fill=self.background_color)
        dwg.add(background)

        # Add a square to the drawing with no fill, using class attributes for stroke
        square = dwg.rect(
            insert=self.from_mm(outer_rec_pos_mm), 
            size=self.from_mm(outer_rec_size_mm), 
            fill='none',
            stroke=self.stroke_color,
            stroke_width=self.stroke_width
        )
        dwg.add(square)
        
        inner_square = dwg.rect(
            insert=self.from_mm(inner_rec_pos_mm), 
            size=self.from_mm(inner_rec_size_mm), 
            fill='none',
            stroke=self.stroke_color,
            stroke_width=self.stroke_width
        )
        dwg.add(inner_square)        

        # X grid
        start_x, start_y = (outer_rec_pos_mm[0], canvas_size_mm[1]/2)
        start_position = self.from_mm((start_x,start_y)) 
        start_position_opp = self.from_mm((canvas_size_mm[0]-start_x,start_y)) 

        end_position = self.from_mm((start_x+ self.border_thk_mm,start_y)) 
        end_position_opp = self.from_mm((canvas_size_mm[0]-(start_x+ self.border_thk_mm),start_y)) 

        # Create the line with the specified properties
        dwg.add(dwg.line(start=start_position,end=end_position,stroke=self.stroke_color,stroke_width=self.stroke_width*2))
        dwg.add(dwg.line(start=start_position_opp,end=end_position_opp,stroke=self.stroke_color,stroke_width=self.stroke_width*2))


        for i in range(self.divs_n-1):
            pitch_y = (i+1)*((inner_rec_size_mm[1])/2)/(self.divs_n)

            dwg.add(dwg.line(
                start=self.from_mm((start_x, start_y+pitch_y)),
                end=self.from_mm((start_x+self.border_thk_mm, start_y+pitch_y)),
                stroke=self.stroke_color, stroke_width=self.stroke_width
            ))
            
            dwg.add(dwg.line(
                start= self.from_mm((start_x, start_y-pitch_y)),
                end=self.from_mm((start_x + self.border_thk_mm, start_y-pitch_y)),
                stroke=self.stroke_color, stroke_width=self.stroke_width
            ) )

            dwg.add(dwg.line(
                start=self.from_mm((canvas_size_mm[0]-(start_x + self.border_thk_mm), start_y+pitch_y)),
                end=self.from_mm((canvas_size_mm[0]-(start_x), start_y+pitch_y)),
                stroke=self.stroke_color, stroke_width=self.stroke_width
            ))
            
            dwg.add(dwg.line(
                start=self.from_mm((canvas_size_mm[0]-(start_x + self.border_thk_mm), start_y-pitch_y)),
                end=self.from_mm((canvas_size_mm[0]-(start_x), start_y-pitch_y)),
                stroke=self.stroke_color, stroke_width=self.stroke_width
            ))

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
            pitch_x = (i+1)*((inner_rec_size_mm[0])/2)/(self.divs_m)

            dwg.add(dwg.line(
                start=self.from_mm((start_x+pitch_x, start_y)),
                end=self.from_mm((start_x+pitch_x, start_y+self.border_thk_mm)),
                stroke=self.stroke_color, stroke_width=self.stroke_width
            ))
            
            dwg.add(dwg.line(
                start= self.from_mm((start_x-pitch_x, start_y)),
                end=self.from_mm((start_x-pitch_x, start_y+self.border_thk_mm)),
                stroke=self.stroke_color, stroke_width=self.stroke_width
            ) )

            dwg.add(dwg.line(
                start=self.from_mm((start_x + pitch_x, canvas_size_mm[1]-(start_y+self.border_thk_mm))),
                end=self.from_mm((start_x + pitch_x, canvas_size_mm[1]-start_y)),
                stroke=self.stroke_color, stroke_width=self.stroke_width
            ))
            
            dwg.add(dwg.line(
                start=self.from_mm((start_x - pitch_x, canvas_size_mm[1]-(start_y+self.border_thk_mm))),
                end=self.from_mm((start_x - pitch_x, canvas_size_mm[1]-start_y)),
                stroke=self.stroke_color, stroke_width=self.stroke_width
            ))

        # Save the drawing as awr   n SVG file
        dwg.save()


svg_creator = SVGCreator(3, 'white', 50, 30)

svg_creator.create_svg_with_rectangle('square_with_background.svg', Specs.A1.value[::-1])


