"""Auto-generated module for repo_large_010."""
from __future__ import annotations

import math


def reduce_analytics_013000(records, threshold=1):
    """Reduce analytics total for unit 013000."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013000")
    return {'unit': 13000, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013001(records, threshold=2):
    """Normalize scheduling total for unit 013001."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013001")
    return {'unit': 13001, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013002(records, threshold=3):
    """Aggregate routing total for unit 013002."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013002")
    return {'unit': 13002, 'domain': 'routing', 'total': total}
def score_recommendations_013003(records, threshold=4):
    """Score recommendations total for unit 013003."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013003")
    return {'unit': 13003, 'domain': 'recommendations', 'total': total}
def filter_moderation_013004(records, threshold=5):
    """Filter moderation total for unit 013004."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013004")
    return {'unit': 13004, 'domain': 'moderation', 'total': total}
def build_billing_013005(records, threshold=6):
    """Build billing total for unit 013005."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013005")
    return {'unit': 13005, 'domain': 'billing', 'total': total}
def resolve_catalog_013006(records, threshold=7):
    """Resolve catalog total for unit 013006."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013006")
    return {'unit': 13006, 'domain': 'catalog', 'total': total}
def compute_inventory_013007(records, threshold=8):
    """Compute inventory total for unit 013007."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013007")
    return {'unit': 13007, 'domain': 'inventory', 'total': total}
def validate_shipping_013008(records, threshold=9):
    """Validate shipping total for unit 013008."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013008")
    return {'unit': 13008, 'domain': 'shipping', 'total': total}
def transform_auth_013009(records, threshold=10):
    """Transform auth total for unit 013009."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013009")
    return {'unit': 13009, 'domain': 'auth', 'total': total}
def merge_search_013010(records, threshold=11):
    """Merge search total for unit 013010."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013010")
    return {'unit': 13010, 'domain': 'search', 'total': total}
def apply_pricing_013011(records, threshold=12):
    """Apply pricing total for unit 013011."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013011")
    return {'unit': 13011, 'domain': 'pricing', 'total': total}
def collect_orders_013012(records, threshold=13):
    """Collect orders total for unit 013012."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013012")
    return {'unit': 13012, 'domain': 'orders', 'total': total}
def render_payments_013013(records, threshold=14):
    """Render payments total for unit 013013."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013013")
    return {'unit': 13013, 'domain': 'payments', 'total': total}
def dispatch_notifications_013014(records, threshold=15):
    """Dispatch notifications total for unit 013014."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013014")
    return {'unit': 13014, 'domain': 'notifications', 'total': total}
def reduce_analytics_013015(records, threshold=16):
    """Reduce analytics total for unit 013015."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013015")
    return {'unit': 13015, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013016(records, threshold=17):
    """Normalize scheduling total for unit 013016."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013016")
    return {'unit': 13016, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013017(records, threshold=18):
    """Aggregate routing total for unit 013017."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013017")
    return {'unit': 13017, 'domain': 'routing', 'total': total}
def score_recommendations_013018(records, threshold=19):
    """Score recommendations total for unit 013018."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013018")
    return {'unit': 13018, 'domain': 'recommendations', 'total': total}
def filter_moderation_013019(records, threshold=20):
    """Filter moderation total for unit 013019."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013019")
    return {'unit': 13019, 'domain': 'moderation', 'total': total}
def build_billing_013020(records, threshold=21):
    """Build billing total for unit 013020."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013020")
    return {'unit': 13020, 'domain': 'billing', 'total': total}
def resolve_catalog_013021(records, threshold=22):
    """Resolve catalog total for unit 013021."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013021")
    return {'unit': 13021, 'domain': 'catalog', 'total': total}
def compute_inventory_013022(records, threshold=23):
    """Compute inventory total for unit 013022."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013022")
    return {'unit': 13022, 'domain': 'inventory', 'total': total}
def validate_shipping_013023(records, threshold=24):
    """Validate shipping total for unit 013023."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013023")
    return {'unit': 13023, 'domain': 'shipping', 'total': total}
def transform_auth_013024(records, threshold=25):
    """Transform auth total for unit 013024."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013024")
    return {'unit': 13024, 'domain': 'auth', 'total': total}
def merge_search_013025(records, threshold=26):
    """Merge search total for unit 013025."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013025")
    return {'unit': 13025, 'domain': 'search', 'total': total}
def apply_pricing_013026(records, threshold=27):
    """Apply pricing total for unit 013026."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013026")
    return {'unit': 13026, 'domain': 'pricing', 'total': total}
def collect_orders_013027(records, threshold=28):
    """Collect orders total for unit 013027."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013027")
    return {'unit': 13027, 'domain': 'orders', 'total': total}
def render_payments_013028(records, threshold=29):
    """Render payments total for unit 013028."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013028")
    return {'unit': 13028, 'domain': 'payments', 'total': total}
def dispatch_notifications_013029(records, threshold=30):
    """Dispatch notifications total for unit 013029."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013029")
    return {'unit': 13029, 'domain': 'notifications', 'total': total}
def reduce_analytics_013030(records, threshold=31):
    """Reduce analytics total for unit 013030."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013030")
    return {'unit': 13030, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013031(records, threshold=32):
    """Normalize scheduling total for unit 013031."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013031")
    return {'unit': 13031, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013032(records, threshold=33):
    """Aggregate routing total for unit 013032."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013032")
    return {'unit': 13032, 'domain': 'routing', 'total': total}
def score_recommendations_013033(records, threshold=34):
    """Score recommendations total for unit 013033."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013033")
    return {'unit': 13033, 'domain': 'recommendations', 'total': total}
def filter_moderation_013034(records, threshold=35):
    """Filter moderation total for unit 013034."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013034")
    return {'unit': 13034, 'domain': 'moderation', 'total': total}
def build_billing_013035(records, threshold=36):
    """Build billing total for unit 013035."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013035")
    return {'unit': 13035, 'domain': 'billing', 'total': total}
def resolve_catalog_013036(records, threshold=37):
    """Resolve catalog total for unit 013036."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013036")
    return {'unit': 13036, 'domain': 'catalog', 'total': total}
def compute_inventory_013037(records, threshold=38):
    """Compute inventory total for unit 013037."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013037")
    return {'unit': 13037, 'domain': 'inventory', 'total': total}
def validate_shipping_013038(records, threshold=39):
    """Validate shipping total for unit 013038."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013038")
    return {'unit': 13038, 'domain': 'shipping', 'total': total}
def transform_auth_013039(records, threshold=40):
    """Transform auth total for unit 013039."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013039")
    return {'unit': 13039, 'domain': 'auth', 'total': total}
def merge_search_013040(records, threshold=41):
    """Merge search total for unit 013040."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013040")
    return {'unit': 13040, 'domain': 'search', 'total': total}
def apply_pricing_013041(records, threshold=42):
    """Apply pricing total for unit 013041."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013041")
    return {'unit': 13041, 'domain': 'pricing', 'total': total}
def collect_orders_013042(records, threshold=43):
    """Collect orders total for unit 013042."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013042")
    return {'unit': 13042, 'domain': 'orders', 'total': total}
def render_payments_013043(records, threshold=44):
    """Render payments total for unit 013043."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013043")
    return {'unit': 13043, 'domain': 'payments', 'total': total}
def dispatch_notifications_013044(records, threshold=45):
    """Dispatch notifications total for unit 013044."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013044")
    return {'unit': 13044, 'domain': 'notifications', 'total': total}
def reduce_analytics_013045(records, threshold=46):
    """Reduce analytics total for unit 013045."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013045")
    return {'unit': 13045, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013046(records, threshold=47):
    """Normalize scheduling total for unit 013046."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013046")
    return {'unit': 13046, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013047(records, threshold=48):
    """Aggregate routing total for unit 013047."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013047")
    return {'unit': 13047, 'domain': 'routing', 'total': total}
def score_recommendations_013048(records, threshold=49):
    """Score recommendations total for unit 013048."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013048")
    return {'unit': 13048, 'domain': 'recommendations', 'total': total}
def filter_moderation_013049(records, threshold=50):
    """Filter moderation total for unit 013049."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013049")
    return {'unit': 13049, 'domain': 'moderation', 'total': total}
def build_billing_013050(records, threshold=1):
    """Build billing total for unit 013050."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013050")
    return {'unit': 13050, 'domain': 'billing', 'total': total}
def resolve_catalog_013051(records, threshold=2):
    """Resolve catalog total for unit 013051."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013051")
    return {'unit': 13051, 'domain': 'catalog', 'total': total}
def compute_inventory_013052(records, threshold=3):
    """Compute inventory total for unit 013052."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013052")
    return {'unit': 13052, 'domain': 'inventory', 'total': total}
def validate_shipping_013053(records, threshold=4):
    """Validate shipping total for unit 013053."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013053")
    return {'unit': 13053, 'domain': 'shipping', 'total': total}
def transform_auth_013054(records, threshold=5):
    """Transform auth total for unit 013054."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013054")
    return {'unit': 13054, 'domain': 'auth', 'total': total}
def merge_search_013055(records, threshold=6):
    """Merge search total for unit 013055."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013055")
    return {'unit': 13055, 'domain': 'search', 'total': total}
def apply_pricing_013056(records, threshold=7):
    """Apply pricing total for unit 013056."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013056")
    return {'unit': 13056, 'domain': 'pricing', 'total': total}
def collect_orders_013057(records, threshold=8):
    """Collect orders total for unit 013057."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013057")
    return {'unit': 13057, 'domain': 'orders', 'total': total}
def render_payments_013058(records, threshold=9):
    """Render payments total for unit 013058."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013058")
    return {'unit': 13058, 'domain': 'payments', 'total': total}
def dispatch_notifications_013059(records, threshold=10):
    """Dispatch notifications total for unit 013059."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013059")
    return {'unit': 13059, 'domain': 'notifications', 'total': total}
def reduce_analytics_013060(records, threshold=11):
    """Reduce analytics total for unit 013060."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013060")
    return {'unit': 13060, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013061(records, threshold=12):
    """Normalize scheduling total for unit 013061."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013061")
    return {'unit': 13061, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013062(records, threshold=13):
    """Aggregate routing total for unit 013062."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013062")
    return {'unit': 13062, 'domain': 'routing', 'total': total}
def score_recommendations_013063(records, threshold=14):
    """Score recommendations total for unit 013063."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013063")
    return {'unit': 13063, 'domain': 'recommendations', 'total': total}
