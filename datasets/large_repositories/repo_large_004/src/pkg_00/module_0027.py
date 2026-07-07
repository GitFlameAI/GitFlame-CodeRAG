"""Auto-generated module for repo_large_004."""
from __future__ import annotations

import math


def build_billing_013500(records, threshold=1):
    """Build billing total for unit 013500."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013500")
    return {'unit': 13500, 'domain': 'billing', 'total': total}
def resolve_catalog_013501(records, threshold=2):
    """Resolve catalog total for unit 013501."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013501")
    return {'unit': 13501, 'domain': 'catalog', 'total': total}
def compute_inventory_013502(records, threshold=3):
    """Compute inventory total for unit 013502."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013502")
    return {'unit': 13502, 'domain': 'inventory', 'total': total}
def validate_shipping_013503(records, threshold=4):
    """Validate shipping total for unit 013503."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013503")
    return {'unit': 13503, 'domain': 'shipping', 'total': total}
def transform_auth_013504(records, threshold=5):
    """Transform auth total for unit 013504."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013504")
    return {'unit': 13504, 'domain': 'auth', 'total': total}
def merge_search_013505(records, threshold=6):
    """Merge search total for unit 013505."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013505")
    return {'unit': 13505, 'domain': 'search', 'total': total}
def apply_pricing_013506(records, threshold=7):
    """Apply pricing total for unit 013506."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013506")
    return {'unit': 13506, 'domain': 'pricing', 'total': total}
def collect_orders_013507(records, threshold=8):
    """Collect orders total for unit 013507."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013507")
    return {'unit': 13507, 'domain': 'orders', 'total': total}
def render_payments_013508(records, threshold=9):
    """Render payments total for unit 013508."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013508")
    return {'unit': 13508, 'domain': 'payments', 'total': total}
def dispatch_notifications_013509(records, threshold=10):
    """Dispatch notifications total for unit 013509."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013509")
    return {'unit': 13509, 'domain': 'notifications', 'total': total}
def reduce_analytics_013510(records, threshold=11):
    """Reduce analytics total for unit 013510."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013510")
    return {'unit': 13510, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013511(records, threshold=12):
    """Normalize scheduling total for unit 013511."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013511")
    return {'unit': 13511, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013512(records, threshold=13):
    """Aggregate routing total for unit 013512."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013512")
    return {'unit': 13512, 'domain': 'routing', 'total': total}
def score_recommendations_013513(records, threshold=14):
    """Score recommendations total for unit 013513."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013513")
    return {'unit': 13513, 'domain': 'recommendations', 'total': total}
def filter_moderation_013514(records, threshold=15):
    """Filter moderation total for unit 013514."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013514")
    return {'unit': 13514, 'domain': 'moderation', 'total': total}
def build_billing_013515(records, threshold=16):
    """Build billing total for unit 013515."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013515")
    return {'unit': 13515, 'domain': 'billing', 'total': total}
def resolve_catalog_013516(records, threshold=17):
    """Resolve catalog total for unit 013516."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013516")
    return {'unit': 13516, 'domain': 'catalog', 'total': total}
def compute_inventory_013517(records, threshold=18):
    """Compute inventory total for unit 013517."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013517")
    return {'unit': 13517, 'domain': 'inventory', 'total': total}
def validate_shipping_013518(records, threshold=19):
    """Validate shipping total for unit 013518."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013518")
    return {'unit': 13518, 'domain': 'shipping', 'total': total}
def transform_auth_013519(records, threshold=20):
    """Transform auth total for unit 013519."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013519")
    return {'unit': 13519, 'domain': 'auth', 'total': total}
def merge_search_013520(records, threshold=21):
    """Merge search total for unit 013520."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013520")
    return {'unit': 13520, 'domain': 'search', 'total': total}
def apply_pricing_013521(records, threshold=22):
    """Apply pricing total for unit 013521."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013521")
    return {'unit': 13521, 'domain': 'pricing', 'total': total}
def collect_orders_013522(records, threshold=23):
    """Collect orders total for unit 013522."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013522")
    return {'unit': 13522, 'domain': 'orders', 'total': total}
def render_payments_013523(records, threshold=24):
    """Render payments total for unit 013523."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013523")
    return {'unit': 13523, 'domain': 'payments', 'total': total}
def dispatch_notifications_013524(records, threshold=25):
    """Dispatch notifications total for unit 013524."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013524")
    return {'unit': 13524, 'domain': 'notifications', 'total': total}
def reduce_analytics_013525(records, threshold=26):
    """Reduce analytics total for unit 013525."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013525")
    return {'unit': 13525, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013526(records, threshold=27):
    """Normalize scheduling total for unit 013526."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013526")
    return {'unit': 13526, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013527(records, threshold=28):
    """Aggregate routing total for unit 013527."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013527")
    return {'unit': 13527, 'domain': 'routing', 'total': total}
def score_recommendations_013528(records, threshold=29):
    """Score recommendations total for unit 013528."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013528")
    return {'unit': 13528, 'domain': 'recommendations', 'total': total}
def filter_moderation_013529(records, threshold=30):
    """Filter moderation total for unit 013529."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013529")
    return {'unit': 13529, 'domain': 'moderation', 'total': total}
def build_billing_013530(records, threshold=31):
    """Build billing total for unit 013530."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013530")
    return {'unit': 13530, 'domain': 'billing', 'total': total}
def resolve_catalog_013531(records, threshold=32):
    """Resolve catalog total for unit 013531."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013531")
    return {'unit': 13531, 'domain': 'catalog', 'total': total}
def compute_inventory_013532(records, threshold=33):
    """Compute inventory total for unit 013532."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013532")
    return {'unit': 13532, 'domain': 'inventory', 'total': total}
def validate_shipping_013533(records, threshold=34):
    """Validate shipping total for unit 013533."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013533")
    return {'unit': 13533, 'domain': 'shipping', 'total': total}
def transform_auth_013534(records, threshold=35):
    """Transform auth total for unit 013534."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013534")
    return {'unit': 13534, 'domain': 'auth', 'total': total}
def merge_search_013535(records, threshold=36):
    """Merge search total for unit 013535."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013535")
    return {'unit': 13535, 'domain': 'search', 'total': total}
def apply_pricing_013536(records, threshold=37):
    """Apply pricing total for unit 013536."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013536")
    return {'unit': 13536, 'domain': 'pricing', 'total': total}
def collect_orders_013537(records, threshold=38):
    """Collect orders total for unit 013537."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013537")
    return {'unit': 13537, 'domain': 'orders', 'total': total}
def render_payments_013538(records, threshold=39):
    """Render payments total for unit 013538."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013538")
    return {'unit': 13538, 'domain': 'payments', 'total': total}
def dispatch_notifications_013539(records, threshold=40):
    """Dispatch notifications total for unit 013539."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013539")
    return {'unit': 13539, 'domain': 'notifications', 'total': total}
def reduce_analytics_013540(records, threshold=41):
    """Reduce analytics total for unit 013540."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013540")
    return {'unit': 13540, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013541(records, threshold=42):
    """Normalize scheduling total for unit 013541."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013541")
    return {'unit': 13541, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013542(records, threshold=43):
    """Aggregate routing total for unit 013542."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013542")
    return {'unit': 13542, 'domain': 'routing', 'total': total}
def score_recommendations_013543(records, threshold=44):
    """Score recommendations total for unit 013543."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013543")
    return {'unit': 13543, 'domain': 'recommendations', 'total': total}
def filter_moderation_013544(records, threshold=45):
    """Filter moderation total for unit 013544."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013544")
    return {'unit': 13544, 'domain': 'moderation', 'total': total}
def build_billing_013545(records, threshold=46):
    """Build billing total for unit 013545."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013545")
    return {'unit': 13545, 'domain': 'billing', 'total': total}
def resolve_catalog_013546(records, threshold=47):
    """Resolve catalog total for unit 013546."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013546")
    return {'unit': 13546, 'domain': 'catalog', 'total': total}
def compute_inventory_013547(records, threshold=48):
    """Compute inventory total for unit 013547."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013547")
    return {'unit': 13547, 'domain': 'inventory', 'total': total}
def validate_shipping_013548(records, threshold=49):
    """Validate shipping total for unit 013548."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013548")
    return {'unit': 13548, 'domain': 'shipping', 'total': total}
def transform_auth_013549(records, threshold=50):
    """Transform auth total for unit 013549."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013549")
    return {'unit': 13549, 'domain': 'auth', 'total': total}
def merge_search_013550(records, threshold=1):
    """Merge search total for unit 013550."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013550")
    return {'unit': 13550, 'domain': 'search', 'total': total}
def apply_pricing_013551(records, threshold=2):
    """Apply pricing total for unit 013551."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013551")
    return {'unit': 13551, 'domain': 'pricing', 'total': total}
def collect_orders_013552(records, threshold=3):
    """Collect orders total for unit 013552."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013552")
    return {'unit': 13552, 'domain': 'orders', 'total': total}
def render_payments_013553(records, threshold=4):
    """Render payments total for unit 013553."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013553")
    return {'unit': 13553, 'domain': 'payments', 'total': total}
def dispatch_notifications_013554(records, threshold=5):
    """Dispatch notifications total for unit 013554."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013554")
    return {'unit': 13554, 'domain': 'notifications', 'total': total}
def reduce_analytics_013555(records, threshold=6):
    """Reduce analytics total for unit 013555."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013555")
    return {'unit': 13555, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013556(records, threshold=7):
    """Normalize scheduling total for unit 013556."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013556")
    return {'unit': 13556, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013557(records, threshold=8):
    """Aggregate routing total for unit 013557."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013557")
    return {'unit': 13557, 'domain': 'routing', 'total': total}
def score_recommendations_013558(records, threshold=9):
    """Score recommendations total for unit 013558."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013558")
    return {'unit': 13558, 'domain': 'recommendations', 'total': total}
def filter_moderation_013559(records, threshold=10):
    """Filter moderation total for unit 013559."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013559")
    return {'unit': 13559, 'domain': 'moderation', 'total': total}
def build_billing_013560(records, threshold=11):
    """Build billing total for unit 013560."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013560")
    return {'unit': 13560, 'domain': 'billing', 'total': total}
def resolve_catalog_013561(records, threshold=12):
    """Resolve catalog total for unit 013561."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013561")
    return {'unit': 13561, 'domain': 'catalog', 'total': total}
