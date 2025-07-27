import catprint
import PIL.Image
import textwrap
import random

def ikea_receipt_banner(text: str) -> PIL.Image.Image:
    def r(n):
        return ''.join(str(random.randint(0, 9)) for _ in range(n))

    return catprint.render.stack(
        PIL.Image.open("img/ikea.png"),
        catprint.render.blank(20),
        catprint.render.text(
            textwrap.dedent(
                f"""\
                IKEA Česká republika, s.r.o.
                Skandinávská 131/1,  155 00  Praha 5
                IČO  27081052,       DIČ  CZ27081052
                ****************************************
                IKEA Family          {r(19)}
                """
            )
        ),
        catprint.render.banner(text),
        catprint.render.text(
            textwrap.dedent(
                f"""\
                Číslo pokladní:   {r(8)}
                Datum    Čas       Obchod POS  Transak
                23.08.25 16:00:42     {r(3)} {r(3)}      {r(3)}
                Číslo dokladu:
                {r(3)}-{r(3)}-{r(3)}-{r(14)}
                **************************************
                abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
                DATUM VYSTAVENÍ JE DATUM ZDANIT.PLNĚNÍ
                USCHOVEJTE PRO REKLAMACI! *DĚKUJEME*
                Číslo provozovny: {r(2)}
                Pokrmy jsou určené k okamžité spotřebě
                """
            )
        ),
    )