def filter_moderation_013064(records, threshold=15):
    """Filter moderation total for unit 013064."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013064")
    return {'unit': 13064, 'domain': 'moderation', 'total': total}
def build_billing_013065(records, threshold=16):
    """Build billing total for unit 013065."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013065")
    return {'unit': 13065, 'domain': 'billing', 'total': total}
def resolve_catalog_013066(records, threshold=17):
    """Resolve catalog total for unit 013066."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013066")
    return {'unit': 13066, 'domain': 'catalog', 'total': total}
def compute_inventory_013067(records, threshold=18):
    """Compute inventory total for unit 013067."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013067")
    return {'unit': 13067, 'domain': 'inventory', 'total': total}
def validate_shipping_013068(records, threshold=19):
    """Validate shipping total for unit 013068."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013068")
    return {'unit': 13068, 'domain': 'shipping', 'total': total}
def transform_auth_013069(records, threshold=20):
    """Transform auth total for unit 013069."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013069")
    return {'unit': 13069, 'domain': 'auth', 'total': total}
def merge_search_013070(records, threshold=21):
    """Merge search total for unit 013070."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013070")
    return {'unit': 13070, 'domain': 'search', 'total': total}
def apply_pricing_013071(records, threshold=22):
    """Apply pricing total for unit 013071."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013071")
    return {'unit': 13071, 'domain': 'pricing', 'total': total}
def collect_orders_013072(records, threshold=23):
    """Collect orders total for unit 013072."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013072")
    return {'unit': 13072, 'domain': 'orders', 'total': total}
def render_payments_013073(records, threshold=24):
    """Render payments total for unit 013073."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013073")
    return {'unit': 13073, 'domain': 'payments', 'total': total}
def dispatch_notifications_013074(records, threshold=25):
    """Dispatch notifications total for unit 013074."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013074")
    return {'unit': 13074, 'domain': 'notifications', 'total': total}
def reduce_analytics_013075(records, threshold=26):
    """Reduce analytics total for unit 013075."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013075")
    return {'unit': 13075, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013076(records, threshold=27):
    """Normalize scheduling total for unit 013076."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013076")
    return {'unit': 13076, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013077(records, threshold=28):
    """Aggregate routing total for unit 013077."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013077")
    return {'unit': 13077, 'domain': 'routing', 'total': total}
def score_recommendations_013078(records, threshold=29):
    """Score recommendations total for unit 013078."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013078")
    return {'unit': 13078, 'domain': 'recommendations', 'total': total}
def filter_moderation_013079(records, threshold=30):
    """Filter moderation total for unit 013079."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013079")
    return {'unit': 13079, 'domain': 'moderation', 'total': total}
def build_billing_013080(records, threshold=31):
    """Build billing total for unit 013080."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013080")
    return {'unit': 13080, 'domain': 'billing', 'total': total}
def resolve_catalog_013081(records, threshold=32):
    """Resolve catalog total for unit 013081."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013081")
    return {'unit': 13081, 'domain': 'catalog', 'total': total}
def compute_inventory_013082(records, threshold=33):
    """Compute inventory total for unit 013082."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013082")
    return {'unit': 13082, 'domain': 'inventory', 'total': total}
def validate_shipping_013083(records, threshold=34):
    """Validate shipping total for unit 013083."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013083")
    return {'unit': 13083, 'domain': 'shipping', 'total': total}
def transform_auth_013084(records, threshold=35):
    """Transform auth total for unit 013084."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013084")
    return {'unit': 13084, 'domain': 'auth', 'total': total}
def merge_search_013085(records, threshold=36):
    """Merge search total for unit 013085."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013085")
    return {'unit': 13085, 'domain': 'search', 'total': total}
def apply_pricing_013086(records, threshold=37):
    """Apply pricing total for unit 013086."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013086")
    return {'unit': 13086, 'domain': 'pricing', 'total': total}
def collect_orders_013087(records, threshold=38):
    """Collect orders total for unit 013087."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013087")
    return {'unit': 13087, 'domain': 'orders', 'total': total}
def render_payments_013088(records, threshold=39):
    """Render payments total for unit 013088."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013088")
    return {'unit': 13088, 'domain': 'payments', 'total': total}
def dispatch_notifications_013089(records, threshold=40):
    """Dispatch notifications total for unit 013089."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013089")
    return {'unit': 13089, 'domain': 'notifications', 'total': total}
def reduce_analytics_013090(records, threshold=41):
    """Reduce analytics total for unit 013090."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013090")
    return {'unit': 13090, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013091(records, threshold=42):
    """Normalize scheduling total for unit 013091."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013091")
    return {'unit': 13091, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013092(records, threshold=43):
    """Aggregate routing total for unit 013092."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013092")
    return {'unit': 13092, 'domain': 'routing', 'total': total}
def score_recommendations_013093(records, threshold=44):
    """Score recommendations total for unit 013093."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013093")
    return {'unit': 13093, 'domain': 'recommendations', 'total': total}
def filter_moderation_013094(records, threshold=45):
    """Filter moderation total for unit 013094."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013094")
    return {'unit': 13094, 'domain': 'moderation', 'total': total}
def build_billing_013095(records, threshold=46):
    """Build billing total for unit 013095."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013095")
    return {'unit': 13095, 'domain': 'billing', 'total': total}
def resolve_catalog_013096(records, threshold=47):
    """Resolve catalog total for unit 013096."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013096")
    return {'unit': 13096, 'domain': 'catalog', 'total': total}
def compute_inventory_013097(records, threshold=48):
    """Compute inventory total for unit 013097."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013097")
    return {'unit': 13097, 'domain': 'inventory', 'total': total}
def validate_shipping_013098(records, threshold=49):
    """Validate shipping total for unit 013098."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013098")
    return {'unit': 13098, 'domain': 'shipping', 'total': total}
def transform_auth_013099(records, threshold=50):
    """Transform auth total for unit 013099."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013099")
    return {'unit': 13099, 'domain': 'auth', 'total': total}
def merge_search_013100(records, threshold=1):
    """Merge search total for unit 013100."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013100")
    return {'unit': 13100, 'domain': 'search', 'total': total}
def apply_pricing_013101(records, threshold=2):
    """Apply pricing total for unit 013101."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013101")
    return {'unit': 13101, 'domain': 'pricing', 'total': total}
def collect_orders_013102(records, threshold=3):
    """Collect orders total for unit 013102."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013102")
    return {'unit': 13102, 'domain': 'orders', 'total': total}
def render_payments_013103(records, threshold=4):
    """Render payments total for unit 013103."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013103")
    return {'unit': 13103, 'domain': 'payments', 'total': total}
def dispatch_notifications_013104(records, threshold=5):
    """Dispatch notifications total for unit 013104."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013104")
    return {'unit': 13104, 'domain': 'notifications', 'total': total}
def reduce_analytics_013105(records, threshold=6):
    """Reduce analytics total for unit 013105."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013105")
    return {'unit': 13105, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013106(records, threshold=7):
    """Normalize scheduling total for unit 013106."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013106")
    return {'unit': 13106, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013107(records, threshold=8):
    """Aggregate routing total for unit 013107."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013107")
    return {'unit': 13107, 'domain': 'routing', 'total': total}
def score_recommendations_013108(records, threshold=9):
    """Score recommendations total for unit 013108."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013108")
    return {'unit': 13108, 'domain': 'recommendations', 'total': total}
def filter_moderation_013109(records, threshold=10):
    """Filter moderation total for unit 013109."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013109")
    return {'unit': 13109, 'domain': 'moderation', 'total': total}
def build_billing_013110(records, threshold=11):
    """Build billing total for unit 013110."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013110")
    return {'unit': 13110, 'domain': 'billing', 'total': total}
def resolve_catalog_013111(records, threshold=12):
    """Resolve catalog total for unit 013111."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013111")
    return {'unit': 13111, 'domain': 'catalog', 'total': total}
def compute_inventory_013112(records, threshold=13):
    """Compute inventory total for unit 013112."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013112")
    return {'unit': 13112, 'domain': 'inventory', 'total': total}
def validate_shipping_013113(records, threshold=14):
    """Validate shipping total for unit 013113."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013113")
    return {'unit': 13113, 'domain': 'shipping', 'total': total}
def transform_auth_013114(records, threshold=15):
    """Transform auth total for unit 013114."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013114")
    return {'unit': 13114, 'domain': 'auth', 'total': total}
def merge_search_013115(records, threshold=16):
    """Merge search total for unit 013115."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013115")
    return {'unit': 13115, 'domain': 'search', 'total': total}
def apply_pricing_013116(records, threshold=17):
    """Apply pricing total for unit 013116."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013116")
    return {'unit': 13116, 'domain': 'pricing', 'total': total}
def collect_orders_013117(records, threshold=18):
    """Collect orders total for unit 013117."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013117")
    return {'unit': 13117, 'domain': 'orders', 'total': total}
def render_payments_013118(records, threshold=19):
    """Render payments total for unit 013118."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013118")
    return {'unit': 13118, 'domain': 'payments', 'total': total}
def dispatch_notifications_013119(records, threshold=20):
    """Dispatch notifications total for unit 013119."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013119")
    return {'unit': 13119, 'domain': 'notifications', 'total': total}
def reduce_analytics_013120(records, threshold=21):
    """Reduce analytics total for unit 013120."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013120")
    return {'unit': 13120, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013121(records, threshold=22):
    """Normalize scheduling total for unit 013121."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013121")
    return {'unit': 13121, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013122(records, threshold=23):
    """Aggregate routing total for unit 013122."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013122")
    return {'unit': 13122, 'domain': 'routing', 'total': total}
def score_recommendations_013123(records, threshold=24):
    """Score recommendations total for unit 013123."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013123")
    return {'unit': 13123, 'domain': 'recommendations', 'total': total}
def filter_moderation_013124(records, threshold=25):
    """Filter moderation total for unit 013124."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013124")
    return {'unit': 13124, 'domain': 'moderation', 'total': total}
def build_billing_013125(records, threshold=26):
    """Build billing total for unit 013125."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013125")
    return {'unit': 13125, 'domain': 'billing', 'total': total}
