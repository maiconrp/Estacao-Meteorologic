import os


def format_font_weight(font_weight):
    """Formata o peso da fonte adicionando espaços antes de cada letra maiúscula que não seja a primeira letra da palavra."""
    if not font_weight.istitle():
        new_string = font_weight[0]
        for i in range(1, len(font_weight)):
            if (
                font_weight[i].isupper()
                and not font_weight[i - 1].isspace()
                and not font_weight[i - 1].isupper()
            ):
                new_string += " "
            new_string += font_weight[i]
        return new_string
    return font_weight


def load():
    """Encontra todas as fontes TTF no diretório de fontes e cria um dicionário com o nome e o caminho da fonte."""
    fonts_folder = os.path.dirname(os.path.abspath(__file__))
    font_dict = {}

    for font_name in os.listdir(fonts_folder):
        font_folder = os.path.join(fonts_folder, font_name)
        if os.path.isdir(font_folder):
            for file_name in os.listdir(font_folder):
                if file_name.endswith(".ttf"):
                    font_path = os.path.join(font_folder, file_name)
                    font_weight = file_name.replace(".ttf", "").split("-")[-1]
                    font_weight = format_font_weight(font_weight)
                    font_dict[f"{font_name} {font_weight}"] = font_path

    return font_dict
