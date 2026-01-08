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


expense_records = []


# Create
@app.post("/expense", status_code=status.HTTP_201_CREATED)
def add_expense(
    expense_desc: str = Query(..., description="Description of the expense"),
    expense_amt: float = Query(..., gt=0, description="Amount of the expense"),
):
    new_expense = {
        "expense_id": randint(111111, 999999),
        "expense_desc": expense_desc,
        "expense_amt": round(expense_amt, 2),
    }
    expense_records.append(new_expense)
    return {"message": "Expense added successfully!", "data": new_expense}


# Retrieve
@app.get("/expenses", status_code=status.HTTP_200_OK)
def fetch_expenses(
    search_id: Annotated[
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
    if search_id is not None:
        for record in expense_records:
            if search_id == record["expense_id"]:
                return {
                    "message": f"Expense with ID {search_id} retrieved successfully.",
                    "data": record,
                }
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found!"
        )
    return {"message": "All expenses retrieved.", "data": expense_records}


# Update
@app.put("/expenses/{expense_id}", status_code=status.HTTP_200_OK)
def modify_expense(
    expense_id: int = Path(
        ge=111111,
        le=999999,
        description="""The ID of the expense to update.
            Must be between 111111 and 999999.
            """,
    ),
    new_desc: Optional[str] = Body(
        None, description="New description of the expense", embed=True
    ),
    new_amt: Optional[float] = Body(
        None, gt=0, description="New amount of the expense", embed=True
    ),
):
    for record in expense_records:
        if expense_id == record["expense_id"]:
            if new_desc is not None:
                record["expense_desc"] = new_desc
            if new_amt is not None:
                record["expense_amt"] = round(new_amt, 2)
            return {
                "message": f"Expense with ID {expense_id} updated successfully.",
                "data": record,
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found!"
    )


# Delete
@app.delete("/expense/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_expense(
    expense_id: int = Path(
        ge=111111,
        le=999999,
        description="""The ID of the expense to delete.
            Must be between 111111 and 999999.
            """,
    )
):
    if expense_id is not None:
        for record in expense_records:
            if expense_id == record["expense_id"]:
                expense_records.remove(record)
                return
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found!"
        )
