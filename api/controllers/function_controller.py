from fastapi import APIRouter, HTTPException, Depends
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


@router.get("/", response_model=List[FunctionDTO])
async def list_functions(
    use_case: ListFunctionsUseCase = Depends(get_list_functions_use_case)
) -> List[FunctionDTO]:
    result = use_case.execute()
    
    if result.is_failure():
        raise HTTPException(status_code=500, detail=result.error)
    
    return result.get_value()


@router.post("/call", response_model=FunctionCallDTO)
async def call_function(
    request: CallFunctionRequest,
    use_case: CallFunctionUseCase = Depends(get_call_function_use_case)
) -> FunctionCallDTO:
    result = use_case.execute(
        function_name=request.name,
        arguments=request.arguments
    )
    
    if result.is_failure():
        raise HTTPException(status_code=404, detail=result.error)
    
    return result.get_value()