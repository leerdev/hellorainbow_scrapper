from PIL import Image
import os
import settings

def convert_images_to_thumbnails(input_dir, output_dir, size):
    input_filenames = os.listdir(input_dir)
    n, counter = len(input_filenames), 0
    print("\n ** Creating thumbnails **")
    for input_filename in input_filenames:
        output_filename = "tn_" + input_filename
        if input_filename != output_filename:
            try:
                im = Image.open(input_dir + input_filename)
                im.thumbnail(size, Image.Resampling.LANCZOS)
                # centering the image
                offset_x = int(max((size[0] - im.size[0]) / 2, 0))
                offset_y = int(max((size[1] - im.size[1]) / 2, 0))
                # final image
                final_im = Image.new(mode='RGBA', size=size, color=settings.collage_background)
                final_im.paste(im, (offset_x, offset_y))
                final_im.save(output_dir + output_filename, 'PNG')
            except IOError as e:
                print(f"\n!! cannot create thumbnail for {input_filename}", e)
        print(f"\rProcessing image {counter} out of {n}", end='')
        counter += 1


def create_collage(input_dir):
    input_filenames = os.listdir(input_dir)
    n = len(input_filenames)
    print("\n ** Creating collage **")
    new_img = Image.new('RGBA', settings.collage_size, settings.collage_background)
    counter = 0
    for v in range(settings.collage_size_in_images[1]):
        for h in range(settings.collage_size_in_images[0]):
            cur_img = Image.open(input_dir + input_filenames[counter])
            new_img.paste(cur_img, (h*settings.thumbnails_size[0], v*settings.thumbnails_size[1]))
            counter += 1
            print(f'\rProcessing image {counter} out of {n}', end='')
    return new_img


if __name__ == '__main__':
    convert_images_to_thumbnails(
        settings.images_dir,
        settings.output_images_dir,
        settings.thumbnails_size)
    img = create_collage('thumbnails/')
    print(' ... saving ...')
    img.save(settings.collage_fname, "png")