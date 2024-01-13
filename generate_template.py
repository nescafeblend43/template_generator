import svgwrite

def create_square(filename, side_length, canvas_size):
    # Create an SVG drawing instance with a specified canvas size.
    # canvas_size should be a tuple in the format (width, height)
    dwg = svgwrite.Drawing(filename, size=canvas_size, profile='tiny')

    # Add a square to the drawing
    dwg.add(dwg.rect(insert=(0, 0), size=(side_length, side_length), fill='blue'))

    # Save the drawing as an SVG file
    dwg.save()

# Usage
create_square('square.svg', 100, (200, 200))