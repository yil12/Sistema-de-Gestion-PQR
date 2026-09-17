from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class BusinessException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
        )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    errores = []

    for error in exc.errors():
        campo = ".".join(
            str(item)
            for item in error["loc"]
            if item != "body"
        )

        error_type = error["type"]
        mensaje = error["msg"]

        if error_type == "string_too_short":
            mensaje = (
                f"El campo debe tener al menos "
                f"{error['ctx']['min_length']} caracteres."
            )

        elif error_type == "string_too_long":
            mensaje = (
                f"El campo no puede superar "
                f"{error['ctx']['max_length']} caracteres."
            )

        elif error_type == "int_parsing":
            mensaje = "Debe ser un número entero."

        elif error_type == "missing":
            mensaje = "El campo es obligatorio."

        elif error_type == "enum":
            opciones = error["ctx"]["expected"]
            mensaje = f"El valor debe ser uno de: {opciones}."

        elif error_type == "value_error":
            mensaje = mensaje.replace(
                "Value error, ",
                "",
                1,
            )

        errores.append(
            {
                "campo": campo,
                "mensaje": mensaje,
            }
        )

    return JSONResponse(
        status_code=422,
        content={
            "exito": False,
            "mensaje": "Los datos enviados no son válidos.",
            "data": errores,
        },
    )


async def business_exception_handler(
    request: Request,
    exc: BusinessException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "exito": False,
            "mensaje": exc.detail,
            "data": None,
        },
    )