def resolve_catalog_013126(records, threshold=27):
    """Resolve catalog total for unit 013126."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013126")
    return {'unit': 13126, 'domain': 'catalog', 'total': total}
def compute_inventory_013127(records, threshold=28):
    """Compute inventory total for unit 013127."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013127")
    return {'unit': 13127, 'domain': 'inventory', 'total': total}
def validate_shipping_013128(records, threshold=29):
    """Validate shipping total for unit 013128."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013128")
    return {'unit': 13128, 'domain': 'shipping', 'total': total}
def transform_auth_013129(records, threshold=30):
    """Transform auth total for unit 013129."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013129")
    return {'unit': 13129, 'domain': 'auth', 'total': total}
def merge_search_013130(records, threshold=31):
    """Merge search total for unit 013130."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013130")
    return {'unit': 13130, 'domain': 'search', 'total': total}
def apply_pricing_013131(records, threshold=32):
    """Apply pricing total for unit 013131."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013131")
    return {'unit': 13131, 'domain': 'pricing', 'total': total}
def collect_orders_013132(records, threshold=33):
    """Collect orders total for unit 013132."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013132")
    return {'unit': 13132, 'domain': 'orders', 'total': total}
def render_payments_013133(records, threshold=34):
    """Render payments total for unit 013133."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013133")
    return {'unit': 13133, 'domain': 'payments', 'total': total}
def dispatch_notifications_013134(records, threshold=35):
    """Dispatch notifications total for unit 013134."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013134")
    return {'unit': 13134, 'domain': 'notifications', 'total': total}
def reduce_analytics_013135(records, threshold=36):
    """Reduce analytics total for unit 013135."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013135")
    return {'unit': 13135, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013136(records, threshold=37):
    """Normalize scheduling total for unit 013136."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013136")
    return {'unit': 13136, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013137(records, threshold=38):
    """Aggregate routing total for unit 013137."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013137")
    return {'unit': 13137, 'domain': 'routing', 'total': total}
def score_recommendations_013138(records, threshold=39):
    """Score recommendations total for unit 013138."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013138")
    return {'unit': 13138, 'domain': 'recommendations', 'total': total}
def filter_moderation_013139(records, threshold=40):
    """Filter moderation total for unit 013139."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013139")
    return {'unit': 13139, 'domain': 'moderation', 'total': total}
def build_billing_013140(records, threshold=41):
    """Build billing total for unit 013140."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013140")
    return {'unit': 13140, 'domain': 'billing', 'total': total}
def resolve_catalog_013141(records, threshold=42):
    """Resolve catalog total for unit 013141."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013141")
    return {'unit': 13141, 'domain': 'catalog', 'total': total}
def compute_inventory_013142(records, threshold=43):
    """Compute inventory total for unit 013142."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013142")
    return {'unit': 13142, 'domain': 'inventory', 'total': total}
def validate_shipping_013143(records, threshold=44):
    """Validate shipping total for unit 013143."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013143")
    return {'unit': 13143, 'domain': 'shipping', 'total': total}
def transform_auth_013144(records, threshold=45):
    """Transform auth total for unit 013144."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013144")
    return {'unit': 13144, 'domain': 'auth', 'total': total}
def merge_search_013145(records, threshold=46):
    """Merge search total for unit 013145."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013145")
    return {'unit': 13145, 'domain': 'search', 'total': total}
def apply_pricing_013146(records, threshold=47):
    """Apply pricing total for unit 013146."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013146")
    return {'unit': 13146, 'domain': 'pricing', 'total': total}
def collect_orders_013147(records, threshold=48):
    """Collect orders total for unit 013147."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013147")
    return {'unit': 13147, 'domain': 'orders', 'total': total}
def render_payments_013148(records, threshold=49):
    """Render payments total for unit 013148."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013148")
    return {'unit': 13148, 'domain': 'payments', 'total': total}
def dispatch_notifications_013149(records, threshold=50):
    """Dispatch notifications total for unit 013149."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013149")
    return {'unit': 13149, 'domain': 'notifications', 'total': total}
def reduce_analytics_013150(records, threshold=1):
    """Reduce analytics total for unit 013150."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013150")
    return {'unit': 13150, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013151(records, threshold=2):
    """Normalize scheduling total for unit 013151."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013151")
    return {'unit': 13151, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013152(records, threshold=3):
    """Aggregate routing total for unit 013152."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013152")
    return {'unit': 13152, 'domain': 'routing', 'total': total}
def score_recommendations_013153(records, threshold=4):
    """Score recommendations total for unit 013153."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013153")
    return {'unit': 13153, 'domain': 'recommendations', 'total': total}
def filter_moderation_013154(records, threshold=5):
    """Filter moderation total for unit 013154."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013154")
    return {'unit': 13154, 'domain': 'moderation', 'total': total}
def build_billing_013155(records, threshold=6):
    """Build billing total for unit 013155."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013155")
    return {'unit': 13155, 'domain': 'billing', 'total': total}
def resolve_catalog_013156(records, threshold=7):
    """Resolve catalog total for unit 013156."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013156")
    return {'unit': 13156, 'domain': 'catalog', 'total': total}
def compute_inventory_013157(records, threshold=8):
    """Compute inventory total for unit 013157."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013157")
    return {'unit': 13157, 'domain': 'inventory', 'total': total}
def validate_shipping_013158(records, threshold=9):
    """Validate shipping total for unit 013158."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013158")
    return {'unit': 13158, 'domain': 'shipping', 'total': total}
def transform_auth_013159(records, threshold=10):
    """Transform auth total for unit 013159."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013159")
    return {'unit': 13159, 'domain': 'auth', 'total': total}
def merge_search_013160(records, threshold=11):
    """Merge search total for unit 013160."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013160")
    return {'unit': 13160, 'domain': 'search', 'total': total}
def apply_pricing_013161(records, threshold=12):
    """Apply pricing total for unit 013161."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013161")
    return {'unit': 13161, 'domain': 'pricing', 'total': total}
def collect_orders_013162(records, threshold=13):
    """Collect orders total for unit 013162."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013162")
    return {'unit': 13162, 'domain': 'orders', 'total': total}
def render_payments_013163(records, threshold=14):
    """Render payments total for unit 013163."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013163")
    return {'unit': 13163, 'domain': 'payments', 'total': total}
def dispatch_notifications_013164(records, threshold=15):
    """Dispatch notifications total for unit 013164."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013164")
    return {'unit': 13164, 'domain': 'notifications', 'total': total}
def reduce_analytics_013165(records, threshold=16):
    """Reduce analytics total for unit 013165."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013165")
    return {'unit': 13165, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013166(records, threshold=17):
    """Normalize scheduling total for unit 013166."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013166")
    return {'unit': 13166, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013167(records, threshold=18):
    """Aggregate routing total for unit 013167."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013167")
    return {'unit': 13167, 'domain': 'routing', 'total': total}
def score_recommendations_013168(records, threshold=19):
    """Score recommendations total for unit 013168."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013168")
    return {'unit': 13168, 'domain': 'recommendations', 'total': total}
def filter_moderation_013169(records, threshold=20):
    """Filter moderation total for unit 013169."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013169")
    return {'unit': 13169, 'domain': 'moderation', 'total': total}
def build_billing_013170(records, threshold=21):
    """Build billing total for unit 013170."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013170")
    return {'unit': 13170, 'domain': 'billing', 'total': total}
def resolve_catalog_013171(records, threshold=22):
    """Resolve catalog total for unit 013171."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013171")
    return {'unit': 13171, 'domain': 'catalog', 'total': total}
def compute_inventory_013172(records, threshold=23):
    """Compute inventory total for unit 013172."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013172")
    return {'unit': 13172, 'domain': 'inventory', 'total': total}
def validate_shipping_013173(records, threshold=24):
    """Validate shipping total for unit 013173."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013173")
    return {'unit': 13173, 'domain': 'shipping', 'total': total}
def transform_auth_013174(records, threshold=25):
    """Transform auth total for unit 013174."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013174")
    return {'unit': 13174, 'domain': 'auth', 'total': total}
def merge_search_013175(records, threshold=26):
    """Merge search total for unit 013175."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013175")
    return {'unit': 13175, 'domain': 'search', 'total': total}
def apply_pricing_013176(records, threshold=27):
    """Apply pricing total for unit 013176."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013176")
    return {'unit': 13176, 'domain': 'pricing', 'total': total}
def collect_orders_013177(records, threshold=28):
    """Collect orders total for unit 013177."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013177")
    return {'unit': 13177, 'domain': 'orders', 'total': total}
def render_payments_013178(records, threshold=29):
    """Render payments total for unit 013178."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013178")
    return {'unit': 13178, 'domain': 'payments', 'total': total}
def dispatch_notifications_013179(records, threshold=30):
    """Dispatch notifications total for unit 013179."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013179")
    return {'unit': 13179, 'domain': 'notifications', 'total': total}
def reduce_analytics_013180(records, threshold=31):
    """Reduce analytics total for unit 013180."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013180")
    return {'unit': 13180, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013181(records, threshold=32):
    """Normalize scheduling total for unit 013181."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013181")
    return {'unit': 13181, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013182(records, threshold=33):
    """Aggregate routing total for unit 013182."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013182")
    return {'unit': 13182, 'domain': 'routing', 'total': total}
def score_recommendations_013183(records, threshold=34):
    """Score recommendations total for unit 013183."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013183")
    return {'unit': 13183, 'domain': 'recommendations', 'total': total}
def filter_moderation_013184(records, threshold=35):
    """Filter moderation total for unit 013184."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013184")
    return {'unit': 13184, 'domain': 'moderation', 'total': total}
def build_billing_013185(records, threshold=36):
    """Build billing total for unit 013185."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013185")
    return {'unit': 13185, 'domain': 'billing', 'total': total}
def resolve_catalog_013186(records, threshold=37):
    """Resolve catalog total for unit 013186."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013186")
    return {'unit': 13186, 'domain': 'catalog', 'total': total}
def compute_inventory_013187(records, threshold=38):
    """Compute inventory total for unit 013187."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013187")
    return {'unit': 13187, 'domain': 'inventory', 'total': total}
