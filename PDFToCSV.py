import pdfplumber 
import pandas as pd
with pdfplumber.open("data/pdf/TestStatement.pdf") as pdf:
    
    page = pdf.pages[0]
    bbox = (30, 440, page.width, page.height - 90)  # Define the bounding box
    
    # Convert the page to an image and draw the bounding box
    img = page.to_image()
    img.draw_rect(pdfplumber.utils.bbox_to_rect(bbox))  # Draw bounding box on the page image
    #img.show()  # Open the image for preview

    page = page.crop(bbox)

    debug = img.debug_tablefinder({
        "vertical_strategy": "explicit", 
        "horizontal_strategy": "lines",
        "explicit_vertical_lines": [44,80,280,400,500, page.width+11],
    })
    debug.show() 
    table = page.extract_table(table_settings={
        "vertical_strategy": "explicit", 
        "horizontal_strategy": "lines",
        "explicit_vertical_lines": [44,80,280,400,500, page.width+11],
    })
    
    df = pd.DataFrame(table, columns=['date', 'description', 'withdrawals', 'deposits', 'balance']) 
    print(df)
    
   
    
    