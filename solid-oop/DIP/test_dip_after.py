from unittest.mock import Mock
from dip_after import ToggleButton


def test_when_toggle_button_is_clicked_light_is_on_and_off():
    mock_light = Mock()
    btn = ToggleButton(mock_light)

    btn.click()
    btn.click()
    btn.click()

    assert mock_light.on.call_count == 2
    mock_light.off.assert_called()
