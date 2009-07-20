from django.core.management.base import NoArgsCommand
from nr_comics.models import Comic
import urllib, re
from django.conf import settings

api_domain = "http://ohnorobot.com/"
comic_id = "48"

class Command(NoArgsCommand):
    help = "Updates the transcriptions at ohnorobot.com"
    
    def handle_noargs(self, **options):
        f = urllib.urlopen(api_domain + "/js/" + comic_id + ".js")
        cmatch = re.compile('u\[\d+\]="s(\d+)"')
        urls = []
        for line in f:
            for token in line.split(";"):
                m = cmatch.match(token)
                if m:
                    urls.append(int(m.group(1)))
        urls.sort()
        last_ohno = urls[-1]
        last_onsite = Comic.comics.public().count()
        for i in Comic.comics.public()[last_ohno-1:]:
            request = "&".join([
                "u=%s" % settings.OHNOROBOT_U,
                "p=%s" % settings.OHNOROBOT_P,
                "c=ADD",
                "url=http://nameremoved.com%s" % i.get_absolute_url(),
                "t=%s" % urllib.quote(i.title),
                "d=%s" % urllib.quote(i.transcript)
            ])
            rurl = urllib.urlopen("%sapi.pl?%s" % (api_domain, request))
            print i.title
            for line in rurl:
                print line,
            print
            