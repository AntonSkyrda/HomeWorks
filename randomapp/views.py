import string
import random

from django.http import JsonResponse
from django.views import View


class RandomStringView(View):
    def get(self, request, *args, **kwargs):
        length = self.get_valid_length(request.GET.get("length", 8))
        specials = self.get_valid_flag(request.GET.get("specials", 0))
        digits = self.get_valid_flag(request.GET.get("digits", 0))

        characters = string.ascii_letters
        if specials:
            characters += '!"№;%:?*()_+'
        if digits:
            characters += string.digits

        random_string = "".join(random.choices(characters, k=length))

        return JsonResponse({"random_string": random_string})

    def get_valid_length(self, length):
        try:
            length = int(length)
            if 1 <= length <= 100:
                return length
        except ValueError:
            pass
        return 8

    def get_valid_flag(self, flag):
        try:
            flag = int(flag)
            if flag in (0, 1):
                return flag
        except ValueError:
            pass
        return 0
