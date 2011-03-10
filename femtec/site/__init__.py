
from django.template import Context, loader
from django.contrib.auth.models import User

def email_all_users(title, template, context=None, test=False, exclude=[]):
    """Send an E-mail to all users. """
    template = loader.get_template('e-mails/user/%s.txt' % template)

    if test:
        users = User.objects.filter(is_superuser=True)
    else:
        users = User.objects.all()

    for user in users:
        if user in exclude:
            continue

        _context = {'user': user}

        if context is not None:
            _context.update(context)

        print ">>> Sending to %s" % user
        body = template.render(Context(_context))
        user.email_user("[FEMTEC 2011] %s" % title, body)

