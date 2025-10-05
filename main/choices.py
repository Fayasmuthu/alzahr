from django.db import models
import calendar
import datetime

import pytz
# Create your models here.

GENDER_CHOICES =(
    ("MALE","Male"),("FEMALE","Female"),("OTHER","Other"),
)

COLOR_CHOICES =(
    ("danger","Red"),("success","Green"),("into","Blue"),("warning","Yellow"),
)
ICON_CHOICES = (
    ('fa-solid fa-baseball-bat-ball', 'Cricket'),
    ('fa-solid fa-futbol', 'Football'),
    ('fa-solid fa-table-tennis-paddle-ball', 'Badminton'),
    ('fa-solid fa-person-biking', 'Cycle'),
    ('fa-solid fa-person-running', 'Running'),
    ('fa-solid fa-person-skiing-nordic', 'Skiing'),
    ('fa-solid fa-dumbbell', 'Fitness'),
)
STATUS_CHOICES =(
    ("Published","Published"),("Private","Private")
)

UNIT_CHOICES = (
    ('Kg', 'Kilogram'),
    ('pc', 'Piece'),
    ('g', 'Gram'),
    ('Itr', 'Liter'),
    ('ml', 'Milliliter'),
    ('m', 'Meter'),
    ('cm', 'Centimeter'),

)

BOOL_CHOICES = ((True, "Yes"), (False, "No"))

COLLECTION_MODE_CHOICES = (
    ("CASH", "Cash"),
    ("CHEQUE", "Cheque"),
    ("BANK_TRANSFER", "Bank Transfer"),
    ("OTHERS", "Others"),
)

ATTENDANCE_LOCATION_CHOICES = (("HOME", "HOME"), ("OFFICE", "OFFICE"))

CONTACT_TYPE_CHOICES = (("PHONE", "PHONE"), ("WHATSAPP", "WHATSAPP"), ("EMAIL", "EMAIL"), ("SMS", "SMS"))

EXPERIENCE_CHOICES = (("EXPERIENCED", "Experienced"), ("FRESHER", "Fresher"))

EMPLOYMENT_TYPE_CHOICES = (
    ("PERMANENT", "Permanent"),
    ("PROBATION", "Probation"),
    ("CONTRACT", "Contract"),
    ("TEMPORARY", "Temporary"),
)

EDUCATION_TYPE_CHOICES = (("PROFESSIONAL", "Professional"), ("VOCATIONAL", "Vocational"), ("OTHERS", "Others"))

GENDER_CHOICES = (("MALE", "Male"), ("FEMALE", "Female"), ("OTHER", "Other"))

GST_CHOICES = (
    ("unregistered", "Unregistered/Consumer"),
    ("regular", "Registered - Regular"),
    ("composite", "Registered -Composite"),
)

JOB_TYPE_CHOICES = (("Contructual", "Contructual"), ("Permanent", "Permanent"), ("Probation", "Probation"))

ORIGIN_CHOICES = (
    ("UAE", "UAE"),
    ("Qatar", "Qatar"),
    ("Oman", "Oman"),
    ("Kuwait", "Kuwait"),
    ("KSA", "KSA"),
    ("EXPAT", "EXPAT"),
    ("Bahrain", "Bahrain"),
)

PAYMODE_CHOICES = (("CASH", "Cash on Hand"), ("BANK", "Bank Account"), ("WPS", "WPS - Wages Protection System"))

PRIORITY_CHOICES = (("Urgent", "Urgent"), ("High", "High"), ("Medium", "Medium"), ("Low", "Low"))

READINESS_CHOICES = (
    ("3", "Within 3 Months"),
    ("5", "with 1 year"),
    ("6", "Within 6 Months"),
    ("12", "Within 12 Months"),
)

RELATION_CHOICES = (
    ("Child", "Child"),
    ("Father", "Father"),
    ("Husbend", "Husbend"),
    ("Mother", "Mother"),
    ("Spouse", "Spouse"),
    ("Wife", "Wife"),
)

REQUEST_STATUS_CHOICES = (
    ("AWAITING", "Awaiting"),
    ("ACCEPTED", "Accepted"),
    ("rejected", "Rejected"),
    ("COMPLETED", "Completed"),
)

RETIRE_TYPE_CHOICES = (
    ("None", "None"),
    ("NOR", "Normal"),
    ("REG", "Resignation"),
    ("TER", "Termination"),
    ("VRS", "VRS"),
)

RATING_CHOICES = ((1, "One"), (2, "Two"), (3, "Three"), (4, "Four"), (5, "Five"))

# STATUS_CHOICES = (("on_hold", "On hold"), ("rejected", "Rejected"), ("approved", "Approved"))

SALUTATION_CHOICES = (("Dr.", "Dr."), ("Miss", "Miss"), ("Mr", "Mr"), ("Mrs", "Mrs"), ("Prof.", "Prof."))

TAX_CHOICES = ((0, "0 %"), (5, "5 %"), (10, "10 %"), (12, "12 %"), (15, "15 %"), (18, "18 %"), (20, "20 %"))

YEAR_CHOICES = [(y, y) for y in range(1950, datetime.date.today().year + 2)]