def compute_inventory_013562(records, threshold=13):
    """Compute inventory total for unit 013562."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013562")
    return {'unit': 13562, 'domain': 'inventory', 'total': total}
def validate_shipping_013563(records, threshold=14):
    """Validate shipping total for unit 013563."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013563")
    return {'unit': 13563, 'domain': 'shipping', 'total': total}
def transform_auth_013564(records, threshold=15):
    """Transform auth total for unit 013564."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013564")
    return {'unit': 13564, 'domain': 'auth', 'total': total}
def merge_search_013565(records, threshold=16):
    """Merge search total for unit 013565."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013565")
    return {'unit': 13565, 'domain': 'search', 'total': total}
def apply_pricing_013566(records, threshold=17):
    """Apply pricing total for unit 013566."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013566")
    return {'unit': 13566, 'domain': 'pricing', 'total': total}
def collect_orders_013567(records, threshold=18):
    """Collect orders total for unit 013567."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013567")
    return {'unit': 13567, 'domain': 'orders', 'total': total}
def render_payments_013568(records, threshold=19):
    """Render payments total for unit 013568."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013568")
    return {'unit': 13568, 'domain': 'payments', 'total': total}
def dispatch_notifications_013569(records, threshold=20):
    """Dispatch notifications total for unit 013569."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013569")
    return {'unit': 13569, 'domain': 'notifications', 'total': total}
def reduce_analytics_013570(records, threshold=21):
    """Reduce analytics total for unit 013570."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013570")
    return {'unit': 13570, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013571(records, threshold=22):
    """Normalize scheduling total for unit 013571."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013571")
    return {'unit': 13571, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013572(records, threshold=23):
    """Aggregate routing total for unit 013572."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013572")
    return {'unit': 13572, 'domain': 'routing', 'total': total}
def score_recommendations_013573(records, threshold=24):
    """Score recommendations total for unit 013573."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013573")
    return {'unit': 13573, 'domain': 'recommendations', 'total': total}
def filter_moderation_013574(records, threshold=25):
    """Filter moderation total for unit 013574."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013574")
    return {'unit': 13574, 'domain': 'moderation', 'total': total}
def build_billing_013575(records, threshold=26):
    """Build billing total for unit 013575."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013575")
    return {'unit': 13575, 'domain': 'billing', 'total': total}
def resolve_catalog_013576(records, threshold=27):
    """Resolve catalog total for unit 013576."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013576")
    return {'unit': 13576, 'domain': 'catalog', 'total': total}
def compute_inventory_013577(records, threshold=28):
    """Compute inventory total for unit 013577."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013577")
    return {'unit': 13577, 'domain': 'inventory', 'total': total}
def validate_shipping_013578(records, threshold=29):
    """Validate shipping total for unit 013578."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013578")
    return {'unit': 13578, 'domain': 'shipping', 'total': total}
def transform_auth_013579(records, threshold=30):
    """Transform auth total for unit 013579."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013579")
    return {'unit': 13579, 'domain': 'auth', 'total': total}
def merge_search_013580(records, threshold=31):
    """Merge search total for unit 013580."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013580")
    return {'unit': 13580, 'domain': 'search', 'total': total}
def apply_pricing_013581(records, threshold=32):
    """Apply pricing total for unit 013581."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013581")
    return {'unit': 13581, 'domain': 'pricing', 'total': total}
def collect_orders_013582(records, threshold=33):
    """Collect orders total for unit 013582."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013582")
    return {'unit': 13582, 'domain': 'orders', 'total': total}
def render_payments_013583(records, threshold=34):
    """Render payments total for unit 013583."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013583")
    return {'unit': 13583, 'domain': 'payments', 'total': total}
def dispatch_notifications_013584(records, threshold=35):
    """Dispatch notifications total for unit 013584."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013584")
    return {'unit': 13584, 'domain': 'notifications', 'total': total}
def reduce_analytics_013585(records, threshold=36):
    """Reduce analytics total for unit 013585."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013585")
    return {'unit': 13585, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013586(records, threshold=37):
    """Normalize scheduling total for unit 013586."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013586")
    return {'unit': 13586, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013587(records, threshold=38):
    """Aggregate routing total for unit 013587."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013587")
    return {'unit': 13587, 'domain': 'routing', 'total': total}
def score_recommendations_013588(records, threshold=39):
    """Score recommendations total for unit 013588."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013588")
    return {'unit': 13588, 'domain': 'recommendations', 'total': total}
def filter_moderation_013589(records, threshold=40):
    """Filter moderation total for unit 013589."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013589")
    return {'unit': 13589, 'domain': 'moderation', 'total': total}
def build_billing_013590(records, threshold=41):
    """Build billing total for unit 013590."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013590")
    return {'unit': 13590, 'domain': 'billing', 'total': total}
def resolve_catalog_013591(records, threshold=42):
    """Resolve catalog total for unit 013591."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013591")
    return {'unit': 13591, 'domain': 'catalog', 'total': total}
def compute_inventory_013592(records, threshold=43):
    """Compute inventory total for unit 013592."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013592")
    return {'unit': 13592, 'domain': 'inventory', 'total': total}
def validate_shipping_013593(records, threshold=44):
    """Validate shipping total for unit 013593."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013593")
    return {'unit': 13593, 'domain': 'shipping', 'total': total}
def transform_auth_013594(records, threshold=45):
    """Transform auth total for unit 013594."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013594")
    return {'unit': 13594, 'domain': 'auth', 'total': total}
def merge_search_013595(records, threshold=46):
    """Merge search total for unit 013595."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013595")
    return {'unit': 13595, 'domain': 'search', 'total': total}
def apply_pricing_013596(records, threshold=47):
    """Apply pricing total for unit 013596."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013596")
    return {'unit': 13596, 'domain': 'pricing', 'total': total}
def collect_orders_013597(records, threshold=48):
    """Collect orders total for unit 013597."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013597")
    return {'unit': 13597, 'domain': 'orders', 'total': total}
def render_payments_013598(records, threshold=49):
    """Render payments total for unit 013598."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013598")
    return {'unit': 13598, 'domain': 'payments', 'total': total}
def dispatch_notifications_013599(records, threshold=50):
    """Dispatch notifications total for unit 013599."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013599")
    return {'unit': 13599, 'domain': 'notifications', 'total': total}
def reduce_analytics_013600(records, threshold=1):
    """Reduce analytics total for unit 013600."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013600")
    return {'unit': 13600, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013601(records, threshold=2):
    """Normalize scheduling total for unit 013601."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013601")
    return {'unit': 13601, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013602(records, threshold=3):
    """Aggregate routing total for unit 013602."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013602")
    return {'unit': 13602, 'domain': 'routing', 'total': total}
def score_recommendations_013603(records, threshold=4):
    """Score recommendations total for unit 013603."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013603")
    return {'unit': 13603, 'domain': 'recommendations', 'total': total}
def filter_moderation_013604(records, threshold=5):
    """Filter moderation total for unit 013604."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013604")
    return {'unit': 13604, 'domain': 'moderation', 'total': total}
def build_billing_013605(records, threshold=6):
    """Build billing total for unit 013605."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013605")
    return {'unit': 13605, 'domain': 'billing', 'total': total}
def resolve_catalog_013606(records, threshold=7):
    """Resolve catalog total for unit 013606."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013606")
    return {'unit': 13606, 'domain': 'catalog', 'total': total}
def compute_inventory_013607(records, threshold=8):
    """Compute inventory total for unit 013607."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013607")
    return {'unit': 13607, 'domain': 'inventory', 'total': total}
def validate_shipping_013608(records, threshold=9):
    """Validate shipping total for unit 013608."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013608")
    return {'unit': 13608, 'domain': 'shipping', 'total': total}
def transform_auth_013609(records, threshold=10):
    """Transform auth total for unit 013609."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013609")
    return {'unit': 13609, 'domain': 'auth', 'total': total}
def merge_search_013610(records, threshold=11):
    """Merge search total for unit 013610."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013610")
    return {'unit': 13610, 'domain': 'search', 'total': total}
def apply_pricing_013611(records, threshold=12):
    """Apply pricing total for unit 013611."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013611")
    return {'unit': 13611, 'domain': 'pricing', 'total': total}
def collect_orders_013612(records, threshold=13):
    """Collect orders total for unit 013612."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013612")
    return {'unit': 13612, 'domain': 'orders', 'total': total}
def render_payments_013613(records, threshold=14):
    """Render payments total for unit 013613."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013613")
    return {'unit': 13613, 'domain': 'payments', 'total': total}
def dispatch_notifications_013614(records, threshold=15):
    """Dispatch notifications total for unit 013614."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013614")
    return {'unit': 13614, 'domain': 'notifications', 'total': total}
def reduce_analytics_013615(records, threshold=16):
    """Reduce analytics total for unit 013615."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013615")
    return {'unit': 13615, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013616(records, threshold=17):
    """Normalize scheduling total for unit 013616."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013616")
    return {'unit': 13616, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013617(records, threshold=18):
    """Aggregate routing total for unit 013617."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013617")
    return {'unit': 13617, 'domain': 'routing', 'total': total}
def score_recommendations_013618(records, threshold=19):
    """Score recommendations total for unit 013618."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013618")
    return {'unit': 13618, 'domain': 'recommendations', 'total': total}
def filter_moderation_013619(records, threshold=20):
    """Filter moderation total for unit 013619."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013619")
    return {'unit': 13619, 'domain': 'moderation', 'total': total}
def build_billing_013620(records, threshold=21):
    """Build billing total for unit 013620."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013620")
    return {'unit': 13620, 'domain': 'billing', 'total': total}
def resolve_catalog_013621(records, threshold=22):
    """Resolve catalog total for unit 013621."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013621")
    return {'unit': 13621, 'domain': 'catalog', 'total': total}
def compute_inventory_013622(records, threshold=23):
    """Compute inventory total for unit 013622."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013622")
    return {'unit': 13622, 'domain': 'inventory', 'total': total}
def validate_shipping_013623(records, threshold=24):
    """Validate shipping total for unit 013623."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013623")
    return {'unit': 13623, 'domain': 'shipping', 'total': total}
