def GPA(list_grades):
    sum_, quantity = sum(list_grades), len(list_grades)
    result = round(sum_ / quantity, 2)
    return result
