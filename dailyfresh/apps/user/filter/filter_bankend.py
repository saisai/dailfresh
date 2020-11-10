from rest_framework.filters import BaseFilterBackend

class AddressFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user_obj
        result = queryset.filter(user=user,is_default=True)
        print(result)
        if result:
            return result