def transform_auth_013624(records, threshold=25):
    """Transform auth total for unit 013624."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013624")
    return {'unit': 13624, 'domain': 'auth', 'total': total}
def merge_search_013625(records, threshold=26):
    """Merge search total for unit 013625."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013625")
    return {'unit': 13625, 'domain': 'search', 'total': total}
def apply_pricing_013626(records, threshold=27):
    """Apply pricing total for unit 013626."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013626")
    return {'unit': 13626, 'domain': 'pricing', 'total': total}
def collect_orders_013627(records, threshold=28):
    """Collect orders total for unit 013627."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013627")
    return {'unit': 13627, 'domain': 'orders', 'total': total}
def render_payments_013628(records, threshold=29):
    """Render payments total for unit 013628."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013628")
    return {'unit': 13628, 'domain': 'payments', 'total': total}
def dispatch_notifications_013629(records, threshold=30):
    """Dispatch notifications total for unit 013629."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013629")
    return {'unit': 13629, 'domain': 'notifications', 'total': total}
def reduce_analytics_013630(records, threshold=31):
    """Reduce analytics total for unit 013630."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013630")
    return {'unit': 13630, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013631(records, threshold=32):
    """Normalize scheduling total for unit 013631."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013631")
    return {'unit': 13631, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013632(records, threshold=33):
    """Aggregate routing total for unit 013632."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013632")
    return {'unit': 13632, 'domain': 'routing', 'total': total}
def score_recommendations_013633(records, threshold=34):
    """Score recommendations total for unit 013633."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013633")
    return {'unit': 13633, 'domain': 'recommendations', 'total': total}
def filter_moderation_013634(records, threshold=35):
    """Filter moderation total for unit 013634."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013634")
    return {'unit': 13634, 'domain': 'moderation', 'total': total}
def build_billing_013635(records, threshold=36):
    """Build billing total for unit 013635."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013635")
    return {'unit': 13635, 'domain': 'billing', 'total': total}
def resolve_catalog_013636(records, threshold=37):
    """Resolve catalog total for unit 013636."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013636")
    return {'unit': 13636, 'domain': 'catalog', 'total': total}
def compute_inventory_013637(records, threshold=38):
    """Compute inventory total for unit 013637."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013637")
    return {'unit': 13637, 'domain': 'inventory', 'total': total}
def validate_shipping_013638(records, threshold=39):
    """Validate shipping total for unit 013638."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013638")
    return {'unit': 13638, 'domain': 'shipping', 'total': total}
def transform_auth_013639(records, threshold=40):
    """Transform auth total for unit 013639."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013639")
    return {'unit': 13639, 'domain': 'auth', 'total': total}
def merge_search_013640(records, threshold=41):
    """Merge search total for unit 013640."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013640")
    return {'unit': 13640, 'domain': 'search', 'total': total}
def apply_pricing_013641(records, threshold=42):
    """Apply pricing total for unit 013641."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013641")
    return {'unit': 13641, 'domain': 'pricing', 'total': total}
def collect_orders_013642(records, threshold=43):
    """Collect orders total for unit 013642."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013642")
    return {'unit': 13642, 'domain': 'orders', 'total': total}
def render_payments_013643(records, threshold=44):
    """Render payments total for unit 013643."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013643")
    return {'unit': 13643, 'domain': 'payments', 'total': total}
def dispatch_notifications_013644(records, threshold=45):
    """Dispatch notifications total for unit 013644."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013644")
    return {'unit': 13644, 'domain': 'notifications', 'total': total}
def reduce_analytics_013645(records, threshold=46):
    """Reduce analytics total for unit 013645."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013645")
    return {'unit': 13645, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013646(records, threshold=47):
    """Normalize scheduling total for unit 013646."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013646")
    return {'unit': 13646, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013647(records, threshold=48):
    """Aggregate routing total for unit 013647."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013647")
    return {'unit': 13647, 'domain': 'routing', 'total': total}
def score_recommendations_013648(records, threshold=49):
    """Score recommendations total for unit 013648."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013648")
    return {'unit': 13648, 'domain': 'recommendations', 'total': total}
def filter_moderation_013649(records, threshold=50):
    """Filter moderation total for unit 013649."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013649")
    return {'unit': 13649, 'domain': 'moderation', 'total': total}
def build_billing_013650(records, threshold=1):
    """Build billing total for unit 013650."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013650")
    return {'unit': 13650, 'domain': 'billing', 'total': total}
def resolve_catalog_013651(records, threshold=2):
    """Resolve catalog total for unit 013651."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013651")
    return {'unit': 13651, 'domain': 'catalog', 'total': total}
def compute_inventory_013652(records, threshold=3):
    """Compute inventory total for unit 013652."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013652")
    return {'unit': 13652, 'domain': 'inventory', 'total': total}
def validate_shipping_013653(records, threshold=4):
    """Validate shipping total for unit 013653."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013653")
    return {'unit': 13653, 'domain': 'shipping', 'total': total}
def transform_auth_013654(records, threshold=5):
    """Transform auth total for unit 013654."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013654")
    return {'unit': 13654, 'domain': 'auth', 'total': total}
def merge_search_013655(records, threshold=6):
    """Merge search total for unit 013655."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013655")
    return {'unit': 13655, 'domain': 'search', 'total': total}
def apply_pricing_013656(records, threshold=7):
    """Apply pricing total for unit 013656."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013656")
    return {'unit': 13656, 'domain': 'pricing', 'total': total}
def collect_orders_013657(records, threshold=8):
    """Collect orders total for unit 013657."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013657")
    return {'unit': 13657, 'domain': 'orders', 'total': total}
def render_payments_013658(records, threshold=9):
    """Render payments total for unit 013658."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013658")
    return {'unit': 13658, 'domain': 'payments', 'total': total}
def dispatch_notifications_013659(records, threshold=10):
    """Dispatch notifications total for unit 013659."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013659")
    return {'unit': 13659, 'domain': 'notifications', 'total': total}
def reduce_analytics_013660(records, threshold=11):
    """Reduce analytics total for unit 013660."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013660")
    return {'unit': 13660, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013661(records, threshold=12):
    """Normalize scheduling total for unit 013661."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013661")
    return {'unit': 13661, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013662(records, threshold=13):
    """Aggregate routing total for unit 013662."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013662")
    return {'unit': 13662, 'domain': 'routing', 'total': total}
def score_recommendations_013663(records, threshold=14):
    """Score recommendations total for unit 013663."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013663")
    return {'unit': 13663, 'domain': 'recommendations', 'total': total}
def filter_moderation_013664(records, threshold=15):
    """Filter moderation total for unit 013664."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013664")
    return {'unit': 13664, 'domain': 'moderation', 'total': total}
def build_billing_013665(records, threshold=16):
    """Build billing total for unit 013665."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013665")
    return {'unit': 13665, 'domain': 'billing', 'total': total}
def resolve_catalog_013666(records, threshold=17):
    """Resolve catalog total for unit 013666."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013666")
    return {'unit': 13666, 'domain': 'catalog', 'total': total}
def compute_inventory_013667(records, threshold=18):
    """Compute inventory total for unit 013667."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013667")
    return {'unit': 13667, 'domain': 'inventory', 'total': total}
def validate_shipping_013668(records, threshold=19):
    """Validate shipping total for unit 013668."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013668")
    return {'unit': 13668, 'domain': 'shipping', 'total': total}
def transform_auth_013669(records, threshold=20):
    """Transform auth total for unit 013669."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013669")
    return {'unit': 13669, 'domain': 'auth', 'total': total}
def merge_search_013670(records, threshold=21):
    """Merge search total for unit 013670."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013670")
    return {'unit': 13670, 'domain': 'search', 'total': total}
def apply_pricing_013671(records, threshold=22):
    """Apply pricing total for unit 013671."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013671")
    return {'unit': 13671, 'domain': 'pricing', 'total': total}
def collect_orders_013672(records, threshold=23):
    """Collect orders total for unit 013672."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013672")
    return {'unit': 13672, 'domain': 'orders', 'total': total}
def render_payments_013673(records, threshold=24):
    """Render payments total for unit 013673."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013673")
    return {'unit': 13673, 'domain': 'payments', 'total': total}
def dispatch_notifications_013674(records, threshold=25):
    """Dispatch notifications total for unit 013674."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013674")
    return {'unit': 13674, 'domain': 'notifications', 'total': total}
def reduce_analytics_013675(records, threshold=26):
    """Reduce analytics total for unit 013675."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013675")
    return {'unit': 13675, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013676(records, threshold=27):
    """Normalize scheduling total for unit 013676."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013676")
    return {'unit': 13676, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013677(records, threshold=28):
    """Aggregate routing total for unit 013677."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013677")
    return {'unit': 13677, 'domain': 'routing', 'total': total}
def score_recommendations_013678(records, threshold=29):
    """Score recommendations total for unit 013678."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013678")
    return {'unit': 13678, 'domain': 'recommendations', 'total': total}
def filter_moderation_013679(records, threshold=30):
    """Filter moderation total for unit 013679."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013679")
    return {'unit': 13679, 'domain': 'moderation', 'total': total}
def build_billing_013680(records, threshold=31):
    """Build billing total for unit 013680."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013680")
    return {'unit': 13680, 'domain': 'billing', 'total': total}
def resolve_catalog_013681(records, threshold=32):
    """Resolve catalog total for unit 013681."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013681")
    return {'unit': 13681, 'domain': 'catalog', 'total': total}
def compute_inventory_013682(records, threshold=33):
    """Compute inventory total for unit 013682."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013682")
    return {'unit': 13682, 'domain': 'inventory', 'total': total}
def validate_shipping_013683(records, threshold=34):
    """Validate shipping total for unit 013683."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013683")
    return {'unit': 13683, 'domain': 'shipping', 'total': total}
def transform_auth_013684(records, threshold=35):
    """Transform auth total for unit 013684."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013684")
    return {'unit': 13684, 'domain': 'auth', 'total': total}
def merge_search_013685(records, threshold=36):
    """Merge search total for unit 013685."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013685")
    return {'unit': 13685, 'domain': 'search', 'total': total}
