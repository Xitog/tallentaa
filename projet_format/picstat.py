import PIL.Image

class ImageStat:

    def __init__(self, path, most_used=90):
        self.img = PIL.Image.open('map.png')
        self.pixels = {}
        for col in range(self.img.width):
            for row in range(self.img.height):
                pix = self.img.getpixel((col, row))
                if pix not in self.pixels:
                    self.pixels[pix] = 1
                else:
                    self.pixels[pix] += 1
        self.total = self.img.width * self.img.height
        self.most_used = most_used
        self.width = self.img.width
        self.height = self.img.height

    def getpixel(self, col, row):
        return self.img.getpixel((col, row))

    def info(self):
        print(f'Number of colors: {len(self.pixels)}')
        count = 0
        cumul = 0
        print('Most used colors:')
        for rgb in sorted(self.pixels, key=self.pixels.get, reverse=True):
            part = self.pixels[rgb]/self.total*100
            cumul += part
            print(count, rgb, self.pixels[rgb], f'{part:5.2f}', f'{cumul:5.2f}', sep='\t')
            count += 1
            if cumul >= self.most_used:
                break
        print(f'There are {count} most used colors (sum is >= {self.most_used})')
        print(f'Number of pixels = {self.total} ({self.img.width}x{self.img.height})')

if __name__ == '__main__':
    ims = ImageStat('map.png', 95)
    ims.info()
