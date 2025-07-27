import asyncio
import catprint
import PIL.Image
from time import gmtime, strftime

START = """\

IKEA Česká republika, s.r.o.
Prodejna ASGARD,   Roseč 1,   378 46 Roseč
IČO 1337      DIČO 8008135      PYČO 69420
******************************************
  catprint v0.0.0 running on PufOS

"""



END = f"""\
 
Číslo pokladní:   0xDEADBEEF
Datum      Čas       Obchod  POS   Transak
{strftime("%Y-%m-%d %H:%M:%S", gmtime())}  42      34        007
Číslo dokladu:
123-456-789-{strftime("%Y%m%d%H%M%S", gmtime())}
******************************************
   catprint v0.0.0 running on PufOS
******************************************
DATUM VYSTAVENÍ JE DATUM ZDANIT.PLNĚNÍ
USCHOVEJTE PRO REKLAMACI! *DĚKUJEME*
Číslo provozovny: -1
Pokrmy jsou určené k okamžité spotřebě
"""

img = catprint.render.stack(
  PIL.Image.open("img/ikea.png"),
  catprint.render.text(START),
  catprint.render.text_banner("ORGOVNA"),
  catprint.render.text(END),
)

img.show()
# asyncio.run(catprint.printer.print(img))