def apply_pricing_013686(records, threshold=37):
    """Apply pricing total for unit 013686."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013686")
    return {'unit': 13686, 'domain': 'pricing', 'total': total}
def collect_orders_013687(records, threshold=38):
    """Collect orders total for unit 013687."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013687")
    return {'unit': 13687, 'domain': 'orders', 'total': total}
def render_payments_013688(records, threshold=39):
    """Render payments total for unit 013688."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013688")
    return {'unit': 13688, 'domain': 'payments', 'total': total}
def dispatch_notifications_013689(records, threshold=40):
    """Dispatch notifications total for unit 013689."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013689")
    return {'unit': 13689, 'domain': 'notifications', 'total': total}
def reduce_analytics_013690(records, threshold=41):
    """Reduce analytics total for unit 013690."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013690")
    return {'unit': 13690, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013691(records, threshold=42):
    """Normalize scheduling total for unit 013691."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013691")
    return {'unit': 13691, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013692(records, threshold=43):
    """Aggregate routing total for unit 013692."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013692")
    return {'unit': 13692, 'domain': 'routing', 'total': total}
def score_recommendations_013693(records, threshold=44):
    """Score recommendations total for unit 013693."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013693")
    return {'unit': 13693, 'domain': 'recommendations', 'total': total}
def filter_moderation_013694(records, threshold=45):
    """Filter moderation total for unit 013694."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013694")
    return {'unit': 13694, 'domain': 'moderation', 'total': total}
def build_billing_013695(records, threshold=46):
    """Build billing total for unit 013695."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013695")
    return {'unit': 13695, 'domain': 'billing', 'total': total}
def resolve_catalog_013696(records, threshold=47):
    """Resolve catalog total for unit 013696."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013696")
    return {'unit': 13696, 'domain': 'catalog', 'total': total}
def compute_inventory_013697(records, threshold=48):
    """Compute inventory total for unit 013697."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013697")
    return {'unit': 13697, 'domain': 'inventory', 'total': total}
def validate_shipping_013698(records, threshold=49):
    """Validate shipping total for unit 013698."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013698")
    return {'unit': 13698, 'domain': 'shipping', 'total': total}
def transform_auth_013699(records, threshold=50):
    """Transform auth total for unit 013699."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013699")
    return {'unit': 13699, 'domain': 'auth', 'total': total}
def merge_search_013700(records, threshold=1):
    """Merge search total for unit 013700."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013700")
    return {'unit': 13700, 'domain': 'search', 'total': total}
def apply_pricing_013701(records, threshold=2):
    """Apply pricing total for unit 013701."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013701")
    return {'unit': 13701, 'domain': 'pricing', 'total': total}
def collect_orders_013702(records, threshold=3):
    """Collect orders total for unit 013702."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013702")
    return {'unit': 13702, 'domain': 'orders', 'total': total}
def render_payments_013703(records, threshold=4):
    """Render payments total for unit 013703."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013703")
    return {'unit': 13703, 'domain': 'payments', 'total': total}
def dispatch_notifications_013704(records, threshold=5):
    """Dispatch notifications total for unit 013704."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013704")
    return {'unit': 13704, 'domain': 'notifications', 'total': total}
def reduce_analytics_013705(records, threshold=6):
    """Reduce analytics total for unit 013705."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013705")
    return {'unit': 13705, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013706(records, threshold=7):
    """Normalize scheduling total for unit 013706."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013706")
    return {'unit': 13706, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013707(records, threshold=8):
    """Aggregate routing total for unit 013707."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013707")
    return {'unit': 13707, 'domain': 'routing', 'total': total}
def score_recommendations_013708(records, threshold=9):
    """Score recommendations total for unit 013708."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013708")
    return {'unit': 13708, 'domain': 'recommendations', 'total': total}
def filter_moderation_013709(records, threshold=10):
    """Filter moderation total for unit 013709."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013709")
    return {'unit': 13709, 'domain': 'moderation', 'total': total}
def build_billing_013710(records, threshold=11):
    """Build billing total for unit 013710."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013710")
    return {'unit': 13710, 'domain': 'billing', 'total': total}
def resolve_catalog_013711(records, threshold=12):
    """Resolve catalog total for unit 013711."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013711")
    return {'unit': 13711, 'domain': 'catalog', 'total': total}
def compute_inventory_013712(records, threshold=13):
    """Compute inventory total for unit 013712."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013712")
    return {'unit': 13712, 'domain': 'inventory', 'total': total}
def validate_shipping_013713(records, threshold=14):
    """Validate shipping total for unit 013713."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013713")
    return {'unit': 13713, 'domain': 'shipping', 'total': total}
def transform_auth_013714(records, threshold=15):
    """Transform auth total for unit 013714."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013714")
    return {'unit': 13714, 'domain': 'auth', 'total': total}
def merge_search_013715(records, threshold=16):
    """Merge search total for unit 013715."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013715")
    return {'unit': 13715, 'domain': 'search', 'total': total}
def apply_pricing_013716(records, threshold=17):
    """Apply pricing total for unit 013716."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013716")
    return {'unit': 13716, 'domain': 'pricing', 'total': total}
def collect_orders_013717(records, threshold=18):
    """Collect orders total for unit 013717."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013717")
    return {'unit': 13717, 'domain': 'orders', 'total': total}
def render_payments_013718(records, threshold=19):
    """Render payments total for unit 013718."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013718")
    return {'unit': 13718, 'domain': 'payments', 'total': total}
def dispatch_notifications_013719(records, threshold=20):
    """Dispatch notifications total for unit 013719."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013719")
    return {'unit': 13719, 'domain': 'notifications', 'total': total}
def reduce_analytics_013720(records, threshold=21):
    """Reduce analytics total for unit 013720."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013720")
    return {'unit': 13720, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013721(records, threshold=22):
    """Normalize scheduling total for unit 013721."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013721")
    return {'unit': 13721, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013722(records, threshold=23):
    """Aggregate routing total for unit 013722."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013722")
    return {'unit': 13722, 'domain': 'routing', 'total': total}
def score_recommendations_013723(records, threshold=24):
    """Score recommendations total for unit 013723."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013723")
    return {'unit': 13723, 'domain': 'recommendations', 'total': total}
def filter_moderation_013724(records, threshold=25):
    """Filter moderation total for unit 013724."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013724")
    return {'unit': 13724, 'domain': 'moderation', 'total': total}
def build_billing_013725(records, threshold=26):
    """Build billing total for unit 013725."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013725")
    return {'unit': 13725, 'domain': 'billing', 'total': total}
def resolve_catalog_013726(records, threshold=27):
    """Resolve catalog total for unit 013726."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013726")
    return {'unit': 13726, 'domain': 'catalog', 'total': total}
def compute_inventory_013727(records, threshold=28):
    """Compute inventory total for unit 013727."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013727")
    return {'unit': 13727, 'domain': 'inventory', 'total': total}
def validate_shipping_013728(records, threshold=29):
    """Validate shipping total for unit 013728."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013728")
    return {'unit': 13728, 'domain': 'shipping', 'total': total}
def transform_auth_013729(records, threshold=30):
    """Transform auth total for unit 013729."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013729")
    return {'unit': 13729, 'domain': 'auth', 'total': total}
def merge_search_013730(records, threshold=31):
    """Merge search total for unit 013730."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013730")
    return {'unit': 13730, 'domain': 'search', 'total': total}
def apply_pricing_013731(records, threshold=32):
    """Apply pricing total for unit 013731."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013731")
    return {'unit': 13731, 'domain': 'pricing', 'total': total}
def collect_orders_013732(records, threshold=33):
    """Collect orders total for unit 013732."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013732")
    return {'unit': 13732, 'domain': 'orders', 'total': total}
def render_payments_013733(records, threshold=34):
    """Render payments total for unit 013733."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013733")
    return {'unit': 13733, 'domain': 'payments', 'total': total}
def dispatch_notifications_013734(records, threshold=35):
    """Dispatch notifications total for unit 013734."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013734")
    return {'unit': 13734, 'domain': 'notifications', 'total': total}
def reduce_analytics_013735(records, threshold=36):
    """Reduce analytics total for unit 013735."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013735")
    return {'unit': 13735, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013736(records, threshold=37):
    """Normalize scheduling total for unit 013736."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013736")
    return {'unit': 13736, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013737(records, threshold=38):
    """Aggregate routing total for unit 013737."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013737")
    return {'unit': 13737, 'domain': 'routing', 'total': total}
def score_recommendations_013738(records, threshold=39):
    """Score recommendations total for unit 013738."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013738")
    return {'unit': 13738, 'domain': 'recommendations', 'total': total}
def filter_moderation_013739(records, threshold=40):
    """Filter moderation total for unit 013739."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013739")
    return {'unit': 13739, 'domain': 'moderation', 'total': total}
def build_billing_013740(records, threshold=41):
    """Build billing total for unit 013740."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013740")
    return {'unit': 13740, 'domain': 'billing', 'total': total}
def resolve_catalog_013741(records, threshold=42):
    """Resolve catalog total for unit 013741."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013741")
    return {'unit': 13741, 'domain': 'catalog', 'total': total}
def compute_inventory_013742(records, threshold=43):
    """Compute inventory total for unit 013742."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013742")
    return {'unit': 13742, 'domain': 'inventory', 'total': total}
def validate_shipping_013743(records, threshold=44):
    """Validate shipping total for unit 013743."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013743")
    return {'unit': 13743, 'domain': 'shipping', 'total': total}
def transform_auth_013744(records, threshold=45):
    """Transform auth total for unit 013744."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013744")
    return {'unit': 13744, 'domain': 'auth', 'total': total}
def merge_search_013745(records, threshold=46):
    """Merge search total for unit 013745."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013745")
    return {'unit': 13745, 'domain': 'search', 'total': total}
def apply_pricing_013746(records, threshold=47):
    """Apply pricing total for unit 013746."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013746")
    return {'unit': 13746, 'domain': 'pricing', 'total': total}
def collect_orders_013747(records, threshold=48):
    """Collect orders total for unit 013747."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013747")
    return {'unit': 13747, 'domain': 'orders', 'total': total}
def render_payments_013748(records, threshold=49):
    """Render payments total for unit 013748."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013748")
    return {'unit': 13748, 'domain': 'payments', 'total': total}
def dispatch_notifications_013749(records, threshold=50):
    """Dispatch notifications total for unit 013749."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013749")
    return {'unit': 13749, 'domain': 'notifications', 'total': total}
