

class Category:
    expense_category: str
    ledger = [{}]
    
    def __init__(self, expense_category: str):
        self.expense_category = expense_category
        self.ledger = []

    def __repr__(self):
        output: str = ""
        length = len(self.expense_category)

        output += int((30 - length)/2) * "*" + self.expense_category + int((30 - length)/2) * "*" +"\n"

        if self.ledger != []:
            for operation in self.ledger:
                if len(operation["description"]) <= 22:
                    output += operation["description"] + (23 - len(operation["description"])) * " "

                else:
                    output += operation["description"][:23]
                
                value_string = f'{operation["amount"]:.2f}'

                if len(value_string) < 7:
                    value_string = (7 - len(value_string)) * " " + value_string

                output += value_string + "\n"
            
            total = self.get_balance()
            output += f"Total: {total}"

        return output

    def get_balance(self):
        total: float = 0
        
        if self.ledger != []:
            for operation in self.ledger:
                total += operation["amount"]

        return total

    def check_funds(self, amount: float):
            total = self.get_balance()

            if amount > total:
                return False
            
            else:
                return True
            
    def deposit(self, amount: float, description: str = ""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount: float, description: str = ""):
        if self.check_funds(amount=amount):
            self.ledger.append({"amount": -amount, "description": description})

            return True
        
        else:
            return False

    def transfer(self, amount: float, expense_category):
        if self.check_funds(amount=amount):
            self.withdraw(amount=amount, description=(f"Transfer to {expense_category.expense_category}"))
            expense_category.deposit(amount=amount, description=(f"Transfer from {self.expense_category}"))

            return True
        
        else:
            return False

def create_spend_chart(categories = [Category]):
    expenses = []
    biggest_len: int = -999
    
    for category in categories:
        total: int = 0
        
        if len(category.expense_category) > biggest_len:
            biggest_len = len(category.expense_category)

        for withdrawal in category.ledger:
            if withdrawal["amount"] < 0:
                total += withdrawal["amount"]
        
        expenses.append(total)
    
    percentages = []

    for expense in expenses:
        percentages.append((expense/sum(expenses)) * 100)

    output: str = "Percentage spent by category\n"
    
    for i in range(11):
        quantity = 100 - i*10
        printed_quantity = str(quantity) + "|"

        if len(printed_quantity) < 4:
            printed_quantity = (4 - len(printed_quantity)) * " " + printed_quantity

        output += printed_quantity

        for percentage in percentages:
            if percentage >= quantity:
                output += " o "
                
            else:
                output += "   "
        output += " \n"
        
    output += "    " + len(categories) * "---" + "-\n"
    
    for i in range(biggest_len):
        output += "    "

        for category in categories:
            if i < len(category.expense_category):
                output += f" {category.expense_category[i]} "

            else:
                output += "   "

        if i < biggest_len - 1:
            output += " \n"
        
        else:
            output += " "

    return output