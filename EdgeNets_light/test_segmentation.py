import torch
import glob
import os
import numpy
from argparse import ArgumentParser
from PIL import Image
from torchvision.transforms import functional as F
from tqdm import tqdm

from utilities.print_utils import *
from utilities.utils import model_parameters, compute_flops
from utilities.segmentation_miou import runningScore,averageMeter
from model.espnetv2 import espnetv2_seg
import imageio

import time


torch.set_grad_enabled(False) 

torch.backends.cudnn.enabled = True
torch.backends.cudnn.benchmark = True



####################################################################

MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]


model_weight_map = {}
# key is of the form <model-name_model-scale>


#ESPNetv2
espnetv2_scales = [0.5, 1.0, 1.5, 2.0]
for scale in espnetv2_scales:
    model_weight_map['espnetv2_{}'.format(scale)] = {
        'pascal_256x256':
            {
                'weights': 'model/model_zoo/espnetv2/espnetv2_s_{}_pascal_256x256.pth'.format(scale)
            },
        'pascal_384x384':
            {
                'weights': 'model/model_zoo/espnetv2/espnetv2_s_{}_pascal_384x384.pth'.format(scale)
            },
        'city_1024x512': {
            'weights': 'model/model_zoo/espnetv2/espnetv2_s_{}_city_1024x512.pth'.format(scale)
        },
        'city_512x256': {
            'weights': 'model/model_zoo/espnetv2/espnetv2_s_{}_city_512x256.pth'.format(scale)
        }
    }
#end



CITYSCAPE_CLASS_LIST = ['road', 'sidewalk', 'building', 'wall', 'fence', 'pole', 'traffic light', 'traffic sign',
                        'vegetation', 'terrain', 'sky', 'person', 'rider', 'car', 'truck', 'bus', 'train', 'motorcycle',
                        'bicycle', 'background']

# This represents all the different classes in the dataset that we are using, and the colors that the model will use
# for each class

COLORS = [  # [  0,   0,   0],
        [128, 64, 128],
        [244, 35, 232],
        [70, 70, 70],
        [102, 102, 156],
        [190, 153, 153],
        [153, 153, 153],
        [250, 170, 30],
        [220, 220, 0],
        [107, 142, 35],
        [152, 251, 152],
        [0, 130, 180],
        [220, 20, 60],
        [255, 0, 0],
        [0, 0, 142],
        [0, 0, 70],
        [0, 60, 100],
        [0, 80, 100],
        [0, 0, 230],
        [119, 11, 32],
    ]

####################################################################


def decode_segmap(temp, seg_classes=19):

    label_colours = dict(zip(range(seg_classes), COLORS))

    r = temp.copy()
    g = temp.copy()
    b = temp.copy()
    for l in range(0, seg_classes-1): #Bug fix here
        # print(l)
        r[temp == l] = label_colours[l][0]
        g[temp == l] = label_colours[l][1]
        b[temp == l] = label_colours[l][2]
    #end

    rgb = numpy.zeros((temp.shape[0], temp.shape[1], 3))
    rgb[:, :, 0] = r #/ 255.0
    rgb[:, :, 1] = g #/ 255.0
    rgb[:, :, 2] = b #/ 255.0
    return rgb
#end

