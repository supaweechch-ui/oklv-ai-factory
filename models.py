"""Data contracts shared by the two AI stages."""

from typing import List

from pydantic import BaseModel, Field


class Scene(BaseModel):
    """A single, producible scene in a short-form ad."""

    scene_number: int = Field(ge=1, description="Scene order, starting at 1")
    duration_seconds: int = Field(ge=1, le=15)
    purpose: str
    description: str
    dialogue: str


class Campaign(BaseModel):
    """The output of the campaign-planning agent."""

    product: str
    target_audience: str
    concept: str
    key_message: str
    tone: str
    total_duration: int = Field(ge=15, le=60)
    scenes: List[Scene] = Field(min_length=4, max_length=4)


class VisualPrompt(BaseModel):
    """Production instructions for turning one scene into an AI video shot."""

    scene_number: int = Field(ge=1)
    image_prompt: str
    video_prompt: str
    camera_direction: str
    lighting: str
    character_consistency: str
    aspect_ratio: str = "9:16"


class VisualPromptPack(BaseModel):
    """The output of the visual-prompt agent."""

    production_notes: str
    prompts: List[VisualPrompt] = Field(min_length=4, max_length=4)
