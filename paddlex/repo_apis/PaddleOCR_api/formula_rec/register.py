# copyright (c) 2024 PaddlePaddle Authors. All Rights Reserve.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import os.path as osp
from pathlib import Path

from ...base.register import register_model_info, register_suite_info
from .model import FormulaRecModel
from .runner import FormulaRecRunner
from .config import FormulaRecConfig

REPO_ROOT_PATH = os.environ.get("PADDLE_PDX_PADDLEOCR_PATH")
PDX_CONFIG_DIR = osp.abspath(osp.join(osp.dirname(__file__), "..", "configs"))

register_suite_info(
    {
        "suite_name": "FormulaRec",
        "model": FormulaRecModel,
        "runner": FormulaRecRunner,
        "config": FormulaRecConfig,
        "runner_root_path": REPO_ROOT_PATH,
    }
)


register_model_info(
    {
        "model_name": "LaTeX_OCR_rec",
        "suite": "FormulaRec",
        "config_path": osp.join(PDX_CONFIG_DIR, "LaTeX_OCR_rec.yml"),
        "supported_apis": ["train", "evaluate", "predict", "export", "infer"],
    }
)

register_model_info(
    {
        "model_name": "UniMERNet",
        "suite": "FormulaRec",
        "config_path": osp.join(PDX_CONFIG_DIR, "UniMERNet.yaml"),
        "supported_apis": ["train", "evaluate", "predict", "export", "infer"],
    }
)


register_model_info(
    {
        "model_name": "PP-FormulaNet-S",
        "suite": "FormulaRec",
        "config_path": osp.join(PDX_CONFIG_DIR, "PP-FormulaNet-S.yaml"),
        "supported_apis": ["train", "evaluate", "predict", "export", "infer"],
    }
)

register_model_info(
    {
        "model_name": "PP-FormulaNet-L",
        "suite": "FormulaRec",
        "config_path": osp.join(PDX_CONFIG_DIR, "PP-FormulaNet-L.yaml"),
        "supported_apis": ["train", "evaluate", "predict", "export", "infer"],
    }
)