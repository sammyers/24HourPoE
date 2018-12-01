from pathlib import Path
import os
import shutil


def organize_files(image_directory):
    """
    Moves JPG files of people's faces into their corresponding folders, renaming them if necessary.
    """
    image_directory = Path(image_directory).resolve()

    for file in image_directory.glob('*.jpg'):
        name = file.stem

        target_dir = image_directory / name
        if target_dir.is_dir():
            suffix = 1
            target_file = target_dir / '{}-{}.jpg'.format(name, suffix)
            while target_file.is_file():
                suffix += 1
                target_file = target_dir / '{}-{}.jpg'.format(name, suffix)
            shutil.move(str(file), str(target_file))
            print('Moved {} to {}.'.format(file, target_file))
        else:
            print('Could not find directory for {}. Creating one.'.format(name))
            os.mkdir(str(target_dir))
            shutil.move(str(file), str(target_dir / (name + '-1.jpg')))
            print('Moved {} to {}.'.format(file, target_dir))


if __name__ == '__main__':
    organize_files('train')
