"""Local video analysis pipeline with optional Ultralytics player detections."""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import cv2
import numpy as np
from ..config import settings

class VideoAnalyzer:
    def __init__(self) -> None:
        self.model = None
        if settings.yolo_model:
            try:
                from ultralytics import YOLO
                self.model = YOLO(settings.yolo_model)
            except Exception:
                self.model = None

    def analyze(self, video_path: str, pass_frame: int | None = None) -> dict:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened(): raise ValueError("The uploaded video cannot be decoded.")
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); fps = max(cap.get(cv2.CAP_PROP_FPS), 1.0)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        stride = max(1, frames // 60); tracks, heatmap, samples = defaultdict(list), np.zeros((12, 20), dtype=int), []
        index = 0
        while True:
            ok, frame = cap.read()
            if not ok: break
            if index % stride == 0:
                detections = self._detect(frame)
                for ident, x, y, w, h, label in detections:
                    cx, cy = x + w / 2, y + h / 2
                    tracks[ident].append({"frame": index, "x": round(cx / max(width, 1), 3), "y": round(cy / max(height, 1), 3), "label": label})
                    heatmap[min(11, int(cy / max(height, 1) * 12)), min(19, int(cx / max(width, 1) * 20))] += 1
                samples.append({"frame": index, "players": len(detections)})
            index += 1
        cap.release()
        pframe = pass_frame if pass_frame is not None else frames // 2
        active = [points[-1] for points in tracks.values() if points]
        # A transparent geometric heuristic: attacker furthest forward vs. second-last defender proxy.
        positions = sorted((p["x"] for p in active), reverse=True)
        separation = positions[0] - positions[1] if len(positions) > 1 else 0.0
        offside = len(active) >= 3 and separation > 0.065
        confidence = round(min(0.96, 0.55 + min(len(active), 10) * .03 + min(separation, .2)), 2)
        decision = "OFFSIDE" if offside else "NOT_OFFSIDE"
        return {"decision": decision, "confidence": confidence, "factors": [
            {"feature": "Attacker position", "impact": round(separation, 3), "direction": "toward offside" if offside else "onside"},
            {"feature": "Tracked players", "impact": len(active), "direction": "evidence coverage"},
            {"feature": "Pass frame", "impact": pframe, "direction": "reference frame"}],
            "timeline": [{"time": round(s["frame"] / fps, 2), "event": "tracking", "value": s["players"]} for s in samples],
            "heatmap": heatmap.tolist(), "tracks": [{"id": key, "points": value} for key, value in tracks.items()],
            "metadata": {"frames": frames, "fps": round(fps, 2), "resolution": f"{width}x{height}", "pass_frame": pframe, "detector": "YOLO" if self.model else "OpenCV motion"}}

    def _detect(self, frame: np.ndarray) -> list[tuple[int, int, int, int, int, str]]:
        if self.model:
            # Ultralytics invokes ByteTrack and preserves its identities across frames.
            result = self.model.track(frame, classes=[0], tracker="bytetrack.yaml", persist=True, verbose=False)[0]
            ids = result.boxes.id.int().cpu().tolist() if result.boxes.id is not None else list(range(len(result.boxes)))
            return [(track_id, int(x1), int(y1), int(x2-x1), int(y2-y1), "player") for track_id, (x1,y1,x2,y2) in zip(ids, result.boxes.xyxy.cpu().tolist())]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return [(ident, x, y, w, h, "player") for ident, c in enumerate(contours) for x,y,w,h in [cv2.boundingRect(c)] if 120 < w*h < frame.shape[0]*frame.shape[1]*.08][:22]