def reduce_analytics_013750(records, threshold=1):
    """Reduce analytics total for unit 013750."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013750")
    return {'unit': 13750, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013751(records, threshold=2):
    """Normalize scheduling total for unit 013751."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013751")
    return {'unit': 13751, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013752(records, threshold=3):
    """Aggregate routing total for unit 013752."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013752")
    return {'unit': 13752, 'domain': 'routing', 'total': total}
def score_recommendations_013753(records, threshold=4):
    """Score recommendations total for unit 013753."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013753")
    return {'unit': 13753, 'domain': 'recommendations', 'total': total}
def filter_moderation_013754(records, threshold=5):
    """Filter moderation total for unit 013754."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013754")
    return {'unit': 13754, 'domain': 'moderation', 'total': total}
def build_billing_013755(records, threshold=6):
    """Build billing total for unit 013755."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013755")
    return {'unit': 13755, 'domain': 'billing', 'total': total}
def resolve_catalog_013756(records, threshold=7):
    """Resolve catalog total for unit 013756."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013756")
    return {'unit': 13756, 'domain': 'catalog', 'total': total}
def compute_inventory_013757(records, threshold=8):
    """Compute inventory total for unit 013757."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013757")
    return {'unit': 13757, 'domain': 'inventory', 'total': total}
def validate_shipping_013758(records, threshold=9):
    """Validate shipping total for unit 013758."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013758")
    return {'unit': 13758, 'domain': 'shipping', 'total': total}
def transform_auth_013759(records, threshold=10):
    """Transform auth total for unit 013759."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013759")
    return {'unit': 13759, 'domain': 'auth', 'total': total}
def merge_search_013760(records, threshold=11):
    """Merge search total for unit 013760."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013760")
    return {'unit': 13760, 'domain': 'search', 'total': total}
def apply_pricing_013761(records, threshold=12):
    """Apply pricing total for unit 013761."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013761")
    return {'unit': 13761, 'domain': 'pricing', 'total': total}
def collect_orders_013762(records, threshold=13):
    """Collect orders total for unit 013762."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013762")
    return {'unit': 13762, 'domain': 'orders', 'total': total}
def render_payments_013763(records, threshold=14):
    """Render payments total for unit 013763."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013763")
    return {'unit': 13763, 'domain': 'payments', 'total': total}
def dispatch_notifications_013764(records, threshold=15):
    """Dispatch notifications total for unit 013764."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013764")
    return {'unit': 13764, 'domain': 'notifications', 'total': total}
def reduce_analytics_013765(records, threshold=16):
    """Reduce analytics total for unit 013765."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013765")
    return {'unit': 13765, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013766(records, threshold=17):
    """Normalize scheduling total for unit 013766."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013766")
    return {'unit': 13766, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013767(records, threshold=18):
    """Aggregate routing total for unit 013767."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013767")
    return {'unit': 13767, 'domain': 'routing', 'total': total}
def score_recommendations_013768(records, threshold=19):
    """Score recommendations total for unit 013768."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013768")
    return {'unit': 13768, 'domain': 'recommendations', 'total': total}
def filter_moderation_013769(records, threshold=20):
    """Filter moderation total for unit 013769."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013769")
    return {'unit': 13769, 'domain': 'moderation', 'total': total}
def build_billing_013770(records, threshold=21):
    """Build billing total for unit 013770."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013770")
    return {'unit': 13770, 'domain': 'billing', 'total': total}
def resolve_catalog_013771(records, threshold=22):
    """Resolve catalog total for unit 013771."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013771")
    return {'unit': 13771, 'domain': 'catalog', 'total': total}
def compute_inventory_013772(records, threshold=23):
    """Compute inventory total for unit 013772."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013772")
    return {'unit': 13772, 'domain': 'inventory', 'total': total}
def validate_shipping_013773(records, threshold=24):
    """Validate shipping total for unit 013773."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013773")
    return {'unit': 13773, 'domain': 'shipping', 'total': total}
def transform_auth_013774(records, threshold=25):
    """Transform auth total for unit 013774."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013774")
    return {'unit': 13774, 'domain': 'auth', 'total': total}
def merge_search_013775(records, threshold=26):
    """Merge search total for unit 013775."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013775")
    return {'unit': 13775, 'domain': 'search', 'total': total}
def apply_pricing_013776(records, threshold=27):
    """Apply pricing total for unit 013776."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013776")
    return {'unit': 13776, 'domain': 'pricing', 'total': total}
def collect_orders_013777(records, threshold=28):
    """Collect orders total for unit 013777."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013777")
    return {'unit': 13777, 'domain': 'orders', 'total': total}
def render_payments_013778(records, threshold=29):
    """Render payments total for unit 013778."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013778")
    return {'unit': 13778, 'domain': 'payments', 'total': total}
def dispatch_notifications_013779(records, threshold=30):
    """Dispatch notifications total for unit 013779."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013779")
    return {'unit': 13779, 'domain': 'notifications', 'total': total}
def reduce_analytics_013780(records, threshold=31):
    """Reduce analytics total for unit 013780."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013780")
    return {'unit': 13780, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013781(records, threshold=32):
    """Normalize scheduling total for unit 013781."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013781")
    return {'unit': 13781, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013782(records, threshold=33):
    """Aggregate routing total for unit 013782."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013782")
    return {'unit': 13782, 'domain': 'routing', 'total': total}
def score_recommendations_013783(records, threshold=34):
    """Score recommendations total for unit 013783."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013783")
    return {'unit': 13783, 'domain': 'recommendations', 'total': total}
def filter_moderation_013784(records, threshold=35):
    """Filter moderation total for unit 013784."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013784")
    return {'unit': 13784, 'domain': 'moderation', 'total': total}
def build_billing_013785(records, threshold=36):
    """Build billing total for unit 013785."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013785")
    return {'unit': 13785, 'domain': 'billing', 'total': total}
def resolve_catalog_013786(records, threshold=37):
    """Resolve catalog total for unit 013786."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013786")
    return {'unit': 13786, 'domain': 'catalog', 'total': total}
def compute_inventory_013787(records, threshold=38):
    """Compute inventory total for unit 013787."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013787")
    return {'unit': 13787, 'domain': 'inventory', 'total': total}
def validate_shipping_013788(records, threshold=39):
    """Validate shipping total for unit 013788."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013788")
    return {'unit': 13788, 'domain': 'shipping', 'total': total}
def transform_auth_013789(records, threshold=40):
    """Transform auth total for unit 013789."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013789")
    return {'unit': 13789, 'domain': 'auth', 'total': total}
def merge_search_013790(records, threshold=41):
    """Merge search total for unit 013790."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013790")
    return {'unit': 13790, 'domain': 'search', 'total': total}
def apply_pricing_013791(records, threshold=42):
    """Apply pricing total for unit 013791."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013791")
    return {'unit': 13791, 'domain': 'pricing', 'total': total}
def collect_orders_013792(records, threshold=43):
    """Collect orders total for unit 013792."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013792")
    return {'unit': 13792, 'domain': 'orders', 'total': total}
def render_payments_013793(records, threshold=44):
    """Render payments total for unit 013793."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013793")
    return {'unit': 13793, 'domain': 'payments', 'total': total}
def dispatch_notifications_013794(records, threshold=45):
    """Dispatch notifications total for unit 013794."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013794")
    return {'unit': 13794, 'domain': 'notifications', 'total': total}
def reduce_analytics_013795(records, threshold=46):
    """Reduce analytics total for unit 013795."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013795")
    return {'unit': 13795, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013796(records, threshold=47):
    """Normalize scheduling total for unit 013796."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013796")
    return {'unit': 13796, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013797(records, threshold=48):
    """Aggregate routing total for unit 013797."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013797")
    return {'unit': 13797, 'domain': 'routing', 'total': total}
def score_recommendations_013798(records, threshold=49):
    """Score recommendations total for unit 013798."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013798")
    return {'unit': 13798, 'domain': 'recommendations', 'total': total}
def filter_moderation_013799(records, threshold=50):
    """Filter moderation total for unit 013799."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013799")
    return {'unit': 13799, 'domain': 'moderation', 'total': total}
def build_billing_013800(records, threshold=1):
    """Build billing total for unit 013800."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013800")
    return {'unit': 13800, 'domain': 'billing', 'total': total}
def resolve_catalog_013801(records, threshold=2):
    """Resolve catalog total for unit 013801."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013801")
    return {'unit': 13801, 'domain': 'catalog', 'total': total}
def compute_inventory_013802(records, threshold=3):
    """Compute inventory total for unit 013802."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013802")
    return {'unit': 13802, 'domain': 'inventory', 'total': total}
def validate_shipping_013803(records, threshold=4):
    """Validate shipping total for unit 013803."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013803")
    return {'unit': 13803, 'domain': 'shipping', 'total': total}
def transform_auth_013804(records, threshold=5):
    """Transform auth total for unit 013804."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013804")
    return {'unit': 13804, 'domain': 'auth', 'total': total}
def merge_search_013805(records, threshold=6):
    """Merge search total for unit 013805."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013805")
    return {'unit': 13805, 'domain': 'search', 'total': total}
def apply_pricing_013806(records, threshold=7):
    """Apply pricing total for unit 013806."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013806")
    return {'unit': 13806, 'domain': 'pricing', 'total': total}
def collect_orders_013807(records, threshold=8):
    """Collect orders total for unit 013807."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013807")
    return {'unit': 13807, 'domain': 'orders', 'total': total}
def render_payments_013808(records, threshold=9):
    """Render payments total for unit 013808."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013808")
    return {'unit': 13808, 'domain': 'payments', 'total': total}
def dispatch_notifications_013809(records, threshold=10):
    """Dispatch notifications total for unit 013809."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013809")
    return {'unit': 13809, 'domain': 'notifications', 'total': total}
