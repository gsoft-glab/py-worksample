from fastapi import APIRouter, Depends
from application.features.function.use_cases.list_functions import ListFunctionsUseCase
from application.features.function.use_cases.call_function import CallFunctionUseCase
from application.features.function.dtos.function_dto import FunctionDTO
from application.features.function.dtos.function_call_dto import FunctionCallDTO
from api.dependencies import (
    get_list_functions_use_case,
    get_call_function_use_case
)
from api.models.requests import (
    CallFunctionRequest
)
from typing import List

router = APIRouter(prefix="/functions", tags=["functions"])


@router.get("/", response_model=List[FunctionDTO], summary="Retrieve a list of all available functions that can be called by the API.")
async def list_functions(
    use_case: ListFunctionsUseCase = Depends(get_list_functions_use_case)
) -> List[FunctionDTO]:
    return use_case.execute()


@router.post("/call", response_model=FunctionCallDTO, summary="Execute a specific function by name with the provided arguments and return the result.")
async def call_function(
    request: CallFunctionRequest,
    use_case: CallFunctionUseCase = Depends(get_call_function_use_case)
) -> FunctionCallDTO:
    return use_case.execute(
        function_name=request.name,
        arguments=request.arguments
    )