"""
TracePoint configuration — all settings in one place.
"""

from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# PDF rendering
PDF_RENDER_DPI = 150          # Default DPI for page rasterization
PDF_THUMBNAIL_DPI = 36        # DPI for thumbnail generation
PDF_MAX_DIMENSION = 4096      # Max pixel dimension for rendered pages

# Geometry engine
CONTOUR_MIN_AREA_RATIO = 0.01   # Ignore contours smaller than 1% of page area
CONTOUR_APPROX_EPSILON = 0.02   # Douglas-Peucker polygon simplification factor

# Dimension filtering (proven from predecessor — garbage filter)
DIM_MIN_FT = 10.0
DIM_MAX_FT = 1000.0

# Architectural scales (feet per inch)
ARCH_SCALES = [
    {"label": '1" = 1\'-0"',   "ft_per_inch": 1},
    {"label": '3/4" = 1\'-0"', "ft_per_inch": 1.333},
    {"label": '1/2" = 1\'-0"', "ft_per_inch": 2},
    {"label": '3/8" = 1\'-0"', "ft_per_inch": 2.667},
    {"label": '1/4" = 1\'-0"', "ft_per_inch": 4},
    {"label": '3/16" = 1\'-0"', "ft_per_inch": 5.333},
    {"label": '1/8" = 1\'-0"', "ft_per_inch": 8},
    {"label": '3/32" = 1\'-0"', "ft_per_inch": 10.667},
    {"label": '1/16" = 1\'-0"', "ft_per_inch": 16},
    {"label": '1" = 10\'',  "ft_per_inch": 10},
    {"label": '1" = 20\'',  "ft_per_inch": 20},
    {"label": '1" = 30\'',  "ft_per_inch": 30},
    {"label": '1" = 40\'',  "ft_per_inch": 40},
    {"label": '1" = 50\'',  "ft_per_inch": 50},
    {"label": '1" = 100\'', "ft_per_inch": 100},
]

# File storage
UPLOAD_DIR = PROJECT_ROOT / "uploads"
CORRECTION_DIR = PROJECT_ROOT / "corrections"
MODEL_DIR = PROJECT_ROOT / "models"