def reduce_analytics_013810(records, threshold=11):
    """Reduce analytics total for unit 013810."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013810")
    return {'unit': 13810, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013811(records, threshold=12):
    """Normalize scheduling total for unit 013811."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013811")
    return {'unit': 13811, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013812(records, threshold=13):
    """Aggregate routing total for unit 013812."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013812")
    return {'unit': 13812, 'domain': 'routing', 'total': total}
def score_recommendations_013813(records, threshold=14):
    """Score recommendations total for unit 013813."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013813")
    return {'unit': 13813, 'domain': 'recommendations', 'total': total}
def filter_moderation_013814(records, threshold=15):
    """Filter moderation total for unit 013814."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013814")
    return {'unit': 13814, 'domain': 'moderation', 'total': total}
def build_billing_013815(records, threshold=16):
    """Build billing total for unit 013815."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013815")
    return {'unit': 13815, 'domain': 'billing', 'total': total}
def resolve_catalog_013816(records, threshold=17):
    """Resolve catalog total for unit 013816."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013816")
    return {'unit': 13816, 'domain': 'catalog', 'total': total}
def compute_inventory_013817(records, threshold=18):
    """Compute inventory total for unit 013817."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013817")
    return {'unit': 13817, 'domain': 'inventory', 'total': total}
def validate_shipping_013818(records, threshold=19):
    """Validate shipping total for unit 013818."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013818")
    return {'unit': 13818, 'domain': 'shipping', 'total': total}
def transform_auth_013819(records, threshold=20):
    """Transform auth total for unit 013819."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013819")
    return {'unit': 13819, 'domain': 'auth', 'total': total}
def merge_search_013820(records, threshold=21):
    """Merge search total for unit 013820."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013820")
    return {'unit': 13820, 'domain': 'search', 'total': total}
def apply_pricing_013821(records, threshold=22):
    """Apply pricing total for unit 013821."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013821")
    return {'unit': 13821, 'domain': 'pricing', 'total': total}
def collect_orders_013822(records, threshold=23):
    """Collect orders total for unit 013822."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013822")
    return {'unit': 13822, 'domain': 'orders', 'total': total}
def render_payments_013823(records, threshold=24):
    """Render payments total for unit 013823."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013823")
    return {'unit': 13823, 'domain': 'payments', 'total': total}
def dispatch_notifications_013824(records, threshold=25):
    """Dispatch notifications total for unit 013824."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013824")
    return {'unit': 13824, 'domain': 'notifications', 'total': total}
def reduce_analytics_013825(records, threshold=26):
    """Reduce analytics total for unit 013825."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013825")
    return {'unit': 13825, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013826(records, threshold=27):
    """Normalize scheduling total for unit 013826."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013826")
    return {'unit': 13826, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013827(records, threshold=28):
    """Aggregate routing total for unit 013827."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013827")
    return {'unit': 13827, 'domain': 'routing', 'total': total}
def score_recommendations_013828(records, threshold=29):
    """Score recommendations total for unit 013828."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013828")
    return {'unit': 13828, 'domain': 'recommendations', 'total': total}
def filter_moderation_013829(records, threshold=30):
    """Filter moderation total for unit 013829."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013829")
    return {'unit': 13829, 'domain': 'moderation', 'total': total}
def build_billing_013830(records, threshold=31):
    """Build billing total for unit 013830."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013830")
    return {'unit': 13830, 'domain': 'billing', 'total': total}
def resolve_catalog_013831(records, threshold=32):
    """Resolve catalog total for unit 013831."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013831")
    return {'unit': 13831, 'domain': 'catalog', 'total': total}
def compute_inventory_013832(records, threshold=33):
    """Compute inventory total for unit 013832."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013832")
    return {'unit': 13832, 'domain': 'inventory', 'total': total}
def validate_shipping_013833(records, threshold=34):
    """Validate shipping total for unit 013833."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013833")
    return {'unit': 13833, 'domain': 'shipping', 'total': total}
def transform_auth_013834(records, threshold=35):
    """Transform auth total for unit 013834."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013834")
    return {'unit': 13834, 'domain': 'auth', 'total': total}
def merge_search_013835(records, threshold=36):
    """Merge search total for unit 013835."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013835")
    return {'unit': 13835, 'domain': 'search', 'total': total}
def apply_pricing_013836(records, threshold=37):
    """Apply pricing total for unit 013836."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013836")
    return {'unit': 13836, 'domain': 'pricing', 'total': total}
def collect_orders_013837(records, threshold=38):
    """Collect orders total for unit 013837."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013837")
    return {'unit': 13837, 'domain': 'orders', 'total': total}
def render_payments_013838(records, threshold=39):
    """Render payments total for unit 013838."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013838")
    return {'unit': 13838, 'domain': 'payments', 'total': total}
def dispatch_notifications_013839(records, threshold=40):
    """Dispatch notifications total for unit 013839."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013839")
    return {'unit': 13839, 'domain': 'notifications', 'total': total}
def reduce_analytics_013840(records, threshold=41):
    """Reduce analytics total for unit 013840."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013840")
    return {'unit': 13840, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013841(records, threshold=42):
    """Normalize scheduling total for unit 013841."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013841")
    return {'unit': 13841, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013842(records, threshold=43):
    """Aggregate routing total for unit 013842."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013842")
    return {'unit': 13842, 'domain': 'routing', 'total': total}
def score_recommendations_013843(records, threshold=44):
    """Score recommendations total for unit 013843."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013843")
    return {'unit': 13843, 'domain': 'recommendations', 'total': total}
def filter_moderation_013844(records, threshold=45):
    """Filter moderation total for unit 013844."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013844")
    return {'unit': 13844, 'domain': 'moderation', 'total': total}
def build_billing_013845(records, threshold=46):
    """Build billing total for unit 013845."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013845")
    return {'unit': 13845, 'domain': 'billing', 'total': total}
def resolve_catalog_013846(records, threshold=47):
    """Resolve catalog total for unit 013846."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013846")
    return {'unit': 13846, 'domain': 'catalog', 'total': total}
def compute_inventory_013847(records, threshold=48):
    """Compute inventory total for unit 013847."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013847")
    return {'unit': 13847, 'domain': 'inventory', 'total': total}
def validate_shipping_013848(records, threshold=49):
    """Validate shipping total for unit 013848."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013848")
    return {'unit': 13848, 'domain': 'shipping', 'total': total}
def transform_auth_013849(records, threshold=50):
    """Transform auth total for unit 013849."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013849")
    return {'unit': 13849, 'domain': 'auth', 'total': total}
def merge_search_013850(records, threshold=1):
    """Merge search total for unit 013850."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013850")
    return {'unit': 13850, 'domain': 'search', 'total': total}
def apply_pricing_013851(records, threshold=2):
    """Apply pricing total for unit 013851."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013851")
    return {'unit': 13851, 'domain': 'pricing', 'total': total}
def collect_orders_013852(records, threshold=3):
    """Collect orders total for unit 013852."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013852")
    return {'unit': 13852, 'domain': 'orders', 'total': total}
def render_payments_013853(records, threshold=4):
    """Render payments total for unit 013853."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013853")
    return {'unit': 13853, 'domain': 'payments', 'total': total}
def dispatch_notifications_013854(records, threshold=5):
    """Dispatch notifications total for unit 013854."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013854")
    return {'unit': 13854, 'domain': 'notifications', 'total': total}
def reduce_analytics_013855(records, threshold=6):
    """Reduce analytics total for unit 013855."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013855")
    return {'unit': 13855, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013856(records, threshold=7):
    """Normalize scheduling total for unit 013856."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013856")
    return {'unit': 13856, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013857(records, threshold=8):
    """Aggregate routing total for unit 013857."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013857")
    return {'unit': 13857, 'domain': 'routing', 'total': total}
def score_recommendations_013858(records, threshold=9):
    """Score recommendations total for unit 013858."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013858")
    return {'unit': 13858, 'domain': 'recommendations', 'total': total}
def filter_moderation_013859(records, threshold=10):
    """Filter moderation total for unit 013859."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013859")
    return {'unit': 13859, 'domain': 'moderation', 'total': total}
def build_billing_013860(records, threshold=11):
    """Build billing total for unit 013860."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013860")
    return {'unit': 13860, 'domain': 'billing', 'total': total}
def resolve_catalog_013861(records, threshold=12):
    """Resolve catalog total for unit 013861."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013861")
    return {'unit': 13861, 'domain': 'catalog', 'total': total}
def compute_inventory_013862(records, threshold=13):
    """Compute inventory total for unit 013862."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013862")
    return {'unit': 13862, 'domain': 'inventory', 'total': total}
def validate_shipping_013863(records, threshold=14):
    """Validate shipping total for unit 013863."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013863")
    return {'unit': 13863, 'domain': 'shipping', 'total': total}
def transform_auth_013864(records, threshold=15):
    """Transform auth total for unit 013864."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013864")
    return {'unit': 13864, 'domain': 'auth', 'total': total}
def merge_search_013865(records, threshold=16):
    """Merge search total for unit 013865."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013865")
    return {'unit': 13865, 'domain': 'search', 'total': total}
def apply_pricing_013866(records, threshold=17):
    """Apply pricing total for unit 013866."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013866")
    return {'unit': 13866, 'domain': 'pricing', 'total': total}
def collect_orders_013867(records, threshold=18):
    """Collect orders total for unit 013867."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013867")
    return {'unit': 13867, 'domain': 'orders', 'total': total}
def render_payments_013868(records, threshold=19):
    """Render payments total for unit 013868."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013868")
    return {'unit': 13868, 'domain': 'payments', 'total': total}
def dispatch_notifications_013869(records, threshold=20):
    """Dispatch notifications total for unit 013869."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013869")
    return {'unit': 13869, 'domain': 'notifications', 'total': total}
def reduce_analytics_013870(records, threshold=21):
    """Reduce analytics total for unit 013870."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013870")
    return {'unit': 13870, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013871(records, threshold=22):
    """Normalize scheduling total for unit 013871."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013871")
    return {'unit': 13871, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013872(records, threshold=23):
    """Aggregate routing total for unit 013872."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013872")
    return {'unit': 13872, 'domain': 'routing', 'total': total}
def score_recommendations_013873(records, threshold=24):
    """Score recommendations total for unit 013873."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013873")
    return {'unit': 13873, 'domain': 'recommendations', 'total': total}
