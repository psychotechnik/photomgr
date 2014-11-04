import hashlib
import shutil
import os.path
import pprint

from PIL import Image
from PIL.ExifTags import TAGS
from dateutil.parser import parse as dateutil_parse
import click

def visit(arg, dirname, names):
    print dirname, arg
    for name in names:
        subname = os.path.join(dirname, name)
        if os.path.isdir(subname):
            print '  %s/' % name
        else:
            print '  %s' % name
    print

"""
['YResolution', 'ResolutionUnit', 'Copyright', 'Make', 'Flash', 'SceneCaptureType', 'GPSInfo', 'MeteringMode', 'XResolution', 'MakerNote', 'ExposureProgram', 'ColorSpace', 'ExifImageWidth', 'DateTimeDigitized', 'ApertureValue', 'UserComment', 'FocalPlaneYResolution', 'WhiteBalance', 'FNumber', 'CustomRendered', 'DateTimeOriginal', 'Artist', 'FocalLength', 'SubsecTimeOriginal', 'ExposureMode', 'ComponentsConfiguration', 'FocalPlaneXResolution', 'ExifOffset', 'ExifImageHeight', 'SubsecTimeDigitized', 'ISOSpeedRatings', 'Model', 'DateTime', 'ExposureTime', 'FocalPlaneResolutionUnit', 'SubsecTime', 'Orientation', 'ExifInteroperabilityOffset', 'FlashPixVersion', 'YCbCrPositioning', 'ExifVersion'] """

@click.command()
@click.argument('src_dir', type=click.Path(exists=True, dir_okay=True))
@click.argument('dest_dir_base', type=click.Path(exists=True, dir_okay=True))
def organize_images(src_dir, dest_dir_base):
    src_dir = click.format_filename(src_dir)
    dest_dir_base = click.format_filename(dest_dir_base)
    click.echo("importing from source dir: %s" % src_dir)
    click.echo("organizing into dir: %s" % dest_dir_base)

    def get_exif(fn):
        ret = {}
        try:
            i = Image.open(fn)
        except IOError:
            return

        click.echo(i)
        if not hasattr(i, '_getexif'):
            return

        info = i._getexif()
        if not info:
            return

        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        _, ext = os.path.splitext(fn)
        new_fn = hashlib.md5(i.tostring()).hexdigest() + ext
        return ret, new_fn


    def run_import(fn):
        if not os.path.exists(fn):
            return
        try:
            exif_data, new_fn = get_exif(fn)
        except TypeError:
            return

        dt_original = dateutil_parse(exif_data.get('DateTimeOriginal'))
        #click.echo("%s - %s" %(fn, dt_original))
        photo_dir = os.path.\
                join(dest_dir_base, dt_original.strftime('%Y/%m/%d'))

        if not os.path.exists(photo_dir):
            os.makedirs(photo_dir)

        click.echo("moving %s to %s" % (fn, photo_dir))
        shutil.move(fn, os.path.join(photo_dir, new_fn))

    def import_dir(arg, dirname, names):
        for name in names:
            fn = os.path.join(dirname, name)
            if not os.path.isdir(fn):
                run_import(fn)

    os.path.walk(src_dir, import_dir, '---')



if __name__ == '__main__':
    organize_images()
