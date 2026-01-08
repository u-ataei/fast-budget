from fastapi import FastAPI, HTTPException, Query, status, Body, Path
from typing import Annotated, Optional
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
@app.post("/expense", status_code=status.HTTP_201_CREATED)
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
    return {"message": "Expense added successfully!", "data": expense}


# Retrieve
@app.get("/expenses", status_code=status.HTTP_200_OK)
def get_expenses(
    expense_id: Annotated[
        int | None,
        Query(
            ge=111111,
            le=999999,
            description="""The ID of the expense to retrieve.
            Must be between 111111 and 999999.
            If not provided, all expenses will be returned.
            """,
        ),
    ] = None,
):
    if expense_id is not None:
        for expense in expenses:
            if expense_id == expense["id"]:
                return {
                    "message": f"Expense with ID {expense_id} retrieved successfully.",
                    "data": expense,
                }
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found!"
        )
    return {"message": "All expenses retrieved.", "data": expenses}


# Update
@app.put("/expenses/{expense_id}", status_code=status.HTTP_200_OK)
def update_expense(
    expense_id: int = Path(
        ge=111111,
        le=999999,
        description="""The ID of the expense to update.
            Must be between 111111 and 999999.
            """,
    ),
    description: Optional[str] = Body(
        None, description="New description of the expense", embed=True
    ),
    amount: Optional[float] = Body(
        None, gt=0, description="New amount of the expense", embed=True
    ),
):
    for expense in expenses:
        if expense_id == expense["id"]:
            if description is not None:
                expense["description"] = description
            if amount is not None:
                expense["amount"] = round(amount, 2)
            return {
                "message": f"Expense with ID {expense_id} updated successfully.",
                "data": expense,
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found!"
    )


# Delete
@app.delete("/expense/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int = Path(
        ge=111111,
        le=999999,
        description="""The ID of the expense to delete.
            Must be between 111111 and 999999.
            """,
    )
):
    if expense_id is not None:
        for expense in expenses:
            if expense_id == expense["id"]:
                expenses.remove(expense)
                return
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found!"
        )
