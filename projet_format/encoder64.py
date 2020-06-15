import base64
import PIL.Image
from io import BytesIO

buffered = BytesIO()

src = r'C:\Users\DGX\Desktop\graphics\textures\aqf018.png'
src = r'C:\Users\DGX\Desktop\graphics\textures\floor4_6.png'
src = r'C:\Users\DGX\Desktop\graphics\textures\flat1_2.png'
src = r'C:\Users\DGX\Desktop\graphics\textures\rrock11.png'
src = r'C:\Users\DGX\Desktop\graphics\textures\aqf010.png'
src = r'C:\Users\DGX\Desktop\graphics\weapons\pisga0.png'

i = PIL.Image.open(src)
i.save(buffered, format="PNG")

s = base64.b64encode(buffered.getvalue())
print('data:image/png;base64,' + str(s))
