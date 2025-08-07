from fastapi import APIRouter, HTTPException, Depends
from application.features.function.use_cases.register_function import RegisterFunctionUseCase
from application.features.function.use_cases.list_functions import ListFunctionsUseCase
from application.features.function.use_cases.call_function import CallFunctionUseCase
from application.features.function.dtos.function_dto import FunctionDTO
from application.features.function.dtos.function_call_dto import FunctionCallDTO
from api.dependencies import (
    get_register_function_use_case,
    get_list_functions_use_case,
    get_call_function_use_case
)
from api.models.function import (
    RegisterFunctionRequest,
    CallFunctionRequest
)
from typing import List

router = APIRouter(prefix="/functions", tags=["functions"])


@router.post("/", response_model=FunctionDTO)
async def register_function(
    request: RegisterFunctionRequest,
    use_case: RegisterFunctionUseCase = Depends(get_register_function_use_case)
) -> FunctionDTO:
    """
    Register a new function.
    """
    result = use_case.execute(
        name=request.name,
        description=request.description,
        parameters_data=request.parameters
    )
    
    if result.is_failure():
        raise HTTPException(status_code=400, detail=result.error)
    
    return result.get_value()


@router.get("/", response_model=List[FunctionDTO])
async def list_functions(
    use_case: ListFunctionsUseCase = Depends(get_list_functions_use_case)
) -> List[FunctionDTO]:
    """
    List all available functions.
    """
    result = use_case.execute()
    
    if result.is_failure():
        raise HTTPException(status_code=500, detail=result.error)
    
    return result.get_value()


@router.post("/call", response_model=FunctionCallDTO)
async def call_function(
    request: CallFunctionRequest,
    use_case: CallFunctionUseCase = Depends(get_call_function_use_case)
) -> FunctionCallDTO:
    """
    Call a function.
    """
    result = use_case.execute(
        function_name=request.name,
        arguments=request.arguments,
        conversation_id=request.conversation_id
    )
    
    if result.is_failure():
        raise HTTPException(status_code=404, detail=result.error)
    
    return result.get_value()