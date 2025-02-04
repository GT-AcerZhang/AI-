#coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import argparse
import functools
import numpy as np
import paddle.fluid as fluid
import deeplearning_backbone.paddlecv.model_provider as paddlecv
#加载自定义文件
import models
from attack.attack_pp import FGSM, PGD, M_PGD, G_FGSM, L_PGD, T_PGD, T_FGSM
from utils import init_prog, save_adv_image, process_img, tensor2img, calc_mse, add_arguments, print_arguments
with_gpu = os.getenv('WITH_GPU', '0') != '0'
#######parse parameters
parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)

add_arg('class_dim',        int,   120,                  "Class number.")
add_arg('shape',            str,   "3,224,224",          "output image shape")
add_arg('input',            str,   "./input_image/",     "Input directory with images")
add_arg('output',           str,   "./output_image/",    "Output directory with images")
add_arg('tt',               int,   0,                    "the num is model")


args = parser.parse_args()
print_arguments(args)

######Init args
image_shape = [int(m) for m in args.shape.split(",")]
class_dim=args.class_dim
input_dir = args.input
output_dir = args.output
tt = args.tt

# model_name ="ResNeXt50_32x4d"
# pretrained_model = "../paddle1.5/ResNeXt50_32x4dxxxxxxxxxxx"
# pretrained_model = ["../paddle1.5/ResNeXt50_32x4dxx",
#                     "../paddle1.5/ResNeXt50_32x4dxxx",
#                     "../paddle1.5/ResNeXt50_32x4dxxxx",
#                     "../paddle1.5/ResNeXt50_32x4dxxxxx",
#                     "../paddle1.5/ResNeXt50_32x4dxxxxxx",
#                     "../paddle1.5/ResNeXt50_32x4dxxxxxxxxx",
#                     "../paddle1.5/ResNeXt50_32x4dxxxxxxxxxx",
#                     "../paddle1.5/ResNeXt50_32x4dxxxxxxxxxxx"]

# model_name0 = "MobileNetV2_x2_0"
# pretrained_model0 = "../paddle1.5/MobileNetV2"

# model_name0 = "InceptionV4"
# pretrained_model0 = "../paddle1.5/InceptionV4"
#
# model_name0 = "VGG19"
# pretrained_model0 = "../paddle1.5/VGG19"

# model_name0 = "DistResNet"
# pretrained_model0 = "../paddle1.5/DistResNet"

# model_name0 ="SE_ResNeXt101_32x4d"
# pretrained_model0 ="../paddle1.5/SE_ResNeXt101_32x4d"


# model_name = "DarkNet53"
# pretrained_model = "../paddle1.6/DarkNet53"

# model_name = "DenseNet161"
# pretrained_model = "../paddle1.6/DenseNet161"

# model_name = "DPN131"
# pretrained_model = "../paddle1.6/DPN131"

model_name0 = "VGG16"
pretrained_model0 = "../paddle1.6/VGG16"

# model_name = "ResNeXt101_32x8d_wsl"
# pretrained_model = "../paddle1.6/ResNeXt101_32x8d_wsl"

model_name0 = "ResNet50"
pretrained_model0 = "../paddle1.6/ResNet50"

# model_name = "SE_ResNet50_vd"
# pretrained_model = "../paddle1.6/SE_ResNet50_vd"

model_name0 = "EfficientNetB0"
pretrained_model0 = "../paddle1.6/EfficientNetB0"

# model_name = "ShuffleNetV2_swish"
# pretrained_model = "../paddle1.6/ShuffleNetV2_swish"

# model_name = "AlexNet"
# pretrained_model = "../paddle1.6/AlexNet"

# model_name = "SqueezeNet1_1"
# pretrained_model = "../paddle1.6/SqueezeNet1_1"

#
# model_name = "ResNet50_vd"
# pretrained_model = "../paddle1.6/ResNet50_vd"

model_name0 ="DenseNet121"
pretrained_model0 ="../paddle1.6/DenseNet121"
#
# model_name0 ="Xception65"
# pretrained_model0 ="../paddle1.6/Xception65"
#
# model_name ="EfficientNetB4"
# pretrained_model ="../paddle1.6/EfficientNetB4"
#
# model_name ="Res2Net50_26w_4s"
# pretrained_model ="../paddle1.6/Res2Net50_26w_4s"
#
# model_name ="HRNet_W32_C"
# pretrained_model ="../paddle1.6/HRNet_W32_C"
#
# model_name ="ResNeXt101_vd_32x4d"
# pretrained_model ="../paddle1.6/ResNeXt101_vd_32x4d"
#
model_name0 = "ResNeXt50_vd_32x4d"
pretrained_model0 = "../paddle1.6/ResNeXt50_vd_32x4d"

