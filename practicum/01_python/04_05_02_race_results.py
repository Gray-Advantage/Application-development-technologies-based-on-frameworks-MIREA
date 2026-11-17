"""Практика дат — результат участника забега.

get_results принимает время лидера и участника в формате ЧЧ:ММ:СС.
Если времена равны, верните «Вы пробежали за <время> и победили!».
Иначе вычислите разницу через datetime и верните «Вы пробежали за
<время> с отставанием от лидера на <Ч:ММ:СС>.».
Формат времени храните в переменной time_format.
"""

from datetime import datetime


def get_results(leader_time, your_time):
    time_format = "%H:%M:%S"
    leader_time_object = datetime.strptime(leader_time, time_format)
    your_time_object = datetime.strptime(your_time, time_format)
    if your_time_object == leader_time_object:
        return f"Вы пробежали за {your_time} и победили!"
    else:
        difference = your_time_object - leader_time_object
        return (
            f"Вы пробежали за {your_time} "
            f"с отставанием от лидера на {difference}."
        )


print(get_results("02:02:02", "02:02:02"))
print(get_results("02:02:02", "03:04:05"))
