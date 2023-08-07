from django.urls import path
from .views import *

urlpatterns = [
    path('register', UserRegisterView.as_view()),
    path('login', UserLoginView.as_view()),
    path('user', GetUserView.as_view()),
    path('users', GetAllUsersForAdmin.as_view()),
    path('plan/add', AddPlanView.as_view()),
    path('plan/delete/<int:plan_id>', DeletePlanView.as_view(), name='plan-delete'),
    path('plan', ViewPlanList.as_view()),
    path('plan/view/admin/<int:user_id>', ViewAdminPlans.as_view(), name='plan-view-admin'),
    path('plan/<int:plan_id>', ViewDetailedPlanView.as_view(), name='plan-view-detail'),
    path('plan/update-date/<int:plan_id>', UpdateDateView.as_view(), name='update-date'),
    path('plan/register/<int:plan_id>/<int:user_id>', RegisterPlanView.as_view(), name='plan-register'),
    path('plan/deregister/<int:plan_id>/<int:user_id>', DeregisterPlanView.as_view(), name='plan-deregister'),
    path('plan/check-registration-status/<int:plan_id>/<int:user_id>', CheckPlanRegistrationStatus.as_view()),
    path('user/registered-plans/<int:user_id>', ViewRegisteredPlans.as_view()),
    path('plan/users/<int:plan_id>', ViewRegisteredUsersForPlan.as_view()),
]














# from django.urls import path
# from .views import *
#
# urlpatterns = [
#     path('register', UserRegisterView.as_view()),
#     path('login', UserLoginView.as_view()),
#     path('user', GetUserView.as_view()),
#     path('users', GetAllUsersForAdmin.as_view()),
#     path('plan/add', AddPlanView.as_view()),
#     path('plan/delete/<int:plan_id>', DeletePlanView.as_view()),
#     path('plan', ViewPlanList.as_view()),
#     path('plan/view/admin/<int:user_id>', ViewAdminPlans.as_view()),
#     path('plan/<int:plan_id>', ViewDetailedPlanView.as_view()),
#     path('plan/update-date/<int:plan_id>', UpdateDateView.as_view()),
#     path('plan/register/<int:plan_id>/<int:user_id>', RegisterPlanView.as_view()),
#     path('plan/deregister/<int:plan_id>/<int:user_id>', DeregisterPlanView.as_view()),
#     path('plan/check-registration-status/<int:plan_id>/<int:user_id>', CheckPlanRegistrationStatus.as_view()),
#     path('user/registered-plans/<int:user_id>', ViewRegisteredPlans.as_view()),
#     path('plan/users/<int:plan_id>', ViewRegisteredUsersForPlan.as_view()),
# ]