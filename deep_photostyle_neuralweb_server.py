from logging import getLogger, StreamHandler, DEBUG, WARN
from PIL import  Image
import numpy as np
import datetime

from photo_style import stylize
from const import StyleConst
from neuralartweb.api_v0.utils import neuralweb_material_download, get_material_detail


class DeepPhotostyleNeuralwebServer:

    def __init__(self, logger=None):
        self.logger = logger or self._logger()
        self.year = ""
        self.month = ""
        self.day = ""
        self.hour = ""
        self.material_detail = None
        self.parameters = None

    def run_everything(self):
        """
        画風変換の一連の作業を実施する関数
        apiからのダウンロードも行う
        :return:
        """
        self.set_start_time()
        if self.prepare_material():
            self.run_deep_photostyle()
            self.logger.info("Successfully complete style transfer.")
        else:
            self.logger.error("Bad prepare material.")

    def prepare_material(self):
        """
        画風変換の素材の用意をする

        変換画像は /tmp 以下にダウンロードされます。
        :return:
        """
        if neuralweb_material_download(self.year, self.month, self.day, self.hour):
            self.logger.debug("Successfully prepare material")
            self.material_detail = get_material_detail(self.year, self.month, self.day, self.hour)
            self.parameters = self.material_detail["parameters"]
            return True
        else:
            self.logger.warn("Fail to prepare material")
            return False

    def run_deep_photostyle(self):
        """
        画風変換を実施する
        :return:
        """
        style_const = StyleConst()
        # Neural Art WebAPIに関する情報も渡す
        style_const.material_detail = self.material_detail

        # Input Options
        # 素材フォルダはあらかじめ決めている
        style_const.content_image_path = "tmp/content_image.jpg"
        style_const.style_image_path = "tmp/style_image.jpg"
        style_const.content_seg_path = "tmp/content_seg.jpg"
        style_const.style_seg_path = "tmp/style_seg.jpg"
        # output Options
        style_const.init_image_path = ""
        style_const.output_image = "outputs/best_stylized/best_stylized.png"
        style_const.serial = "outputs"

        # Training Optimizer Options
        #style_const.max_iter = 1000
        style_const.max_iter = int(self.parameters["max_iter"])
        style_const.learning_rate = 1.0
        style_const.print_iter = 1
        style_const.save_iter = 100
        style_const.lbfgs = True

        # Weight Options
        #style_const.content_weight = 5e0
        style_const.content_weight = float(self.parameters["content_weight"])
        #style_const.style_weight = 1e2
        style_const.style_weight = float(self.parameters["style_weight"])
        style_const.tv_weight = 1e-3
        style_const.affine_weight = 1e4

        # style Options
        style_const.style_option = 0
        style_const.apply_smooth = True

        # Smoothing Argment
        style_const.f_radius = 15
        style_const.f_edge = 1e-1

        beset_image_bgr = stylize(style_const, False)
        result = Image.fromarray(np.uint8(np.clip(beset_image_bgr[:, :, ::-1], 0, 255.0)))
        result.save(style_const.output_image)

    def set_start_time(self):
        """
        neuralartweb apiに渡す日付を計算する関数
        :return:
        """
        # 実行は10分前を想定している
        # ex: 生成開始時間が10:00の場合
        # cronでの実行開始は9:50となる
        now = datetime.datetime.now()
        now = now + datetime.timedelta(hours=1)  # 1時間進める
        now = datetime.datetime(2019, 1, 11, 14)  # テスト用(本番時はコメントアウトすること)

        self.year = str(now.year)
        self.month = str(now.month)
        self.day = str(now.day)
        self.hour = str(now.hour)

        """"
        self.year = "2018"
        self.month = "12"
        self.day = "19"
        self.hour = "17"
        """

    def _logger(self):
        _logger = getLogger(__name__)
        _handler = StreamHandler()
        _handler.setLevel(DEBUG)
        _logger.setLevel(DEBUG)
        _logger.addHandler(_handler)
        _logger.propagate = False

        return _logger


if __name__ == "__main__":
    logger = getLogger(__name__)
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.propagate = False



    dpns = DeepPhotostyleNeuralwebServer(logger)
    dpns.run_everything()
