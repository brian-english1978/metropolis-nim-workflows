# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing

from pydantic import BaseModel
from pydantic import Discriminator
from pydantic import Field
from pydantic import Tag


def _llm_discriminator(v: typing.Any) -> str:

    if isinstance(v, dict):
        return v.get("service").get("type")
    return getattr(getattr(v, "service"), "type")


class NeMoLLMServiceConfig(BaseModel):

    type: typing.Literal["nemo"] = "nemo"

    api_key: str | None = None
    org_id: str | None = None


class NeMoLLMModelConfig(BaseModel):

    service: NeMoLLMServiceConfig

    model_name: str
    customization_id: str | None = None
    temperature: float = 0.0
    top_k: int = 0
    tokens_to_generate: int = 300


class NVFoundationLLMServiceConfig(BaseModel):

    type: typing.Literal["nvfoundation"] = "nvfoundation"

    api_key: str | None = None


class NVFoundationLLMModelConfig(BaseModel):

    service: NVFoundationLLMServiceConfig

    model_name: str
    temperature: float = 0.0


class OpenAIServiceConfig(BaseModel):

    type: typing.Literal["openai"] = "openai"


class OpenAIMModelConfig(BaseModel):

    service: OpenAIServiceConfig

    model_name: str


class NIMServiceConfig(BaseModel):

    type: typing.Literal["NIM"] = "NIM"


class NIMModelConfig(BaseModel):

    service: NIMServiceConfig

    model_name: str
    base_url: str
    temperature: float = 0.0
    top_p: float = 1


LLMModelConfig = typing.Annotated[
    typing.Annotated[NeMoLLMModelConfig, Tag("nemo")]
    | typing.Annotated[OpenAIMModelConfig, Tag("openai")]
    | typing.Annotated[NVFoundationLLMModelConfig, Tag("nvfoundation")]
    | typing.Annotated[NIMModelConfig, Tag("NIM")],
    Discriminator(_llm_discriminator),
]


class HttpServerInputConfig(BaseModel):

    type: typing.Literal["http_server"] = "http_server"


class NspectFileInputConfig(BaseModel):

    type: typing.Literal["nspect_file"] = "nspect_file"


class CveFileInputConfig(BaseModel):

    type: typing.Literal["cve_file"] = "cve_file"


class EngineChecklistConfig(BaseModel):

    model: LLMModelConfig


class EngineSBOMConfig(BaseModel):

    data_file: str


class EngineVideoConfig(BaseModel):

    file_id: str
    start_timestamp: int = 60
    end_timestamp: int = 120
    vlm_port: str = "31012"


class EngineCodeRepoConfig(BaseModel):

    faiss_dir: str

    embedding_model_name: str = "sentence-transformers/all-mpnet-base-v2"


class EngineAgentConfig(BaseModel):

    model: LLMModelConfig

    video: EngineVideoConfig

    text_db: EngineCodeRepoConfig

    verbose: bool = True


class EngineConfig(BaseModel):

    checklist: EngineChecklistConfig

    agent: EngineAgentConfig
