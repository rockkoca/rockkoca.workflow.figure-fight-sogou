#!/usr/bin/env python
# -*- coding: utf-8 -*-

from workflow import Workflow3
from lib import GifFight
import sys

reload(sys)
sys.setdefaultencoding('utf8')

ICON_UPDATE = 'icon_update.png'


def check_update():
    if wf.update_available:
        arg = ['', '', '', '', 'error']
        arg = '$%'.join(arg)
        wf.add_item(
            title='New Version', subtitle='', arg=arg,
            valid=True, icon=ICON_UPDATE)
    else:
        wf.add_item('Gif Fight')


def main(wf):
    query = wf.args[0].strip().replace("\\", "")

    def get_data():
        return GifFight.get_instance().get_images(query)

    age = 3600 * 24 * 365
    # wf.clear_cache()
    imgs = wf.cached_data(query, max_age=age) or wf.cached_data(query, get_data, max_age=age)
    GifFight.download_images(imgs.get('imgs', []), True)
    if not imgs.get('err') and imgs.get('imgs'):
        for img in imgs['imgs']:
            wf.add_item(
                title=img['url'],
                subtitle=img['path'],
                arg=img['path'],
                # arg=img['url'],
                valid=True,
                icon=img['path'],
            )
    # logging.debug(wf.items())
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3(update_settings={
        'github_slug': 'rockkoca/alfred.workflows.figure-fight-sogou',

        'frequency': 7
    })
    sys.exit(wf.run(main))
