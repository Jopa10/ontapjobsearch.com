"""Controlled evidence rules for review-only job-card summaries."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

RULE_VERSION = "2"
DEFAULT_APP_ROOT = Path("app")
DEFAULT_CSV_OUTPUT = Path("reviews/at-a-glance/at-a-glance-review.csv")
DEFAULT_MARKDOWN_OUTPUT = Path("reviews/at-a-glance/at-a-glance-review.md")

WORD_RE = re.compile(r"[A-Za-z0-9£]+(?:[’'-][A-Za-z0-9]+)*")
TRUNCATION_PATTERNS = (
    re.compile(r"\bclick apply for full job details\b", re.I),
    re.compile(r"\bclick apply for more details\b", re.I),
    re.compile(r"\bsee full job details\b", re.I),
    re.compile(r"\bfull job details(?:\s+by)?\s+click(?:ing)? apply\b", re.I),
)

DUTY_HEADINGS = (
    "key responsibilities",
    "responsibilities",
    "main responsibilities",
    "the key duties and requirements are",
    "key duties and requirements are",
    "key duties",
    "main duties",
    "duties",
    "role overview",
    "about the role",
    "your new role",
    "the role",
    "what you'll do",
    "what you will do",
    "your day-to-day",
    "your day to day",
    "day-to-day",
    "day to day",
    "in this role",
    "job role",
    "description",
)
STOP_HEADINGS = (
    "about you",
    "what we're looking for",
    "what we are looking for",
    "what you'll need",
    "what you will need",
    "requirements",
    "key requirements",
    "skills and experience",
    "key skills",
    "experience required",
    "person specification",
    "profile",
    "the ideal candidate",
    "successful applicant",
    "we'd love to speak to candidates",
    "we would love to speak to candidates",
    "you are",
    "why join",
    "why us",
    "why work",
    "why choose",
    "what we offer",
    "what you'll receive",
    "what you will receive",
    "what you'll get",
    "what you will get",
    "benefits",
    "our benefits",
    "amazing benefits",
    "rewards and benefits",
    "salary and benefits",
    "rewards",
    "rewards package",
    "job offer",
    "next steps",
    "what next",
    "how to apply",
    "application process",
    "safer recruitment",
    "equal opportunities",
    "about the company",
    "about the organisation",
    "about the organization",
    "about us",
)

INSERT_HEADING_BREAKS = tuple(
    sorted(set(DUTY_HEADINGS + STOP_HEADINGS), key=len, reverse=True)
)


@dataclass(frozen=True)
class AttributeRule:
    key: str
    label: str
    phrase: str
    patterns: tuple[re.Pattern[str], ...]
    categories: tuple[str, ...]


def patterns(*values: str) -> tuple[re.Pattern[str], ...]:
    return tuple(re.compile(value, re.I) for value in values)


ATTRIBUTE_RULES: tuple[AttributeRule, ...] = (
    AttributeRule(
        "visitor_reception",
        "Visitor reception",
        "visitor reception",
        patterns(
            r"\bgreet(?:ing)? (?:clients and )?visitors\b",
            r"\bmeet and greet (?:patients|clients|visitors)\b",
            r"\bwelcome (?:clients and )?visitors\b",
            r"\bfirst point of contact for visitors\b",
            r"\bfront[- ]of[- ]house reception\b",
            r"\bhandle reception duties\b",
            r"\bmanage the reception area\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "telephone_calls",
        "Telephone handling",
        "telephone handling",
        patterns(
            r"\banswer(?:ing)? (?:and redirect(?:ing)? )?(?:incoming )?(?:phone|telephone) calls\b",
            r"\bmanage incoming calls\b",
            r"\bhandle incoming calls\b",
            r"\btaking enquiries .*?\bphone\b",
            r"\btelephone enquiries\b",
            r"\bcall handling\b",
            r"\bmeet and greet .*?\bcalls\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "customer_enquiries",
        "Customer enquiries",
        "customer enquiries",
        patterns(
            r"\bcustomer enquiries\b",
            r"\bclient enquiries\b",
            r"\bcustomer quer(?:y|ies)\b",
            r"\bclient quer(?:y|ies)\b",
            r"\brespond(?:ing)? to (?:general |customer |client )?enquiries\b",
            r"\bhandle(?:ing)? (?:general |customer |client )?enquiries\b",
            r"\btaking enquiries from clients\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "email_handling",
        "Email handling",
        "email handling",
        patterns(
            r"\bmanage (?:incoming )?emails\b",
            r"\brespond(?:ing)? to (?:customer |client )?emails\b",
            r"\bemail enquiries\b",
            r"\btaking enquiries .*?\bemail\b",
            r"\btelephone and email enquiries\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "shared_inbox",
        "Shared inboxes",
        "shared inbox management",
        patterns(r"\bshared (?:service )?inbox(?:es)?\b"),
        ("admin",),
    ),
    AttributeRule(
        "scheduling",
        "Scheduling and bookings",
        "appointment scheduling",
        patterns(
            r"\bcoordinat(?:e|ing) diar(?:y|ies)\b",
            r"\bmanag(?:e|ing) diar(?:y|ies)\b",
            r"\bschedul(?:e|ing) (?:meetings|appointments|interviews)\b",
            r"\barrang(?:e|ing) (?:meetings|appointments|interviews)\b",
            r"\bmeeting room bookings\b",
            r"\bmanage meeting rooms\b",
            r"\broom bookings\b",
            r"\bcoordinat(?:e|ing) appointments\b",
            r"\bliaising .*? to arrange appointments\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "records",
        "Records administration",
        "records administration",
        patterns(
            r"\bmaintain(?:ing)? (?:accurate )?(?:customer |employee |service |job |client |housing |tenancy )?records\b",
            r"\bcomplete detailed and accurate records\b",
            r"\brecords administration\b",
            r"\bcompliance records\b",
            r"\bstatutory records\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "systems",
        "Systems administration",
        "systems updates",
        patterns(
            r"\bupdat(?:e|ing) (?:internal |administrative |customer )?(?:systems|databases)\b",
            r"\bmaintain(?:ing)? (?:the )?(?:relevant |internal )?systems\b",
            r"\bpatient management system\b",
            r"\bjob status updates\b",
            r"\bCRM systems?\b",
            r"\bERP systems?\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "customer_portals",
        "Customer portals",
        "customer portal updates",
        patterns(r"\bcustomer portals\b"),
        ("admin",),
    ),
    AttributeRule(
        "data_entry",
        "Data entry",
        "data entry",
        patterns(
            r"\bdata entry\b",
            r"\binput(?:ting)? data\b",
            r"\baccurate data input\b",
            r"\buploading referrals\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "documents",
        "Document preparation",
        "document preparation",
        patterns(
            r"\bprepar(?:e|ing) documents\b",
            r"\bprepare company documentation\b",
            r"\bservice documentation\b",
            r"\bworks order documentation\b",
            r"\bcomplete client documentation\b",
            r"\bprocess .*?documentation\b",
            r"\bdocument preparation\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "correspondence",
        "Correspondence",
        "correspondence",
        patterns(
            r"\bwritten correspondence\b",
            r"\bdraft employee correspondence\b",
            r"\breports and correspondence\b",
            r"\bcorrespondence to a high standard\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "filing",
        "Filing and document handling",
        "filing and document handling",
        patterns(
            r"\btyping, photocopying and filing\b",
            r"\bfiling and document management\b",
            r"\bdocument management\b",
            r"\bfiling documents\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "reports",
        "Reporting",
        "report preparation",
        patterns(
            r"\bprepar(?:e|ing) reports\b",
            r"\bproduc(?:e|ing) reports\b",
            r"\brunning and reviewing HR reports\b",
            r"\bKPI reporting\b",
            r"\bcollating reports\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "quotations",
        "Quotations",
        "quotation preparation",
        patterns(
            r"\bprepare quotations\b",
            r"\bpreparing quotations\b",
            r"\bprovide accurate quotations\b",
            r"\bquotation(?:s)?\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "estimates",
        "Estimates",
        "estimate preparation",
        patterns(r"\bprepare estimates\b", r"\bcalculat(?:e|ing) .*?costs\b"),
        ("admin",),
    ),
    AttributeRule(
        "orders",
        "Order processing",
        "order processing",
        patterns(
            r"\bprocess(?:ing)? (?:customer |sales |purchase )?orders\b",
            r"\bmanage customer orders\b",
            r"\braise (?:stock |sales |purchase )?orders\b",
            r"\bend-to-end processing of customer orders\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "service_calls",
        "Service-call coordination",
        "service-call coordination",
        patterns(
            r"\blogging service calls\b",
            r"\bcoordinate appointments and service calls\b",
            r"\breactive and planned service jobs\b",
            r"\bupdat(?:e|ing) service jobs\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "engineer_records",
        "Engineer records",
        "engineer record-keeping",
        patterns(
            r"\bengineer service records\b",
            r"\bmonitoring engineer activity\b",
            r"\bengineer time bookings\b",
            r"\bengineer records\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "rotas",
        "Rota administration",
        "rota administration",
        patterns(r"\bengineer call-out rotas\b", r"\bstaff rotas\b"),
        ("admin",),
    ),
    AttributeRule(
        "pre_employment",
        "Pre-employment administration",
        "pre-employment checks",
        patterns(r"\bpre-employment checks\b"),
        ("admin",),
    ),
    AttributeRule(
        "starters_leavers",
        "Starters and leavers",
        "starter and leaver processing",
        patterns(
            r"\bprocessing new starters.*?\bprocessing leavers\b",
            r"\bnew starters.*?\bleavers\b",
            r"\bstarters and leavers\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "contract_changes",
        "Contract changes",
        "contract changes",
        patterns(r"\bcontract changes\b"),
        ("admin",),
    ),
    AttributeRule(
        "hr_guidance",
        "HR process guidance",
        "HR process guidance",
        patterns(
            r"\bguidance for managers in line with .*?policy\b",
            r"\bprocedural advice\/guidance to managers\b",
            r"\badvising managers.*?HR processes\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "payroll",
        "Payroll administration",
        "payroll administration",
        patterns(
            r"\bpayroll deadlines\b",
            r"\bpayroll changes\b",
            r"\binput .*?timesheets\b",
            r"\bcheck timesheets\b",
            r"\bpayroll administration\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "mail",
        "Mail handling",
        "mail handling",
        patterns(
            r"\bincoming and outgoing mail\b",
            r"\bcoordinating incoming and outgoing mail\b",
            r"\bhandle(?:ing)? mail\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "deliveries",
        "Delivery coordination",
        "delivery coordination",
        patterns(
            r"\barrange deliveries\b",
            r"\bcoordinat(?:e|ing) deliveries\b",
            r"\bhandle(?:ing)? deliveries\b",
        ),
        ("admin",),
    ),
    AttributeRule(
        "personal_care",
        "Personal care",
        "personal care",
        patterns(r"\bpersonal care\b", r"\bpersonal and domestic care\b"),
        ("support",),
    ),
    AttributeRule(
        "daily_living",
        "Daily living support",
        "daily-living support",
        patterns(
            r"\baspects of daily life\b",
            r"\bdaily living\b",
            r"\bindependent living\b",
            r"\bkey life skills\b",
            r"\bdomestic care\b",
        ),
        ("support",),
    ),
    AttributeRule(
        "community_access",
        "Community access",
        "community access",
        patterns(
            r"\baccessing the community\b",
            r"\bcommunity access\b",
            r"\bsupport within the community\b",
            r"\bcommunity activities\b",
        ),
        ("support",),
    ),
    AttributeRule(
        "medical_welfare",
        "Medical and welfare support",
        "medical and welfare support",
        patterns(r"\bmedical (?:and|&) welfare needs\b"),
        ("support",),
    ),
    AttributeRule(
        "medical_needs",
        "Medical support",
        "medical support",
        patterns(
            r"\bmedical needs\b",
            r"\bmedication support\b",
            r"\bassist with medication\b",
        ),
        ("support",),
    ),
    AttributeRule(
        "support_plans",
        "Support plans",
        "support planning",
        patterns(r"\bsupport plans\b", r"\bSMART support plans\b"),
        ("support",),
    ),
    AttributeRule(
        "assessments",
        "Risk and needs assessments",
        "risk and needs assessments",
        patterns(
            r"\brisk and needs assessments\b",
            r"\brisk assessments\b",
            r"\bneeds assessments\b",
        ),
        ("support",),
    ),
    AttributeRule(
        "safeguarding",
        "Safeguarding",
        "safeguarding",
        patterns(r"\bsafeguard(?:ing)?\b", r"\bprotect(?:ing)? vulnerable\b"),
        ("support",),
    ),
    AttributeRule(
        "emotional_support",
        "Emotional support",
        "emotional support",
        patterns(
            r"\bphysical (?:and|&) emotional support\b",
            r"\bemotional support\b",
        ),
        ("support",),
    ),
    AttributeRule(
        "independence",
        "Promoting independence",
        "promoting independence",
        patterns(
            r"\bsupport(?:ing)? (?:service user |resident |client )?independence\b",
            r"\bempower(?:ing)? residents\b",
            r"\bachieve independence\b",
            r"\blive as independently as possible\b",
        ),
        ("support",),
    ),
    AttributeRule(
        "incident_response",
        "Incident response",
        "incident response",
        patterns(r"\brespond(?:ing)? to incidents\b", r"\bincident response\b"),
        ("support",),
    ),
    AttributeRule(
        "accommodation_support",
        "Accommodation support",
        "accommodation support",
        patterns(
            r"\bsupported accommodation\b",
            r"\bsafe,? supportive accommodation\b",
            r"\bhelp new residents settle\b",
            r"\bresidential service\b",
        ),
        ("support",),
    ),
    AttributeRule(
        "education_employment",
        "Education and employment goals",
        "education and employment support",
        patterns(
            r"\beducation, training, employment\b",
            r"\beducation and employment\b",
            r"\btraining and employment opportunities\b",
        ),
        ("support",),
    ),
)