MONTH_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1, 13)]

TIMEZONES = [(tz, tz) for tz in pytz.common_timezones]

TAG_CHOICES = (
    ("primary", "Blue"),
    ("secondary", "Orange"),
    ("success", "Green"),
    ("warning", "Yellow"),
    ("danger", "Red"),
)

MEAL_TYPE_CHOICES = (("break_fast", "Break Fast"), ("lunch", "Lunch"), ("dinner", "Dinner"), ("other", "Other"))

ANNUAL_CTC_CHOICES = (
    ("LT_2LPA", "< 2 LPA"),
    ("2LPA_3LPA", "2-3 LPA"),
    ("3LPA_5LPA", "3-5 LPA"),
    ("5LPA_7LPA", "5-7 LPA"),
    ("7LPA_10LPA", "7-10 LPA"),
    ("10LPA_15LPA", "10-15 LPA"),
    ("15LPA_20LPA", "15-20 LPA"),
    ("GT_20LPA", ">20+ LPA"),
)
APPLICATION_STATUS_CHOICES = (
    ("APPLIED", "APPLIED"),
    ("REVIEWED", "REVIEWED"),
    ("INTERVIEWED", "INTERVIEWED"),
    ("ACCEPTED", "ACCEPTED"),
    ("rejected", "rejected"),
)
APPLICATION_SOURCE_CHOICES = (
    ("EMAIL", "Email"),
    ("WEBSITE", "Website"),
    ("LINKEDIN", "LinkedIn"),
    ("INDEED", "Indeed"),
    ("GLASSDOOR", "Glassdoor"),
    ("JOB_APP", "Other Job Applications"),
)
BLOOD_CHOICES = (
    ("a-positive", "A +Ve"),
    ("b-positive", "B +Ve"),
    ("ab-positive", "AB +Ve"),
    ("o-positive", "O +Ve"),
    ("a-negative", "A -Ve"),
    ("b-negative", "B -Ve"),
    ("ab-negative", "AB -Ve"),
    ("o-negative", "O -Ve"),
)

COLOR_PALETTE = [
    ("#FF5733", "#FF5733"),
    ("#FFBD33", "#FFBD33"),
    ("#DBFF33", "#DBFF33"),
    ("#75FF33", "#75FF33"),
    ("#33FF57", "#33FF57"),
    ("#33FFBD", "#33FFBD"),
    ("#FF58DE", "#FF58DE"),
    ("#7C80FF", "#7C80FF"),
]
DURATION_CHOICES = (
    ("None", "None"),
    ("0-1 Years", "0-1 Years"),
    ("1-2 Years", "1-2 Years"),
    ("2-3 Years", "2-3 Years"),
    ("3-4 Years", "3-4 Years"),
    ("4-5 Years", "4-5 Years"),
    ("5+ Years", "5+ Years"),
)
ENQUIRY_STATUS_TYPE_CHOICES = (
    ("OPEN", "OPEN"),
    ("CLOSED", "CLOSED"),
    ("REJECTED_BY_COMPANY", "REJECTED_BY_COMPANY"),
    ("REJECTED_BY_CLIENT", "rejected_BY_CLIENT"),
)

MARITAL_CHOICES = (
    ("SINGLE", "Single"),
    ("MARRIED", "Married"),
    ("IN_A_RELATIONSHIP", "In a Relationship"),
    ("DIVORCED", "Divorced"),
    ("WIDOWED", "Widowed"),
    ("OTHER", "Other"),
)
NOTICE_PERIOD_CHOICES = (
    ("0", "0"),
    ("1-15", "15 days or less"),
    ("15-30", "15-30 days"),
    ("31-45", "31-45 days"),
    ("46-60", "46-60 days"),
    ("61-90", "61-90 days"),
    ("90+", "More than 90 days"),
)
PROJECT_STATUS_CHOICES = (
    ("ON_SCHEDULE", "On Schedule"),
    ("JUST_STARTED", "Just Started"),
    ("ONGOING", "Ongoing"),
    ("DELAYED", "Delayed"),
    ("W4C", "W4C Approval"),
    ("COMPLETED", "Completed"),
)
PROJECT_PRIORITY_CHOICES = (
    ("URGENT_AND_IMPORTANT", "Urgent and Important"),
    ("NOT_URGENT_AND_IMPORTANT", "Not Urgent and Important"),
    ("URGENT_AND_NOT_IMPORTANT", "Urgent and Not Important"),
    ("NOT_URGENT_AND_NOT_IMPORTANT", "Not Urgent and Not Important"),
)
RESIDENCE_CHOICES = (
    ("SELF_OWNED", "Self Owned"),
    ("FAMILY_OWNED", "Family Owned"),
    ("SELF_RENTED", "Self Rented"),
    ("FAMILY_RENTED", "Family Rented"),
    ("COMPANY_RENTED", "Company Rented"),
    ("COMPANY_OWNED", "Company Owned"),
    ("SHARED", "Shared"),
    ("OTHER", "Other"),
)



STAGE_CHOICES = [
        ("lead_open", "Lead Open"),
        ("lead_lost", "Lead Lost"),
        ("converted_to_deal", "Converted to Deal"),
    ]