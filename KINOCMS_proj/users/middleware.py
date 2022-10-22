from users.models import DevicesStatisticCounter
from django.utils.datetime_safe import datetime

from .tasks import identify_user_device_task




def identify_user_device(get_response):
    def middleware(request):
        if request.user_agent.is_mobile:
            current_device_type = 'mobile' 
        elif request.user_agent.is_tablet or request.user_agent.is_touch_capable:
            current_device_type = 'tablet_and_other_sensor_devices'
        elif request.user_agent.is_pc:
            current_device_type = 'pc'
        identify_user_device_task.delay(current_device_type)
        response = get_response(request)
        return response
    return middleware
