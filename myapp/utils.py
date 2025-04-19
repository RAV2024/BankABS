# utils.py
from datetime import date, timedelta

def passport_needs_update(birth_date, passport_issue_date):
    today = date.today()
    age = (today - birth_date).days // 365

    # Возрастные пороги с датой "должен заменить"
    milestones = [(20, birth_date.replace(year=birth_date.year + 20)),
                  (45, birth_date.replace(year=birth_date.year + 45))]

    for milestone_age, milestone_date in milestones:
        if age >= milestone_age:
            if (today - milestone_date).days > 90:
                if passport_issue_date <= milestone_date:
                    return True  # Паспорт просрочен
    return False
