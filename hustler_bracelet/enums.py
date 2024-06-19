from enum import Enum


class FinanceTransactionType(str, Enum):
    INCOME = 'INCOME'
    SPENDING = 'SPENDING'


class ProofCompletionStatus(str, Enum):
    PENDING = 'PENDING'
    VERIFIED = 'VERIFIED'
    REJECTED = 'REJECTED'


class PayoutReason(str, Enum):
    REFERRAL = 'REFERRAL'
    ACTIVITY = 'ACTIVITY'
    OTHER = 'OTHER'


class PaymentReason(str, Enum):
    BRACELET = 'BRACELET'
    OTHER = 'OTHER'


class TransactionType(str, Enum):
    INCOME = 'INCOME'
    OUTCOME = 'OUTCOME'


class TransactionStatus(str, Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    DECLINED = 'DECLINED'


class ActivityUserEventType(str, Enum):
    JOIN = 'JOIN'
    LEAVE = 'LEAVE'


class ActivityTaskUserEventType(str, Enum):
    JOIN = 'JOIN'
    LEAVE = 'LEAVE'


class NotificationType(str, Enum):
    SUB_END_IN_3_DAYS = 'SUB_END_IN_3_DAYS'
