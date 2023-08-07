import pytest
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from myapp.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_user_register(user, client):
    response = client.post("/register", user)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == user["name"]
    assert response.data["email"] == user["email"]
    assert response.data["role"] == user["role"]
    assert "password" not in response.data


@pytest.mark.django_db
def test_user_login(user, client):
    response1 = client.post("/register", user)
    response = client.post("/login", user)

    assert response1.status_code == status.HTTP_201_CREATED
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == user["name"]
    assert response.data["email"] == user["email"]
    assert response.data["role"] == user["role"]
    assert "password" not in response.data
    assert "jwt" in response.data
    assert "jwt" in response.cookies


@pytest.mark.django_db
def test_get_all_users(admin, user, client):
    response3 = client.post("/register", user)
    response2 = client.post("/register", admin)
    response1 = client.post("/login", admin)
    token = "Bearer " + response1.data["jwt"]
    client.credentials(HTTP_AUTHORIZATION=token)

    response = client.get("/users")

    assert response.status_code == status.HTTP_200_OK
    # print('following is the response data   ', response.data)
    assert len(response.data) > 0


@pytest.mark.django_db
def test_single_user(user, client):
    response2 = client.post("/register", user)
    response1 = client.post("/login", user)
    token = "Bearer " + response1.data["jwt"]
    client.credentials(HTTP_AUTHORIZATION=token)

    response = client.get("/user")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_plan_add(admin, client, plan):
    response2 = client.post("/register", admin)
    response1 = client.post("/login", admin)
    id = response1.data["id"]
    plan["author"] = id

    # print('id is here --------->>>>>', id)
    token = "Bearer " + response1.data["jwt"]
    client.credentials(HTTP_AUTHORIZATION=token)

    response = client.post("/plan/add", plan)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_plan_list_view(admin, client, plan):
    response3 = client.post("/register", admin)
    response2 = client.post("/login", admin)
    id = response2.data["id"]
    plan["author"] = id

    token = "Bearer " + response2.data["jwt"]
    client.credentials(HTTP_AUTHORIZATION=token)

    response1 = client.post("/plan/add", plan)

    response = client.get("/plan")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0

@pytest.mark.django_db
def test_plan_delete_view(admin, client, plan):
    response3 = client.post("/register", admin)
    response2 = client.post("/login", admin)
    id = response2.data["id"]
    plan["author"] = id

    token = "Bearer " + response2.data["jwt"]
    client.credentials(HTTP_AUTHORIZATION=token)

    response1 = client.post("/plan/add", plan)
    plan_id = response1.data["id"]

    url = reverse('plan-delete', args=[plan_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_view_admin_plan(admin, client, plan):
    response3 = client.post("/register", admin)
    response2 = client.post("/login", admin)
    id = response2.data["id"]
    plan["author"] = id

    token = "Bearer " + response2.data["jwt"]
    client.credentials(HTTP_AUTHORIZATION=token)

    response1 = client.post("/plan/add", plan)

    url = reverse('plan-view-admin', args=[id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0

@pytest.mark.django_db
def test_view_detailed_plan(admin, user, client, plan):
    response3 = client.post("/register", admin)
    response2 = client.post("/login", admin)
    id = response2.data["id"]
    plan["author"] = id

    token = "Bearer " + response2.data["jwt"]
    client.credentials(HTTP_AUTHORIZATION=token)

    response1 = client.post("/plan/add", plan)
    plan_id = response1.data["id"]

    url = reverse('plan-view-detail', args=[plan_id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    assert response.data["title"] == plan["title"]
    assert response.data["description"] == plan["description"]
    assert response.data["start_date"] == plan["start_date"]
    assert response.data["end_date"] == plan["end_date"]
    assert response.data["price"] == plan["price"]
    assert response.data["id"] == response1.data["id"]

@pytest.mark.django_db
def test_plan_update_date(admin, client, plan):
    response3 = client.post("/register", admin)
    response2 = client.post("/login", admin)
    id = response2.data["id"]
    plan["author"] = id

    token = "Bearer " + response2.data["jwt"]
    client.credentials(HTTP_AUTHORIZATION=token)

    response1 = client.post("/plan/add", plan)
    plan_id = response1.data["id"]

    url = reverse('update-date', args=[plan_id])

    new_start_date = "2024-01-01"
    plan["start_date"] = new_start_date
    response = client.put(url)

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_user_register_plan(user, admin, client, plan):

    response1 = client.post("/register", admin)
    response2 = client.post("/login", admin)
    token = "Bearer " + response2.data["jwt"]
    client.credentials(HTTP_AUTHORIZATION=token)

    id = response2.data["id"]
    plan["author"] = id

    response_plan = client.post("/plan/add", plan)
    plan_id = response_plan.data["id"]

    assert response_plan.status_code == status.HTTP_201_CREATED

    response3 = client.post("/register", user)
    response4 = client.post("/login", user)
    token2 = "Bearer " + response4.data["jwt"]
    client.credentials(HTTP_AUTHORIZATION=token2)

    user_id = response4.data["id"]

    assert response4.status_code == status.HTTP_200_OK

    url = reverse('plan-register', args=[plan_id, user_id])
    response = client.post(url)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_user_deregister_plan(user, admin, client, plan):
    response1 = client.post("/register", admin)
    response2 = client.post("/login", admin)
    token = "Bearer " + response2.data["jwt"]
    client.credentials(HTTP_AUTHORIZATION=token)

    id = response2.data["id"]
    plan["author"] = id

    response_plan = client.post("/plan/add", plan)
    plan_id = response_plan.data["id"]

    assert response_plan.status_code == status.HTTP_201_CREATED

    response3 = client.post("/register", user)
    response4 = client.post("/login", user)
    token2 = "Bearer " + response4.data["jwt"]
    client.credentials(HTTP_AUTHORIZATION=token2)

    user_id = response4.data["id"]

    assert response4.status_code == status.HTTP_200_OK

    url = reverse('plan-register', args=[plan_id, user_id])
    response = client.post(url)

    assert response.status_code == status.HTTP_201_CREATED

    url2 = reverse('plan-deregister', args=[plan_id, user_id])
    final_response = client.post(url2)

    assert final_response.status_code == status.HTTP_200_OK


