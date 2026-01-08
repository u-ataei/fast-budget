from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from typing import Annotated
from contextlib import asynccontextmanager
from random import randint


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")


app = FastAPI(lifespan=lifespan)


expenses = []


# Create
@app.post("/expense")
def create_expense(
    description: str = Query(..., description="Description of the expense"),
    amount: float = Query(..., gt=0, description="Amount of the expense"),
):
    expense = {
        "id": randint(111111, 999999),
        "description": description,
        "amount": round(amount, 2),
    }
    expenses.append(expense)
    return JSONResponse(
        content={"detail": "Expense created successfully!", "data": expense},
        status_code=status.HTTP_201_CREATED,
    )


# Retrieve
@app.get("/expenses")
def get_expenses(expense_id: Annotated[int | None, Query(ge=111111, le=999999)] = None):
    if expense_id is not None:
        for expense in expenses:
            if expense_id == expense["id"]:
                return expense
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found!"
        )
    return expenses


# Update

# Delete
