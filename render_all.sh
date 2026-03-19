#!/usr/bin/env bash
# render_all.sh — Render every scene and concatenate into one video
# Usage:  chmod +x render_all.sh && ./render_all.sh
# Quality flags: -ql (low), -qm (medium), -qh (high — use for final)

set -e

QUALITY=${1:--qm}   # default medium; pass -qh for final render
FILE="sum_check_animation.py"

SCENES=(
  TitleScene
  SudokuMotivation
  SumCheckProblem
  InteractiveProof
  PrimeFields
  SchwartzZippel
  Round1
  Round2
  GeneralRounds
  FinalRound
  SoundnessAnalysis
  Conclusion
)

echo "=== Rendering ${#SCENES[@]} scenes at quality: $QUALITY ==="
for scene in "${SCENES[@]}"; do
  echo "--- Rendering $scene ---"
  manim $QUALITY "$FILE" "$scene"
done

# ── Concatenate with ffmpeg ────────────────────────────────────────────────
# Manim outputs to media/videos/<file_stem>/<resolution>/
# Adjust the path below if your Manim version differs.

RESOLUTION="720p30"   # matches -qm; change to 1080p60 for -qh
MEDIA_DIR="media/videos/sum_check_animation/$RESOLUTION"

echo "=== Concatenating scenes with ffmpeg ==="
CONCAT_LIST="concat_list.txt"
> "$CONCAT_LIST"

for scene in "${SCENES[@]}"; do
  VIDEO="$MEDIA_DIR/${scene}.mp4"
  if [ -f "$VIDEO" ]; then
    echo "file '$VIDEO'" >> "$CONCAT_LIST"
  else
    echo "WARNING: $VIDEO not found — skipping"
  fi
done

ffmpeg -y -f concat -safe 0 -i "$CONCAT_LIST" -c copy "sum_check_protocol_full.mp4"
echo "=== Done! Output: sum_check_protocol_full.mp4 ==="