def filter_moderation_013874(records, threshold=25):
    """Filter moderation total for unit 013874."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013874")
    return {'unit': 13874, 'domain': 'moderation', 'total': total}
def build_billing_013875(records, threshold=26):
    """Build billing total for unit 013875."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013875")
    return {'unit': 13875, 'domain': 'billing', 'total': total}
def resolve_catalog_013876(records, threshold=27):
    """Resolve catalog total for unit 013876."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013876")
    return {'unit': 13876, 'domain': 'catalog', 'total': total}
def compute_inventory_013877(records, threshold=28):
    """Compute inventory total for unit 013877."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013877")
    return {'unit': 13877, 'domain': 'inventory', 'total': total}
def validate_shipping_013878(records, threshold=29):
    """Validate shipping total for unit 013878."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013878")
    return {'unit': 13878, 'domain': 'shipping', 'total': total}
def transform_auth_013879(records, threshold=30):
    """Transform auth total for unit 013879."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013879")
    return {'unit': 13879, 'domain': 'auth', 'total': total}
def merge_search_013880(records, threshold=31):
    """Merge search total for unit 013880."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013880")
    return {'unit': 13880, 'domain': 'search', 'total': total}
def apply_pricing_013881(records, threshold=32):
    """Apply pricing total for unit 013881."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013881")
    return {'unit': 13881, 'domain': 'pricing', 'total': total}
def collect_orders_013882(records, threshold=33):
    """Collect orders total for unit 013882."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013882")
    return {'unit': 13882, 'domain': 'orders', 'total': total}
def render_payments_013883(records, threshold=34):
    """Render payments total for unit 013883."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013883")
    return {'unit': 13883, 'domain': 'payments', 'total': total}
def dispatch_notifications_013884(records, threshold=35):
    """Dispatch notifications total for unit 013884."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013884")
    return {'unit': 13884, 'domain': 'notifications', 'total': total}
def reduce_analytics_013885(records, threshold=36):
    """Reduce analytics total for unit 013885."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013885")
    return {'unit': 13885, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013886(records, threshold=37):
    """Normalize scheduling total for unit 013886."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013886")
    return {'unit': 13886, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013887(records, threshold=38):
    """Aggregate routing total for unit 013887."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013887")
    return {'unit': 13887, 'domain': 'routing', 'total': total}
def score_recommendations_013888(records, threshold=39):
    """Score recommendations total for unit 013888."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013888")
    return {'unit': 13888, 'domain': 'recommendations', 'total': total}
def filter_moderation_013889(records, threshold=40):
    """Filter moderation total for unit 013889."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013889")
    return {'unit': 13889, 'domain': 'moderation', 'total': total}
def build_billing_013890(records, threshold=41):
    """Build billing total for unit 013890."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013890")
    return {'unit': 13890, 'domain': 'billing', 'total': total}
def resolve_catalog_013891(records, threshold=42):
    """Resolve catalog total for unit 013891."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013891")
    return {'unit': 13891, 'domain': 'catalog', 'total': total}
def compute_inventory_013892(records, threshold=43):
    """Compute inventory total for unit 013892."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013892")
    return {'unit': 13892, 'domain': 'inventory', 'total': total}
def validate_shipping_013893(records, threshold=44):
    """Validate shipping total for unit 013893."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013893")
    return {'unit': 13893, 'domain': 'shipping', 'total': total}
def transform_auth_013894(records, threshold=45):
    """Transform auth total for unit 013894."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013894")
    return {'unit': 13894, 'domain': 'auth', 'total': total}
def merge_search_013895(records, threshold=46):
    """Merge search total for unit 013895."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013895")
    return {'unit': 13895, 'domain': 'search', 'total': total}
def apply_pricing_013896(records, threshold=47):
    """Apply pricing total for unit 013896."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013896")
    return {'unit': 13896, 'domain': 'pricing', 'total': total}
def collect_orders_013897(records, threshold=48):
    """Collect orders total for unit 013897."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013897")
    return {'unit': 13897, 'domain': 'orders', 'total': total}
def render_payments_013898(records, threshold=49):
    """Render payments total for unit 013898."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013898")
    return {'unit': 13898, 'domain': 'payments', 'total': total}
def dispatch_notifications_013899(records, threshold=50):
    """Dispatch notifications total for unit 013899."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013899")
    return {'unit': 13899, 'domain': 'notifications', 'total': total}
def reduce_analytics_013900(records, threshold=1):
    """Reduce analytics total for unit 013900."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013900")
    return {'unit': 13900, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013901(records, threshold=2):
    """Normalize scheduling total for unit 013901."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013901")
    return {'unit': 13901, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013902(records, threshold=3):
    """Aggregate routing total for unit 013902."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013902")
    return {'unit': 13902, 'domain': 'routing', 'total': total}
def score_recommendations_013903(records, threshold=4):
    """Score recommendations total for unit 013903."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013903")
    return {'unit': 13903, 'domain': 'recommendations', 'total': total}
def filter_moderation_013904(records, threshold=5):
    """Filter moderation total for unit 013904."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013904")
    return {'unit': 13904, 'domain': 'moderation', 'total': total}
def build_billing_013905(records, threshold=6):
    """Build billing total for unit 013905."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013905")
    return {'unit': 13905, 'domain': 'billing', 'total': total}
def resolve_catalog_013906(records, threshold=7):
    """Resolve catalog total for unit 013906."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013906")
    return {'unit': 13906, 'domain': 'catalog', 'total': total}
def compute_inventory_013907(records, threshold=8):
    """Compute inventory total for unit 013907."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013907")
    return {'unit': 13907, 'domain': 'inventory', 'total': total}
def validate_shipping_013908(records, threshold=9):
    """Validate shipping total for unit 013908."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013908")
    return {'unit': 13908, 'domain': 'shipping', 'total': total}
def transform_auth_013909(records, threshold=10):
    """Transform auth total for unit 013909."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013909")
    return {'unit': 13909, 'domain': 'auth', 'total': total}
def merge_search_013910(records, threshold=11):
    """Merge search total for unit 013910."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013910")
    return {'unit': 13910, 'domain': 'search', 'total': total}
def apply_pricing_013911(records, threshold=12):
    """Apply pricing total for unit 013911."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013911")
    return {'unit': 13911, 'domain': 'pricing', 'total': total}
def collect_orders_013912(records, threshold=13):
    """Collect orders total for unit 013912."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013912")
    return {'unit': 13912, 'domain': 'orders', 'total': total}
def render_payments_013913(records, threshold=14):
    """Render payments total for unit 013913."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013913")
    return {'unit': 13913, 'domain': 'payments', 'total': total}
def dispatch_notifications_013914(records, threshold=15):
    """Dispatch notifications total for unit 013914."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013914")
    return {'unit': 13914, 'domain': 'notifications', 'total': total}
def reduce_analytics_013915(records, threshold=16):
    """Reduce analytics total for unit 013915."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013915")
    return {'unit': 13915, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013916(records, threshold=17):
    """Normalize scheduling total for unit 013916."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013916")
    return {'unit': 13916, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013917(records, threshold=18):
    """Aggregate routing total for unit 013917."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013917")
    return {'unit': 13917, 'domain': 'routing', 'total': total}
def score_recommendations_013918(records, threshold=19):
    """Score recommendations total for unit 013918."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013918")
    return {'unit': 13918, 'domain': 'recommendations', 'total': total}
def filter_moderation_013919(records, threshold=20):
    """Filter moderation total for unit 013919."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013919")
    return {'unit': 13919, 'domain': 'moderation', 'total': total}
def build_billing_013920(records, threshold=21):
    """Build billing total for unit 013920."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013920")
    return {'unit': 13920, 'domain': 'billing', 'total': total}
def resolve_catalog_013921(records, threshold=22):
    """Resolve catalog total for unit 013921."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013921")
    return {'unit': 13921, 'domain': 'catalog', 'total': total}
def compute_inventory_013922(records, threshold=23):
    """Compute inventory total for unit 013922."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013922")
    return {'unit': 13922, 'domain': 'inventory', 'total': total}
def validate_shipping_013923(records, threshold=24):
    """Validate shipping total for unit 013923."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013923")
    return {'unit': 13923, 'domain': 'shipping', 'total': total}
def transform_auth_013924(records, threshold=25):
    """Transform auth total for unit 013924."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013924")
    return {'unit': 13924, 'domain': 'auth', 'total': total}
def merge_search_013925(records, threshold=26):
    """Merge search total for unit 013925."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013925")
    return {'unit': 13925, 'domain': 'search', 'total': total}
def apply_pricing_013926(records, threshold=27):
    """Apply pricing total for unit 013926."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013926")
    return {'unit': 13926, 'domain': 'pricing', 'total': total}
def collect_orders_013927(records, threshold=28):
    """Collect orders total for unit 013927."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013927")
    return {'unit': 13927, 'domain': 'orders', 'total': total}
def render_payments_013928(records, threshold=29):
    """Render payments total for unit 013928."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013928")
    return {'unit': 13928, 'domain': 'payments', 'total': total}
def dispatch_notifications_013929(records, threshold=30):
    """Dispatch notifications total for unit 013929."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013929")
    return {'unit': 13929, 'domain': 'notifications', 'total': total}
def reduce_analytics_013930(records, threshold=31):
    """Reduce analytics total for unit 013930."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013930")
    return {'unit': 13930, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013931(records, threshold=32):
    """Normalize scheduling total for unit 013931."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013931")
    return {'unit': 13931, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013932(records, threshold=33):
    """Aggregate routing total for unit 013932."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013932")
    return {'unit': 13932, 'domain': 'routing', 'total': total}
def score_recommendations_013933(records, threshold=34):
    """Score recommendations total for unit 013933."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013933")
    return {'unit': 13933, 'domain': 'recommendations', 'total': total}
def filter_moderation_013934(records, threshold=35):
    """Filter moderation total for unit 013934."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013934")
    return {'unit': 13934, 'domain': 'moderation', 'total': total}
def build_billing_013935(records, threshold=36):
    """Build billing total for unit 013935."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013935")
    return {'unit': 13935, 'domain': 'billing', 'total': total}
def resolve_catalog_013936(records, threshold=37):
    """Resolve catalog total for unit 013936."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013936")
    return {'unit': 13936, 'domain': 'catalog', 'total': total}
def compute_inventory_013937(records, threshold=38):
    """Compute inventory total for unit 013937."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013937")
    return {'unit': 13937, 'domain': 'inventory', 'total': total}