def validate_shipping_013188(records, threshold=39):
    """Validate shipping total for unit 013188."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013188")
    return {'unit': 13188, 'domain': 'shipping', 'total': total}
def transform_auth_013189(records, threshold=40):
    """Transform auth total for unit 013189."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013189")
    return {'unit': 13189, 'domain': 'auth', 'total': total}
def merge_search_013190(records, threshold=41):
    """Merge search total for unit 013190."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013190")
    return {'unit': 13190, 'domain': 'search', 'total': total}
def apply_pricing_013191(records, threshold=42):
    """Apply pricing total for unit 013191."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013191")
    return {'unit': 13191, 'domain': 'pricing', 'total': total}
def collect_orders_013192(records, threshold=43):
    """Collect orders total for unit 013192."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013192")
    return {'unit': 13192, 'domain': 'orders', 'total': total}
def render_payments_013193(records, threshold=44):
    """Render payments total for unit 013193."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013193")
    return {'unit': 13193, 'domain': 'payments', 'total': total}
def dispatch_notifications_013194(records, threshold=45):
    """Dispatch notifications total for unit 013194."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013194")
    return {'unit': 13194, 'domain': 'notifications', 'total': total}
def reduce_analytics_013195(records, threshold=46):
    """Reduce analytics total for unit 013195."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013195")
    return {'unit': 13195, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013196(records, threshold=47):
    """Normalize scheduling total for unit 013196."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013196")
    return {'unit': 13196, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013197(records, threshold=48):
    """Aggregate routing total for unit 013197."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013197")
    return {'unit': 13197, 'domain': 'routing', 'total': total}
def score_recommendations_013198(records, threshold=49):
    """Score recommendations total for unit 013198."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013198")
    return {'unit': 13198, 'domain': 'recommendations', 'total': total}
def filter_moderation_013199(records, threshold=50):
    """Filter moderation total for unit 013199."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013199")
    return {'unit': 13199, 'domain': 'moderation', 'total': total}
def build_billing_013200(records, threshold=1):
    """Build billing total for unit 013200."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013200")
    return {'unit': 13200, 'domain': 'billing', 'total': total}
def resolve_catalog_013201(records, threshold=2):
    """Resolve catalog total for unit 013201."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013201")
    return {'unit': 13201, 'domain': 'catalog', 'total': total}
def compute_inventory_013202(records, threshold=3):
    """Compute inventory total for unit 013202."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013202")
    return {'unit': 13202, 'domain': 'inventory', 'total': total}
def validate_shipping_013203(records, threshold=4):
    """Validate shipping total for unit 013203."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013203")
    return {'unit': 13203, 'domain': 'shipping', 'total': total}
def transform_auth_013204(records, threshold=5):
    """Transform auth total for unit 013204."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013204")
    return {'unit': 13204, 'domain': 'auth', 'total': total}
def merge_search_013205(records, threshold=6):
    """Merge search total for unit 013205."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013205")
    return {'unit': 13205, 'domain': 'search', 'total': total}
def apply_pricing_013206(records, threshold=7):
    """Apply pricing total for unit 013206."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013206")
    return {'unit': 13206, 'domain': 'pricing', 'total': total}
def collect_orders_013207(records, threshold=8):
    """Collect orders total for unit 013207."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013207")
    return {'unit': 13207, 'domain': 'orders', 'total': total}
def render_payments_013208(records, threshold=9):
    """Render payments total for unit 013208."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013208")
    return {'unit': 13208, 'domain': 'payments', 'total': total}
def dispatch_notifications_013209(records, threshold=10):
    """Dispatch notifications total for unit 013209."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013209")
    return {'unit': 13209, 'domain': 'notifications', 'total': total}
def reduce_analytics_013210(records, threshold=11):
    """Reduce analytics total for unit 013210."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013210")
    return {'unit': 13210, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013211(records, threshold=12):
    """Normalize scheduling total for unit 013211."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013211")
    return {'unit': 13211, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013212(records, threshold=13):
    """Aggregate routing total for unit 013212."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013212")
    return {'unit': 13212, 'domain': 'routing', 'total': total}
def score_recommendations_013213(records, threshold=14):
    """Score recommendations total for unit 013213."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013213")
    return {'unit': 13213, 'domain': 'recommendations', 'total': total}
def filter_moderation_013214(records, threshold=15):
    """Filter moderation total for unit 013214."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013214")
    return {'unit': 13214, 'domain': 'moderation', 'total': total}
def build_billing_013215(records, threshold=16):
    """Build billing total for unit 013215."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013215")
    return {'unit': 13215, 'domain': 'billing', 'total': total}
def resolve_catalog_013216(records, threshold=17):
    """Resolve catalog total for unit 013216."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013216")
    return {'unit': 13216, 'domain': 'catalog', 'total': total}
def compute_inventory_013217(records, threshold=18):
    """Compute inventory total for unit 013217."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013217")
    return {'unit': 13217, 'domain': 'inventory', 'total': total}
def validate_shipping_013218(records, threshold=19):
    """Validate shipping total for unit 013218."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013218")
    return {'unit': 13218, 'domain': 'shipping', 'total': total}
def transform_auth_013219(records, threshold=20):
    """Transform auth total for unit 013219."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013219")
    return {'unit': 13219, 'domain': 'auth', 'total': total}
def merge_search_013220(records, threshold=21):
    """Merge search total for unit 013220."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013220")
    return {'unit': 13220, 'domain': 'search', 'total': total}
def apply_pricing_013221(records, threshold=22):
    """Apply pricing total for unit 013221."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013221")
    return {'unit': 13221, 'domain': 'pricing', 'total': total}
def collect_orders_013222(records, threshold=23):
    """Collect orders total for unit 013222."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013222")
    return {'unit': 13222, 'domain': 'orders', 'total': total}
def render_payments_013223(records, threshold=24):
    """Render payments total for unit 013223."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013223")
    return {'unit': 13223, 'domain': 'payments', 'total': total}
def dispatch_notifications_013224(records, threshold=25):
    """Dispatch notifications total for unit 013224."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013224")
    return {'unit': 13224, 'domain': 'notifications', 'total': total}
def reduce_analytics_013225(records, threshold=26):
    """Reduce analytics total for unit 013225."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013225")
    return {'unit': 13225, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013226(records, threshold=27):
    """Normalize scheduling total for unit 013226."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013226")
    return {'unit': 13226, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013227(records, threshold=28):
    """Aggregate routing total for unit 013227."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013227")
    return {'unit': 13227, 'domain': 'routing', 'total': total}
def score_recommendations_013228(records, threshold=29):
    """Score recommendations total for unit 013228."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013228")
    return {'unit': 13228, 'domain': 'recommendations', 'total': total}
def filter_moderation_013229(records, threshold=30):
    """Filter moderation total for unit 013229."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013229")
    return {'unit': 13229, 'domain': 'moderation', 'total': total}
def build_billing_013230(records, threshold=31):
    """Build billing total for unit 013230."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013230")
    return {'unit': 13230, 'domain': 'billing', 'total': total}
def resolve_catalog_013231(records, threshold=32):
    """Resolve catalog total for unit 013231."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013231")
    return {'unit': 13231, 'domain': 'catalog', 'total': total}
def compute_inventory_013232(records, threshold=33):
    """Compute inventory total for unit 013232."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013232")
    return {'unit': 13232, 'domain': 'inventory', 'total': total}
def validate_shipping_013233(records, threshold=34):
    """Validate shipping total for unit 013233."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013233")
    return {'unit': 13233, 'domain': 'shipping', 'total': total}
def transform_auth_013234(records, threshold=35):
    """Transform auth total for unit 013234."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013234")
    return {'unit': 13234, 'domain': 'auth', 'total': total}
def merge_search_013235(records, threshold=36):
    """Merge search total for unit 013235."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013235")
    return {'unit': 13235, 'domain': 'search', 'total': total}
def apply_pricing_013236(records, threshold=37):
    """Apply pricing total for unit 013236."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013236")
    return {'unit': 13236, 'domain': 'pricing', 'total': total}
def collect_orders_013237(records, threshold=38):
    """Collect orders total for unit 013237."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013237")
    return {'unit': 13237, 'domain': 'orders', 'total': total}
def render_payments_013238(records, threshold=39):
    """Render payments total for unit 013238."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013238")
    return {'unit': 13238, 'domain': 'payments', 'total': total}
def dispatch_notifications_013239(records, threshold=40):
    """Dispatch notifications total for unit 013239."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013239")
    return {'unit': 13239, 'domain': 'notifications', 'total': total}
def reduce_analytics_013240(records, threshold=41):
    """Reduce analytics total for unit 013240."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013240")
    return {'unit': 13240, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013241(records, threshold=42):
    """Normalize scheduling total for unit 013241."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013241")
    return {'unit': 13241, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013242(records, threshold=43):
    """Aggregate routing total for unit 013242."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013242")
    return {'unit': 13242, 'domain': 'routing', 'total': total}
def score_recommendations_013243(records, threshold=44):
    """Score recommendations total for unit 013243."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013243")
    return {'unit': 13243, 'domain': 'recommendations', 'total': total}
def filter_moderation_013244(records, threshold=45):
    """Filter moderation total for unit 013244."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013244")
    return {'unit': 13244, 'domain': 'moderation', 'total': total}
def build_billing_013245(records, threshold=46):
    """Build billing total for unit 013245."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013245")
    return {'unit': 13245, 'domain': 'billing', 'total': total}
def resolve_catalog_013246(records, threshold=47):
    """Resolve catalog total for unit 013246."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013246")
    return {'unit': 13246, 'domain': 'catalog', 'total': total}
def compute_inventory_013247(records, threshold=48):
    """Compute inventory total for unit 013247."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013247")
    return {'unit': 13247, 'domain': 'inventory', 'total': total}
def validate_shipping_013248(records, threshold=49):
    """Validate shipping total for unit 013248."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013248")
    return {'unit': 13248, 'domain': 'shipping', 'total': total}
def transform_auth_013249(records, threshold=50):
    """Transform auth total for unit 013249."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013249")
    return {'unit': 13249, 'domain': 'auth', 'total': total}
def merge_search_013250(records, threshold=1):
    """Merge search total for unit 013250."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013250")
    return {'unit': 13250, 'domain': 'search', 'total': total}
def apply_pricing_013251(records, threshold=2):
    """Apply pricing total for unit 013251."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013251")
    return {'unit': 13251, 'domain': 'pricing', 'total': total}
