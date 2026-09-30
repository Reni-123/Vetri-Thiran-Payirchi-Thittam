from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
        },
    )


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "request": request,
        },
    )


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request,
        },
    )


@router.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
        },
    )


@router.get("/planner/home")
def home_planner_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home_planner.html",
        context={
            "request": request,
        },
    )


@router.get("/planner/party")
def party_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="party_planner.html",
        context={
            "request": request,
        },
    )


@router.get("/planner/jewelry")
def jewelry_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="jewelry_planner.html",
        context={
            "request": request,
        },
    )