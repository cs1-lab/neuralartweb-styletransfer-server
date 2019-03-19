import os
import shutil
import requests
import json

BASE_SERVER = "133.37.61.82:50503"

def neuralweb_material_download(year, month, day, hour):
    BASE_URL = "{}/api_v0".format(BASE_SERVER)
    MATERIAL_DETAIL_URL = "/material_detail"

    r = requests.get("http://{}{}/{}/{}/{}/{}".format(BASE_URL, MATERIAL_DETAIL_URL,
                                               year, month, day, hour))
    material_detail = json.loads(r.text)
    if not(len(material_detail) > 0):
        # 指定条件のmaterial detailが存在しないとき
        return False
    else:
        # 存在するときはダウンロードする
        material_detail = material_detail[0]  # material detail apiではリストの0番目が結果である
        save_photostyle_materials(material_detail["content_image"],
                                  material_detail["style_image"],
                                  material_detail["content_segmap"],
                                  material_detail["style_segmap"])
        return True  # 正常時は情報を返す


def get_material_detail(year, month, day, hour):
    BASE_URL = "{}/api_v0".format(BASE_SERVER)
    MATERIAL_DETAIL_URL = "/material_detail"

    r = requests.get("http://{}{}/{}/{}/{}/{}".format(BASE_URL, MATERIAL_DETAIL_URL,
                                               year, month, day, hour))
    material_detail = json.loads(r.text)
    if not(len(material_detail) > 0):
        return False
    else:
        return material_detail[0]


def save_photostyle_materials(content_image_url, style_image_url, content_seg_url, style_seg_url):
    TEMP_DIR = "tmp"
    clean_directory(TEMP_DIR)
    download_img(content_image_url, "{}/content_image.jpg".format(TEMP_DIR))
    download_img(style_image_url, "{}/style_image.jpg".format(TEMP_DIR))
    download_img(content_seg_url, "{}/content_seg.jpg".format(TEMP_DIR))
    download_img(style_seg_url, "{}/style_seg.jpg".format(TEMP_DIR))


def download_img(url, path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            f.write(r.content)


def clean_directory(target_dir):
    shutil.rmtree(target_dir)
    os.mkdir(target_dir)


def save_result(material_detail, img_path, iteration):
    """
    neural art webへの画像保存用
    :param img:
    :param iteration:
    :return:
    """
    BASE_URL = "{}/api_v0".format(BASE_SERVER)
    MATERIAL_DETAIL_URL = "/result_set"

    files = {}
    data = {}
    files["result_image"] = open(img_path, 'rb')
    data["iteration"] = iteration
    data["result_info"] = json.dumps(material_detail["parameters"])

    url = "http://{}{}/{}".format(BASE_URL, MATERIAL_DETAIL_URL, material_detail["id"])
    res = requests.post(url, files=files, data=data)


if __name__ == "__main__":
    year = "2018"
    month = "12"
    day = "21"
    hour = "11"

    neuralweb_material_download(year, month, day, hour)
