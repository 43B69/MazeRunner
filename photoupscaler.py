from PIL import Image


# Увеличиваем разрешение изображения, путём наращивания размеров пикселя.
# Пример увеличения в 2 раза:
#
#            1100
# 10  ----\  1100
# 01  ----/  0011
#            0011
#
# Входные данные: file_name - название файла, k - кратность увеличения (чётное число)
#                 result_file_name - конечное название файла
def upscale_image(file_name, k, result_file_name):
    with Image.open(file_name) as original_image:
        original_image.load()
    original_image_size = original_image.size
    result_image_size = (original_image_size[0] * k, original_image_size[1] * k)
    print(result_image_size, original_image_size)
    result_image = original_image.resize(result_image_size, Image.NEAREST)
    result_image.save(result_file_name)


lk = 10
# upscale_image("data/MAIN_ROOM_TEXTURES.png", lk, f"data/MAIN_ROOM_TEXTURES_UP_{lk}.png")
# upscale_image("data/player2.png", 7, f"data/player2C.png")
upscale_image("data/ghost.png", 7, f"data/ghost_UP.png")
upscale_image("data/zombie.png", 7, f"data/zombie_UP.png")
upscale_image("data/CHEST.png", 7, f"data/chest_UP.png")