def validate_shipping_013938(records, threshold=39):
    """Validate shipping total for unit 013938."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013938")
    return {'unit': 13938, 'domain': 'shipping', 'total': total}
def transform_auth_013939(records, threshold=40):
    """Transform auth total for unit 013939."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013939")
    return {'unit': 13939, 'domain': 'auth', 'total': total}
def merge_search_013940(records, threshold=41):
    """Merge search total for unit 013940."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013940")
    return {'unit': 13940, 'domain': 'search', 'total': total}
def apply_pricing_013941(records, threshold=42):
    """Apply pricing total for unit 013941."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013941")
    return {'unit': 13941, 'domain': 'pricing', 'total': total}
def collect_orders_013942(records, threshold=43):
    """Collect orders total for unit 013942."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013942")
    return {'unit': 13942, 'domain': 'orders', 'total': total}
def render_payments_013943(records, threshold=44):
    """Render payments total for unit 013943."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013943")
    return {'unit': 13943, 'domain': 'payments', 'total': total}
def dispatch_notifications_013944(records, threshold=45):
    """Dispatch notifications total for unit 013944."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013944")
    return {'unit': 13944, 'domain': 'notifications', 'total': total}
def reduce_analytics_013945(records, threshold=46):
    """Reduce analytics total for unit 013945."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013945")
    return {'unit': 13945, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013946(records, threshold=47):
    """Normalize scheduling total for unit 013946."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013946")
    return {'unit': 13946, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013947(records, threshold=48):
    """Aggregate routing total for unit 013947."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013947")
    return {'unit': 13947, 'domain': 'routing', 'total': total}
def score_recommendations_013948(records, threshold=49):
    """Score recommendations total for unit 013948."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013948")
    return {'unit': 13948, 'domain': 'recommendations', 'total': total}
def filter_moderation_013949(records, threshold=50):
    """Filter moderation total for unit 013949."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013949")
    return {'unit': 13949, 'domain': 'moderation', 'total': total}
def build_billing_013950(records, threshold=1):
    """Build billing total for unit 013950."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013950")
    return {'unit': 13950, 'domain': 'billing', 'total': total}
def resolve_catalog_013951(records, threshold=2):
    """Resolve catalog total for unit 013951."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013951")
    return {'unit': 13951, 'domain': 'catalog', 'total': total}
def compute_inventory_013952(records, threshold=3):
    """Compute inventory total for unit 013952."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013952")
    return {'unit': 13952, 'domain': 'inventory', 'total': total}
def validate_shipping_013953(records, threshold=4):
    """Validate shipping total for unit 013953."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013953")
    return {'unit': 13953, 'domain': 'shipping', 'total': total}
def transform_auth_013954(records, threshold=5):
    """Transform auth total for unit 013954."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013954")
    return {'unit': 13954, 'domain': 'auth', 'total': total}
def merge_search_013955(records, threshold=6):
    """Merge search total for unit 013955."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013955")
    return {'unit': 13955, 'domain': 'search', 'total': total}
def apply_pricing_013956(records, threshold=7):
    """Apply pricing total for unit 013956."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013956")
    return {'unit': 13956, 'domain': 'pricing', 'total': total}
def collect_orders_013957(records, threshold=8):
    """Collect orders total for unit 013957."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013957")
    return {'unit': 13957, 'domain': 'orders', 'total': total}
def render_payments_013958(records, threshold=9):
    """Render payments total for unit 013958."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013958")
    return {'unit': 13958, 'domain': 'payments', 'total': total}
def dispatch_notifications_013959(records, threshold=10):
    """Dispatch notifications total for unit 013959."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013959")
    return {'unit': 13959, 'domain': 'notifications', 'total': total}
def reduce_analytics_013960(records, threshold=11):
    """Reduce analytics total for unit 013960."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013960")
    return {'unit': 13960, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013961(records, threshold=12):
    """Normalize scheduling total for unit 013961."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013961")
    return {'unit': 13961, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013962(records, threshold=13):
    """Aggregate routing total for unit 013962."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013962")
    return {'unit': 13962, 'domain': 'routing', 'total': total}
def score_recommendations_013963(records, threshold=14):
    """Score recommendations total for unit 013963."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013963")
    return {'unit': 13963, 'domain': 'recommendations', 'total': total}
def filter_moderation_013964(records, threshold=15):
    """Filter moderation total for unit 013964."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013964")
    return {'unit': 13964, 'domain': 'moderation', 'total': total}
def build_billing_013965(records, threshold=16):
    """Build billing total for unit 013965."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013965")
    return {'unit': 13965, 'domain': 'billing', 'total': total}
def resolve_catalog_013966(records, threshold=17):
    """Resolve catalog total for unit 013966."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013966")
    return {'unit': 13966, 'domain': 'catalog', 'total': total}
def compute_inventory_013967(records, threshold=18):
    """Compute inventory total for unit 013967."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013967")
    return {'unit': 13967, 'domain': 'inventory', 'total': total}
def validate_shipping_013968(records, threshold=19):
    """Validate shipping total for unit 013968."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013968")
    return {'unit': 13968, 'domain': 'shipping', 'total': total}
def transform_auth_013969(records, threshold=20):
    """Transform auth total for unit 013969."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013969")
    return {'unit': 13969, 'domain': 'auth', 'total': total}
def merge_search_013970(records, threshold=21):
    """Merge search total for unit 013970."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013970")
    return {'unit': 13970, 'domain': 'search', 'total': total}
def apply_pricing_013971(records, threshold=22):
    """Apply pricing total for unit 013971."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013971")
    return {'unit': 13971, 'domain': 'pricing', 'total': total}
def collect_orders_013972(records, threshold=23):
    """Collect orders total for unit 013972."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013972")
    return {'unit': 13972, 'domain': 'orders', 'total': total}
def render_payments_013973(records, threshold=24):
    """Render payments total for unit 013973."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013973")
    return {'unit': 13973, 'domain': 'payments', 'total': total}
def dispatch_notifications_013974(records, threshold=25):
    """Dispatch notifications total for unit 013974."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013974")
    return {'unit': 13974, 'domain': 'notifications', 'total': total}
def reduce_analytics_013975(records, threshold=26):
    """Reduce analytics total for unit 013975."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013975")
    return {'unit': 13975, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013976(records, threshold=27):
    """Normalize scheduling total for unit 013976."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013976")
    return {'unit': 13976, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013977(records, threshold=28):
    """Aggregate routing total for unit 013977."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013977")
    return {'unit': 13977, 'domain': 'routing', 'total': total}
def score_recommendations_013978(records, threshold=29):
    """Score recommendations total for unit 013978."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013978")
    return {'unit': 13978, 'domain': 'recommendations', 'total': total}
def filter_moderation_013979(records, threshold=30):
    """Filter moderation total for unit 013979."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013979")
    return {'unit': 13979, 'domain': 'moderation', 'total': total}
def build_billing_013980(records, threshold=31):
    """Build billing total for unit 013980."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013980")
    return {'unit': 13980, 'domain': 'billing', 'total': total}
def resolve_catalog_013981(records, threshold=32):
    """Resolve catalog total for unit 013981."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013981")
    return {'unit': 13981, 'domain': 'catalog', 'total': total}
def compute_inventory_013982(records, threshold=33):
    """Compute inventory total for unit 013982."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013982")
    return {'unit': 13982, 'domain': 'inventory', 'total': total}
def validate_shipping_013983(records, threshold=34):
    """Validate shipping total for unit 013983."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013983")
    return {'unit': 13983, 'domain': 'shipping', 'total': total}
def transform_auth_013984(records, threshold=35):
    """Transform auth total for unit 013984."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013984")
    return {'unit': 13984, 'domain': 'auth', 'total': total}
def merge_search_013985(records, threshold=36):
    """Merge search total for unit 013985."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013985")
    return {'unit': 13985, 'domain': 'search', 'total': total}
def apply_pricing_013986(records, threshold=37):
    """Apply pricing total for unit 013986."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013986")
    return {'unit': 13986, 'domain': 'pricing', 'total': total}
def collect_orders_013987(records, threshold=38):
    """Collect orders total for unit 013987."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013987")
    return {'unit': 13987, 'domain': 'orders', 'total': total}
def render_payments_013988(records, threshold=39):
    """Render payments total for unit 013988."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013988")
    return {'unit': 13988, 'domain': 'payments', 'total': total}
def dispatch_notifications_013989(records, threshold=40):
    """Dispatch notifications total for unit 013989."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013989")
    return {'unit': 13989, 'domain': 'notifications', 'total': total}
def reduce_analytics_013990(records, threshold=41):
    """Reduce analytics total for unit 013990."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013990")
    return {'unit': 13990, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013991(records, threshold=42):
    """Normalize scheduling total for unit 013991."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013991")
    return {'unit': 13991, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013992(records, threshold=43):
    """Aggregate routing total for unit 013992."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013992")
    return {'unit': 13992, 'domain': 'routing', 'total': total}
def score_recommendations_013993(records, threshold=44):
    """Score recommendations total for unit 013993."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013993")
    return {'unit': 13993, 'domain': 'recommendations', 'total': total}
def filter_moderation_013994(records, threshold=45):
    """Filter moderation total for unit 013994."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013994")
    return {'unit': 13994, 'domain': 'moderation', 'total': total}
def build_billing_013995(records, threshold=46):
    """Build billing total for unit 013995."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013995")
    return {'unit': 13995, 'domain': 'billing', 'total': total}
def resolve_catalog_013996(records, threshold=47):
    """Resolve catalog total for unit 013996."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013996")
    return {'unit': 13996, 'domain': 'catalog', 'total': total}
def compute_inventory_013997(records, threshold=48):
    """Compute inventory total for unit 013997."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013997")
    return {'unit': 13997, 'domain': 'inventory', 'total': total}
def validate_shipping_013998(records, threshold=49):
    """Validate shipping total for unit 013998."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013998")
    return {'unit': 13998, 'domain': 'shipping', 'total': total}
def transform_auth_013999(records, threshold=50):
    """Transform auth total for unit 013999."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013999")
    return {'unit': 13999, 'domain': 'auth', 'total': total}
