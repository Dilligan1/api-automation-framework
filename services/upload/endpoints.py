# Эндпоинт загрузки изображений (multipart/form-data, до 5 MB).

from config.stages import API_PREFIX


class UploadEndpoints:
    image = f"{API_PREFIX}/upload/image"
