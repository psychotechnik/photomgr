import time
import os, os.path
import hashlib
import traceback
import shutil

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
@click.option('--dry-run', default=False)
@click.argument('src_dir', type=click.Path(exists=True, dir_okay=True))
@click.argument('dest_dir_base', type=click.Path(exists=True, dir_okay=True))
def organize_images(dry_run, src_dir, dest_dir_base):
    src_dir = click.format_filename(src_dir)
    dest_dir_base = click.format_filename(dest_dir_base)
    click.echo("importing from source dir: %s" % src_dir)
    click.echo("organizing into dir: %s" % dest_dir_base)

    num_moved = 0
    num_skipped = 0

    def get_exif(fn):
        ret = {}
        try:
            i = Image.open(fn)
        except IOError, ioe:
            click.echo("could not open image file.")
            return {}, None

        #click.echo(i)
        if not hasattr(i, '_getexif'):
            click.echo("no _getexif ")
            return {}, None

        info = i._getexif()
        if not info:
            click.echo("_getexif returned nothing")
            return {}, None

        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        _, ext = os.path.splitext(fn)
        new_fn = hashlib.md5(i.tostring()).hexdigest() + ext.lower()
        return ret, new_fn


    def run_import(full_fn):
        """
        exif_data = {}
        try:
            exif_data, new_fn = get_exif(full_fn)
        except TypeError, e:
            click.echo("problem while getting exif")
            click.echo(traceback.format_exc())
        if exif_data:
            click.echo(exif_data)
        created_exif = exif_data.get('DateTimeOriginal') or \
                exif_data.get('DateTimeDigitized')
                #or \ exif_data.get('DateTime')
        click.echo("got creation date from exif: %s" % created_exif)
        else:
            created = dateutil_parse(created_exif)
        """
        st = os.stat(full_fn)

        created = time.ctime(st.st_mtime)
        click.echo("got creation date from os.stat: %s" % created)
        original_fn, ext = os.path.splitext(full_fn)

        new_fn = hashlib.md5(original_fn+u"|"+str(st.st_size)).\
                hexdigest() + ext.lower()
        created = dateutil_parse(created)
        #click.echo("%s %s" %(dest_dir_base, created.strftime('%Y/%m/%d')))
        photo_dir = os.path.\
                join(dest_dir_base, created.strftime('%Y/%m/%d'))

        if not os.path.exists(photo_dir):
            os.makedirs(photo_dir)

        #shutil.move(fn, os.path.join(photo_dir, new_fn))
        new_full_fn = os.path.join(photo_dir, new_fn)
        click.echo(new_full_fn)
        if os.path.exists(new_full_fn):
            click.echo("%s exists. skipping." % new_full_fn)
            num_skipped+=1

        print "dry_run: ", dry_run
        print "type dry_run: ", type(dry_run)

        if dry_run == False:
            click.echo("moving %s to %s" % (full_fn, new_full_fn))
            shutil.copy2(full_fn, new_full_fn)
            num_moved+=1

    def import_dir(arg, dirname, names):
        """
        names is the list of files in the dir being traversed
        """
        for name in names:
            fn = os.path.join(dirname, name)
            if os.path.exists(fn) and not os.path.isdir(name):
                click.echo(u"starting import %s" % fn)
                run_import(fn)

    os.path.walk(src_dir, import_dir, '---')

    click.echo("moved %d files" % num_moved)
    click.echo("skipped %d files" % num_skipped)



if __name__ == '__main__':
    organize_images()