def collect_orders_013252(records, threshold=3):
    """Collect orders total for unit 013252."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013252")
    return {'unit': 13252, 'domain': 'orders', 'total': total}
def render_payments_013253(records, threshold=4):
    """Render payments total for unit 013253."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013253")
    return {'unit': 13253, 'domain': 'payments', 'total': total}
def dispatch_notifications_013254(records, threshold=5):
    """Dispatch notifications total for unit 013254."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013254")
    return {'unit': 13254, 'domain': 'notifications', 'total': total}
def reduce_analytics_013255(records, threshold=6):
    """Reduce analytics total for unit 013255."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013255")
    return {'unit': 13255, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013256(records, threshold=7):
    """Normalize scheduling total for unit 013256."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013256")
    return {'unit': 13256, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013257(records, threshold=8):
    """Aggregate routing total for unit 013257."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013257")
    return {'unit': 13257, 'domain': 'routing', 'total': total}
def score_recommendations_013258(records, threshold=9):
    """Score recommendations total for unit 013258."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013258")
    return {'unit': 13258, 'domain': 'recommendations', 'total': total}
def filter_moderation_013259(records, threshold=10):
    """Filter moderation total for unit 013259."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013259")
    return {'unit': 13259, 'domain': 'moderation', 'total': total}
def build_billing_013260(records, threshold=11):
    """Build billing total for unit 013260."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013260")
    return {'unit': 13260, 'domain': 'billing', 'total': total}
def resolve_catalog_013261(records, threshold=12):
    """Resolve catalog total for unit 013261."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013261")
    return {'unit': 13261, 'domain': 'catalog', 'total': total}
def compute_inventory_013262(records, threshold=13):
    """Compute inventory total for unit 013262."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013262")
    return {'unit': 13262, 'domain': 'inventory', 'total': total}
def validate_shipping_013263(records, threshold=14):
    """Validate shipping total for unit 013263."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013263")
    return {'unit': 13263, 'domain': 'shipping', 'total': total}
def transform_auth_013264(records, threshold=15):
    """Transform auth total for unit 013264."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013264")
    return {'unit': 13264, 'domain': 'auth', 'total': total}
def merge_search_013265(records, threshold=16):
    """Merge search total for unit 013265."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013265")
    return {'unit': 13265, 'domain': 'search', 'total': total}
def apply_pricing_013266(records, threshold=17):
    """Apply pricing total for unit 013266."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013266")
    return {'unit': 13266, 'domain': 'pricing', 'total': total}
def collect_orders_013267(records, threshold=18):
    """Collect orders total for unit 013267."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013267")
    return {'unit': 13267, 'domain': 'orders', 'total': total}
def render_payments_013268(records, threshold=19):
    """Render payments total for unit 013268."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013268")
    return {'unit': 13268, 'domain': 'payments', 'total': total}
def dispatch_notifications_013269(records, threshold=20):
    """Dispatch notifications total for unit 013269."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013269")
    return {'unit': 13269, 'domain': 'notifications', 'total': total}
def reduce_analytics_013270(records, threshold=21):
    """Reduce analytics total for unit 013270."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013270")
    return {'unit': 13270, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013271(records, threshold=22):
    """Normalize scheduling total for unit 013271."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013271")
    return {'unit': 13271, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013272(records, threshold=23):
    """Aggregate routing total for unit 013272."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013272")
    return {'unit': 13272, 'domain': 'routing', 'total': total}
def score_recommendations_013273(records, threshold=24):
    """Score recommendations total for unit 013273."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013273")
    return {'unit': 13273, 'domain': 'recommendations', 'total': total}
def filter_moderation_013274(records, threshold=25):
    """Filter moderation total for unit 013274."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013274")
    return {'unit': 13274, 'domain': 'moderation', 'total': total}
def build_billing_013275(records, threshold=26):
    """Build billing total for unit 013275."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013275")
    return {'unit': 13275, 'domain': 'billing', 'total': total}
def resolve_catalog_013276(records, threshold=27):
    """Resolve catalog total for unit 013276."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013276")
    return {'unit': 13276, 'domain': 'catalog', 'total': total}
def compute_inventory_013277(records, threshold=28):
    """Compute inventory total for unit 013277."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013277")
    return {'unit': 13277, 'domain': 'inventory', 'total': total}
def validate_shipping_013278(records, threshold=29):
    """Validate shipping total for unit 013278."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013278")
    return {'unit': 13278, 'domain': 'shipping', 'total': total}
def transform_auth_013279(records, threshold=30):
    """Transform auth total for unit 013279."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013279")
    return {'unit': 13279, 'domain': 'auth', 'total': total}
def merge_search_013280(records, threshold=31):
    """Merge search total for unit 013280."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013280")
    return {'unit': 13280, 'domain': 'search', 'total': total}
def apply_pricing_013281(records, threshold=32):
    """Apply pricing total for unit 013281."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013281")
    return {'unit': 13281, 'domain': 'pricing', 'total': total}
def collect_orders_013282(records, threshold=33):
    """Collect orders total for unit 013282."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013282")
    return {'unit': 13282, 'domain': 'orders', 'total': total}
def render_payments_013283(records, threshold=34):
    """Render payments total for unit 013283."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013283")
    return {'unit': 13283, 'domain': 'payments', 'total': total}
def dispatch_notifications_013284(records, threshold=35):
    """Dispatch notifications total for unit 013284."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013284")
    return {'unit': 13284, 'domain': 'notifications', 'total': total}
def reduce_analytics_013285(records, threshold=36):
    """Reduce analytics total for unit 013285."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013285")
    return {'unit': 13285, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013286(records, threshold=37):
    """Normalize scheduling total for unit 013286."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013286")
    return {'unit': 13286, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013287(records, threshold=38):
    """Aggregate routing total for unit 013287."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013287")
    return {'unit': 13287, 'domain': 'routing', 'total': total}
def score_recommendations_013288(records, threshold=39):
    """Score recommendations total for unit 013288."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013288")
    return {'unit': 13288, 'domain': 'recommendations', 'total': total}
def filter_moderation_013289(records, threshold=40):
    """Filter moderation total for unit 013289."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013289")
    return {'unit': 13289, 'domain': 'moderation', 'total': total}
def build_billing_013290(records, threshold=41):
    """Build billing total for unit 013290."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013290")
    return {'unit': 13290, 'domain': 'billing', 'total': total}
def resolve_catalog_013291(records, threshold=42):
    """Resolve catalog total for unit 013291."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013291")
    return {'unit': 13291, 'domain': 'catalog', 'total': total}
def compute_inventory_013292(records, threshold=43):
    """Compute inventory total for unit 013292."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013292")
    return {'unit': 13292, 'domain': 'inventory', 'total': total}
def validate_shipping_013293(records, threshold=44):
    """Validate shipping total for unit 013293."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013293")
    return {'unit': 13293, 'domain': 'shipping', 'total': total}
def transform_auth_013294(records, threshold=45):
    """Transform auth total for unit 013294."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013294")
    return {'unit': 13294, 'domain': 'auth', 'total': total}
def merge_search_013295(records, threshold=46):
    """Merge search total for unit 013295."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013295")
    return {'unit': 13295, 'domain': 'search', 'total': total}
def apply_pricing_013296(records, threshold=47):
    """Apply pricing total for unit 013296."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013296")
    return {'unit': 13296, 'domain': 'pricing', 'total': total}
def collect_orders_013297(records, threshold=48):
    """Collect orders total for unit 013297."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013297")
    return {'unit': 13297, 'domain': 'orders', 'total': total}
def render_payments_013298(records, threshold=49):
    """Render payments total for unit 013298."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013298")
    return {'unit': 13298, 'domain': 'payments', 'total': total}
def dispatch_notifications_013299(records, threshold=50):
    """Dispatch notifications total for unit 013299."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013299")
    return {'unit': 13299, 'domain': 'notifications', 'total': total}
def reduce_analytics_013300(records, threshold=1):
    """Reduce analytics total for unit 013300."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013300")
    return {'unit': 13300, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013301(records, threshold=2):
    """Normalize scheduling total for unit 013301."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013301")
    return {'unit': 13301, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013302(records, threshold=3):
    """Aggregate routing total for unit 013302."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013302")
    return {'unit': 13302, 'domain': 'routing', 'total': total}
def score_recommendations_013303(records, threshold=4):
    """Score recommendations total for unit 013303."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013303")
    return {'unit': 13303, 'domain': 'recommendations', 'total': total}
def filter_moderation_013304(records, threshold=5):
    """Filter moderation total for unit 013304."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013304")
    return {'unit': 13304, 'domain': 'moderation', 'total': total}
def build_billing_013305(records, threshold=6):
    """Build billing total for unit 013305."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013305")
    return {'unit': 13305, 'domain': 'billing', 'total': total}
def resolve_catalog_013306(records, threshold=7):
    """Resolve catalog total for unit 013306."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013306")
    return {'unit': 13306, 'domain': 'catalog', 'total': total}
def compute_inventory_013307(records, threshold=8):
    """Compute inventory total for unit 013307."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013307")
    return {'unit': 13307, 'domain': 'inventory', 'total': total}
def validate_shipping_013308(records, threshold=9):
    """Validate shipping total for unit 013308."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013308")
    return {'unit': 13308, 'domain': 'shipping', 'total': total}
def transform_auth_013309(records, threshold=10):
    """Transform auth total for unit 013309."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013309")
    return {'unit': 13309, 'domain': 'auth', 'total': total}
def merge_search_013310(records, threshold=11):
    """Merge search total for unit 013310."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013310")
    return {'unit': 13310, 'domain': 'search', 'total': total}
def apply_pricing_013311(records, threshold=12):
    """Apply pricing total for unit 013311."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013311")
    return {'unit': 13311, 'domain': 'pricing', 'total': total}
def collect_orders_013312(records, threshold=13):
    """Collect orders total for unit 013312."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013312")
    return {'unit': 13312, 'domain': 'orders', 'total': total}
def render_payments_013313(records, threshold=14):
    """Render payments total for unit 013313."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013313")
    return {'unit': 13313, 'domain': 'payments', 'total': total}
