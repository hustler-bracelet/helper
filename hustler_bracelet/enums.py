from enum import Enum


class FinanceTransactionType(str, Enum):
    INCOME = 'INCOME'
    SPENDING = 'SPENDING'


class CompletionStatus(str, Enum):
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
