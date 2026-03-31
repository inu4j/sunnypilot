from openpilot.common.params import Params
from openpilot.system.ui.widgets import Widget
from openpilot.system.ui.widgets.list_view import multiple_button_item, toggle_item, simple_item, slider_item
from openpilot.system.ui.widgets.scroller import Scroller

# Description constants
DESCRIPTIONS = {
  "OpenpilotEnabledToggle": (
    "Use the openpilot system for adaptive cruise control and lane keep driver assistance. " +
    "Your attention is required at all times to use this feature."
  ),
  "DisengageOnAccelerator": "When enabled, pressing the accelerator pedal will disengage openpilot.",
  "LongitudinalPersonality": (
    "Standard is recommended. In aggressive mode, openpilot will follow lead cars closer and be more aggressive with the gas and brake. " +
    "In relaxed mode openpilot will stay further away from lead cars. On supported cars, you can cycle through these personalities with " +
    "your steering wheel distance button."
  ),
  "IsLdwEnabled": (
    "Receive alerts to steer back into the lane when your vehicle drifts over a detected lane line " +
    "without a turn signal activated while driving over 31 mph (50 km/h)."
  ),
  "AlwaysOnDM": "Enable driver monitoring even when openpilot is not engaged.",
  'RecordFront': "Upload data from the driver facing camera and help improve the driver monitoring algorithm.",
  "IsMetric": "Display speed in km/h instead of mph.",
  "RecordAudio": "Record and store microphone audio while driving. The audio will be included in the dashcam video in comma connect.",
  "SAMSection": (
    "Sunnypilot Advanced Modulation - Fine-tune acceleration and steering behavior for your driving preference."
  ),
  "CustomAccelerationSmoothing": (
    "[0.3 = Very Smooth | 1.0 = Standard | 2.0 = Very Fast]\n\n" +
    "↓값 = 중단후 부드럽고 천천히 가속 | ↑값 = 빠르게 가속\n" +
    "슬라이더를 드래그해서 0.3~2.0 범위에서 자유롭게 조정하세요."
  ),
  "CustomSteeringStrength": (
    "[0.5 = 약한조향 | 1.0 = 표준 | 2.0 = 강한조향]\n\n" +
    "↓값 = 가벼운 조향감, 넓은 각도 필요 | ↑값 = 강한 조향감, 날카로운 턴\n" +
    "슬라이더를 드래그해서 0.5~2.0 범위에서 자유롭게 조정하세요."
  ),
  "CustomSteeringFriction": (
    "[−1.0 = 낮은마찰 | 0.0 = 기본값 | +1.0 = 높은마찰]\n\n" +
    "조향 시작에 필요한 초기 저항력 조정 (타이어 마찰, 조종 안정성)\n" +
    "↓값 = 조향 쉬움 | ↑값 = 의도하지않은 조향방지\n" +
    "슬라이더를 드래그해서 −1.0~+1.0 범위에서 자유롭게 조정하세요."
  ),
}


class TogglesLayout(Widget):
  def __init__(self):
    super().__init__()
    self._params = Params()
    items = [
      toggle_item(
        "Enable openpilot",
        DESCRIPTIONS["OpenpilotEnabledToggle"],
        self._params.get_bool("OpenpilotEnabledToggle"),
        icon="chffr_wheel.png",
      ),
      toggle_item(
        "Experimental Mode",
        initial_state=self._params.get_bool("ExperimentalMode"),
        icon="experimental_white.png",
      ),
      toggle_item(
        "Disengage on Accelerator Pedal",
        DESCRIPTIONS["DisengageOnAccelerator"],
        self._params.get_bool("DisengageOnAccelerator"),
        icon="disengage_on_accelerator.png",
      ),
      multiple_button_item(
        "Driving Personality",
        DESCRIPTIONS["LongitudinalPersonality"],
        buttons=["Aggressive", "Standard", "Relaxed"],
        button_width=255,
        callback=self._set_longitudinal_personality,
        selected_index=self._params.get("LongitudinalPersonality", return_default=True),
        icon="speed_limit.png"
      ),
      toggle_item(
        "Enable Lane Departure Warnings",
        DESCRIPTIONS["IsLdwEnabled"],
        self._params.get_bool("IsLdwEnabled"),
        icon="warning.png",
      ),
      toggle_item(
        "Always-On Driver Monitoring",
        DESCRIPTIONS["AlwaysOnDM"],
        self._params.get_bool("AlwaysOnDM"),
        icon="monitoring.png",
      ),
      toggle_item(
        "Record and Upload Driver Camera",
        DESCRIPTIONS["RecordFront"],
        self._params.get_bool("RecordFront"),
        icon="monitoring.png",
      ),
      toggle_item(
        "Record Microphone Audio",
        DESCRIPTIONS["RecordAudio"],
        self._params.get_bool("RecordAudio"),
        icon="microphone.png",
      ),
      toggle_item(
        "Use Metric System", DESCRIPTIONS["IsMetric"], self._params.get_bool("IsMetric"), icon="metric.png"
      ),
      simple_item("━━━ SAM Section (Sunnypilot Advanced Modulation) ━━━"),
      slider_item(
        "Acceleration Smoothing",
        DESCRIPTIONS["CustomAccelerationSmoothing"],
        min_val=0.3, max_val=2.0,
        current_val=self._params.get_float("CustomAccelerationSmoothing") or 1.0,
        step=0.1,
        callback=self._set_acceleration_smoothing,
        icon="speed_limit.png"
      ),
      slider_item(
        "Steering Strength",
        DESCRIPTIONS["CustomSteeringStrength"],
        min_val=0.5, max_val=2.0,
        current_val=self._params.get_float("CustomSteeringStrength") or 1.0,
        step=0.1,
        callback=self._set_steering_strength,
        icon="steering.png"
      ),
      slider_item(
        "Steering Friction",
        DESCRIPTIONS["CustomSteeringFriction"],
        min_val=-1.0, max_val=1.0,
        current_val=self._params.get_float("CustomSteeringFriction") or 0.0,
        step=0.1,
        callback=self._set_steering_friction,
        icon="friction.png"
      ),
    ]

    self._scroller = Scroller(items, line_separator=True, spacing=0)

  def _render(self, rect):
    self._scroller.render(rect)

  def _set_longitudinal_personality(self, button_index: int):
    self._params.put("LongitudinalPersonality", button_index)

  def _set_acceleration_smoothing(self, value: float):
    self._params.put_float("CustomAccelerationSmoothing", value)

  def _set_steering_strength(self, value: float):
    self._params.put_float("CustomSteeringStrength", value)

  def _set_steering_friction(self, value: float):
    self._params.put_float("CustomSteeringFriction", value)
