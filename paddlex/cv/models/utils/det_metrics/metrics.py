# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import paddle
import numpy as np
import json

from .map_utils import prune_zero_padding, DetectionMAP
from .coco_utils import get_infer_results, cocoapi_eval
import paddlex.utils.logging as logging

__all__ = ['Metric', 'VOCMetric', 'COCOMetric']


class Metric(paddle.metric.Metric):
    def name(self):
        return self.__class__.__name__

    def reset(self):
        pass

    def accumulate(self):
        pass

    # paddle.metric.Metric defined :metch:`update`, :meth:`accumulate`
    # :metch:`reset`, in ppdet, we also need following 2 methods:

    # abstract method for logging metric results
    def log(self):
        pass

    # abstract method for getting metric results
    def get_results(self):
        pass


class VOCMetric(Metric):
    def __init__(self,
                 labels,
                 overlap_thresh=0.5,
                 map_type='11point',
                 is_bbox_normalized=False,
                 evaluate_difficult=False,
                 classwise=False):

        self.cid2cname = {i: name for i, name in enumerate(labels)}
        self.overlap_thresh = overlap_thresh
        self.map_type = map_type
        self.evaluate_difficult = evaluate_difficult
        self.detection_map = DetectionMAP(
            class_num=len(labels),
            overlap_thresh=overlap_thresh,
            map_type=map_type,
            is_bbox_normalized=is_bbox_normalized,
            evaluate_difficult=evaluate_difficult,
            catid2name=self.cid2cname,
            classwise=classwise)

        self.reset()

    def reset(self):
        self.detection_map.reset()

    def update(self, inputs, outputs):
        bboxes = outputs['bbox'][:, 2:].numpy()
        scores = outputs['bbox'][:, 1].numpy()
        labels = outputs['bbox'][:, 0].numpy()
        bbox_lengths = outputs['bbox_num'].numpy()

        if bboxes.shape == (1, 1) or bboxes is None:
            return
        gt_boxes = inputs['gt_bbox'].numpy()
        gt_labels = inputs['gt_class'].numpy()
        difficults = inputs['difficult'].numpy(
        ) if not self.evaluate_difficult else None

        scale_factor = inputs['scale_factor'].numpy(
        ) if 'scale_factor' in inputs else np.ones(
            (gt_boxes.shape[0], 2)).astype('float32')

        bbox_idx = 0
        for i in range(gt_boxes.shape[0]):
            gt_box = gt_boxes[i]
            h, w = scale_factor[i]
            gt_box = gt_box / np.array([w, h, w, h])
            gt_label = gt_labels[i]
            difficult = None if difficults is None else difficults[i]
            bbox_num = bbox_lengths[i]
            bbox = bboxes[bbox_idx:bbox_idx + bbox_num]
            score = scores[bbox_idx:bbox_idx + bbox_num]
            label = labels[bbox_idx:bbox_idx + bbox_num]
            gt_box, gt_label, difficult = prune_zero_padding(gt_box, gt_label,
                                                             difficult)
            self.detection_map.update(bbox, score, label, gt_box, gt_label,
                                      difficult)
            bbox_idx += bbox_num

    def accumulate(self):
        logging.info("Accumulating evaluatation results...")
        self.detection_map.accumulate()

    def log(self):
        map_stat = 100. * self.detection_map.get_map()
        logging.info("mAP({:.2f}, {}) = {:.2f}%".format(
            self.overlap_thresh, self.map_type, map_stat))

    def get_results(self):
        return {'bbox': [self.detection_map.get_map()]}

    def get(self):
        map_stat = 100. * self.detection_map.get_map()
        stats = {
            "mAP({:.2f}, {})".format(self.overlap_thresh, self.map_type):
            map_stat
        }
        return stats


class COCOMetric(Metric):
    def __init__(self, coco_gt, classwise=False):
        self.clsid2catid = {
            i: cat['id']
            for i, cat in enumerate(coco_gt.loadCats(coco_gt.getCatIds()))
        }
        self.classwise = classwise
        self.bias = 0
        self.reset()

    def reset(self):
        # only bbox and mask evaluation support currently
        self.results = {'bbox': [], 'mask': []}
        self.eval_results = {}

    def update(self, inputs, outputs):
        outs = {}
        # outputs Tensor -> numpy.ndarray
        for k, v in outputs.items():
            outs[k] = v.numpy() if isinstance(v, paddle.Tensor) else v

        im_id = inputs['im_id']
        outs['im_id'] = im_id.numpy() if isinstance(im_id,
                                                    paddle.Tensor) else im_id

        infer_results = get_infer_results(
            outs, self.clsid2catid, bias=self.bias)
        self.results['bbox'] += infer_results[
            'bbox'] if 'bbox' in infer_results else []
        self.results['mask'] += infer_results[
            'mask'] if 'mask' in infer_results else []

    def accumulate(self):
        if len(self.results['bbox']) > 0:
            output = "bbox.json"
            if self.output_eval:
                output = os.path.join(self.output_eval, output)
            with open(output, 'w') as f:
                json.dump(self.results['bbox'], f)
                logging.info('The bbox result is saved to bbox.json.')

            bbox_stats = cocoapi_eval(
                output,
                'bbox',
                anno_file=self.anno_file,
                classwise=self.classwise)
            self.eval_results['bbox'] = bbox_stats
            sys.stdout.flush()

        if len(self.results['mask']) > 0:
            output = "mask.json"
            if self.output_eval:
                output = os.path.join(self.output_eval, output)
            with open(output, 'w') as f:
                json.dump(self.results['mask'], f)
                logging.info('The mask result is saved to mask.json.')

            seg_stats = cocoapi_eval(
                output,
                'segm',
                anno_file=self.anno_file,
                classwise=self.classwise)
            self.eval_results['mask'] = seg_stats
            sys.stdout.flush()

    def log(self):
        pass

    def get(self):
        return self.eval_results