from pywebio.input import input, FLOAT
from pywebio.output import put_text
from pywebio import session

class Cook:
    def __init__(self):
        self.ingredients: list[str] = []
        self.dry_g: list[int] = []
        self.cooked_g: list[int] = []
        self.trans_coefs: list[float] = []
        self.portions_g: list[list[int]] = []
        self.portions_dry_g: list[list[int]] = []

    def get_ingredients_and_weight(self):
        ingredient_num = 1
        while True:
            ingredient = input(f"Write ingredient #{ingredient_num} name or exit: ")
            if ingredient != 'exit':    
                self.ingredients.append(ingredient)
                ingredient_num += 1
            else:
                break
            self.dry_g.append(input("How much does it weight before cooking in grams? ", type=FLOAT))

    def get_cooked(self): 
        for ingredient in self.ingredients:
            self.cooked_g.append(input(f"How much does '{ingredient.upper()}' weight after cooking in grams? ", type=FLOAT))

    def get_portions(self):
        portion_num = 1
        while True:
            portion = []
            for ingredient in self.ingredients:
                portion_g = input(f"How much of '{ingredient.upper()}' does portion #{portion_num} have in grams or exit? ")
                if portion_g != 'exit':
                    portion.append(int(portion_g))
                else:
                    break
            if portion:
                self.portions_g.append(portion)
                portion_num += 1
            else:
                break

    def calculate_trans_coef(self):
        self.trans_coefs = [dry/cooked for dry, cooked in zip(self.dry_g, self.cooked_g)]

    def calculate_dry_in_cooked_portions(self):
        for portion in self.portions_g:
            dry_in_cooked = [int(cooked_portion * coef) for cooked_portion, coef in zip(portion, self.trans_coefs)]
            self.portions_dry_g.append(dry_in_cooked)

    def get_result_dict(self):
        return {f"portion #{i}": {ingredient: grams for ingredient, grams in zip(self.ingredients, portion)} for i, portion in  enumerate(self.portions_dry_g, start=1)}

    def print_inputted_data(self):
        for ingredient, dry, cooked in zip(self.ingredients, self.dry_g, self.cooked_g):
            put_text(ingredient, dry, cooked)
        
        for portion in self.portions_g:
            put_text(portion)

    @staticmethod
    def show_result_dict(result_dict):
        put_text(result_dict)

if __name__ == "__main__":
    cook = Cook()
    cook.get_ingredients_and_weight()
    cook.get_cooked()
    cook.get_portions()
    cook.calculate_trans_coef()
    cook.calculate_dry_in_cooked_portions()
    # cook.print_inputted_data()
    result = cook.get_result_dict()
    cook.show_result_dict(result)
    session.hold()
