"""Assemble one paste-ready Google Flow prompt per scene.

This is pure text-combination logic (no AI call): it takes what AI1
(planner) and AI2 (prompt_engine) already produced and merges the
scene's dialogue, camera direction, and lighting into a single block
so nothing has to be copy-pasted together by hand before going into
Google Flow.
"""

from typing import List

from models import Campaign, VisualPromptPack


def build_flow_prompts(campaign: Campaign, prompt_pack: VisualPromptPack) -> List[str]:
    """Return one ready-to-paste prompt per scene, ordered to match campaign.scenes.

    Each string is safe to paste directly into Google Flow's prompt box.
    """
    scenes_by_number = {scene.scene_number: scene for scene in campaign.scenes}
    prompts_by_number = {p.scene_number: p for p in prompt_pack.prompts}

    flow_prompts: List[str] = []
    for scene in sorted(campaign.scenes, key=lambda s: s.scene_number):
        visual = prompts_by_number[scene.scene_number]

        block = [visual.video_prompt.strip()]

        dialogue = scene.dialogue.strip()
        if dialogue:
            block.append(f'The character says, "{dialogue}"')

        block.append(f"Camera: {visual.camera_direction.strip()}")
        block.append(f"Lighting: {visual.lighting.strip()}")

        flow_prompts.append("\n".join(block))

    return flow_prompts