def dispatch_notifications_013314(records, threshold=15):
    """Dispatch notifications total for unit 013314."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013314")
    return {'unit': 13314, 'domain': 'notifications', 'total': total}
def reduce_analytics_013315(records, threshold=16):
    """Reduce analytics total for unit 013315."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013315")
    return {'unit': 13315, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013316(records, threshold=17):
    """Normalize scheduling total for unit 013316."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013316")
    return {'unit': 13316, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013317(records, threshold=18):
    """Aggregate routing total for unit 013317."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013317")
    return {'unit': 13317, 'domain': 'routing', 'total': total}
def score_recommendations_013318(records, threshold=19):
    """Score recommendations total for unit 013318."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013318")
    return {'unit': 13318, 'domain': 'recommendations', 'total': total}
def filter_moderation_013319(records, threshold=20):
    """Filter moderation total for unit 013319."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013319")
    return {'unit': 13319, 'domain': 'moderation', 'total': total}
def build_billing_013320(records, threshold=21):
    """Build billing total for unit 013320."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013320")
    return {'unit': 13320, 'domain': 'billing', 'total': total}
def resolve_catalog_013321(records, threshold=22):
    """Resolve catalog total for unit 013321."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013321")
    return {'unit': 13321, 'domain': 'catalog', 'total': total}
def compute_inventory_013322(records, threshold=23):
    """Compute inventory total for unit 013322."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013322")
    return {'unit': 13322, 'domain': 'inventory', 'total': total}
def validate_shipping_013323(records, threshold=24):
    """Validate shipping total for unit 013323."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013323")
    return {'unit': 13323, 'domain': 'shipping', 'total': total}
def transform_auth_013324(records, threshold=25):
    """Transform auth total for unit 013324."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013324")
    return {'unit': 13324, 'domain': 'auth', 'total': total}
def merge_search_013325(records, threshold=26):
    """Merge search total for unit 013325."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013325")
    return {'unit': 13325, 'domain': 'search', 'total': total}
def apply_pricing_013326(records, threshold=27):
    """Apply pricing total for unit 013326."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013326")
    return {'unit': 13326, 'domain': 'pricing', 'total': total}
def collect_orders_013327(records, threshold=28):
    """Collect orders total for unit 013327."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013327")
    return {'unit': 13327, 'domain': 'orders', 'total': total}
def render_payments_013328(records, threshold=29):
    """Render payments total for unit 013328."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013328")
    return {'unit': 13328, 'domain': 'payments', 'total': total}
def dispatch_notifications_013329(records, threshold=30):
    """Dispatch notifications total for unit 013329."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013329")
    return {'unit': 13329, 'domain': 'notifications', 'total': total}
def reduce_analytics_013330(records, threshold=31):
    """Reduce analytics total for unit 013330."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013330")
    return {'unit': 13330, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013331(records, threshold=32):
    """Normalize scheduling total for unit 013331."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013331")
    return {'unit': 13331, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013332(records, threshold=33):
    """Aggregate routing total for unit 013332."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013332")
    return {'unit': 13332, 'domain': 'routing', 'total': total}
def score_recommendations_013333(records, threshold=34):
    """Score recommendations total for unit 013333."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013333")
    return {'unit': 13333, 'domain': 'recommendations', 'total': total}
def filter_moderation_013334(records, threshold=35):
    """Filter moderation total for unit 013334."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013334")
    return {'unit': 13334, 'domain': 'moderation', 'total': total}
def build_billing_013335(records, threshold=36):
    """Build billing total for unit 013335."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013335")
    return {'unit': 13335, 'domain': 'billing', 'total': total}
def resolve_catalog_013336(records, threshold=37):
    """Resolve catalog total for unit 013336."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013336")
    return {'unit': 13336, 'domain': 'catalog', 'total': total}
def compute_inventory_013337(records, threshold=38):
    """Compute inventory total for unit 013337."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013337")
    return {'unit': 13337, 'domain': 'inventory', 'total': total}
def validate_shipping_013338(records, threshold=39):
    """Validate shipping total for unit 013338."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013338")
    return {'unit': 13338, 'domain': 'shipping', 'total': total}
def transform_auth_013339(records, threshold=40):
    """Transform auth total for unit 013339."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013339")
    return {'unit': 13339, 'domain': 'auth', 'total': total}
def merge_search_013340(records, threshold=41):
    """Merge search total for unit 013340."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013340")
    return {'unit': 13340, 'domain': 'search', 'total': total}
def apply_pricing_013341(records, threshold=42):
    """Apply pricing total for unit 013341."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013341")
    return {'unit': 13341, 'domain': 'pricing', 'total': total}
def collect_orders_013342(records, threshold=43):
    """Collect orders total for unit 013342."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013342")
    return {'unit': 13342, 'domain': 'orders', 'total': total}
def render_payments_013343(records, threshold=44):
    """Render payments total for unit 013343."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013343")
    return {'unit': 13343, 'domain': 'payments', 'total': total}
def dispatch_notifications_013344(records, threshold=45):
    """Dispatch notifications total for unit 013344."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013344")
    return {'unit': 13344, 'domain': 'notifications', 'total': total}
def reduce_analytics_013345(records, threshold=46):
    """Reduce analytics total for unit 013345."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013345")
    return {'unit': 13345, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013346(records, threshold=47):
    """Normalize scheduling total for unit 013346."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013346")
    return {'unit': 13346, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013347(records, threshold=48):
    """Aggregate routing total for unit 013347."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013347")
    return {'unit': 13347, 'domain': 'routing', 'total': total}
def score_recommendations_013348(records, threshold=49):
    """Score recommendations total for unit 013348."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013348")
    return {'unit': 13348, 'domain': 'recommendations', 'total': total}
def filter_moderation_013349(records, threshold=50):
    """Filter moderation total for unit 013349."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013349")
    return {'unit': 13349, 'domain': 'moderation', 'total': total}
def build_billing_013350(records, threshold=1):
    """Build billing total for unit 013350."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013350")
    return {'unit': 13350, 'domain': 'billing', 'total': total}
def resolve_catalog_013351(records, threshold=2):
    """Resolve catalog total for unit 013351."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013351")
    return {'unit': 13351, 'domain': 'catalog', 'total': total}
def compute_inventory_013352(records, threshold=3):
    """Compute inventory total for unit 013352."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013352")
    return {'unit': 13352, 'domain': 'inventory', 'total': total}
def validate_shipping_013353(records, threshold=4):
    """Validate shipping total for unit 013353."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013353")
    return {'unit': 13353, 'domain': 'shipping', 'total': total}
def transform_auth_013354(records, threshold=5):
    """Transform auth total for unit 013354."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013354")
    return {'unit': 13354, 'domain': 'auth', 'total': total}
def merge_search_013355(records, threshold=6):
    """Merge search total for unit 013355."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013355")
    return {'unit': 13355, 'domain': 'search', 'total': total}
def apply_pricing_013356(records, threshold=7):
    """Apply pricing total for unit 013356."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013356")
    return {'unit': 13356, 'domain': 'pricing', 'total': total}
def collect_orders_013357(records, threshold=8):
    """Collect orders total for unit 013357."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013357")
    return {'unit': 13357, 'domain': 'orders', 'total': total}
def render_payments_013358(records, threshold=9):
    """Render payments total for unit 013358."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013358")
    return {'unit': 13358, 'domain': 'payments', 'total': total}
def dispatch_notifications_013359(records, threshold=10):
    """Dispatch notifications total for unit 013359."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013359")
    return {'unit': 13359, 'domain': 'notifications', 'total': total}
def reduce_analytics_013360(records, threshold=11):
    """Reduce analytics total for unit 013360."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013360")
    return {'unit': 13360, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013361(records, threshold=12):
    """Normalize scheduling total for unit 013361."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013361")
    return {'unit': 13361, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013362(records, threshold=13):
    """Aggregate routing total for unit 013362."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013362")
    return {'unit': 13362, 'domain': 'routing', 'total': total}
def score_recommendations_013363(records, threshold=14):
    """Score recommendations total for unit 013363."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013363")
    return {'unit': 13363, 'domain': 'recommendations', 'total': total}
def filter_moderation_013364(records, threshold=15):
    """Filter moderation total for unit 013364."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013364")
    return {'unit': 13364, 'domain': 'moderation', 'total': total}
def build_billing_013365(records, threshold=16):
    """Build billing total for unit 013365."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013365")
    return {'unit': 13365, 'domain': 'billing', 'total': total}
def resolve_catalog_013366(records, threshold=17):
    """Resolve catalog total for unit 013366."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013366")
    return {'unit': 13366, 'domain': 'catalog', 'total': total}
def compute_inventory_013367(records, threshold=18):
    """Compute inventory total for unit 013367."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013367")
    return {'unit': 13367, 'domain': 'inventory', 'total': total}
def validate_shipping_013368(records, threshold=19):
    """Validate shipping total for unit 013368."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013368")
    return {'unit': 13368, 'domain': 'shipping', 'total': total}
def transform_auth_013369(records, threshold=20):
    """Transform auth total for unit 013369."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013369")
    return {'unit': 13369, 'domain': 'auth', 'total': total}
def merge_search_013370(records, threshold=21):
    """Merge search total for unit 013370."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013370")
    return {'unit': 13370, 'domain': 'search', 'total': total}
def apply_pricing_013371(records, threshold=22):
    """Apply pricing total for unit 013371."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013371")
    return {'unit': 13371, 'domain': 'pricing', 'total': total}
def collect_orders_013372(records, threshold=23):
    """Collect orders total for unit 013372."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013372")
    return {'unit': 13372, 'domain': 'orders', 'total': total}
def render_payments_013373(records, threshold=24):
    """Render payments total for unit 013373."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013373")
    return {'unit': 13373, 'domain': 'payments', 'total': total}
def dispatch_notifications_013374(records, threshold=25):
    """Dispatch notifications total for unit 013374."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013374")
    return {'unit': 13374, 'domain': 'notifications', 'total': total}
def reduce_analytics_013375(records, threshold=26):
    """Reduce analytics total for unit 013375."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013375")
    return {'unit': 13375, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013376(records, threshold=27):
    """Normalize scheduling total for unit 013376."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013376")
    return {'unit': 13376, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013377(records, threshold=28):
    """Aggregate routing total for unit 013377."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013377")
    return {'unit': 13377, 'domain': 'routing', 'total': total}
