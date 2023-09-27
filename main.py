from PIL import Image, ImageDraw, ImageFont
import re

def get_text_line_width(text, font, max_width):
    width, _ = font.getsize(text)
    return min(width, max_width)


def justify_text(text, font, max_width):
    words = text.split()
    space_pixel_len = max_width - get_text_line_width(text, font, max_width)
    space_size = font.getsize(' ')[0]
    space_count = space_pixel_len / space_size

    num_spaces = (len(words) - 1 + round(space_count))
    if num_spaces > 0:
        space_per_gap = num_spaces // (len(words) - 1)
        extra_spaces = num_spaces % (len(words) - 1)

        result = ''
        for i in range(len(words) - 1):
            result += words[i]
            result += ' ' * space_per_gap
            if i < extra_spaces:
                result += ' '

        result += words[-1]
    else:
        result = ''.join(words)
    return result


def split_text_into_lines(text, font, max_width):
    lines = []
    current_line = []
    current_line_width = 0

    words = text.split()
    for word in words:
        word_width, _ = font.getsize(word)
        if current_line_width + word_width <= max_width:
            current_line.append(word)
            current_line_width += word_width
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_line_width = word_width

    if current_line:
        lines.append(' '.join(current_line))

    return lines

def create_image_with_text(text, font_path, font_size, image_width, image_height, max_width, min_width, line_spacing_percent):
    font = ImageFont.truetype(font_path, font_size)

    data = split_text_into_lines(text, font, min_width)
    result = []

    for item in data:
        line_width = get_text_line_width(item, font, max_width)

        if line_width <= 1200:
            result.append(item)
        elif line_width <= 1540:
            line = justify_text(item, font, max_width)
            result.append(line)
        elif line_width == 1560:
            result.append(item)

    text = '\n'.join(result)

    image = Image.new("RGB", (image_width, image_height), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    font_color = (255, 255, 255)

    total_text_height = sum(draw.textsize(line, font=font)[1] for line in result)

    left_margin = 180
    right_margin = 180

    available_width = image_width - left_margin - right_margin


    y = (image_height - total_text_height) // 2 - line_spacing_percent * 2
    x = left_margin  # Set x-coordinate to the left margin

    for line in result:

        text_width, text_height = draw.textsize(line, font=font)
        y += (text_height + int(text_height * (line_spacing_percent / 100.0))) // 2
        draw.text((x, y), line, font=font, fill=font_color)
        y += (text_height + int(text_height * (line_spacing_percent / 100.0))) // 2

    image.save("img/output_image_{:02d}.png".format(count + 1))




if __name__ == "__main__":
    font_path = 'fonts/noto/NotoSans-Bold.ttf'
    font_size = int(input('Enter pls text size: '))
    image_width = 1960
    image_height = 1180
    max_width = 1560
    min_width = 1360
    line_spacing_percent = 35
    count = 0
    # text = input('Enter your text pls: ')
    # create_image_with_text(text, font_path, font_size, image_width, image_height, max_width, min_width, line_spacing_percent)



    data_text = input('Введіть текст, будь ласка: ')
    sentences = re.split(r'(?<=[.])\s*', data_text)
    for text in sentences:
        count += 1
        create_image_with_text(text, font_path, font_size, image_width, image_height, max_width, min_width, line_spacing_percent)