import zipfile

z = zipfile.ZipFile("1.docx")
print(dir(z))

all_files = z.namelist()
print(all_files)

images = filter(lambda x: x.startswith('word/media/'), all_files)
print('Количество изображений: ', len(images))