# model_name ="ResNeXt50_vd_64x4d"
# pretrained_model ="../paddle1.6/ResNeXt50_vd_64x4d"
#
# model_name ="ShuffleNetV2_x2_0"
# pretrained_model ="../paddle1.6/ShuffleNetV2_x2_0"
#
# model_name ="SENet154_vd"
# pretrained_model ="../paddle1.6/SENet154_vd"

model_name0 ="ResNeXt152_64x4d"
pretrained_model0 ="../paddle1.6/ResNeXt152_64x4d"

# model_name0 ="ResNeXt101_32x32d_wsl"
# pretrained_model0 ="../paddle1.6/ResNeXt101_32x32d_wsl"

model_name0 ="DenseNet264"
pretrained_model0 ="../paddle1.6/DenseNet264"

model_name0 ="HRNet_W64_C"
pretrained_model0 ="../paddle1.6/HRNet_W64_C"
# model_name = ["ResNeXt50_32x4d", "MobileNetV2_x2_0", "InceptionV4", "VGG19", "DistResNet", "SE_ResNeXt101_32x4d"]
# pretrained_model = ["../paddle1.5/ResNeXt50_32x4d", "../paddle1.5/MobileNetV2", "../paddle1.5/InceptionV4", "../paddle1.5/VGG19", "../paddle1.5/DistResNet", "../paddle1.5/SE_ResNeXt101_32x4d"]
# #
# model_name = ["DarkNet53", "DenseNet161", "DPN131", "VGG16", "ResNeXt101_32x8d_wsl", "ResNet50", "SE_ResNet50_vd", "EfficientNetB0", "ShuffleNetV2_swish", "AlexNet", "SqueezeNet1_1", "ResNet50_vd", "DenseNet121", "Xception65", "EfficientNetB4", "Res2Net50_26w_4s", "HRNet_W32_C", "ResNeXt101_vd_32x4d", "ResNeXt50_vd_64x4d", "ShuffleNetV2_x2_0", "SENet154_vd", "InceptionV4"]
# pretrained_model = "../paddle1.6/" + model_name[tt]

model_name = "DARTS_4M"
pretrained_model = "../paddle1.6/DARTS_4M"

model_name0 = "DARTS_6M"
pretrained_model0 = "../paddle1.6/DARTS_6M"

val_list = 'val_list.txt'
use_gpu=False

######Attack graph

adv_program=fluid.Program()
#完成初始化
with fluid.program_guard(adv_program):

    input_layer = fluid.layers.data(name='image', shape=image_shape, dtype='float32')
    # 设置为可以计算梯度
    input_layer.stop_gradient = False

    #model definition
    model = models.__dict__[model_name]()
    #model = paddlecv.get_model("inceptionv4")

    out_logits = model.net(input=input_layer, class_dim=class_dim)
    out = fluid.layers.softmax(out_logits)

    # place = fluid.CUDAPlace(0) if with_gpu else fluid.CPUPlace()
    place = fluid.CPUPlace()
    exe = fluid.Executor(place)
    exe.run(fluid.default_startup_program())

    fluid.io.load_params(executor=exe, dirname=pretrained_model, main_program=adv_program)


#设置adv_program的BN层状态
init_prog(adv_program)

#创建测试用评估模式
eval_program = adv_program.clone(for_test=True)

### 定义梯度
with fluid.program_guard(adv_program):
    label = fluid.layers.data(name="label", shape=[1] ,dtype='int64')
    loss = fluid.layers.cross_entropy(input=out, label=label)
    gradients = fluid.backward.gradients(targets=loss, inputs=[input_layer])[0]




######Inference
def inference(img):
    fetch_list = [out.name]

    result = exe.run(eval_program,
                     fetch_list=fetch_list,
                     feed={ 'image':img })
    result = result[0][0]
    pred_label = np.argmax(result)
    pred_score = result[pred_label].copy()
    return pred_label, pred_score

