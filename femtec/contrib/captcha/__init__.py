"""Captcha (Completely Automated Public Turing test to tell Computers and
Humans Apart) module for django

Author: Martin Winkler, June 2007
License: BSD
"""

from os import listdir, sep, access, mkdir, W_OK, R_OK, remove, chmod, path, rmdir, stat
from urllib import basejoin
import md5
from random import choice, randrange
from sys import modules
import tempfile
import datetime
from PIL import Image, ImageColor, ImageFont, ImageDraw
from django.forms import *
from django.forms.fields import CharField
from django.conf import settings
from django.utils.translation import gettext
from django.utils.datastructures import MultiValueDict
from django.utils.safestring import mark_safe

def clean_old_entries(captchas_dir, max_age=1200):
    """maintainance function for deleting all expired captchas

    captchas_dir: parent directory of the individual image-directories
                 default: [settings.MEDIA_ROOT]/captchas
    max_age:     maximum allowed age of directories in seconds.
                 defaults to 1200 seconds (20 minutes)
    """
    if access(captchas_dir, W_OK):
        basetime = datetime.datetime.now() - datetime.timedelta(seconds=max_age)
        for dname in listdir(captchas_dir):
            d = path.join(captchas_dir, dname)
            if basetime > datetime.datetime.fromtimestamp(stat(d).st_mtime):
                try:
                    for f in listdir(d):
                        remove(path.join(d, f))
                    rmdir(d)
                except:
                    pass

def mycrypt(value, salt):
    return md5.new(value.lower() + salt + settings.SECRET_KEY).hexdigest()