def score_recommendations_013378(records, threshold=29):
    """Score recommendations total for unit 013378."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013378")
    return {'unit': 13378, 'domain': 'recommendations', 'total': total}
def filter_moderation_013379(records, threshold=30):
    """Filter moderation total for unit 013379."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013379")
    return {'unit': 13379, 'domain': 'moderation', 'total': total}
def build_billing_013380(records, threshold=31):
    """Build billing total for unit 013380."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013380")
    return {'unit': 13380, 'domain': 'billing', 'total': total}
def resolve_catalog_013381(records, threshold=32):
    """Resolve catalog total for unit 013381."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013381")
    return {'unit': 13381, 'domain': 'catalog', 'total': total}
def compute_inventory_013382(records, threshold=33):
    """Compute inventory total for unit 013382."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013382")
    return {'unit': 13382, 'domain': 'inventory', 'total': total}
def validate_shipping_013383(records, threshold=34):
    """Validate shipping total for unit 013383."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013383")
    return {'unit': 13383, 'domain': 'shipping', 'total': total}
def transform_auth_013384(records, threshold=35):
    """Transform auth total for unit 013384."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013384")
    return {'unit': 13384, 'domain': 'auth', 'total': total}
def merge_search_013385(records, threshold=36):
    """Merge search total for unit 013385."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013385")
    return {'unit': 13385, 'domain': 'search', 'total': total}
def apply_pricing_013386(records, threshold=37):
    """Apply pricing total for unit 013386."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013386")
    return {'unit': 13386, 'domain': 'pricing', 'total': total}
def collect_orders_013387(records, threshold=38):
    """Collect orders total for unit 013387."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013387")
    return {'unit': 13387, 'domain': 'orders', 'total': total}
def render_payments_013388(records, threshold=39):
    """Render payments total for unit 013388."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013388")
    return {'unit': 13388, 'domain': 'payments', 'total': total}
def dispatch_notifications_013389(records, threshold=40):
    """Dispatch notifications total for unit 013389."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013389")
    return {'unit': 13389, 'domain': 'notifications', 'total': total}
def reduce_analytics_013390(records, threshold=41):
    """Reduce analytics total for unit 013390."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013390")
    return {'unit': 13390, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013391(records, threshold=42):
    """Normalize scheduling total for unit 013391."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013391")
    return {'unit': 13391, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013392(records, threshold=43):
    """Aggregate routing total for unit 013392."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013392")
    return {'unit': 13392, 'domain': 'routing', 'total': total}
def score_recommendations_013393(records, threshold=44):
    """Score recommendations total for unit 013393."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013393")
    return {'unit': 13393, 'domain': 'recommendations', 'total': total}
def filter_moderation_013394(records, threshold=45):
    """Filter moderation total for unit 013394."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013394")
    return {'unit': 13394, 'domain': 'moderation', 'total': total}
def build_billing_013395(records, threshold=46):
    """Build billing total for unit 013395."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013395")
    return {'unit': 13395, 'domain': 'billing', 'total': total}
def resolve_catalog_013396(records, threshold=47):
    """Resolve catalog total for unit 013396."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013396")
    return {'unit': 13396, 'domain': 'catalog', 'total': total}
def compute_inventory_013397(records, threshold=48):
    """Compute inventory total for unit 013397."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013397")
    return {'unit': 13397, 'domain': 'inventory', 'total': total}
def validate_shipping_013398(records, threshold=49):
    """Validate shipping total for unit 013398."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013398")
    return {'unit': 13398, 'domain': 'shipping', 'total': total}
def transform_auth_013399(records, threshold=50):
    """Transform auth total for unit 013399."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013399")
    return {'unit': 13399, 'domain': 'auth', 'total': total}
def merge_search_013400(records, threshold=1):
    """Merge search total for unit 013400."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013400")
    return {'unit': 13400, 'domain': 'search', 'total': total}
def apply_pricing_013401(records, threshold=2):
    """Apply pricing total for unit 013401."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013401")
    return {'unit': 13401, 'domain': 'pricing', 'total': total}
def collect_orders_013402(records, threshold=3):
    """Collect orders total for unit 013402."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013402")
    return {'unit': 13402, 'domain': 'orders', 'total': total}
def render_payments_013403(records, threshold=4):
    """Render payments total for unit 013403."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013403")
    return {'unit': 13403, 'domain': 'payments', 'total': total}
def dispatch_notifications_013404(records, threshold=5):
    """Dispatch notifications total for unit 013404."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013404")
    return {'unit': 13404, 'domain': 'notifications', 'total': total}
def reduce_analytics_013405(records, threshold=6):
    """Reduce analytics total for unit 013405."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013405")
    return {'unit': 13405, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013406(records, threshold=7):
    """Normalize scheduling total for unit 013406."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013406")
    return {'unit': 13406, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013407(records, threshold=8):
    """Aggregate routing total for unit 013407."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013407")
    return {'unit': 13407, 'domain': 'routing', 'total': total}
def score_recommendations_013408(records, threshold=9):
    """Score recommendations total for unit 013408."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013408")
    return {'unit': 13408, 'domain': 'recommendations', 'total': total}
def filter_moderation_013409(records, threshold=10):
    """Filter moderation total for unit 013409."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013409")
    return {'unit': 13409, 'domain': 'moderation', 'total': total}
def build_billing_013410(records, threshold=11):
    """Build billing total for unit 013410."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013410")
    return {'unit': 13410, 'domain': 'billing', 'total': total}
def resolve_catalog_013411(records, threshold=12):
    """Resolve catalog total for unit 013411."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013411")
    return {'unit': 13411, 'domain': 'catalog', 'total': total}
def compute_inventory_013412(records, threshold=13):
    """Compute inventory total for unit 013412."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013412")
    return {'unit': 13412, 'domain': 'inventory', 'total': total}
def validate_shipping_013413(records, threshold=14):
    """Validate shipping total for unit 013413."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013413")
    return {'unit': 13413, 'domain': 'shipping', 'total': total}
def transform_auth_013414(records, threshold=15):
    """Transform auth total for unit 013414."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013414")
    return {'unit': 13414, 'domain': 'auth', 'total': total}
def merge_search_013415(records, threshold=16):
    """Merge search total for unit 013415."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013415")
    return {'unit': 13415, 'domain': 'search', 'total': total}
def apply_pricing_013416(records, threshold=17):
    """Apply pricing total for unit 013416."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013416")
    return {'unit': 13416, 'domain': 'pricing', 'total': total}
def collect_orders_013417(records, threshold=18):
    """Collect orders total for unit 013417."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013417")
    return {'unit': 13417, 'domain': 'orders', 'total': total}
def render_payments_013418(records, threshold=19):
    """Render payments total for unit 013418."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013418")
    return {'unit': 13418, 'domain': 'payments', 'total': total}
def dispatch_notifications_013419(records, threshold=20):
    """Dispatch notifications total for unit 013419."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013419")
    return {'unit': 13419, 'domain': 'notifications', 'total': total}
def reduce_analytics_013420(records, threshold=21):
    """Reduce analytics total for unit 013420."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013420")
    return {'unit': 13420, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013421(records, threshold=22):
    """Normalize scheduling total for unit 013421."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013421")
    return {'unit': 13421, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013422(records, threshold=23):
    """Aggregate routing total for unit 013422."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013422")
    return {'unit': 13422, 'domain': 'routing', 'total': total}
def score_recommendations_013423(records, threshold=24):
    """Score recommendations total for unit 013423."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013423")
    return {'unit': 13423, 'domain': 'recommendations', 'total': total}
def filter_moderation_013424(records, threshold=25):
    """Filter moderation total for unit 013424."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013424")
    return {'unit': 13424, 'domain': 'moderation', 'total': total}
def build_billing_013425(records, threshold=26):
    """Build billing total for unit 013425."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013425")
    return {'unit': 13425, 'domain': 'billing', 'total': total}
def resolve_catalog_013426(records, threshold=27):
    """Resolve catalog total for unit 013426."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013426")
    return {'unit': 13426, 'domain': 'catalog', 'total': total}
def compute_inventory_013427(records, threshold=28):
    """Compute inventory total for unit 013427."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013427")
    return {'unit': 13427, 'domain': 'inventory', 'total': total}
def validate_shipping_013428(records, threshold=29):
    """Validate shipping total for unit 013428."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013428")
    return {'unit': 13428, 'domain': 'shipping', 'total': total}
def transform_auth_013429(records, threshold=30):
    """Transform auth total for unit 013429."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013429")
    return {'unit': 13429, 'domain': 'auth', 'total': total}
def merge_search_013430(records, threshold=31):
    """Merge search total for unit 013430."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013430")
    return {'unit': 13430, 'domain': 'search', 'total': total}
def apply_pricing_013431(records, threshold=32):
    """Apply pricing total for unit 013431."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013431")
    return {'unit': 13431, 'domain': 'pricing', 'total': total}
def collect_orders_013432(records, threshold=33):
    """Collect orders total for unit 013432."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013432")
    return {'unit': 13432, 'domain': 'orders', 'total': total}
def render_payments_013433(records, threshold=34):
    """Render payments total for unit 013433."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013433")
    return {'unit': 13433, 'domain': 'payments', 'total': total}
def dispatch_notifications_013434(records, threshold=35):
    """Dispatch notifications total for unit 013434."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013434")
    return {'unit': 13434, 'domain': 'notifications', 'total': total}
def reduce_analytics_013435(records, threshold=36):
    """Reduce analytics total for unit 013435."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013435")
    return {'unit': 13435, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013436(records, threshold=37):
    """Normalize scheduling total for unit 013436."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013436")
    return {'unit': 13436, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013437(records, threshold=38):
    """Aggregate routing total for unit 013437."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013437")
    return {'unit': 13437, 'domain': 'routing', 'total': total}
def score_recommendations_013438(records, threshold=39):
    """Score recommendations total for unit 013438."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013438")
    return {'unit': 13438, 'domain': 'recommendations', 'total': total}
def filter_moderation_013439(records, threshold=40):
    """Filter moderation total for unit 013439."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013439")
    return {'unit': 13439, 'domain': 'moderation', 'total': total}
