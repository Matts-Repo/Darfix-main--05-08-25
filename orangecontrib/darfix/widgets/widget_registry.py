"""
Widget registry for Darfix Orange widgets.
This file helps Orange discover available widgets.
"""

# Import all widget classes to register them
from .rockingcurves import RockingCurvesWidgetOW
from .rockingcurvesoptimized import RockingCurvesOptimizedWidgetOW

# List of all available widgets
WIDGET_CLASSES = [
    RockingCurvesWidgetOW,
    RockingCurvesOptimizedWidgetOW,
]

# Widget categories
CATEGORIES = {
    "Darfix Processing": [
        RockingCurvesWidgetOW,
        RockingCurvesOptimizedWidgetOW,
    ]
}

__all__ = ['WIDGET_CLASSES', 'CATEGORIES']