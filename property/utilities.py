"""
Simple Additive Weighting Algorithm
"""
from .models import Customer, Estate, Profession

WEIGHT = {
    "job": 0.1,
    "salary": 0.2,
    "loan_state": 0.3,
    "price": 0.4,
}

# def populate_matrix():
def calc_loan_weight(loan_state):
    if loan_state in ("1", "Approval"):
        return 70
    elif loan_state in ("2", "Penalty"):
        return 40
    elif loan_state in ("3", "In Arrears"):
        return 30
    elif loan_state in ("4", "Paid Off"):
        return 80
    else:
        return 90

def calculate_min_max():
    customers = Customer.objects.all()
    jobs = Profession.objects.all()
    loan_weight = [calc_loan_weight(cust.loan_state) for cust in customers]
    estates = Estate.objects.all()

    job = max([data.weight for data in jobs])
    salary = max([data.salary for data in customers])
    loan_state = max(loan_weight)
    price = min([data.price for data in estates])

    return {
        "job": job,
        "salary": salary,
        "loan_state": loan_state,
        "price": price,
    }

def normalize(matrix, maxmin):
    return {
        "id": matrix["id"],
        "job": (
            maxmin["job"] / matrix["job"]
            if matrix.get("job") > 0 else 0
        ),
        "salary": (
            maxmin["salary"] / matrix["salary"]
            if matrix.get("salary") > 0 else 0
        ),
        "loan_state": (
            maxmin["loan_state"] / matrix["loan_state"]
            if matrix.get("loan_state") > 0 else 0
        ),
        "price": (
            maxmin["price"] / matrix["price"]
            if matrix.get("price") > 0 else 0
        ),
    }

def calculate_rank(value):
    total = (
        (WEIGHT["job"] * float(value["job"])) +
        (WEIGHT["salary"] * float(value["salary"])) +
        (WEIGHT["loan_state"] * float(value["loan_state"])) +
        (WEIGHT["price"] * float(value["price"]))
    )

    return {
        "id": value["id"],
        "total": total
    }

def get_recomendation(data):
    """
    [
        {
            "id": "Estate Name",
            "job": "Guru", => weight in models
            "salary": 4500000,
            "loan_state": "paid_off", => needs specify the weight of state
            "price": 5000000000
        }, ...
    ]
    """
    minmax = calculate_min_max()
    normalized = [normalize(matrix, minmax) for matrix in data]
    ranked = [calculate_rank(val) for val in normalized]
    rank_sorted = sorted(ranked, key=lambda key: key["total"])
    results = [rank["id"] for rank in rank_sorted]

    return results
    