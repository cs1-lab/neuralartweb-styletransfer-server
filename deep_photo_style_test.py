from PIL import Image
import numpy as np
import os
from photo_style import stylize
from const import StyleConst


def main():

    style_const = StyleConst()
    # Input Options
    #style_const.content_image_path = "inputs/content_image/neuralart_orange_logo.jpg"
    #style_const.style_image_path = "inputs/style_image/hokusai.jpg"
    #style_const.content_seg_path = "inputs/content_seg/neuralart_orange_logo.jpg"
    #style_const.style_seg_path = "inputs/style_seg/hokusai_seg.jpg"
    style_const.content_image_path = "tmp/content_image.jpg"
    style_const.style_image_path = "tmp/style_image.jpg"
    style_const.content_seg_path = "tmp/content_seg.jpg"
    style_const.style_seg_path = "tmp/style_seg.jpg"
    # output Options
    style_const.init_image_path = ""
    style_const.output_image = "outputs/best_stylized/best_stylized.png"
    style_const.serial = "outputs"

    # Training Optimizer Options
    style_const.max_iter = 1000
    style_const.learning_rate = 1.0
    style_const.print_iter = 1
    style_const.save_iter = 100
    style_const.lbfgs = True

    # Weight Options
    style_const.content_weight = 5e0
    style_const.style_weight = 1e2
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


if __name__ == "__main__":
    main()
