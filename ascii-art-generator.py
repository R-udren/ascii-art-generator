import argparse
from pyfiglet import Figlet, FigletFont
from colorama import init

init(autoreset=True)

class Gradient:
    def __init__(self, start_color: tuple[int, int, int], end_color: tuple[int, int, int]):
        self.start_color = start_color
        self.end_color = end_color

    def get_color_at(self, fraction: float) -> tuple[int, int, int]:
        r = int(self.start_color[0] + fraction * (self.end_color[0] - self.start_color[0]))
        g = int(self.start_color[1] + fraction * (self.end_color[1] - self.start_color[1]))
        b = int(self.start_color[2] + fraction * (self.end_color[2] - self.start_color[2]))
        return r, g, b


def get_gradient_ascii(text: str, start_color: tuple[int, int, int], end_color: tuple[int, int, int], font: str, gradient_direction: str) -> str:
    fig = Figlet(font=font, width=160, justify="auto")
    ascii_art = fig.renderText(text)

    gradient = Gradient(start_color, end_color)
    lines = ascii_art.split("\n")
    colored_ascii_art = ""

    for row, line in enumerate(lines):
        if row > 0:
            colored_ascii_art += "\n"
        for i, char in enumerate(line):
            if char.isspace():
                colored_ascii_art += char
                continue

            if gradient_direction == "vertical":
                fraction = row / (len(lines) - 1)
            elif gradient_direction == "horizontal":
                fraction = i / (len(line) - 1)
            elif gradient_direction == "both":
                frac_row = row / (len(lines) - 1)
                frac_col = i / (len(line) - 1)
                fraction = max(frac_row, frac_col)
            else:
                raise ValueError("Invalid gradient direction")

            r, g, b = gradient.get_color_at(fraction)
            colored_ascii_art += f"\x1b[38;2;{r};{g};{b}m{char}\x1b[0m"

    return colored_ascii_art


def font_showcase(text: str, start_color: tuple[int, int, int], end_color: tuple[int, int, int], gradient_direction: str):
    print("Available fonts:")
    for font in FigletFont.getFonts():
        print(f"Font: {font}")
        print(get_gradient_ascii(text, start_color, end_color, font, gradient_direction))


def main():
    parser = argparse.ArgumentParser(description="Generate gradient-colored ASCII art.")
    parser.add_argument("--show-fonts", action="store_true", help="Show available fonts")
    parser.add_argument("text", type=str, help="Text for the banner")
    parser.add_argument("-f", "--from-color", type=int, nargs=3, default=[255, 0, 0], metavar=("R", "G", "B"),
                        help="Starting color in RGB format (default: 255 0 0)")
    parser.add_argument("-t", "--to-color", type=int, nargs=3, default=[0, 0, 255], metavar=("R", "G", "B"),
                        help="Ending color in RGB format (default: 0 0 255)")
    parser.add_argument("--font", type=str, default="slant", help="Font for the banner (default: slant)")
    parser.add_argument("-d", "--direction", choices=["vertical", "horizontal", "both"], default="both",
                        help="Gradient direction (default: both)")
    parser.add_argument("-o", "--output-file", type=str, help="File to save the output ASCII art")

    args = parser.parse_args()

    colored_ascii = get_gradient_ascii(args.text, tuple(args.from_color), tuple(args.to_color), args.font, args.direction)

    if not args.show_fonts:
        print(colored_ascii)

    if args.output_file:
        with open(args.output_file, "w", encoding="UTF-8") as f:
            f.write(colored_ascii)

    if args.show_fonts:
        font_showcase(args.text, tuple(args.from_color), tuple(args.to_color), args.direction)


if __name__ == "__main__":
    main()
