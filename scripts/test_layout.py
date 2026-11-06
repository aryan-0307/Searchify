import subprocess
import os
import re

for page in ['sorting.html', 'searching.html']:
    html = open(page, encoding='utf-8').read()
    # Let's reorder: Array, Playback, Settings in HTML
    # and adjust CSS to test
    html_mod = html
    # Swap settings and playback cluster in HTML
    # Let's inspect where they are
    pass

