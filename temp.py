from alive_progress import alive_bar
from alive_progress.animations import bar_factory
from time import sleep

t=1000

_bar = bar_factory("▁▂▃▅▆▇", tip="", background=" ", borders=("|","|"))
with alive_bar(t, title=f"TITTOLO", spinner="waves", bar=_bar) as b:
    for i in range(t):
        sleep(0.01)
        b()