######FGSM attack
#untarget attack
def attack_nontarget_by_FGSM(img, src_label):
    pred_label = src_label
    #mom = 0.8
    step = 8.0/256.0
    eps = 128.0/256.0
    while pred_label == src_label:

        #生成对抗样本
        # adv=L_PGD(adv_program=adv_program,eval_program=eval_program,gradients=gradients,o=img,
        #          input_layer=input_layer,output_layer=out, step_size=step,epsilon=eps, iteration=8, pix_num=224*224*3/30,
        #          isTarget=False,target_label=0,use_gpu=use_gpu)

        # adv = G_FGSM(adv_program=adv_program, eval_program=eval_program, gradients=gradients, o=img,
        #             input_layer=input_layer, output_layer=out, step_size=step, epsilon=eps,
        #             pix_num=224 * 224 * 3, isTarget=False, target_label=0, use_gpu=use_gpu)

        # adv = T_PGD(adv_program=adv_program, eval_program=eval_program, gradients=gradients, o=img,
        #              input_layer=input_layer, output_layer=out, step_size=step, epsilon=eps,iteration=8,t=0,
        #              pix_num=3*224*224/30, isTarget=False, target_label=0, use_gpu=use_gpu)

        adv = T_FGSM(adv_program=adv_program, eval_program=eval_program, gradients=gradients, o=img,
                     input_layer=input_layer, output_layer=out, step_size=step, epsilon=eps, t=0.6,
                     pix_num=3*224*224/30, isTarget=False, target_label=0, use_gpu=use_gpu)

        pred_label, pred_score = inference(adv)
        step *= 1.5
        #mom *= 0.8
        if step > eps:
            break


    print("Test-score: {0}, class {1}".format(pred_score, pred_label))

    if pred_label != src_label:
        print("攻击成功，{0}->{1}".format(src_label, pred_label))
    else:
        adv = img
        print("攻击失败，去除扰动，保存为源图像")

    adv_img=tensor2img(adv)
    return adv_img

######PGD attack
#untarget attack
def attack_nontarget_by_PGD(img, src_label):
    pred_label = src_label

    step = 8.0/256.0
    eps = 16.0/256.0
    while pred_label == src_label:
        #生成对抗样本
        adv=PGD(adv_program=adv_program,eval_program=eval_program,gradients=gradients,o=img,
                 input_layer=input_layer,output_layer=out,step_size=step,epsilon=eps,iteration=10,
                 isTarget=False,target_label=0,use_gpu=use_gpu)

        pred_label, pred_score = inference(adv)
        step *= 2
        if step > eps:
            break

    print("Test-score: {0}, class {1}".format(pred_score, pred_label))



    adv_img=tensor2img(adv)
    return adv_img


####### Main #######
def get_original_file(filepath):
    with open(filepath, 'r') as cfile:
        full_lines = [line.strip() for line in cfile]
    cfile.close()
    original_files = []
    for line in full_lines:
        label, file_name = line.split()
        original_files.append([file_name, int(label)])
    return original_files




def gen_adv():
    mse = 0
    original_files = get_original_file(input_dir + val_list)
    num = 1
    cout = 0

    print("the model is {}".format(model_name))
    for filename, label in original_files:



        img_path = input_dir + filename
        print("Image: {0} ".format(img_path))
        img=process_img(img_path)

        #print(img.shape)

        result = exe.run(eval_program,
                         fetch_list=[out],
                         feed={input_layer.name: img})
        result = result[0][0]

        o_label = np.argsort(result)[::-1][:1][0]

        print("原始标签为{0}".format(o_label))

        if o_label == int(label):
            adv_img = attack_nontarget_by_FGSM(img, label)
            #adv_img = attack_nontarget_by_PGD(img, label)
        else:
            print("{0}个样本已为对抗样本, name为{1}".format(num, filename))
            img = tensor2img(img)
            #print(img.shape)
            image_name, image_ext = filename.split('.')
            save_adv_image(img, output_dir + image_name + '.png')
            num += 1
            cout += 1
            continue
        image_name, image_ext = filename.split('.')
        ##Save adversarial image(.png)
        save_adv_image(adv_img, output_dir+image_name+'.png')

        org_img = tensor2img(img)
        score = calc_mse(org_img, adv_img)
        mse += score
        num += 1
    print("成功attack的有 {}".format(120-cout))
    print("ADV {} files, AVG MSE: {} ".format(len(original_files), mse/len(original_files)))


def main():
    #gen_adv(0)
    gen_adv()


if __name__ == '__main__':
    main()