def main(args):
    # read all the images in the folder
    image_path = os.path.join(args.data_path, "leftImg8bit", args.split, "*", "*.png")
    image_list = glob.glob(image_path)

    if len(image_list) == 0:
        print_error_message('No files in directory: {}'.format(image_path))
    #end

    # set-up mIoU evaluator
    seg_classes = len(CITYSCAPE_CLASS_LIST)
    miou_class = runningScore(n_classes=seg_classes)
    # run_time = averageMeter(100)

    new_run_time = []

    # initialize model
    args.classes = seg_classes
    model = espnetv2_seg(args)
 
    # print model information
    num_params = model_parameters(model)
    flops = compute_flops(model, input=torch.Tensor(1, 3, args.im_size[0], args.im_size[1]))
    print_info_message('FLOPs for an input of size {}x{}: {:.2f} million'.format(args.im_size[0], args.im_size[1], flops))
    print_info_message('# of parameters: {}'.format(num_params))

    # load pretrained model
    model_key = '{}_{}'.format(args.model, args.s)
    print_info_message(f'Scale: {args.s}')
    dataset_key = '{}_{}x{}'.format(args.dataset, args.im_size[0], args.im_size[1])
    assert model_key in model_weight_map.keys(), '{} does not exist'.format(model_key)
    assert dataset_key in model_weight_map[model_key].keys(), '{} does not exist'.format(dataset_key)
    weights_test = model_weight_map[model_key][dataset_key]['weights']
    print_info_message('Loading model weights')
    weight_dict = torch.load(weights_test, map_location=torch.device('cpu'))
    model.load_state_dict(weight_dict)
    print_info_message('Weight loaded successfully')

    if not os.path.isfile(weights_test):
        print_error_message('weight file does not exist: {}'.format(weights_test))
    #end

    # deploy model to device
    num_gpus = torch.cuda.device_count()
    # print(num_gpus)
    device = 'cuda' if (num_gpus > 0) else 'cpu'
    # print(device)
    model = model.to(device=device)


    # start evaluation
    model.eval()
    # model.half()

    for i, imgName in tqdm(enumerate(image_list)):

        # get the path to groundtruth file
        gtName = imgName.replace('leftImg8bit','gtFine').replace('_ds.png','_labelTrainIds_ds.png')

        # read image and groundtruth
        img = Image.open(imgName).convert('RGB')
        gt = Image.open(gtName)

        # keep the input resolution for resizing output
        w, h = img.size

        # resize input to a give szie
        img = img.resize(tuple(args.im_size), Image.BILINEAR)
        img = F.to_tensor(img)  # convert to tensor (values between 0 and 1)
        img = F.normalize(img, MEAN, STD)  # normalize the tensor

        img = img.unsqueeze(0)  # add a batch dimension
        img = img.to(device)  #send input to device

        # img = img.half()

        # set-up timer
        if device == 'cuda':
            torch.cuda.synchronize()
        #end
        t_0 = time.time()

        img_out = model(img)  #testing

        # end-up timer
        if device == 'cuda':
            torch.cuda.synchronize()
        #end
        t_1 = time.time()

        new_run_time.append(t_1-t_0)

        # count time
        # run_time.update(t_1-t_0)
        # print_info_message(f'Time: {t_1-t_0}')
        # print_info_message(f'Check: {new_run_time[-1]}')

        img_out = img_out.squeeze(0)  # remove the batch dimension
        img_out = img_out.max(0)[1].byte()  # get the label map
        img_out = img_out.to(device='cpu').numpy()

        # resize to original size
        img_out = Image.fromarray(img_out)
        img_out = img_out.resize((w, h), Image.NEAREST)

        # evaluate IoU
        miou_class.update(numpy.array(gt), numpy.array(img_out))
        
        # save the segmentation mask
        if True:
            name = imgName.split('/')[-1]
            img_extn = imgName.split('.')[-1]
            name = '{}/{}'.format(args.savedir, name.replace(img_extn, 'png'))
            img_out = decode_segmap(numpy.array(img_out),seg_classes)
            imageio.imwrite(name, img_out.astype(numpy.uint8))
        #end
    #end



    # print mIoU and run time
    score = miou_class.get_scores()
    outscore = None
    for k, v in score.items():
        print_info_message('{} : {}'.format(k,v))
        outscore = v
    #end

    print_info_message('Speed : {} ms/f'.format(numpy.mean(new_run_time)))

    return {
            "s": args.s,
            "im_size": f"{args.im_size[0]}x{args.im_size[1]}",
            "flops": flops,
            "num_params": num_params,
            "miou": outscore,
            "speed": numpy.mean(new_run_time)
           }
#end

def alt_start(s, im_size): # to be called from data.py, basically identical to regular start

    parser = ArgumentParser()
    # mdoel details
    parser.add_argument('--model', default="espnetv2", choices=['espnetv2'], help='Model name')
    parser.add_argument('--s', default=s, type=float, help='scale')
    # dataset details
    parser.add_argument('--data-path', default="../vision_datasets/cityscapes/", help='Data directory')
    parser.add_argument('--dataset', default='city', choices=['city'], help='Dataset name')
    # input details
    parser.add_argument('--im-size', type=int, nargs="+", default=im_size, help='Image size for testing (W x H)')
    parser.add_argument('--split', default='val', choices=['val', 'test'], help='data split')
    parser.add_argument('--channels', default=3, type=int, help='Input channels')

    args = parser.parse_args()

    # set-up results path
    args.savedir = '{}_{}_{}/results'.format('results', args.dataset, args.split)

    if not os.path.isdir(args.savedir):
        os.makedirs(args.savedir)
    #end

    return main(args)

if __name__ == '__main__':

    parser = ArgumentParser()
    # mdoel details
    parser.add_argument('--model', default="espnetv2", choices=['espnetv2'], help='Model name')
    parser.add_argument('--s', default=1.0, type=float, help='scale')
    # dataset details
    parser.add_argument('--data-path', default="../vision_datasets/cityscapes/", help='Data directory')
    parser.add_argument('--dataset', default='city', choices=['city'], help='Dataset name')
    # input details
    parser.add_argument('--im-size', type=int, nargs="+", default=[512, 256], help='Image size for testing (W x H)')
    parser.add_argument('--split', default='val', choices=['val', 'test'], help='data split')
    parser.add_argument('--channels', default=3, type=int, help='Input channels')

    args = parser.parse_args()

    # set-up results path
    args.savedir = '{}_{}_{}/results'.format('results', args.dataset, args.split)

    if not os.path.isdir(args.savedir):
        os.makedirs(args.savedir)
    #end

    main(args)
#end