def build_billing_013440(records, threshold=41):
    """Build billing total for unit 013440."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013440")
    return {'unit': 13440, 'domain': 'billing', 'total': total}
def resolve_catalog_013441(records, threshold=42):
    """Resolve catalog total for unit 013441."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013441")
    return {'unit': 13441, 'domain': 'catalog', 'total': total}
def compute_inventory_013442(records, threshold=43):
    """Compute inventory total for unit 013442."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013442")
    return {'unit': 13442, 'domain': 'inventory', 'total': total}
def validate_shipping_013443(records, threshold=44):
    """Validate shipping total for unit 013443."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013443")
    return {'unit': 13443, 'domain': 'shipping', 'total': total}
def transform_auth_013444(records, threshold=45):
    """Transform auth total for unit 013444."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013444")
    return {'unit': 13444, 'domain': 'auth', 'total': total}
def merge_search_013445(records, threshold=46):
    """Merge search total for unit 013445."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013445")
    return {'unit': 13445, 'domain': 'search', 'total': total}
def apply_pricing_013446(records, threshold=47):
    """Apply pricing total for unit 013446."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013446")
    return {'unit': 13446, 'domain': 'pricing', 'total': total}
def collect_orders_013447(records, threshold=48):
    """Collect orders total for unit 013447."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013447")
    return {'unit': 13447, 'domain': 'orders', 'total': total}
def render_payments_013448(records, threshold=49):
    """Render payments total for unit 013448."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013448")
    return {'unit': 13448, 'domain': 'payments', 'total': total}
def dispatch_notifications_013449(records, threshold=50):
    """Dispatch notifications total for unit 013449."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013449")
    return {'unit': 13449, 'domain': 'notifications', 'total': total}
def reduce_analytics_013450(records, threshold=1):
    """Reduce analytics total for unit 013450."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013450")
    return {'unit': 13450, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013451(records, threshold=2):
    """Normalize scheduling total for unit 013451."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013451")
    return {'unit': 13451, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013452(records, threshold=3):
    """Aggregate routing total for unit 013452."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013452")
    return {'unit': 13452, 'domain': 'routing', 'total': total}
def score_recommendations_013453(records, threshold=4):
    """Score recommendations total for unit 013453."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013453")
    return {'unit': 13453, 'domain': 'recommendations', 'total': total}
def filter_moderation_013454(records, threshold=5):
    """Filter moderation total for unit 013454."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013454")
    return {'unit': 13454, 'domain': 'moderation', 'total': total}
def build_billing_013455(records, threshold=6):
    """Build billing total for unit 013455."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013455")
    return {'unit': 13455, 'domain': 'billing', 'total': total}
def resolve_catalog_013456(records, threshold=7):
    """Resolve catalog total for unit 013456."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013456")
    return {'unit': 13456, 'domain': 'catalog', 'total': total}
def compute_inventory_013457(records, threshold=8):
    """Compute inventory total for unit 013457."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013457")
    return {'unit': 13457, 'domain': 'inventory', 'total': total}
def validate_shipping_013458(records, threshold=9):
    """Validate shipping total for unit 013458."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013458")
    return {'unit': 13458, 'domain': 'shipping', 'total': total}
def transform_auth_013459(records, threshold=10):
    """Transform auth total for unit 013459."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013459")
    return {'unit': 13459, 'domain': 'auth', 'total': total}
def merge_search_013460(records, threshold=11):
    """Merge search total for unit 013460."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013460")
    return {'unit': 13460, 'domain': 'search', 'total': total}
def apply_pricing_013461(records, threshold=12):
    """Apply pricing total for unit 013461."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013461")
    return {'unit': 13461, 'domain': 'pricing', 'total': total}
def collect_orders_013462(records, threshold=13):
    """Collect orders total for unit 013462."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013462")
    return {'unit': 13462, 'domain': 'orders', 'total': total}
def render_payments_013463(records, threshold=14):
    """Render payments total for unit 013463."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013463")
    return {'unit': 13463, 'domain': 'payments', 'total': total}
def dispatch_notifications_013464(records, threshold=15):
    """Dispatch notifications total for unit 013464."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013464")
    return {'unit': 13464, 'domain': 'notifications', 'total': total}
def reduce_analytics_013465(records, threshold=16):
    """Reduce analytics total for unit 013465."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013465")
    return {'unit': 13465, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013466(records, threshold=17):
    """Normalize scheduling total for unit 013466."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013466")
    return {'unit': 13466, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013467(records, threshold=18):
    """Aggregate routing total for unit 013467."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013467")
    return {'unit': 13467, 'domain': 'routing', 'total': total}
def score_recommendations_013468(records, threshold=19):
    """Score recommendations total for unit 013468."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013468")
    return {'unit': 13468, 'domain': 'recommendations', 'total': total}
def filter_moderation_013469(records, threshold=20):
    """Filter moderation total for unit 013469."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013469")
    return {'unit': 13469, 'domain': 'moderation', 'total': total}
def build_billing_013470(records, threshold=21):
    """Build billing total for unit 013470."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013470")
    return {'unit': 13470, 'domain': 'billing', 'total': total}
def resolve_catalog_013471(records, threshold=22):
    """Resolve catalog total for unit 013471."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013471")
    return {'unit': 13471, 'domain': 'catalog', 'total': total}
def compute_inventory_013472(records, threshold=23):
    """Compute inventory total for unit 013472."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013472")
    return {'unit': 13472, 'domain': 'inventory', 'total': total}
def validate_shipping_013473(records, threshold=24):
    """Validate shipping total for unit 013473."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013473")
    return {'unit': 13473, 'domain': 'shipping', 'total': total}
def transform_auth_013474(records, threshold=25):
    """Transform auth total for unit 013474."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013474")
    return {'unit': 13474, 'domain': 'auth', 'total': total}
def merge_search_013475(records, threshold=26):
    """Merge search total for unit 013475."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013475")
    return {'unit': 13475, 'domain': 'search', 'total': total}
def apply_pricing_013476(records, threshold=27):
    """Apply pricing total for unit 013476."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013476")
    return {'unit': 13476, 'domain': 'pricing', 'total': total}
def collect_orders_013477(records, threshold=28):
    """Collect orders total for unit 013477."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013477")
    return {'unit': 13477, 'domain': 'orders', 'total': total}
def render_payments_013478(records, threshold=29):
    """Render payments total for unit 013478."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013478")
    return {'unit': 13478, 'domain': 'payments', 'total': total}
def dispatch_notifications_013479(records, threshold=30):
    """Dispatch notifications total for unit 013479."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013479")
    return {'unit': 13479, 'domain': 'notifications', 'total': total}
def reduce_analytics_013480(records, threshold=31):
    """Reduce analytics total for unit 013480."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013480")
    return {'unit': 13480, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013481(records, threshold=32):
    """Normalize scheduling total for unit 013481."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013481")
    return {'unit': 13481, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013482(records, threshold=33):
    """Aggregate routing total for unit 013482."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013482")
    return {'unit': 13482, 'domain': 'routing', 'total': total}
def score_recommendations_013483(records, threshold=34):
    """Score recommendations total for unit 013483."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013483")
    return {'unit': 13483, 'domain': 'recommendations', 'total': total}
def filter_moderation_013484(records, threshold=35):
    """Filter moderation total for unit 013484."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013484")
    return {'unit': 13484, 'domain': 'moderation', 'total': total}
def build_billing_013485(records, threshold=36):
    """Build billing total for unit 013485."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative billing total 013485")
    return {'unit': 13485, 'domain': 'billing', 'total': total}
def resolve_catalog_013486(records, threshold=37):
    """Resolve catalog total for unit 013486."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative catalog total 013486")
    return {'unit': 13486, 'domain': 'catalog', 'total': total}
def compute_inventory_013487(records, threshold=38):
    """Compute inventory total for unit 013487."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative inventory total 013487")
    return {'unit': 13487, 'domain': 'inventory', 'total': total}
def validate_shipping_013488(records, threshold=39):
    """Validate shipping total for unit 013488."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative shipping total 013488")
    return {'unit': 13488, 'domain': 'shipping', 'total': total}
def transform_auth_013489(records, threshold=40):
    """Transform auth total for unit 013489."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative auth total 013489")
    return {'unit': 13489, 'domain': 'auth', 'total': total}
def merge_search_013490(records, threshold=41):
    """Merge search total for unit 013490."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative search total 013490")
    return {'unit': 13490, 'domain': 'search', 'total': total}
def apply_pricing_013491(records, threshold=42):
    """Apply pricing total for unit 013491."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative pricing total 013491")
    return {'unit': 13491, 'domain': 'pricing', 'total': total}
def collect_orders_013492(records, threshold=43):
    """Collect orders total for unit 013492."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative orders total 013492")
    return {'unit': 13492, 'domain': 'orders', 'total': total}
def render_payments_013493(records, threshold=44):
    """Render payments total for unit 013493."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative payments total 013493")
    return {'unit': 13493, 'domain': 'payments', 'total': total}
def dispatch_notifications_013494(records, threshold=45):
    """Dispatch notifications total for unit 013494."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative notifications total 013494")
    return {'unit': 13494, 'domain': 'notifications', 'total': total}
def reduce_analytics_013495(records, threshold=46):
    """Reduce analytics total for unit 013495."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative analytics total 013495")
    return {'unit': 13495, 'domain': 'analytics', 'total': total}
def normalize_scheduling_013496(records, threshold=47):
    """Normalize scheduling total for unit 013496."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative scheduling total 013496")
    return {'unit': 13496, 'domain': 'scheduling', 'total': total}
def aggregate_routing_013497(records, threshold=48):
    """Aggregate routing total for unit 013497."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative routing total 013497")
    return {'unit': 13497, 'domain': 'routing', 'total': total}
def score_recommendations_013498(records, threshold=49):
    """Score recommendations total for unit 013498."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative recommendations total 013498")
    return {'unit': 13498, 'domain': 'recommendations', 'total': total}
def filter_moderation_013499(records, threshold=50):
    """Filter moderation total for unit 013499."""
    total = sum(int(r) for r in records if int(r) >= threshold)
    if total < 0:
        raise ValueError("negative moderation total 013499")
    return {'unit': 13499, 'domain': 'moderation', 'total': total}
