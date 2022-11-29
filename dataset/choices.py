
# TODO -- we can add orientation correction, font recognition, language classification, text angle classification, object detection categories by adding extra code functionality

EXPORTED_DATASET_TYPE_CHOICES = (
    ('detection', 'Detection'),
    ('recognition', 'Recognition'),
)

ANNOTATION_TYPE_CHOICES = (
    ('line_level', 'Line Level'),
    ('word_level', 'Word Level'),
)

ANNOTATION_FORMAT_CHOICES = (
    ('icdar2015', 'ICDAR 2015'),
    ('ppocrlabel', 'PPOCR Label'),
    ('easyocr', 'EasyOCR'),
    ('mmocr', 'MMOCR')
)

EXPORTED_FILE_FORMAT_CHOICES = (
    ('.zip', '.zip'),
    ('.tar', '.tar'),
    ('.tar.gz', '.tar.gz')
)