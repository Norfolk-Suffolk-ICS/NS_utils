from typing import List, Literal, Dict


# Function for Sequential palettes 
def get_sequential_palettes(num_colours: int, colour:Literal["green","purple","pink","blue","yellow"])->List[str]: 
    """    
    Args:
        number of colours (int): The number of colours needed in the palette (Accepted values are from 1 to 5)
        name of colour (str): Name of the colour you want (Accepted values are green, purple, pink, blue and yellow).
    
    Returns:
        list: A list of sequential colours.
    """
    seq_palette = []
    # 1 colour: Primary 
    if num_colours == 1:
        seq_palette.append(CORE_COLOUR_STYLE[colour][2])
    # 2 colours: Primary + Light 2 
    elif num_colours == 2:
        seq_palette.append([CORE_COLOUR_STYLE[colour][2], CORE_COLOUR_STYLE[colour][4]])
    # 3 colours: Dark 2 + Primary + Light 2 
    elif num_colours == 3:
        seq_palette.append([CORE_COLOUR_STYLE[colour][0], CORE_COLOUR_STYLE[colour][2], CORE_COLOUR_STYLE[colour][4]])
    # 4 colours: Dark 2 + Primary + Light 1 + Light 2 
    elif num_colours == 4:
        seq_palette.append([CORE_COLOUR_STYLE[colour][0], CORE_COLOUR_STYLE[colour][2], CORE_COLOUR_STYLE[colour][3], CORE_COLOUR_STYLE[colour][4]])
    # 5 colours: Dark 2 + Dark 1 + Primary + Light 1 + Light 2 
    elif num_colours == 5:
        seq_palette.append([CORE_COLOUR_STYLE[colour][0], CORE_COLOUR_STYLE[colour][1], CORE_COLOUR_STYLE[colour][2], CORE_COLOUR_STYLE[colour][3], CORE_COLOUR_STYLE[colour][4]])
        
    return seq_palette


# Qualitative palette 
QUAL_ONE_COLOUR_PALETTE   = ["#0D9C93"]
QUAL_TWO_COLOUR_PALETTE   = ["#0D9C93", "#55408E"]
QUAL_THREE_COLOUR_PALETTE = ["#0D9C93", "#55408E", "#B41E8C"]
QUAL_FOUR_COLOUR_PALETTE  = ["#0D9C93", "#55408E", "#B41E8C", "#005EB8"]
QUAL_FIVE_COLOUR_PALETTE  = ["#0D9C93", "#55408E", "#B41E8C", "#005EB8", "#E28C03"]


# Diverging palettes
DIVERGE_ONE_COLOUR_PALETTE   = ["#0D9C93"]
DIVERGE_TWO_COLOUR_PALETTE   = ["#0D9C93", "#55408E"]
DIVERGE_THREE_COLOUR_PALETTE = ["#0D9C93", "#8879AF", "#55408E"]
DIVERGE_FOUR_COLOUR_PALETTE  = ["#0D9C93", "#55B9B3", "#8879AF", "#55408E"]
DIVERGE_FIVE_COLOUR_PALETTE  = ["#0A7C75", "#0D9C93", "#55B9B3", "#8879AF", "#55408E"]
DIVERGE_SIX_COLOUR_PALETTE   = ["#0A7C75", "#0D9C93", "#55B9B3", "#8879AF", "#55408E", "#443371"]
DIVERGE_SEVEN_COLOUR_PALETTE = ["#075D58", "#0A7C75", "#0D9C93", "#55B9B3", "#8879AF", "#55408E", "#443371"]
DIVERGE_EIGHT_COLOUR_PALETTE = ["#075D58", "#0A7C75", "#0D9C93", "#55B9B3", "#8879AF", "#55408E", "#443371", "#332655"]
DIVERGE_NINE_COLOUR_PALETTE  = ["#075D58", "#0A7C75", "#0D9C93", "#55B9B3", "#9ED7D3", "#8879AF", "#55408E", "#443371", "#332655"]
DIVERGE_TEN_COLOUR_PALETTE   = ["#075D58", "#0A7C75", "#0D9C93", "#55B9B3", "#9ED7D3", "#BBB2D1", "#8879AF", "#55408E", "#443371", "#332655"]


TITLE_COLOUR =  "#064169"

TEXT_COLOUR = "#231F20"

TEXT_HIGHLIGHT_COLOUR = "#408CC4"

BACKGROUND_DIVERGENT_COLOUR = "#C0CED8"

CORE_COLOUR_STYLE = { 'green' : ["#075D58","#0A7C75", "#0D9C93", "#55B9B3", "#9ED7D3"],
                     'purple': ["#332655","#443371", "#55408E", "#8879AF", "#BBB2D1"],
                     'pink'  : ["#6C1254","#901870", "#B41E8C", "#CA61AE", "#E1A5D1"],
                     'blue'  : ["#00386E","#004B93", "#005EB8", "#4C8ECD", "#99BEE2"],
                     'yellow': ["#875401","#B47002", "#E28C03", "#EAAE4E", "#F3D19A"] 
                    }

CORE_GREEN_CYCLE = ["#075D58", "#0A7C75", "#0D9C93", "#55B9B3", "#9ED7D3"]

CORE_PURPLE_CYCLE = ["#332655", "#443371", "#55408E", "#8879AF", "#BBB2D1"]

CORE_PINK_CYCLE = ["#6C1254", "#901870", "#B41E8C", "#CA61AE", "#E1A5D1"]

CORE_BLUE_CYCLE = ["#00386E", "#004B93", "#005EB8", "#4C8ECD", "#99BEE2"]

CORE_YELLOW_CYCLE = ["#875401", "#B47002", "#E28C03", "#EAAE4E", "#F3D19A"]

COLOUR_SET_NAMES = ["DARK_2_CYCLE", "DARK_1_CYCLE", "PRIMARY_COLOUR_CYCLE", "LIGHT_1_CYCLE", "LIGHT_2_CYCLE"]

COLOURS_BY_CYCLE:Dict[str,List[str]] = {
    COLOUR_SET_NAMES[i]: [values[i] for values in CORE_COLOUR_STYLE.values()]
    for i in range(len(COLOUR_SET_NAMES))
}