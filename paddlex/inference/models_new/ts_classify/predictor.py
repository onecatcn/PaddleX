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

from typing import Any, Union, Dict, List, Tuple
import numpy as np
import pandas as pd
import os

from ....modules.ts_classification.model_list import MODELS
from ...common.batch_sampler import TSBatchSampler
from ...common.reader import ReadTS
from ..common import (
    TSCutOff,
    BuildTSDataset,
    TSNormalize,
    TimeFeature,
    TStoArray,
    TStoBatch,
    StaticInfer,
)

from .processors import GetCls, BuildPadMask
from ..base import BasicPredictor
from .result import TSClsResult


class TSClsPredictor(BasicPredictor):
    """TSClsPredictor that inherits from BasicPredictor."""

    entities = MODELS

    def __init__(self, *args: List, **kwargs: Dict) -> None:
        """Initializes TSClsPredictor.

        Args:
            *args: Arbitrary positional arguments passed to the superclass.
            **kwargs: Arbitrary keyword arguments passed to the superclass.
        """
        super().__init__(*args, **kwargs)
        self.preprocessors, self.infer, self.postprocessors = self._build()

    def _build_batch_sampler(self) -> TSBatchSampler:
        """Builds and returns an TSBatchSampler instance.

        Returns:
            TSBatchSampler: An instance of TSBatchSampler.
        """
        return TSBatchSampler()

    def _get_result_class(self) -> type:
        """Returns the result class.

        Returns:
            type: The Result class.
        """
        return TSClsResult

    def _build(self) -> Tuple:
        """Build the preprocessors, inference engine, and postprocessors based on the configuration.

        Returns:
            tuple: A tuple containing the preprocessors, inference engine, and postprocessors.
        """
        preprocessors = {
            "ReadTS": ReadTS(),
            "TSCutOff": TSCutOff(self.config["size"]),
        }

        if self.config.get("scale", None):
            scaler_file_path = os.path.join(self.model_dir, "scaler.pkl")
            if not os.path.exists(scaler_file_path):
                raise Exception(f"Cannot find scaler file: {scaler_file_path}")
            preprocessors["TSNormalize"] = TSNormalize(
                scaler_file_path, self.config["info_params"]
            )

        preprocessors["BuildTSDataset"] = BuildTSDataset(self.config["info_params"])
        preprocessors["BuildPadMask"] = BuildPadMask(self.config["input_data"])
        preprocessors["TStoArray"] = TStoArray(self.config["input_data"])
        preprocessors["TStoBatch"] = TStoBatch()
        infer = StaticInfer(
            model_dir=self.model_dir,
            model_prefix=self.MODEL_FILE_PREFIX,
            option=self.pp_option,
        )
        postprocessors = {}
        postprocessors["GetCls"] = GetCls()
        return preprocessors, infer, postprocessors

    def process(self, batch_data: List[Union[str, pd.DataFrame]]) -> Dict[str, Any]:
        """
        Processes a batch of time series data through a series of preprocessing, inference, and postprocessing steps.

        Args:
            batch_data (List[Union[str, pd.DataFrame]]): A list of paths or identifiers for the batch of time series data to be processed.

        Returns:
            Dict[str, Any]: A dictionary containing the paths to the input data, the raw input time series, and the classification results.
        """
        batch_raw_ts = self.preprocessors["ReadTS"](ts_list=batch_data)

        if "TSNormalize" in self.preprocessors:
            batch_ts = self.preprocessors["TSNormalize"](ts_list=batch_raw_ts)
            batch_input_ts = self.preprocessors["BuildTSDataset"](ts_list=batch_ts)
        else:
            batch_input_ts = self.preprocessors["BuildTSDataset"](ts_list=batch_raw_ts)

        batch_input_ts = self.preprocessors["BuildPadMask"](ts_list=batch_input_ts)
        batch_ts = self.preprocessors["TStoArray"](ts_list=batch_input_ts)

        x = self.preprocessors["TStoBatch"](ts_list=batch_ts)
        batch_preds = self.infer(x=x)

        batch_ts_preds = self.postprocessors["GetCls"](pred_list=batch_preds)

        return {
            "input_path": batch_data,
            "input_ts": batch_raw_ts,
            "classification": batch_ts_preds,
        }