class CaptchaWidget(Widget):
    """generate a captcha image and display the image along with
    a hidden field and a input field"""
    def __init__(self, options={}, *args, **kwargs):
        self.csettings = {
        'fgcolor': '#000000', # default:  '#000000' (color for characters and lines)
        'bgcolor': '#ffffff', # default:  '#ffffff' (color for background)
        'captchas_dir': None, # default:  None (uses MEDIA_ROOT/captchas)
        'upload_url': None, # default:  None (uses MEDIA_URL/captchas)
        'captchaconf_dir': None, # default:  None  (uses MEDIA_ROOT)
        'auto_cleanup': True, # default:  True (delete all captchas older than 20 minutes)
        'minmaxvpos': (8, 15), # default:  (8, 15) (vertical position of characters)
        'minmaxrotations': (-30,31), # default:  (-30,31) (rotate characters)
        'minmaxheight': (30,45), # default:  (30,45) (font size)
        'minmaxkerning': (-2,1), # default:  (-2,1) (space between characters)
        'alphabet': "abdeghkmnqrt2346789AEFGHKMNRT", # default:  "abdeghkmnqrt2346789AEFGHKMNRT"
        'num_lines': 1, # default: 1
        'line_weight': 3, # default: 3
        'imagesize': (200,60), # default: (200,60)
        'iterations': 1, # default 1 (change to a high value (200 is a good choice)
                         # for trying out new settings)
        }
        # change colors to tuples if possible
        try:
            for k in settings.CAPTCHA.keys():
                self.csettings[k] = settings.CAPTCHA[k]
        except:
            pass
        for k in options.keys():
            self.csettings[k] = options[k]
        for col in ('fgcolor', 'bgcolor'):
            if not isinstance(self.csettings[col], (list, tuple)):
                self.csettings[col] = ImageColor.getrgb(self.csettings[col])

        self.csettings['captchas_dir'] = self.csettings.get('captchas_dir') or \
                path.join(settings.MEDIA_ROOT, 'captchas')
        self.csettings['upload_url'] = self.csettings.get('upload_url') or \
                basejoin(settings.MEDIA_URL, "captchas")

        if not self.csettings['captchaconf_dir']:
            self.csettings['captchaconf_dir'] = settings.MEDIA_ROOT

        super(CaptchaWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        img = Image.new('RGB',self.csettings['imagesize'], self.csettings['bgcolor'])
        for dummy in range(self.csettings['iterations']):
            img = self.generate_image(img)
        return mark_safe(u'''<input type="hidden" name="%(name)s" value="captcha.%(hiddentext)s"
/><img src="%(imageurl)s" alt="" /><br
/><input type="text" name="%(name)s" id="id_%(name)s" />''' % {'name':name,
        'hiddentext': self.hiddentext,
        'imageurl': self.imageurl })

    def generate_image(self, bgimage):
        """ create a image file.
        the filename looks like TMPNAME.HASH.EXT
        where TMPNAME is a system generated temporary name and
        HASH is the hashed solution.
        """
        if self.csettings['auto_cleanup']:
            clean_old_entries(self.csettings['captchas_dir'])

        cs = self.csettings
        imagesize = cs['imagesize']
        posnew = 7
        fontdir = path.join(cs['captchaconf_dir'], 'fonts')
        fontnames = [path.join(fontdir, x) for x in listdir(fontdir) ]

        # generate characters
        solution = ''
        for i in range(choice((5,6))):
            solution += choice(cs['alphabet'])

        # render characters
        for c in solution:
            fgimage = Image.new('RGB', imagesize, cs['fgcolor'])
            font = ImageFont.truetype(choice(fontnames), randrange(*cs['minmaxheight']))
            charimage = Image.new('L', font.getsize(' %s ' % c), '#000000')
            draw = ImageDraw.Draw(charimage)
            draw.text((0,0), ' %s' % c, font=font, fill='#ffffff')
            charimage = charimage.rotate(randrange(*cs['minmaxrotations']), expand=1,
                    resample=Image.BICUBIC)
            charimage = charimage.crop(charimage.getbbox())
            maskimage = Image.new('L', imagesize)
            ypos = randrange(*cs['minmaxvpos'])
            maskimage.paste(charimage,
                    (posnew, ypos,
                        charimage.size[0]+posnew,
                        charimage.size[1]+ypos)
                    )
            bgimage = Image.composite(fgimage, bgimage, maskimage)
            posnew += charimage.size[0] + randrange(*cs['minmaxkerning'])

        # draw line(s)
        for dummy in range(cs.get('num_lines')):
            linex = choice( range(2, cs['minmaxheight'][1]) )
            minmaxliney = ( cs['minmaxvpos'][0],
                    cs['minmaxvpos'][1] + cs['minmaxheight'][0])
            linepoints = [linex, randrange(*minmaxliney)]
            while linex < posnew:
                linex += randrange(*cs['minmaxheight']) * 0.8
                linepoints.append(linex)
                linepoints.append(randrange(*minmaxliney))
            draw = ImageDraw.Draw(bgimage)
            draw.line(linepoints, width=cs['line_weight'],
                fill=cs['fgcolor'])

        # save file
        if not access(cs['captchas_dir'], W_OK):
            mkdir(cs['captchas_dir'])
            chmod(cs['captchas_dir'], 0755)
        dirpath = tempfile.mkdtemp(prefix='c', dir=cs['captchas_dir'])
        chmod(dirpath, 0755)
        self.hiddentext = dirpath[dirpath.rfind(sep)+1:]
        plainfilename = mycrypt(solution, self.hiddentext)
        self.imageurl = '%s/%s/%s' % (cs['upload_url'],
                self.hiddentext, plainfilename)
        imagepath = path.join(dirpath, plainfilename)
        bgimage.convert('P', palette=Image.ADAPTIVE, colors=4).save(imagepath + '.gif', transparency=0)
        ext = '.gif'
        self.imageurl += ext
        chmod(imagepath + ext, 0644)
        return bgimage

    def value_from_datadict(self, data, files, name):
        if isinstance(data, MultiValueDict):
            return data.getlist(name)
        else:
            return data.get(name, None)

class CaptchaField(Field):
    """Field definition for a captcha

    Special options:
    fgcolor: color to use for the letters and line
    bgcolor: color to use for the background of the image
    captchas_dir: file system directory for the captchas
        defaults to [settings.MEDIA_ROOT]/captchas
    upload_url: absolute URL of captchas_dir
    captchaconf_dir: file system directory for the captcha module
        contains a "fonts" directory with all available fonts
    auto_cleanup: clean up captchas_dir deleting all entries older
        than 30 minutes
    """

    def __init__(self, required=True, label=None, help_text=None,
            options={}, *args, **kwargs):
        try:
            settingcaptchas_dir = settings.CAPTCHA['captchas_dir']
        except:
            settingcaptchas_dir = None
        self.captchas_dir = options.get('captchas_dir') or settingcaptchas_dir or \
                path.join(settings.MEDIA_ROOT, 'captchas')
        super(CaptchaField, self).__init__(required=required,
            widget=CaptchaWidget(options=options),
            label=label, help_text=help_text, *args, **kwargs
            )

    def clean(self, value):
        errormsg = gettext(u'You did not enter the correct code.')
        if not isinstance(value, (list, tuple)):
            raise ValidationError(errormsg)
        hiddenval = None
        val = None
        for val in value:
            if val.startswith('captcha.'):
                hiddenval = val[8:]
            else:
                val = ''.join(val.split())
        if not hiddenval:
            raise ValidationError(errormsg)

        imagedir = path.join(self.captchas_dir, hiddenval)
        success = False
        for ext in ('.gif', '.jpg', '.png'):
            if access(path.join(imagedir, mycrypt(val, hiddenval) + ext), R_OK):
                success = True

        try:
            for f in listdir(imagedir):
                remove(path.join(imagedir, f))
            rmdir(imagedir)
        except OSError:
            pass

        if not success:
            raise ValidationError(errormsg)

        return True

