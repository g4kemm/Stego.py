# Görüntü Steganografisini uygulayan Python programı

# PIL module is used to extract
from PIL import Image

# Kodlama verilerini 8 bit ikili dosyaya dönüştürün
# karakterlerin ASCII değerini kullanan form
def genData(data):

        # ikili kod listesi
        # verilen veri
        yenid = []

        for i in data:
            yenid.append(format(ord(i), '08b'))
        return yenid

# Pikseller buna göre değiştirilir
# 8-bit ikili veri ve sonunda döndürüldü
def modPix(pix, data):

    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Bir seferde 3 piksel çıkarma
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]

        # Piksel değeri yapılmalı
        # 1 için tek ve 0 için çift
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1

        # Her kümenin sekizinci pikseli söyler
        # daha fazla okumanın durdurulup durdurulmayacağı.
        # 0 okumaya devam et anlamına gelir; 1 demektir
        #mesaj bitti.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Değiştirilen pikselleri yeni görüntüye yerleştirme
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# Verileri görüntüye kodlayın
def encode():
    img = input("Resim adını girin (uzantılı): ")
    image = Image.open(img, 'r')

    data = input("Kodlanacak verileri girin: ")
    if (len(data) == 0):
        raise ValueError('Veri Boş')

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = input("Yeni resmin adını girin(uzantılı) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Decode the data in the image
def decode():
    img = input("Resim adını girin (uzantılı): ")
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]

        # ikili veri dizisi
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

# Main Function
def main():
    a = int(input("::Steganografi'ye Hoş Geldiniz ::\n"
                        "1. Encode\n2. Decode\n"))
    if (a == 1):
        encode()

    elif (a == 2):
        print("Kodu Çözülen Kelime : " + decode())
    else:
        raise Exception("İnput girişi girin")

# Driver Code
if __name__ == '__main__' :

    # Calling main function
    main()